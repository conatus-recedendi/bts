# https://dumps.wikimedia.org/kowiki/
# Download the latest Korean Wikipedia dump
import os
import requests
from tqdm import tqdm
import bz2
import shutil
import xml.etree.ElementTree as ET
import re
from pathlib import Path
from multiprocessing import Pool
from nltk.tokenize import sent_tokenize
import nltk

nltk.download("punkt")
from konlpy.tag import Okt

okt = Okt()
from glob import glob


def download_wikipedia_dump(url, output_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte
    with open(output_path, "wb") as file, tqdm(
        desc=output_path,
        total=total_size,
        unit="iB",
        unit_scale=True,
    ) as bar:
        for data in response.iter_content(block_size):
            file.write(data)
            bar.update(len(data))


def decompress_bz2(input_path, output_path):
    with bz2.BZ2File(input_path, "rb") as file, open(output_path, "wb") as out_file:
        shutil.copyfileobj(file, out_file)


def extract_text_from_wiki_dump(input_path, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    context = ET.iterparse(input_path, events=("end",))
    for event, elem in tqdm(context, desc="Extracting Text", ncols=100):
        if elem.tag.endswith("page"):
            title = elem.find("{http://www.mediawiki.org/xml/export-0.10/}title").text
            text_elem = elem.find(
                "{http://www.mediawiki.org/xml/export-0.10/}revision/{http://www.mediawiki.org/xml/export-0.10/}text"
            )
            if text_elem is not None and text_elem.text:
                text = text_elem.text
                # Clean the text
                text = re.sub(r"<[^>]+>", "", text)  # Remove XML tags
                text = re.sub(r"\{\{[^}]+\}\}", "", text)  # Remove templates
                text = re.sub(r"\[\[[^\]]+\]\]", "", text)  # Remove links
                text = re.sub(r"==+[^=]+==+", "", text)  # Remove headings
                text = re.sub(r"\s+", " ", text)  # Normalize whitespace

                # Save to file
                safe_title = re.sub(r"[\\/*?\"<>|:]", "_", title)
                output_file = output_dir / f"{safe_title}.txt"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(text)
            elem.clear()


def process_wikipedia_dump(input_path, output_dir):
    extract_text_from_wiki_dump(input_path, output_dir)


def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    # text = clean_text(text)
    # sentences = split_sentences(text)
    # sentences = re.split(r'(?<=[.!?]) +', text)
    # tokenized_sentences = tokenize_sentences(sentences)
    # tokenized_sentences = [tokenize_korean_text(sent, okt) for sent in sentences]

    return text


def save_tokenized_sentences(tokenized_sentences, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for sentence in tokenized_sentences:
            f.write(" ".join(sentence) + "\n")


def main():
    wiki_dump_url = (
        "https://dumps.wikimedia.org/kowiki/latest/kowiki-latest-pages-articles.xml.bz2"
    )
    download_path = "kowiki-latest-pages-articles.xml.bz2"
    decompressed_path = "kowiki-latest-pages-articles.xml"
    extracted_text_dir = "wiki_extracted"
    tokenized_output_path = "dataset/data/train.txt"

    # Step 1: Download Wikipedia dump
    download_wikipedia_dump(wiki_dump_url, download_path)
    # Step 2: Decompress the dump
    decompress_bz2(download_path, decompressed_path)
    # Step 3: Extract text from the dump
    process_wikipedia_dump(decompressed_path, extracted_text_dir)
    # Step 4: Process and tokenize the extracted text
    all_tokenized_sentences = []
    text_files = glob(os.path.join(extracted_text_dir, "**", "*.txt"), recursive=True)
    with Pool(processes=os.cpu_count()) as pool:
        for tokenized_sentences in tqdm(
            pool.imap_unordered(process_file, text_files), total=len(text_files)
        ):
            all_tokenized_sentences.extend(tokenized_sentences)
    # Step 5: Save tokenized sentences to output file
    save_tokenized_sentences(all_tokenized_sentences, tokenized_output_path)


if __name__ == "__main__":
    main()
