#!/usr/bin/env python3
import os
import json
import argparse
from together import Together
from dotenv import load_dotenv

# ====== 初期化 ======
load_dotenv()
API_KEY = os.environ.get("TOGETHER_API_KEY")

if not API_KEY:
    raise ValueError("❌ TOGETHER_API_KEY が設定されていません")

client = Together(api_key=API_KEY)


def main(log_jsonl, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(log_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            rec = json.loads(line)
            batch_id = rec.get("id")

            if not batch_id:
                print("⚠️ バッチIDがありません: スキップ")
                continue

            out_file = os.path.join(output_dir, f"{batch_id}.out.jsonl")

            print(f"\n🔍 Checking batch {batch_id}")

            batch = client.batches.get_batch(batch_id)
            print(f"📌 status: {batch.status}")

            if batch.status != "COMPLETED":
                print("⏳ Not ready yet, skipping")
                continue

            output_file_id = batch.output_file_id
            if not output_file_id:
                print("⚠️ No output_file_id, skipping")
                continue

            print(f"⬇️ Downloading → {out_file}")
            client.files.retrieve_content(
                id=output_file_id,
                output=out_file
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("log_file", help="JSONL log file from batch upload")
    parser.add_argument("output_dir", help="Directory to save batch outputs")
    args = parser.parse_args()

    main(args.log_file, args.output_dir)
