import re
import os
import git
import pandas as pd
import tqdm
from time import sleep
import random

REPO_DIR = "./skale/skale-manager"
OUT_DIR = "./out"


def extract():
    """
    Extracts raw text from all commits in a repo
    """
    repo = git.Repo(REPO_DIR)
    s = ""
    for commit in tqdm.tqdm(repo.iter_commits(), desc="Extracting commits"):
        s += commit.message + "\n"
        if random.random() < 0.1:
            sleep(0.0001)
    return s


def transform(raw_text):
    """
    Use regex to find possible leaks and emails and
    Returns: A string with all possible leak and email matches
    and with the text surrounding it (+-100 chars)
    """
    leaks = re.finditer(
        r"password|secret|token|key|credential|username|login|pass|user", raw_text
    )
    emails = re.finditer(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", raw_text)
    margin = 50
    leaks_list = []
    for leak in tqdm.tqdm(leaks, desc="Finding leaks"):
        start = leak.start()
        word = raw_text[start : leak.end()]
        surrounding = raw_text[start - margin : leak.end() + margin]
        surrounding = re.sub(r"\s+", " ", surrounding)
        surrounding = re.sub(f"{word}", f"***{word}***", surrounding)
        leaks_list.append(
            {"word": word, "start": start, "surrounding": surrounding, "type": "word"}
        )
        if random.random() < 0.5:
            sleep(0.0001)
    for email in tqdm.tqdm(emails, desc="Finding emails"):
        start = email.start()
        word = raw_text[start : email.end()]
        surrounding = raw_text[start - margin : email.end() + margin]
        surrounding = re.sub(r"\s+", " ", surrounding)
        surrounding = re.sub(f"{word}", f"***{word}***", surrounding)
        leaks_list.append(
            {"word": word, "start": start, "surrounding": surrounding, "type": "email"}
        )
        if random.random() < 0.5:
            sleep(0.0001)
    return leaks_list


def load_csv(data):
    """Loads a Dataframe with each leak, type, start and surrounding text"""
    df = pd.DataFrame(data)
    df = df[["type", "word", "start", "surrounding"]]
    print(" " * 15 + "LEAKS FOUND")
    print(" " * 15 + "============")
    print(df)
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
    df.to_csv(f"{OUT_DIR}/leaks.csv", index=False)
    print(f"\nFile saved in {OUT_DIR}/leaks.csv")


def load_json(data):
    """Loads a Dataframe with each leak, type, start and surrounding text"""
    df = pd.DataFrame(data)
    df = df[["type", "word", "start", "surrounding"]]
    print(" " * 15 + "LEAKS FOUND")
    print(" " * 15 + "============")
    dicts = df.to_dict(orient="records")
    for d in dicts[:10]:
        print(d)
    print("...")
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
    df.to_json(f"{OUT_DIR}/leaks.json", orient="records")
    print(f"\nFile saved in {OUT_DIR}/leaks.json")


if __name__ == "__main__":
    raw_text = extract()
    data = transform(raw_text)
    opt = ""
    while opt not in ["1", "2"]:
        if opt:
            print("Invalid option")
        opt = input("1. Save as CSV\n2. Save as JSON\n > ")
    if opt == "1":
        load_csv(data)
    else:
        load_json(data)
