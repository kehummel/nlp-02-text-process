"""lyrics_text_preprocessing.py - Project script (example).

Purpose

  Read text data, preprocess the text, compare raw and cleaned tokens,
  and summarize the results.

Analytical Questions

- What does the raw text of lyrics look like before preprocessing?
- How does tokenization change the text into analyzable units?
- How do lowercasing, punctuation removal, and stop word removal
  affect the results?
- What preprocessing steps might improve later NLP tasks?


Run from root project folder with:

  uv run python -m nlp.lyrics_text_preprocessing
"""

# ============================================================
# Section 1. Setup and Imports (includes logging deps)
# ============================================================
import logging
from pathlib import Path
import re

from datafun_toolkit.logger import get_logger, log_header, log_path
import matplotlib.pyplot as plt
import polars as pl

print("Imports complete.")

# ============================================================
# Configure Logging (script execution only)
# ============================================================

LOG: logging.Logger = get_logger("CI", level="DEBUG")

ROOT_PATH: Path = Path.cwd()
DATA_PATH: Path = ROOT_PATH / "data"
NOTEBOOKS_PATH: Path = ROOT_PATH / "notebooks"
SCRIPTS_PATH: Path = ROOT_PATH / "scripts"

log_header(LOG, "NLP")
LOG.info("START script.....")

log_path(LOG, "ROOT_PATH", ROOT_PATH)
log_path(LOG, "DATA_PATH", DATA_PATH)
log_path(LOG, "NOTEBOOKS_PATH", NOTEBOOKS_PATH)
log_path(LOG, "SCRIPTS_PATH", SCRIPTS_PATH)

# ============================================================
# Section 2. Read the Text Data
# ============================================================

# Choose a text file to analyze.
# Each line is treated as one text record.
input_path1: Path = DATA_PATH / "dolly-parton.txt"
input_path2: Path = DATA_PATH / "johnny-cash.txt"

# Read all lines from the file.
text_list1: list[str] = input_path1.read_text(encoding="utf-8").splitlines()
text_list2: list[str] = input_path2.read_text(encoding="utf-8").splitlines()

# Remove blank lines.
text_list1 = [line.strip() for line in text_list1 if line.strip()]
text_list2 = [line.strip() for line in text_list2 if line.strip()]

print("Data loaded successfully.")
print(f"Loaded {len(text_list1):,} text records.")
print(f"Loaded {len(text_list2):,} text records.")

# Combine all text rows into one large string for simple preprocessing.
raw_text1: str = " ".join(text_list1)
raw_text2: str = " ".join(text_list2)

print(f"Raw text length for Dolly Parton: {len(raw_text1):,} characters")
print("First 50 characters of Dolly Parton:")
print(raw_text1[:50])
print(f"Raw text length for Johnny Cash: {len(raw_text2):,} characters")
print("First 50 characters of Johnny Cash:")
print(raw_text2[:50])

# ============================================================
# Section 3. Inspect the Raw Text
# ============================================================

# Review the text records before preprocessing.
# This helps confirm the data loaded correctly and gives a
# sense of the structure of the text.

# Dolly Parton
print("First 5 text records for Dolly Parton:")
for line in text_list1[:5]:
    print("-", line)

print(f"\nLoaded {len(text_list1):,} text records.")
print(f"Raw text length: {len(raw_text1):,} characters")

print("\nFirst 50 characters of Dolly Parton text:")
print(raw_text1[:50])

# Johnny Cash
print("First 5 text records for Johnny Cash:")
for line in text_list2[:5]:
    print("-", line)

print(f"\nLoaded {len(text_list2):,} text records.")
print(f"Raw text length: {len(raw_text2):,} characters")

print("\nFirst 50 characters of Johnny Cash text:")
print(raw_text2[:50])

# ============================================================
# Section 4. Tokenize the Raw Text
# ============================================================

# Split the raw text into rough word-like pieces using whitespace.

# Dolly Parton
raw_tokens1: list[str] = raw_text1.split()
count_of_raw_tokens1: int = len(raw_tokens1)

print("First 20 raw tokens:")
print(raw_tokens1[:20])
print(f"Dolly Partonn's total raw tokens: {count_of_raw_tokens1:,}")

# Johnny Cash
raw_tokens2: list[str] = raw_text2.split()
count_of_raw_tokens2: int = len(raw_tokens2)

print("First 20 raw tokens:")
print(raw_tokens2[:20])
print(f"Johnny Cash's total raw tokens: {count_of_raw_tokens2:,}")

# ============================================================
# Section 5. Normalize the Text
# ============================================================

# Convert all text to lowercase so words like "Data" and "data"
# are treated as the same token.

# Dolly Parton
lower_text1: str = raw_text1.lower()

print("First 50 characters of Dolly Parton's lowercase text:")
print(lower_text1[:50])

# Johnny Cash
lower_text2: str = raw_text2.lower()

print("First 50 characters of Johnny Cash'slowercase text:")
print(lower_text2[:50])

# ============================================================
# Section 6. Remove Punctuation and Tokenize Again
# ============================================================

# Replace any character that is not a letter, number, or whitespace
# with a space. This removes punctuation and many special characters.

# Dolly Parton
no_punct_text1: str = re.sub(r"[^a-z0-9\s]", " ", lower_text1)

