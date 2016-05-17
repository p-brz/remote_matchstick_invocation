from colorama import Style
from .defs import *


def text_custom(string_val, color=None, prefix=TEXT_PREFIX):
    if color is None or not COLORS_ENABLED:
        return prefix + str(string_val)
    else:
        return prefix + color + str(string_val) + Style.RESET_ALL


def text_default(string_val, prefix=TEXT_PREFIX):
    return text_custom(string_val, DEFAULT_TEXT_COLOR, prefix)


def text_primary(string_val, prefix=TEXT_PREFIX):
    return text_custom(string_val, PRIMARY_TEXT_COLOR, prefix)


def text_success(string_val, prefix=TEXT_PREFIX):
    return text_custom(string_val, SUCCESS_TEXT_COLOR, prefix)


def text_info(string_val, prefix=TEXT_PREFIX):
    return text_custom(string_val, INFO_TEXT_COLOR, prefix)


def text_warning(string_val, prefix=TEXT_PREFIX):
    return text_custom(string_val, WARNING_TEXT_COLOR, prefix)


def text_danger(string_val, prefix=TEXT_PREFIX):
    return text_custom(string_val, DANGER_TEXT_COLOR, prefix)


def text_same_space(source, target):
    target_len = len(target)
    source_len = len(source)
    difference = target_len - source_len
    text = source
    for i in range(difference):
        text = text + " "

    return text
