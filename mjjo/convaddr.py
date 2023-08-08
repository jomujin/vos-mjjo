import re
import pkg_resources
import pandas as pd
from typing import (
    List,
    Dict,
    Optional
)
from dataclasses import dataclass
from mjjo.bjd import Bjd


@dataclass
class ConvAddr():


    def __init__(self):
        self._prepare()
        pass

    def _prepare(self):
        cls_bjd = Bjd()
        file_name_bjd: str = cls_bjd.file_name_bjd
        file_name_bjd_current: str = cls_bjd.file_name_bjd_current
        file_name_bjd_changed: str = cls_bjd.file_name_bjd_changed
        file_name_bjd_smallest: str = cls_bjd.file_name_bjd_smallest
        file_name_bjd_frequency_dictionary: str = cls_bjd.file_name_bjd_frequency_dictionary

        self.bjd_current_dic: Dict[str, str] = dict((line.split('\t')[2], line.split('\t')[9].replace('\n', '')) for line in open(file_name_bjd_current, 'r'))
        self.bjd_smallest_list: List[str] = [(line.strip()) for line in open(file_name_bjd_smallest, 'r')]
        bjd_changed_df: pd.DataFrame = pd.read_csv(file_name_bjd_changed, sep='\t', engine='python', encoding='utf-8')
        old_bjd_nm_list: List[str] = list(bjd_changed_df['법정동명_변경전'])
        new_bjd_nm_list: List[str] = list(bjd_changed_df['법정동명_변경후'])
        self.bjd_changed_dic: Dict[str, str] = dict((oldnm, newnm) for oldnm, newnm in zip(old_bjd_nm_list, new_bjd_nm_list))

    @staticmethod
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
