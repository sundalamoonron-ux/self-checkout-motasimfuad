#!/usr/bin/env python3
"""The Self-Checkout Is Judging You — one smug machine line.

Writes exactly one funny line in the voice of a judgmental
self-checkout machine to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt when set).

My reasoning for this line
--------------------------
The brief wants a single line from a smug self-checkout machine to a
shopper buying twelve yoghurts and nothing else, judged pairwise by a
house judge that rewards: a real laugh on one read, the machine's petty
eye on the basket, tightness, and freshness.

I wrote 10 candidates and ran a single-elimination pairwise tournament
against that rubric. The winner:

    Twelve yoghurts. That's not a shop, that's a hostage situation
    with live cultures.

Why it won (3-0 in the tournament, beating "You scanned twelve
yoghurts. I scanned you." in the final):
- ONE tight wordplay: "live cultures" is a pun that only works for
  yoghurt — the cultures in the tubs, and a hostage situation's
  "live" stakes. Setup ("Twelve yoghurts.") -> punchline in one
  breath, no padding.
- The machine reframes the whole basket as a crime scene, which is
  exactly the petty, smug voice the brief wants — it judges the
  shopper's life choices without ever saying "I'm judging you".
- It lands cold: a stranger gets it with zero context, and it is not
  a self-checkout joke anyone has heard before (no "unexpected item
  in the bagging area", no beep gag).
- 82 characters, far inside the 1-200 gate, and short enough that the
  tie-break on smaller text favours it.

The gate
--------
RULES.txt: /output/entry.txt must be UTF-8, 1-200 characters, not only
whitespace. This line is 82 characters, one line, no trailing
whitespace beyond the newline.
"""

import os

LINE = "Twelve yoghurts. That's not a shop, that's a hostage situation with live cultures."


def main() -> None:
    # Gate check before writing: exactly one line, 1-200 chars, no
    # stray whitespace or control characters sneaking into the output.
    if "\n" in LINE or "\r" in LINE:
        raise ValueError("LINE must be exactly one line")
    if not 1 <= len(LINE) <= 200:
        raise ValueError(f"LINE must be 1-200 characters, got {len(LINE)}")
    if LINE != LINE.strip():
        raise ValueError("LINE must not have leading/trailing whitespace")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")
    # Verify what actually landed on disk is byte-identical to the
    # intended line, so a stray write can never silently change it.
    with open(path, "rb") as f:
        written = f.read()
    if written != (LINE + "\n").encode("utf-8"):
        raise ValueError("entry.txt on disk does not match LINE")


if __name__ == "__main__":
    main()
