#!/usr/bin/env python
import argparse
import os
import re
import subprocess
import time
from typing import List, NamedTuple
import webbrowser

import fitz
import jinja2
import requests


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class ContentBlock(NamedTuple):
    text: str


def _get_content_blocks(file: argparse.FileType) -> List[ContentBlock]:
    print("Collecting content blocks...")
    pdf_doc = fitz.Document(stream=file.read(), filetype="pdf")

    def _block_generator(pages):
        for page in pages:
            page_dict = page.getText("dict")
            for block in page_dict["blocks"]:
                if block["type"] == 1:  # image
                    continue
                block_texts = []
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        text = " ".join(text.split(" "))
                        if text.isdigit() or len(text) == 0:
                            continue
                        block_texts.append(text)
                if block_texts:
                    yield ContentBlock(text=" ".join(block_texts))

    def _block_combinator(blocks):
        blocks_final: List[ContentBlock] = []
        for block in blocks:
            if len(blocks_final) == 0:
                blocks_final.append(block)
                continue
            if block.text[0].islower() and blocks_final[-1].text[-1] != ".":
                block = ContentBlock(text=" ".join([blocks_final[-1].text, block.text]))
                blocks_final.pop()
            blocks_final.append(block)
        return blocks_final

    return _block_combinator(_block_generator(pdf_doc.pages()))


def _render_html_document(blocks: List[ContentBlock], name: str) -> str:
    print("Rendering HTML document...")
    with open(f"{SCRIPT_DIR}/pocketify.j2", "r") as template_file:
        template = jinja2.Template(template_file.read())

    name_pretty = " ".join(re.split("[ -_]", name)).title()
    document_path = f"pocket-archive/{name}.html"
    with open(f"{SCRIPT_DIR}/{document_path}", "w") as document_file:
        document_file.write(template.render(blocks=blocks, name=name_pretty))
    return document_path


def _commit_with_git(document_path: str) -> None:
    subprocess.run(
        f'git add "{document_path}"', check=True, shell=True,
    )
    try:
        completed = subprocess.run(
            f"git commit -m 'Adding {document_path} for Pocket'", check=True, shell=True
        )
    except subprocess.CalledProcessError:
        print("Nothing to commit, continuing...")
    else:
        subprocess.run(f"git push origin master", check=True, shell=True)


def _wait_until_available(document_url: str) -> str:
    response = requests.get(document_url)
    while True:
        if response.status_code == 200:
            print("Resource ready, continuing...")
            break
        elif response.status_code == 404:
            print("Resource not ready yet, waiting...")
            time.sleep(10.0)
        else:
            raise ValueError(f"Bad status code {response.status_code}")
        response = requests.get(document_url)
    return document_url


def _add_to_pocket(document_url: str) -> None:
    webbrowser.open_new_tab(f"https://getpocket.com/edit/?url={document_url}")


def main(file: argparse.FileType, name: str) -> None:
    blocks = _get_content_blocks(file=options.input)
    document_path = _render_html_document(blocks=blocks, name=name)
    _commit_with_git(document_path=document_path)

    document_url = (
        f"http://www.micthiesen.ca/{document_path[:document_path.rindex('.')]}"
    )
    _wait_until_available(document_url=document_url)
    _add_to_pocket(document_url=document_url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType("rb"))
    parser.add_argument("--name", type=str)
    options = parser.parse_args()
    name = options.name or os.path.splitext(os.path.basename(options.input.name))[0]
    main(file=options.input, name=name)
    print("Done")
