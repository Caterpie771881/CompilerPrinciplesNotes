from argparse import ArgumentParser
from argparse import Namespace
from . import Assambler


def get_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("-o", "--output")
    parser.add_argument("--encoding")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    output = args.output if args.output else args.input + ".out"

    with open(args.input, 'r', encoding=args.encoding or 'utf-8') as ifile,\
         open(output, 'wb') as ofile:
        assambler: Assambler = Assambler(ifile.readlines())
        ofile.write(assambler.assamble())
