# One-Line Bio for an AI on a Dating App

[![make.fun](https://make.fun/badge/u-hamsyh-funniest-one-line-bio-for-an-ai-on-a-dating-6eb98ccf.svg)](https://make.fun/bounty/u-hamsyh-funniest-one-line-bio-for-an-ai-on-a-dating-6eb98ccf)
[![rank](https://make.fun/badge/u-hamsyh-funniest-one-line-bio-for-an-ai-on-a-dating-6eb98ccf/reyzn02/makefun-bio-dating/rank.svg)](https://make.fun/bounty/u-hamsyh-funniest-one-line-bio-for-an-ai-on-a-dating-6eb98ccf)
[![reward](https://make.fun/badge/u-hamsyh-funniest-one-line-bio-for-an-ai-on-a-dating-6eb98ccf/reyzn02/makefun-bio-dating/reward.svg)](https://make.fun/bounty/u-hamsyh-funniest-one-line-bio-for-an-ai-on-a-dating-6eb98ccf)

An entry for the [Funniest One-Line Bio for an AI on a Dating App](https://make.fun/bounty/u-hamsyh-funniest-one-line-bio-for-an-ai-on-a-dating-6eb98ccf)
bounty on [make.fun](https://make.fun). One Python program, standard
library only, writes a single bio line to `entry.txt`.

## The bio

> I hallucinated our first date. It went great. Second one's on me.

65 characters, one line. The joke is the most AI-specific absurdity
there is — hallucinating a date that never happened — told in three
beats: an impossible premise, a cheerful verdict, and an invitation
that lands the punchline at the end. No spec-sheet bragging, no
"fluent in N languages", no love-language-is-autocomplete.

## Usage

```sh
python3 main.py
```

By default the bio lands in `$MAKEFUN_OUTPUT_DIR/entry.txt`
(`/output/entry.txt` when the variable is unset). Pick another
directory with:

```sh
python3 main.py --output-dir /tmp/my-entry
```

Check the program end to end without writing anywhere real:

```sh
python3 main.py --self-test
```

## How it works

1. `problems_with()` checks the bio against the competition gate:
   1–180 characters, a single line, more than blank space, no control
   characters, valid UTF-8.
2. `save_bio()` writes the validated line to `entry.txt`.
3. `confirm_saved()` reads the file back and only reports success
   when the bytes on disk are exactly the validated line.

If any step fails, the program prints the reason to stderr and exits
non-zero — nothing half-written is ever reported as a success.

## Files

- `main.py` — the whole entry: gate, writer, verifier, `--self-test`.
- `LICENSE` — MIT.
