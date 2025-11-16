import argparse

def parse(self):
    parser = argparse.ArgumentParser(
        prog = "snakemake",
        description = "Python tools for CMake development."
    )
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init")
    
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("classname")
    
    rm_parser = subparsers.add_parser("rm")

    try:
        args = parser.parse_args()
        return args
    except:
        exit(1)