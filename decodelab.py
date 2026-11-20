#!/usr/bin/env python3
"""
decodelab — a small CLI for the encode/decode/hash tasks you'd normally
reach for CyberChef for: Base64, Base32, Hex, Binary, URL (de/encoding),
hash generation, and dictionary-based hash cracking.

Pure Python standard library — no pip install required.
"""
import argparse
import base64
import binascii
import hashlib
import sys
import urllib.parse

__version__ = "1.0.0"


def read_input(value):
    if value is not None:
        return value
    return sys.stdin.read().rstrip("\n")


def b64_encode(s): return base64.b64encode(s.encode()).decode()
def b64_decode(s): return base64.b64decode(s).decode(errors="replace")

def b32_encode(s): return base64.b32encode(s.encode()).decode()
def b32_decode(s): return base64.b32decode(s.upper()).decode(errors="replace")

def hex_encode(s): return s.encode().hex()
def hex_decode(s): return bytes.fromhex(s.replace(" ", "")).decode(errors="replace")

def bin_encode(s): return " ".join(format(b, "08b") for b in s.encode())

def bin_decode(s):
    groups = s.split()
    return bytes(int(g, 2) for g in groups).decode(errors="replace")

def url_encode(s): return urllib.parse.quote(s)
def url_decode(s): return urllib.parse.unquote(s)

CODECS = {
    "b64": (b64_encode, b64_decode, "Base64"),
    "b32": (b32_encode, b32_decode, "Base32"),
    "hex": (hex_encode, hex_decode, "Hex"),
    "bin": (bin_encode, bin_decode, "Binary (space-separated 8-bit groups)"),
    "url": (url_encode, url_decode, "URL / percent-encoding"),
}

HASH_ALGOS = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]


def do_hash(algo, s):
    h = hashlib.new(algo)
    h.update(s.encode())
    return h.hexdigest()


def do_crack(target_hash, algo, wordlist_path, encoding="utf-8"):
    target_hash = target_hash.strip().lower()
    try:
        f = open(wordlist_path, "r", encoding=encoding, errors="ignore")
    except OSError as e:
        print(f"[!] Could not open wordlist: {e}", file=sys.stderr)
        sys.exit(1)

    with f:
        for i, line in enumerate(f, 1):
            word = line.rstrip("\n").rstrip("\r")
            if not word:
                continue
            h = hashlib.new(algo)
            h.update(word.encode(encoding, errors="ignore"))
            if h.hexdigest().lower() == target_hash:
                print(f"[+] Match found: '{word}'  (line {i})")
                return word
    print("[-] No match found in wordlist.")
    return None


EPILOG = """\
examples:
  decodelab.py b64 encode "hello"
  decodelab.py b32 decode "NBSWY3DP"
  cat payload.txt | decodelab.py hex decode
  decodelab.py hash sha256 "hello"
  decodelab.py crack --hash 5d41402abc4b2a76b9719d911017c592 \\
      --algo md5 --wordlist /usr/share/wordlists/rockyou.txt

If VALUE is omitted for a codec/hash subcommand, input is read from stdin,
so every subcommand is pipe-friendly.
"""


def build_parser():
    p = argparse.ArgumentParser(
        prog="decodelab",
        description="Encode/decode, hash, and dictionary-crack toolkit — a CyberChef-style CLI.",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--version", action="version", version=f"decodelab {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    for name, (_, _, label) in CODECS.items():
        sp = sub.add_parser(name, help=f"{label} encode/decode")
        sp.add_argument("mode", choices=["encode", "decode"])
        sp.add_argument("value", nargs="?", help="input text; reads stdin if omitted")

    hp = sub.add_parser("hash", help="generate a hash digest")
    hp.add_argument("algo", choices=HASH_ALGOS)
    hp.add_argument("value", nargs="?", help="input text; reads stdin if omitted")

    cp = sub.add_parser("crack", help="dictionary attack against a hash digest")
    cp.add_argument("--hash", required=True, dest="target_hash", help="target hash (hex)")
    cp.add_argument("--algo", required=True, choices=HASH_ALGOS)
    cp.add_argument("--wordlist", required=True, help="path to a newline-delimited wordlist")

    return p


def main():
    args = build_parser().parse_args()

    if args.cmd == "crack":
        do_crack(args.target_hash, args.algo, args.wordlist)
        return

    if args.cmd == "hash":
        value = read_input(args.value)
        print(do_hash(args.algo, value))
        return

    enc, dec, _ = CODECS[args.cmd]
    value = read_input(args.value)
    try:
        result = enc(value) if args.mode == "encode" else dec(value)
    except (binascii.Error, ValueError) as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)
    print(result)


if __name__ == "__main__":
    main()
