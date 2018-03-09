import re
import argparse
import base64
import binascii
import itertools
import base58


def find_base64(text):
    for match in re.finditer('[a-zA-Z0-9+/]+={0,2}', content):
        try:
            yield base64.b64decode(match[0])
        except binascii.Error:
            pass


def find_base32(text):
    for match in re.finditer('[a-zA-Z2-7+/]+={0,5}', content):
        try:
            yield base64.b32decode(match[0], True)
        except binascii.Error:
            pass


def find_base58(text):
    for match in re.finditer('[a-zA-Z1-9]+', content):
        for alphabet in base58.alphabets:
            try:
                yield base58.b58decode(match[0], alphabet)
            except binascii.Error:
                pass


def score(bytestring):
    total_ascii = 0
    for byte in bytestring:
        if 0x20 <= byte <= 0x7E:
            total_ascii += 1
            if chr(byte).isalnum():
                total_ascii += 1
    return total_ascii / len(bytestring)


def is_utf8(bytestring):
    try:
        bytestring.decode()
        return True
    except UnicodeDecodeError:
        return False


def display(bytestring):
    if is_utf8(bytestring):
        print(f'\033[92m{bytestring.decode()}\033[0m')
    else:
        print(bytestring)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    with open(args.filename) as infile:
        content = infile.read()
        # TODO add hex
        # TODO improve score function to find flags
        results = set(itertools.chain(
            find_base64(content),
            find_base32(content),
            find_base58(content)))
        results = sorted(results, key=lambda k: -score(k))
        for bytestring in results:
            display(bytestring)
