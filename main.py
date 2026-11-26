#!/usr/bin/env python3
"""Write the champion one-line AI dating-app bio to entry.txt.

Entry for the make.fun bounty "Funniest One-Line Bio for an AI on a
Dating App" (u-hamsyh-funniest-one-line-bio-for-an-ai-on-a-dating-6eb98ccf).

Python standard library only. The bio is written to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt) after the
competition gate is validated: UTF-8 text of 1 to 180 characters, not
only white space.
"""

import os
import sys

LINE = "I hallucinated our first date. It went great. Second one's on me."

MAX_CHARS = 180


def gate_ok(text):
    """Return True when the text passes the sealed gate."""
    if not text or not text.strip():
        return False
    if text != text.strip():
        return False
    # A one-line bio: no line breaks of any kind.
    if "\n" in text or "\r" in text:
        return False
    if len(text) > MAX_CHARS:
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def main():
    if not gate_ok(LINE):
        print("entry fails the gate", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(LINE)
    # Verify what landed on disk is exactly the validated line.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != LINE or not gate_ok(written):
        print("written entry does not match the validated line", file=sys.stderr)
        return 1
    print("wrote %d chars to %s" % (len(LINE), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
