import os
import re
import time
import json
from typing import (
    List,
    Dict,
    Optional
)
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class Bjd():


    def __init__(self):
        load_dotenv()
        self.api_base_url = "https://api.odcloud.kr/api"
        self.api_get_url = "/15063424/v1/uddi:257e1510-0eeb-44de-8883-8295c94dadf7" # https://www.data.go.kr/data/15063424/fileData.do#layer-api-guide API 목록 중 국토교통부_전국 법정동_20230710 GET
        self.api_key = os.environ['BJD_API_KEY']
        self.api_page = 0
        self.api_per_page = 1024
        self.bjd_api_dictionary = None
        self.bjd_api_df = None
        self._create_bjd()

    @staticmethod
    def _request_api(api_url):
        return requests.get(api_url)

    @staticmethod
    def _convert_json(response):
        return json.loads(response.content)

    def _crawl_api(self) -> Dict[str, Dict[str, str]]:
        res_dic: Dict[str, Dict[str, str]] = dict()
        api_page = self.api_page
        while True:
            api_url = f"{self.api_base_url}{self.api_get_url}?page={api_page}&perPage={self.api_per_page}&serviceKey={self.api_key}"
            response = self._request_api(api_url)
            json_datas = self._convert_json(response)
            if json_datas['data']:
                print(f"Crawling... {self.api_base_url}{self.api_get_url}?page={api_page}&perPage={self.api_per_page}")
                for data in json_datas['data']:
                    res_dic[f"{data['법정동코드']}"] = {
                        '과거법정동코드': data['과거법정동코드'],
                        '리명': data['리명'],
                        '법정동코드': data['법정동코드'],
                        '삭제일자': data['삭제일자'],
                        '생성일자': data['생성일자'],
                        '순위': data['순위'],
                        '시군구명': data['시군구명'],
                        '시도명': data['시도명'],
                        '읍면동명': data['읍면동명'],
                    }
                api_page += 1
            else:
                break
        return res_dic

    @staticmethod
    def _split_sgg_nm(
        sgg_nm: Optional[str]
    ) -> Optional[str]:
        """
        시군구 행정구역명에서 시와 군 혹은 구가 결합되어있는 행정구역명을 분리하는 기능 \n
        조건에 부합하지 않을 경우 sgg_nm 을 그대로 반환한다
        
        - 조건 1: 결측값이 아님
        - 조건 2: 문자열수가 4개 이상
        - 조건 3: 마지막 문자열이 '구' 혹은 '군'
        - 조건 4: 첫번째와 마지막 문자열을 제외한 나머지 문자열 중 '시' 가 포함
        """

        if sgg_nm is not None \
        and len(sgg_nm) > 3 \
        and sgg_nm[-1] in ['구', '군'] \
        and '시' in sgg_nm[1:-1]:
            result = sgg_nm.split('시', 1)
            result[0] = result[0] + '시'
            return ' '.join(result)
        else:
            return sgg_nm

    @staticmethod
    def _clean_bjd_nm(
        bjd_nm: Optional[str]
    ) -> str:
        """
        행정구역명에서 한글과 숫자를 제외하고 삭제하는 기능 \n
        bjd_nm is None 일 경우 ''을 반환한다
        """

        if bjd_nm is not None:
            return re.sub(r'[^0-9ㄱ-ㅎ가-힣]+', '', bjd_nm)
        return ''

    def _get_full_bjd_nm(
        self,
        sido_nm: Optional[str],
        sgg_nm: Optional[str],
        emd_nm: Optional[str],
        ri_nm: Optional[str]
    ) -> str:
        """
        행정구역명을 결합하여 전체 법정동명을 생성하는 기능
        """

        sido_nm = self._clean_bjd_nm(sido_nm)
        sgg_nm = self._clean_bjd_nm(self._split_sgg_nm(sgg_nm))
        emd_nm = self._clean_bjd_nm(emd_nm)
        ri_nm = self._clean_bjd_nm(ri_nm)

        full_bjd_nm = f'{sido_nm} {sgg_nm} {emd_nm} {ri_nm}'
        full_bjd_nm = full_bjd_nm.strip()  # 맨 앞과 맨 뒤의 공백 제거
        full_bjd_nm = re.sub(r'\s+', ' ', full_bjd_nm)  # 공백이 여러 칸인 것을 한 칸으로 변경
        return full_bjd_nm

    def _make_dataframe(self, res_dic) -> pd.DataFrame:
        res_df = pd.DataFrame(res_dic).T.sort_values('법정동코드').reset_index().drop(columns='index').replace(0, None).replace('0', None)
        res_df['법정동명'] = res_df[[
            '시도명',
            '시군구명',
            '읍면동명',
            '리명'
        ]].apply(lambda x: self._get_full_bjd_nm(*x), axis=1)
        return res_df
    
    def _create_bjd(self):
        res_dic = self._crawl_api()
        res_df = self._make_dataframe(res_dic)
        self.bjd_api_dictionary = res_dic
        self.bjd_api_df = res_df