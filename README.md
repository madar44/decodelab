# decodelab

A small, dependency-free CLI for the encode/decode/hash tasks you'd normally
reach for CyberChef for — Base64, Base32, Hex, Binary, URL encoding, hash
generation, and dictionary-based hash cracking.

Pure Python standard library. No pip install, no internet connection
required. Built to run anywhere Python 3 does, including Kali Linux out of
the box.

## Why

CyberChef is great, but sometimes you want the same handful of operations
available directly in your terminal — scriptable, pipeable, and part of
your own toolkit rather than a browser tab.

## Install

```bash
git clone https://github.com/madar44/decodelab.git
cd decodelab
chmod +x decodelab.py
```

No dependencies to install — it only uses the Python standard library.

## Usage

```bash
decodelab.py <codec> <encode|decode> [value]
decodelab.py hash <algorithm> [value]
decodelab.py crack --hash <hex> --algo <algorithm> --wordlist <path>
```

If value is omitted, input is read from stdin, so every subcommand is
pipe-friendly.

### Codecs

| Codec | Description               |
|-------|----------------------------|
| b64   | Base64                     |
| b32   | Base32                     |
| hex   | Hexadecimal                |
| bin   | Binary (8-bit groups)      |
| url   | URL / percent-encoding     |

### Examples

```bash
# Encode / decode
./decodelab.py b64 encode "hello"
./decodelab.py b32 decode "NBSWY3DP"
cat payload.txt | ./decodelab.py hex decode

# Hash generation
./decodelab.py hash sha256 "hello"
echo -n "hello" | ./decodelab.py hash md5

# Dictionary attack against a known hash
./decodelab.py crack --hash 5d41402abc4b2a76b9719d911017c592 \
    --algo md5 --wordlist /usr/share/wordlists/rockyou.txt
```

Supported hash algorithms: md5, sha1, sha224, sha256, sha384, sha512.

## Disclaimer

This tool is intended for educational use and authorized security testing
only (CTFs, labs, your own systems, or engagements you're explicitly
authorized for). Don't use it against systems or data you don't have
permission to test.

## License

MIT — see LICENSE.
