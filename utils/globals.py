""" List of globals, paths used in the project """
import datetime
import time
import re

# Set verbosity level related to how much info could be printed out when running the code.
# 0: none, 1: occasional print outs, 2: detailed print outs
# Notice, it is up to you to use this variable when constructing the code and deciding what could be printed out.
global_debug = 0

# read_docs.py: save content of every processed file into the text file
flag_text_file_save = True

# read_docs.py: supported file types
supported_file_types = ["pdf", "doc", "docx", "rtf", "txt"]

# ocr.py: if set then we use Division, Unsharp, Threshold in OCR processing
# global_DUT = True

# ocr.py: language of documents in tesseract, it could be also set as lang='eng+fra'
lang_ocr = "eng"

# Timestamp in format: 20240501
ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d')


def get_length_of_text(text: str, round_to: int = 0) -> int:
    """ Count number of characters excluding spaces in the text buffer.

    Parameters:
    text (str)
    round_to (int):
    round_to = 0 -> no rounding,
    round_to = -1 -> rounds to tens,
    round_to = -2 -> rounds to hundreds,
    round_to = -3 -> rounds to thousands etc.
    Return:
    length (int): number of characters without spaces
    """
    # Length w/o spaces
    length = len(text) - text.count(' ')
    length = round(length, round_to)

    return length


def contains_non_special_characters(s: str) -> bool:
    # This pattern looks for any character that is not a whitespace character
    return bool(re.search(r'\S', s))
