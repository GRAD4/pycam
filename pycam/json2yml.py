"""
  2 Copyright (c) 2021 Nikita Letov (letovnn@gmail.com)
  3 Distributed under the MIT software license, see the accompanying
  4 file COPYING or http://www.opensource.org/licenses/mit-license.php.
  5 
  6 This script converts STEP files to STL file.
  7 Usage:
  8     python main.py -i input.dxf -o output.png
  9 or
 10     python main.py --input input.dxf --output output.png
 11 
 12 For more info see the PythonOCC Tutorial:
 13 https://pythonocc-doc.readthedocs.io/en/latest/convert/
 14 """

import json
import yaml

from optparse import OptionParser

def read_json(json_file_name: str) -> dict:
    """
    Opens and reads a JSON file
    """
    with open(json_file_name) as reader:
        data = json.load(reader)
        return data

def write_to_yml(yml_file_name: str, data: dict) -> None:
    dict_file = [data]
    with open(yml_file_name, 'w') as writer:
        documents = yaml.dump(dict_file, writer)
        print("Data written to " + yml_file_name)

def main():
    # Setting up the parser
    parser = OptionParser()
    parser.add_option("-i", "--input", dest = "input_filename",
            help = "Input STEP file name")
    parser.add_option("-o", "--output", dest = "output_filename",
            help = "Output stl file name")
    (options, args) = parser.parse_args()
    input_filename = str(options.input_filename)
    output_filename = str(options.output_filename)
    data = read_json(input_filename)
    print(data)
    print(type(data))
    write_to_yml(output_filename, data)

if __name__ == '__main__':
    main()

