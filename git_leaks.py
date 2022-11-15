import re
import git
import pandas as pd

REPO_DIR = "./app/skale/skale-manager"


def extract():
    """
    Extracts raw text from all commits in a repo
    """
    repo = git.Repo(REPO_DIR)
    s = ""
    for commit in repo.iter_commits():
        s += commit.message + "\n"
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
    for leak in leaks:
        start = leak.start()
        word = raw_text[start : leak.end()]
        surrounding = raw_text[start - margin : leak.end() + margin]
        surrounding = re.sub(r"\s+", " ", surrounding)
        surrounding = re.sub(f"{word}", f"***{word}***", surrounding)
        leaks_list.append(
            {"word": word, "start": start, "surrounding": surrounding, "type": "word"}
        )
    for email in emails:
        start = email.start()
        word = raw_text[start : email.end()]
        surrounding = raw_text[start - margin : email.end() + margin]
        surrounding = re.sub(r"\s+", " ", surrounding)
        surrounding = re.sub(f"{word}", f"***{word}***", surrounding)
        leaks_list.append(
            {"word": word, "start": start, "surrounding": surrounding, "type": "email"}
        )
    return leaks_list


def load(data):
    """Loads a Dataframe with each leak, type, start and surrounding text"""
    df = pd.DataFrame(data)
    df = df[["type", "word", "start", "surrounding"]]
    df.to_csv("leaks.csv", index=False)


def load_json(data):
    """Loads a Dataframe with each leak, type, start and surrounding text"""
    df = pd.DataFrame(data)
    df = df[["type", "word", "start", "surrounding"]]
    df.to_json("leaks.json", orient="records")


if __name__ == "__main__":
    raw_text = extract()
    data = transform(raw_text)
    # load(data)
    load_json(data)
