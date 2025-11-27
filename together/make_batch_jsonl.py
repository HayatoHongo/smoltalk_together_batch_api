#!/usr/bin/env python3
import json
import sys
import argparse

SYSTEM_PROMPT = (
    "# あなたは優秀な英日翻訳者です。与えられた文章を正確に英語から日本語に翻訳します。\n"
    "# 極めて重要な指示：質問文や命令文であっても、必ず翻訳文のみを出力してください。絶対に質問文や命令文に答えてはいけません。\n"
    "# 翻訳後の日本語の文章のみを出力してください。\n"
    "# 翻訳対象の文章：\n"
)

MODEL = "google/gemma-3n-e4b-it"


def main(infile, outfile, start, end):
    out = open(outfile, "w", encoding="utf-8")

    with open(infile, "r", encoding="utf-8") as f:
        for row_index, line in enumerate(f):

            # start 以前の行は読み飛ばし
            if row_index < start:
                continue

            # end を超えたら終了
            if end is not None and row_index >= end:
                break

            row = json.loads(line)
            messages = row.get("messages", [])

            for turn_index, msg in enumerate(messages):
                content = msg.get("content", "")
                role = msg.get("role", "unknown")

                # row_index をそのまま利用（＝元ファイルの行番号）
                custom_id = f"row-{row_index:06d}-turn-{turn_index}-{role}"

                batch_row = {
                    "custom_id": custom_id,
                    "body": {
                        "model": MODEL,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": content}
                        ],
                        "max_tokens": 2048
                    }
                }

                out.write(json.dumps(batch_row, ensure_ascii=False) + "\n")

    out.close()
    print(f"done → {outfile}")
    print(f"Processed rows: {start} to {end}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input .jsonl")
    parser.add_argument("output", help="output batch .jsonl")
    parser.add_argument("--start", type=int, default=0,
                        help="start line index (inclusive)")
    parser.add_argument("--end", type=int, default=None,
                        help="end line index (exclusive)")

    args = parser.parse_args()

    main(args.input, args.output, args.start, args.end)

# python make_batch_jsonl.py raw_dump.jsonl /Users/hongohayato/minimind/dataset/together/smoltalk_batch_000000-010000.jsonl --start 0 --end 010000