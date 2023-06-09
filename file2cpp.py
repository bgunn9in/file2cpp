# pylint: disable=missing-module-docstring, missing-function-docstring

#!/usr/bin/env python

# coding: utf-8

import argparse
import os
import sys


def bytes_to_str(data: bytearray) -> str:
    return "".join(f"{hex(b)}, " for b in data)


def data_to_str(data: bytearray) -> str:
    chunk_size: int = 16
    data_str: str = "{\n"
    for i in range(0, len(data), chunk_size):
        data_str += f"\t{bytes_to_str(data[i:i+chunk_size])}\n"
    data_str += "};\n"
    return data_str


def make_space(space: str) -> tuple[str, str]:
    if space == "empty":
        return "", ""
    return f"namespace {space} {{\n", "}\n"


def fill_template(data: bytearray, name: str, space: str) -> str:
    space_begin, space_end = make_space(space)
    template: str = (
        f"#pragma once"
        f"\n\n"
        f"#include <array>\n"
        f"\n"
        f"{space_begin}"
        f"static constexpr std::array<uint8_t, {len(data)}> {name} = {data_to_str(data)}"
        f"{space_end}"
    )
    return template


def check_path_exists_and_permissions(input_path: str, output_path: str) -> None:
    if not os.path.exists(input_path):
        sys.exit(f"Input file {input_path} not exists!")
    if not os.access(input_path, os.R_OK):
        sys.exit(f"Input file {input_path} doesn't have read permissions")

    output_dir: str = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        sys.exit(f"Directory {output_dir} not exists! Exit.")
    if not os.access(output_dir, os.W_OK):
        sys.exit(f"Directory {output_dir} doesn't have write permissions")


def parse_args() -> tuple[str, str, str, str]:
    parser = argparse.ArgumentParser(prog="file2cpp")
    parser.add_argument("-i", "--input", help="Input file", type=str, required=True)
    parser.add_argument("-o", "--output", help="Output file", type=str, required=True)
    parser.add_argument("-n", "--name", help="Variable name", type=str, default="data")
    parser.add_argument(
        "-s", "--space", help="Using namespace", type=str, default="empty"
    )
    args = parser.parse_args()
    input_path: str = os.path.abspath(args.input)
    output_path: str = os.path.abspath(args.output)
    check_path_exists_and_permissions(input_path, output_path)
    return input_path, output_path, args.name, args.space


def main() -> None:
    input_path, output_path, name, space = parse_args()
    input_bytes: bytearray = bytearray()
    with open(input_path, "rb") as input_file:
        input_bytes = bytearray(input_file.read())
    template: str = fill_template(input_bytes, name, space)
    with open(output_path, "wb") as output_file:
        output_file.write(template.encode("utf-8"))


if __name__ == "__main__":
    main()
