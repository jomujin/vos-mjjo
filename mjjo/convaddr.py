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
class Address():


    def __init__(
        self,
        address: str
    ):
        self.address: str = address
        self.main_address: str = None
        self.detail_address: str = None
        self.smallest_bjd: str = None
        self.sido: str = None
        self.sgg: str = None
        self.emd: str = None
        self.ri: str = None


@dataclass
class ConvAddr():


    def __init__(self):
        self._prepare()
        pass

    @staticmethod
    def _concat_sido_sgg(
        sido_nm,
        sgg_nm
    ):
        if sido_nm is not None and sgg_nm is not None:
            return f'{sido_nm} {sgg_nm}'
        elif sido_nm is not None and sgg_nm is None:
            return sido_nm
        else:
            return None

    def _prepare(self):
        cls_bjd = Bjd()
        file_name_bjd: str = cls_bjd.file_name_bjd
        file_name_bjd_current: str = cls_bjd.file_name_bjd_current
        file_name_bjd_changed: str = cls_bjd.file_name_bjd_changed
        file_name_bjd_smallest: str = cls_bjd.file_name_bjd_smallest
        file_name_bjd_frequency_dictionary: str = cls_bjd.file_name_bjd_frequency_dictionary
        input_encoding = cls_bjd.output_encoding
        input_index = cls_bjd.output_index
        input_sep = cls_bjd.output_sep

        self.bjd_current_dic: Dict[str, str] = dict((line.split('\t')[2], line.split('\t')[9].replace('\n', '')) for line in open(file_name_bjd_current, 'r'))
        self.bjd_smallest_list: List[str] = [(line.strip()) for line in open(file_name_bjd_smallest, 'r')]
        
        self.bjd_current_df: pd.DataFrame = pd.read_csv(
            file_name_bjd_current,
            sep=input_sep,
            engine='python',
            encoding=input_encoding)
        self.bjd_current_df['시도시군구명'] = self.bjd_current_df[['시도명', '시군구명']].apply(lambda x: self._concat_sido_sgg(*x), axis=1)
        self.current_sido_sgg_list: List[str] = list(self.bjd_current_df['시도시군구명'].unique())
        self.current_sido_list: List[str] = list(self.bjd_current_df['시도명'].unique())
        self.current_sgg_list: List[str] = list(self.bjd_current_df['시군구명'].unique())
        self.current_emd_list: List[str] = list(self.bjd_current_df['읍면동명'].unique())
        self.current_ri_list: List[str] = list(self.bjd_current_df['리명'].unique())

        bjd_changed_df: pd.DataFrame = pd.read_csv(
            file_name_bjd_changed,
            sep=input_sep,
            engine='python',
            encoding=input_encoding)
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

    # 가장 작은 법정동명 뒤 번지가 띄어쓰기 없이 붙어있을 경우,
    # 가장 작은 법정동명에 포함된 숫자중 2자리수는 없음. 예 당산동1가, 을지로5가 등
    def correct_smallest_bjd_spacing(
        self,
        addr: str
    ) -> str:

        """
        입력된 문자열(한글 주소)의 가장 작은 법정동명과 번지 사이 빈공백을 단일 공백으로 정규화한 문자열로 반환

        Args:
            addr (str): The input korean address string.

        Raises:
            TypeError: If the 'addr' object is not of type string.

        Returns:
            str: A string that normalize multiple consecutive spaces in a string to a single space.
        """

        for bjdnm in self.bjd_smallest_list:
            if bjdnm in addr and (addr.split(bjdnm)[1][:2]).replace('-', '').isdigit() == True:
                addr = addr.split(bjdnm)[0] + bjdnm + ' ' + addr.split(bjdnm)[1]
                return addr
        return addr