# Tokenize again after punctuation removal.
tokens_no_punct1: list[str] = no_punct_text1.split()
count_of_tokens_no_punct1: int = len(tokens_no_punct1)

print("First 20 tokens after lowercasing and punctuation removal for Dolly Parton:")
print(tokens_no_punct1[:20])
print(f"Total tokens after punctuation removal: {count_of_tokens_no_punct1:,}")

# Johnny Cash
no_punct_text2: str = re.sub(r"[^a-z0-9\s]", " ", lower_text2)

# Tokenize again after punctuation removal.
tokens_no_punct2: list[str] = no_punct_text2.split()
count_of_tokens_no_punct2: int = len(tokens_no_punct2)

print("First 20 tokens after lowercasing and punctuation removal for Johnny Cash")
print(tokens_no_punct2[:20])
print(f"Total tokens after punctuation removal: {count_of_tokens_no_punct2:,}")

# ============================================================
# Section 7. Remove Stop Words
# ============================================================

# Stop words are very common words that often add little meaning
# for simple frequency analysis.
STOP_WORDS: set[str] = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
}

# Keep only tokens that:
# - are longer than 2 characters
# - are not in the stop word list

# Dolly Parton
clean_tokens1: list[str] = [
    token for token in tokens_no_punct1 if len(token) > 2 and token not in STOP_WORDS
]

count_of_clean_tokens1: int = len(clean_tokens1)

print("First 20 cleaned tokens for Dolly Parton:")
print(clean_tokens1[:20])
print(f"Total cleaned tokens: {count_of_clean_tokens1:,}")

# Johnny Case
clean_tokens2: list[str] = [
    token for token in tokens_no_punct2 if len(token) > 2 and token not in STOP_WORDS
]

count_of_clean_tokens2: int = len(clean_tokens2)

print("First 20 cleaned tokens for Johnny Cash:")
print(clean_tokens2[:20])
print(f"Total cleaned tokens: {count_of_clean_tokens2:,}")

# ============================================================
# Section 8. Build a Before/After Summary Table
# ============================================================

summary_df: pl.DataFrame = pl.DataFrame(
    {
        "stage": [
            "raw tokens for Dolly Parton",
            "after punctuation removal for Dolly Parton",
            "after stop word removal for Dolly Parton",
            "raw tokens for Johnny Cash",
            "after punctuation removal for Johnny Cash",
            "after stop word removal for Johnny Cassh",
        ],
        "count": [
            count_of_raw_tokens1,
            count_of_tokens_no_punct1,
            count_of_clean_tokens1,
            count_of_raw_tokens2,
            count_of_tokens_no_punct2,
            count_of_clean_tokens2,
        ],
    }
)

print("Preprocessing summary:")
print(summary_df)

# ============================================================
# Section 9. Build a Frequency Table with Polars
# ============================================================

# Create a Polars DataFrame with one row per cleaned token.
# Dolly Parton Dataframe
tokenDP_df: pl.DataFrame = pl.DataFrame({"tokenDP": clean_tokens1})

# Group by token, count occurrences, and sort from most common to least common.
freqDP_df: pl.DataFrame = (
    tokenDP_df.group_by("tokenDP").len().sort("len", descending=True)
)

print("Top 20 most frequent cleaned tokens for Dolly Parton:")
print(freqDP_df.head(20))

# Johnny Cash Dataframe
tokenJC_df: pl.DataFrame = pl.DataFrame({"tokenJC": clean_tokens2})

# Group by token, count occurrences, and sort from most common to least common.
freqJC_df: pl.DataFrame = (
    tokenJC_df.group_by("tokenJC").len().sort("len", descending=True)
)

print("Top 20 most frequent cleaned tokens for Johnny Cash:")
print(freqJC_df.head(20))

# ============================================================
# Section 10. Build a "Most Frequent Cleaned Tokens" Bar Chart
# ============================================================

# Dolly Parton
topDP_df: pl.DataFrame = freqDP_df.head(15)

plt.figure(figsize=(10, 5))
plt.bar(topDP_df["tokenDP"], topDP_df["len"])

ax = plt.gca()
ax.tick_params(axis="x", labelrotation=45)

plt.title("Most Frequent Cleaned Tokens For Dolly Parton's Songs")
plt.xlabel("Token")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Johnny Cash
topJC_df: pl.DataFrame = freqJC_df.head(15)

plt.figure(figsize=(10, 5))
plt.bar(topJC_df["tokenJC"], topJC_df["len"])

ax = plt.gca()
ax.tick_params(axis="x", labelrotation=45)

plt.title("Most Frequent Cleaned Tokens For Johnny Cash's Songs")
plt.xlabel("Token")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# ============================================================
# Section 11. Compare Raw vs Clean Token Counts
# ============================================================

plt.figure(figsize=(8, 5))
plt.bar(summary_df["stage"], summary_df["count"])

ax = plt.gca()
ax.tick_params(axis="x", labelrotation=90)

plt.title("Token Counts Across Preprocessing Stages")
plt.xlabel("Stage")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# ============================================================
# LOG THE END (only in the script)
# ============================================================

LOG.info("========================")
LOG.info("Pipeline executed successfully!")
LOG.info("========================")
LOG.info("END main()")
