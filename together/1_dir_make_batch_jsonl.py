#!/usr/bin/env python3
import os
import subprocess
import argparse

CHUNK = 5000  # 5,000行ごとに処理

MAKE_SCRIPT = "/Users/hongohayato/minimind/dataset/together/make_batch_jsonl.py"


def count_lines(path):
    """高速に行数を数える"""
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def main(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    total_lines = count_lines(input_file)
    print(f"📘 Total lines: {total_lines}")

    batch_index = 0

    for start in range(0, total_lines, CHUNK):
        end = min(start + CHUNK, total_lines)

        outfile = os.path.join(
            output_dir,
            f"batch_{start:06d}-{end:06d}.jsonl"
        )

        print(f"\n🚀 Generating batch: {outfile}")
        print(f"   Lines {start} to {end}")

        cmd = [
            "python",
            MAKE_SCRIPT,
            input_file,
            outfile,
            "--start", str(start),
            "--end", str(end)
        ]

        subprocess.run(cmd, check=True)

        batch_index += 1

    print("\n🎉 All batches generated successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_dir")
    args = parser.parse_args()

    main(args.input_file, args.output_dir)
