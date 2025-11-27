#!/usr/bin/env python3
import json
import argparse
from together import Together
from dotenv import load_dotenv
import os

# ====== 初期化 ======
load_dotenv()
API_KEY = os.environ.get("TOGETHER_API_KEY")

if not API_KEY:
    raise ValueError("❌ TOGETHER_API_KEY が設定されていません")

client = Together(api_key=API_KEY)

# Together 最新仕様：キャンセル可能ステータス
CANCELABLE = {"VALIDATING", "QUEUED", "RUNNING", "IN_PROGRESS", "PROCESSING"}

def main(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            batch_id = rec["id"]

            print(f"\n🔍 Checking batch {batch_id}")

            batch = client.batches.get_batch(batch_id)
            st = batch.status

            print(f"   → Status: {st}")

            if st in CANCELABLE:
                print("   💥 Cancelling...")
                resp = client.batches.cancel_batch(batch_id)
                print(f"   ✔ Cancelled: {resp.status}")
            else:
                print("   ⏭ Skip (not cancelable)")

    print("\n✨ Cancel operation finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("log_file")
    args = parser.parse_args()

    main(args.log_file)


# python cancel_batch.py /Users/hongohayato/minimind/dataset/together/upload_log.jsonl
