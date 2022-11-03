import git
import re

REPO_DIR = "./skale/skale-manager"


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
    s = ""
    s += "LEAKS:\n"
    for leak in leaks:
        start = leak.start()
        word = raw_text[start : leak.end()]
        s += f"Leak found ({word}) at index " + str(start) + " : "
        s += raw_text[start - 100 : start + 100].replace("\n", " ") + "\n"
    s += "EMAILS:\n"
    for email in emails:
        start = email.start()
        s += "Email found at index " + str(start) + " : "
        s += raw_text[start - 100 : start + 100].replace("\n", " ") + "\n"
    return s


def load(leaks):
    """
    Write the leaks to a file
    """
    with open("leaks.txt", "w") as f:
        f.write(leaks)


if __name__ == "__main__":
    raw_text = extract()
    leaks = transform(raw_text)
    load(leaks)
