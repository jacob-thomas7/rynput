import os, argparse, sys
from pathlib import Path

import parser

class SnakeMake:
    def __init__(self):
        path = Path(os.getcwd())
        while path.parent:
            if os.path.isdir(path / ".snakemake"):
                files = os.listdir(path)
                break
            if path.parent == path:
                print("Fatal: .snakemake directory not found.")
                print("(You can run 'snakemake init' to initialize snakemake)")
                exit(1)
            path = path.parent
        self.project_source_dir = path
    
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
        except:
            exit(1)
        
        match args.command:
            case "init":
                pass
            case "add":
                self.add(args)
            case "rm":
                pass
        
    def add(self, args):
        os.chdir(self.project_source_dir)
        source_dir = Path("src")
        include_dir = Path("include")

        if not os.path.isdir(source_dir):
            os.makedirs(source_dir)
        if not os.path.isdir(include_dir):
            os.makedirs(include_dir)
        
        source_file_name = (source_dir / (args.classname + ".cpp"))
        source_file_name = source_file_name.as_posix()

        include_file_name = (include_dir / (args.classname + ".cpp"))
        include_file_name = include_file_name.as_posix()

        source_file = open(source_file_name, "w")
        source_file.write(f"include \"{include_file_name}\"")
        source_file.close()

        include_file = open(include_file_name, "w")
        include_file.write(f"#pragma once\n\nclass {args.classname} {{\n\t\n}};")
        include_file.close()

        cmake_sources = open("cmake/sources.cmake", "r")
        lines = cmake_sources.read().split("\n")
        lines.insert(-1, f"\t{source_file_name}")
        cmake_sources.close()

        cmake_sources = open("cmake/sources.cmake", "w")
        cmake_sources.write("\n".join(lines))

# webapp.py
import json
from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

class WebRequestHandler(BaseHTTPRequestHandler):
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def cookies(self):
        return SimpleCookie(self.headers.get("Cookie"))

    def do_GET(self):
        print("GET recieved")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(self.get_response().encode("utf-8"))

    def do_POST(self):
        self.do_GET()

    def get_response(self):
        return json.dumps(
            {
                "path": self.url.path,
                "query_data": self.query_data,
                "post_data": self.post_data.decode("utf-8"),
                "form_data": self.form_data,
                "cookies": {
                    name: cookie.value
                    for name, cookie in self.cookies.items()
                },
            }
        )

def find_source_dir():
    path = Path(os.getcwd())
    while path.parent:
        if os.path.isdir(path / ".snakemake"):
            files = os.listdir(path)
            break
        if path.parent == path:
            print("Fatal: .snakemake directory not found.")
            print("(You can run 'snakemake init' to initialize snakemake)")
            exit(1)
        path = path.parent
    return path

def main():
    # Find .snakemake directory
    project_source_dir = find_source_dir()
    
    # Parse command line arguments
    args = parser.parse()
    
if __name__ == "__main__":
    main()
    #server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    #server.serve_forever()
