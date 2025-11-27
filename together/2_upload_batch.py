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

client = Together()

def main(input_dir, log_file):
    files = sorted(f for f in os.listdir(input_dir) if f.endswith(".jsonl"))

    with open(log_file, "a", encoding="utf-8") as log:
        for fname in files:
            path = os.path.join(input_dir, fname)
            print(f"📤 Uploading {path}")

            file_resp = client.files.upload(file=path, purpose="batch-api")

            batch = client.batches.create_batch(
                file_id=file_resp.id,
                endpoint="/v1/chat/completions"
            )

            # 👇 これが最もミニマムなログ（生レスポンスをそのまま1行）
            log.write(batch.json() + "\n")

            print(f"🆔 Created batch {batch.id}")

    print(f"✨ Log saved to {log_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("log_file")
    args = parser.parse_args()
    main(args.input_dir, args.log_file)

# python /Users/hongohayato/minimind/dataset/together/upload_batch.py /Users/hongohayato/minimind/dataset/together/smoltalk/ /Users/hongohayato/minimind/dataset/together/upload_log.jsonl
