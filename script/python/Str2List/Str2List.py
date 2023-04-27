import sys, os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser ()
    parser.add_argument ('-s', '--input_string_file', type=os.path.abspath, default='./Str.txt')
    parser.add_argument ('-l', '--output_list_file', type=os.path.abspath, default='./List.txt')

    args = parser.parse_args()

    with open (args.input_string_file, 'r') as input:
        strs = input.read()

    strs_list = strs.split(' ')

    with open (args.output_list_file, 'w') as output:
        output.write(str(strs_list))

    with open (args.output_list_file, 'r+') as output:
        strs = output.read()
        strs = strs.replace("'", '"')
        output.seek(0)
        output.truncate(0)
        output.write(strs)