#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys


def convert_csv(input_file, output_file):
    """
    CSV 파일을 변환합니다.
    "a,b,c" -> "a b" (첫 두 컬럼을 공백으로 연결)
    """
    try:
        with open(input_file, "r", encoding="utf-8") as infile, open(
            output_file, "w", encoding="utf-8", newline=""
        ) as outfile:

            reader = csv.reader(infile)

            # 헤더 건너뛰기
            next(reader)

            # 각 행 처리
            for row in reader:
                # 3개 컬럼이 있는 경우: 첫 두 컬럼을 공백으로 연결
                if len(row) >= 2:
                    converted_row = row[0] + " " + row[1]
                    outfile.write(converted_row + "\n")
                elif len(row) == 1:
                    outfile.write(row[0] + "\n")
                else:
                    outfile.write("\n")

        print(f"✓ 변환 완료!")
        print(f"  입력 파일: {input_file}")
        print(f"  출력 파일: {output_file}")

    except FileNotFoundError:
        print(f"❌ 오류: '{input_file}' 파일을 찾을 수 없습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print("=" * 50)
        print("CSV 파일 변환 도구")
        print("=" * 50)
        print("\n사용법: python3 convert_csv.py <입력파일> <출력파일>")
        print("\n예시: python3 convert_csv.py dataset/WS353_korean.csv output.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # 변환 실행
    convert_csv(input_file, output_file)


if __name__ == "__main__":
    main()
