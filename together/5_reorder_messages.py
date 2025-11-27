#!/usr/bin/env python3
import json
import argparse

def reorder_message(msg):
    """content → content_ja → role → その他 の順に並べ替える"""
    ordered = {}

    # 指定順
    if "content" in msg:
        ordered["content"] = msg["content"]
    if "content_ja" in msg:
        ordered["content_ja"] = msg["content_ja"]
    if "role" in msg:
        ordered["role"] = msg["role"]

    # その他のキー（残り）を後ろに
    for k, v in msg.items():
        if k not in ordered:
            ordered[k] = v

    return ordered


def main(input_jsonl, output_jsonl):
    with open(input_jsonl, "r", encoding="utf-8") as fin, \
         open(output_jsonl, "w", encoding="utf-8") as fout:

        for line in fin:
            if not line.strip():
                continue

            row = json.loads(line)

            if "messages" in row:
                row["messages"] = [reorder_message(msg) for msg in row["messages"]]

            fout.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"✅ 完了: {output_jsonl}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_jsonl")
    parser.add_argument("output_jsonl")
    args = parser.parse_args()

    main(args.input_jsonl, args.output_jsonl)

# python /Users/hongohayato/minimind/dataset/together/reorder_messages.py /Users/hongohayato/minimind/dataset/together/restored.jsonl /Users/hongohayato/minimind/dataset/together/restored_ordered.jsonl