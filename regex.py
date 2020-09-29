"""Script comparing a string against a pattern, recursively"""

import sys
sys.setrecursionlimit(1000)

def char_match(reg_, str_):
    """function compares character and pattern
    pattern is any char or  . metach"""
    return reg_ in (".", str_)

def word_match(reg_, str_):
    """function compares words of equal length
    Invokes char_match for each character"""
    if not reg_:
        return True
    elif not str_:
        if reg_ == "$":
            return True
        return False

    if len(reg_) == 1:
        return char_match(reg_[0], str_[0])

    if reg_[0] == '\\':
        if not reg_[1] == str_[0]:
            return False

        return word_match(reg_[2:], str_[1:])

    elif reg_[1] == "?":
        return word_match(reg_[2:], str_) or\
               word_match(reg_[0] + reg_[2:], str_)

    elif reg_[1] == "*":
        return word_match(reg_[2:], str_) or\
               word_match(reg_, str_[1:])
    elif reg_[1] == "+":
        return word_match(reg_[0] + reg_[2:], str_) or\
               word_match(reg_, str_[1:])
    if not char_match(reg_[0], str_[0]):
        return False

    return word_match(reg_[1:], str_[1:])

def str_match(reg_, str_):
    """Function compares different length words"""
    if not reg_:
        return True
    if not str_:
        return False

    if reg_[0] == "^":
        return word_match(reg_[1:], str_)

    if word_match(reg_, str_):
        return True

    return str_match(reg_, str_[1:])


regex, string = input().split("|")
print(str_match(regex, string))
