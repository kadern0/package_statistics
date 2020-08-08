#!/usr/bin/env python3

"""Package statistics docstring"""

import re
import sys
import gzip
import argparse
import tempfile
from itertools import islice

import requests
from requests.exceptions import HTTPError

def take(n, iterable):
    "Return first n items of the iterable as a list"
    # Courtesy of:
    # https://stackoverflow.com/questions/7971618/python-return-first-n-keyvalue-pairs-from-dict
    return list(islice(iterable, n))

def get_stats(arch, top=10):
    """Prints packages statistics"""
 #   fname = '../../Contents-i386-2'
    temporary_file = tempfile.NamedTemporaryFile()
    # Initial regexp
    reg = re.compile(b'^(?:(?:\w+/)+\S+(?:\s?\w).*\w*)\s+(\S+)\n$')
    package_store = {}
    try:
        indices_file = open(temporary_file.name, 'r+b')
    except OSError:
        print(f"Could not open/read file:{temporary_file.name}")
        sys.exit(1)
    with indices_file:
        download_file(arch, indices_file)
        # Go to the begining of the file
        indices_file.seek(0)
        for line in indices_file:
            # Go through the whole file
            matching_string = reg.match(line)
            if matching_string:
                packages = matching_string.groups()[0].split(b',')
                for package in packages:
                    package_name = package.split(b'/')[-1]
                    package_store[package_name] = package_store.get(package_name, 0) + 1
    sorted_packages = sorted(package_store.items(), key=lambda x: x[1], reverse=True)
    return sorted_packages[:top]

def download_file(arch, f_name, mirror='http://ftp.uk.debian.org/debian/dists/stable/main/'):
    """Downloads indices file content"""
    full_url = mirror + f'Contents-{arch}.gz'
    try:
        print("Downloading file. Please stand by...")
        response = requests.get(full_url, stream=True)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        sys.exit(1)
    except Exception as err:
        print(f'Other error occurred: {err}')
        sys.exit(1)
    if not response.ok:
        print("Error downloading file")
        sys.exit(1)
    # Maybe verifying data is valid
    f_name.write(gzip.decompress(response.raw.read()))


def get_arch():
    """Get architecture passed from command line"""
    cmd_description = "Check package stats from Debian repo"
    argparser = argparse.ArgumentParser(description=cmd_description)
    # Add the arguments
    argparser.add_argument('architecture')

    arguments = argparser.parse_args()
    return arguments.architecture


def is_arch_valid(arch):
    """Check if the architecture is correct"""
    supported_archs = ["amd64", "arm64", "armel", "armhf", "i386", "mips",
                       "mips64el", "mipsel", "ppc64el", "s390x"]
    return arch in supported_archs


if __name__ == '__main__':
    arch = get_arch()
    if not is_arch_valid(arch):
        print(f"The architecture entereded {arch} is not valid")
        sys.exit(1)

    sorted_pkgs = get_stats(arch)
    for ind, item in enumerate(sorted_pkgs, start=1):
        print(f'{ind}. {item[0].decode("utf-8")} {item[1]}')
