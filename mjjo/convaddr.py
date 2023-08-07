import re
import pkg_resources
from typing import (
    Optional,
    List
)
from dataclasses import dataclass


@dataclass
class CorDate():


    def __init__(self):
        pass

def correct_simple_spacing(
    addr: str
) -> str:

    """
    입력된 문자열(한글 주소)의 연속된 공백을 단일 공백으로 정규화한 문자열로 반환

    Args:
        addr (str): The input korean address string.

    Raises:
        TypeError: If the 'addr' object is not of type string.

    Returns:
        str: A string that normalize multiple consecutive spaces in a string to a single space.
    """

    if not isinstance(addr, str):
        raise TypeError("type of object must be string")

    return re.sub(r'\s+', ' ', addr)
