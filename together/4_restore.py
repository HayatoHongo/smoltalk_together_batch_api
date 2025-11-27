#!/usr/bin/env python3
import json
import argparse
from collections import defaultdict

"""
必要なファイル:
  1. original.jsonl      → 元のデータ（messages[] を持つ）
  2. batch_output.jsonl  → Together Batch の結果（custom_id と content）

出力:
  merged_output.jsonl    → content_ja を挿入した最終 JSONL
"""

def parse_custom_id(custom_id):
    # 形式: row-000001-turn-0-user
    parts = custom_id.split("-")
    row = int(parts[1])
    turn = int(parts[3])
    return row, turn


def load_translations(batch_output_file):
    """custom_id → translated_text を dict に格納"""
    translations = defaultdict(dict)

    with open(batch_output_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            rec = json.loads(line)
            custom_id = rec.get("custom_id")

            # 200 OK のもののみ処理
            message = rec["response"]["body"]["choices"][0]["message"]
            translated = message["content"]

            row, turn = parse_custom_id(custom_id)
            translations[row][turn] = translated

    return translations


def main(original_file, batch_output_file, out_file):
    translations = load_translations(batch_output_file)

    with open(original_file, "r", encoding="utf-8") as fin, \
         open(out_file, "w", encoding="utf-8") as fout:

        for row_index, line in enumerate(fin):
            row = json.loads(line)

            msgs = row.get("messages", [])

            if row_index in translations:
                for turn_index, translated_text in translations[row_index].items():
                    if turn_index < len(msgs):
                        msgs[turn_index]["content_ja"] = translated_text

            row["messages"] = msgs
            fout.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"✅ 完了: {out_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("original_jsonl")
    parser.add_argument("batch_output_jsonl")
    parser.add_argument("out_jsonl")
    args = parser.parse_args()

    main(args.original_jsonl, args.batch_output_jsonl, args.out_jsonl)

# python /Users/hongohayato/minimind/dataset/together/restore.py /Users/hongohayato/minimind/dataset/together/raw_dump.jsonl /Users/hongohayato/minimind/dataset/together/batch_outputs/79b32848-0f78-4c9e-8bc4-78ba84322e95.out.jsonl /Users/hongohayato/minimind/dataset/together/restored.jsonl