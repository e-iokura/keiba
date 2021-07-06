import re

def get_from_text(pattern, text):
    match = re.findall(pattern, text)
    return match[0] if len(match) > 0 else ""

def trim_bs_text(text):
    return text.replace("\n", "").strip()
