import re
import pkg_resources
import pandas as pd
from typing import (
    List,
    Dict,
    Optional
)
from dataclasses import dataclass
from mjjo import Log
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
        self.logger = Log('ConvertAddress').stream_handler("INFO")
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

    @staticmethod
    def _create_bjd_changed_dictionary(bjd_changed_df):
        bjd_changed_dictionary: Dict[str, str] = dict()
        for old_bjd_nm, new_bjd_nm in zip(bjd_changed_df['법정동명_변경전'], bjd_changed_df['법정동명_변경후']):
            if old_bjd_nm is not None \
            and new_bjd_nm is not None \
            and old_bjd_nm != new_bjd_nm:
                bjd_changed_dictionary[old_bjd_nm] = new_bjd_nm
        return bjd_changed_dictionary

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

        self.bjd_changed_df: pd.DataFrame = pd.read_csv(
            file_name_bjd_changed,
            sep=input_sep,
            engine='python',
            encoding=input_encoding)
        self.bjd_changed_old_bjd_nm_list: List[str] = list(old_nm for old_nm in self.bjd_current_df['법정동명_변경전'] if old_nm is not None)
        self.bjd_changed_dic: Dict[str, str] = self._create_bjd_changed_dictionary(self.bjd_changed_df)

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
            str: A string that is the smallest administrative division name and address number space of the input string, with multiple spaces normalized to a single space.
        """

        if not isinstance(addr, str):
            raise TypeError("type of object must be string")

        for bjdnm in self.bjd_smallest_list:
            if bjdnm in addr and (addr.split(bjdnm)[1][:2]).replace('-', '').isdigit() == True:
                addr = addr.split(bjdnm)[0] + bjdnm + ' ' + addr.split(bjdnm)[1]
                return addr
        return addr

    def correct_changed_bjd(
        self,
        addr: str,
        is_log: bool
    ) -> str:

        """
        입력된 문자열(한글 주소)에 변경전 법정동이 포함되어있으면 변경후 법정동명으로 교환하여 반환

        Args:
            addr (str): The input korean address string.

        Raises:
            TypeError: If the 'addr' object is not of type string.

        Returns:
            str: If the input string contains the previous administrative division name, eplace it with the modified administrative division name and return.
        """

        if not isinstance(addr, str):
            raise TypeError("type of object must be string")

        for old_bjd_nm in self.bjd_changed_old_bjd_nm_list:
            if old_bjd_nm in addr:
                new_bjd_nm = self.bjd_changed_dic[old_bjd_nm]
                correct_addr = addr.replace(old_bjd_nm, new_bjd_nm)
                if is_log:
                    self.logger.info(f'해당 법정동명은 변경되었습니다. 변경전 : [ {old_bjd_nm} ] 변경후 : [ {new_bjd_nm} ]')
                return correct_addr
        return addr
