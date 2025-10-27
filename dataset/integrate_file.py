# read ./data/modu.txt, ./data/sejong.txt, ./data/wiki.txt and integrate them into ./data/train_default.txt
# but, each sentence randomly shuffled
# read must binary

import random
from pathlib import Path
import sys
import codecs
from tqdm import tqdm


def integrate_files(input_files, output_file):
    all_lines = []
    for file_path in input_files:
        with open(file_path, "rb") as f:
            lines = f.readlines()
            lines = [line.decode("utf-8").strip() for line in lines if line.strip()]
            all_lines.extend(lines)

    random.shuffle(all_lines)

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines("\n".join(all_lines))


if __name__ == "__main__":
    input_files = ["./data/modu.txt", "./data/sejong.txt", "./data/wiki.txt"]
    output_file = "./data/train_default.txt"
    integrate_files(input_files, output_file)
    main()
