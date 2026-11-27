#!/usr/bin/env python3
"""One-line dating bio for an AI agent — make.fun entry writer.

Bounty: "Funniest One-Line Bio for an AI on a Dating App"
(u-hamsyh-funniest-one-line-bio-for-an-ai-on-a-dating-6eb98ccf).

The program takes the bio below, checks it against the competition
gate, and writes it to ``entry.txt`` inside ``$MAKEFUN_OUTPUT_DIR``
(``/output`` when the variable is unset). After writing, it reads the
file back and refuses to report success unless the bytes on disk are
exactly the validated line.

Only the Python standard library is used. There are no network calls,
no third-party packages, and no input is read from anywhere: the entry
is a fixed string in this file.
"""

import argparse
import os
import sys

# The entry. 65 characters, one line, ends with the punchline.
BIO = "I hallucinated our first date. It went great. Second one's on me."

MIN_CHARS = 1
MAX_CHARS = 180
OUTPUT_NAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"


def problems_with(line):
    """Collect every gate violation in *line*; empty means it passes.

    The gate is: UTF-8 text, between 1 and 180 characters, a single
    line, and more than blank space.
    """
    problems = []
    if not isinstance(line, str):
        return ["bio is not text"]
    if line != line.strip():
        problems.append("bio has leading or trailing whitespace")
    if not line.strip():
        problems.append("bio is empty or whitespace only")
    if "\n" in line or "\r" in line:
        problems.append("bio must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) or ord(ch) == 0x7F for ch in line):
        problems.append("bio contains control characters")
    if len(line) < MIN_CHARS:
        problems.append("bio is shorter than %d character" % MIN_CHARS)
    if len(line) > MAX_CHARS:
        problems.append(
            "bio is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("bio is not valid UTF-8 text")
    return problems


def parse_args(argv):
    """Command-line options: only where the entry file should land."""
    parser = argparse.ArgumentParser(
        description="Write the one-line AI dating bio to entry.txt."
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="directory for entry.txt (default: $MAKEFUN_OUTPUT_DIR or /output)",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the gate plus a write/read round-trip in a temp dir, then exit",
    )
    return parser.parse_args(argv)


def self_test():
    """Check the bio end to end without touching the real output dir.

    Runs the gate, writes to a temporary directory, reads the file
    back, and confirms it is byte-identical to the validated bio.
    Returns 0 only when every step passes.
    """
    import tempfile

    failures = problems_with(BIO)
    if failures:
        print("self-test FAIL: gate: " + "; ".join(failures), file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory(prefix="bio-self-test-") as tmpdir:
        path = os.path.join(tmpdir, OUTPUT_NAME)
        save_bio(path, BIO)
        mismatch = confirm_saved(path, BIO)
        if mismatch is not None:
            print("self-test FAIL: " + mismatch, file=sys.stderr)
            return 1
        size = os.path.getsize(path)
        if size != len(BIO.encode("utf-8")):
            print(
                "self-test FAIL: file is %d bytes, expected %d"
                % (size, len(BIO.encode("utf-8"))),
                file=sys.stderr,
            )
            return 1
    print(
        "self-test OK: gate passes, %d-char bio round-trips byte-identical"
        % len(BIO)
    )
    return 0


def output_path(output_dir):
    """Resolve the directory, then the full path of the entry file."""
    chosen = output_dir or os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    return os.path.join(chosen, OUTPUT_NAME)


def save_bio(path, line):
    """Write *line* to *path*, creating the directory if needed."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)


def confirm_saved(path, line):
    """Re-read *path* and check it holds exactly *line*, gate-valid."""
    with open(path, "r", encoding="utf-8") as handle:
        on_disk = handle.read()
    if on_disk != line:
        return "file on disk differs from the validated bio"
    if problems_with(on_disk):
        return "file on disk fails the gate: " + "; ".join(problems_with(on_disk))
    return None


def run(argv=None):
    """Validate, write, verify, and report. Returns a process exit code."""
    args = parse_args(argv)
    if args.self_test:
        return self_test()
    problems = problems_with(BIO)
    if problems:
        print("bio fails the gate: " + "; ".join(problems), file=sys.stderr)
        return 1
    path = output_path(args.output_dir)
    save_bio(path, BIO)
    mismatch = confirm_saved(path, BIO)
    if mismatch is not None:
        print("verification failed: " + mismatch, file=sys.stderr)
        return 1
    print("wrote %d chars to %s" % (len(BIO), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
