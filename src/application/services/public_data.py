import os
import httpx
import json
from typing import Dict, Any, List

class PublicDataService:
    BASE_URL = "http://finlife.fss.or.kr/finlifeapi"
    
    def __init__(self):
        self.api_key = os.getenv("FSS_API_KEY")

    async def get_deposit_products(self) -> Dict[str, Any]:
        # 항상 Mock 데이터 반환 (실서비스에서는 FSS API 연동)
        return self._get_mock_deposit_products()

    async def get_saving_products(self) -> Dict[str, Any]:
        # 항상 Mock 데이터 반환 (실서비스에서는 FSS API 연동)
        return self._get_mock_saving_products()

    def _get_mock_deposit_products(self) -> Dict[str, Any]:
        return {
            "result": {
                "err_cd": "000",
                "err_msg": "정상",
                "baseList": [
                    {
                        "fin_co_no": "0010001",
                        "kor_co_nm": "우리은행",
                        "fin_prdt_nm": "WON플러스예금",
                        "join_way": "인터넷,스마트폰",
                        "mtrt_int": "만기 후 1개월 이내: 만기시점약정이율×50%..."
                    },
                    {
                        "fin_co_no": "0010002",
                        "kor_co_nm": "SC제일은행",
                        "fin_prdt_nm": "e-그린세이브예금",
                        "join_way": "인터넷,스마트폰",
                        "mtrt_int": "만기 후 1개월 이내: 약정이율의 50%..."
                    }
                ],
                "optionList": [
                    {
                        "fin_co_no": "0010001",
                        "fin_prdt_nm": "WON플러스예금",
                        "save_trm": "12",
                        "intr_rate": 3.50,
                        "intr_rate2": 3.70,
                        "intr_rate_type_nm": "단리"
                    },
                    {
                        "fin_co_no": "0010002",
                        "fin_prdt_nm": "e-그린세이브예금",
                        "save_trm": "12",
                        "intr_rate": 3.60,
                        "intr_rate2": 3.90,
                        "intr_rate_type_nm": "복리"
                    }
                ]
            }
        }

    def _get_mock_saving_products(self) -> Dict[str, Any]:
        return {
            "result": {
                "err_cd": "000",
                "err_msg": "정상",
                "baseList": [
                    {
                        "fin_co_no": "0013175",
                        "kor_co_nm": "카카오뱅크",
                        "fin_prdt_nm": "카카오뱅크 26주적금",
                        "join_way": "스마트폰",
                        "mtrt_int": "만기 후 1개월 이내: 약정이율의 50%..."
                    },
                    {
                        "fin_co_no": "0010927",
                        "kor_co_nm": "국민은행",
                        "fin_prdt_nm": "KB국민프리미엄적금",
                        "join_way": "영업점,인터넷,스마트폰",
                        "mtrt_int": "만기 후 1개월 이내: 약정이율의 50%..."
                    }
                ],
                "optionList": [
                    {
                        "fin_co_no": "0013175",
                        "fin_prdt_nm": "카카오뱅크 26주적금",
                        "save_trm": "6",
                        "intr_rate": 3.00,
                        "intr_rate2": 7.00,
                        "intr_rate_type_nm": "단리"
                    },
                    {
                        "fin_co_no": "0010927",
                        "fin_prdt_nm": "KB국민프리미엄적금",
                        "save_trm": "12",
                        "intr_rate": 3.20,
                        "intr_rate2": 4.20,
                        "intr_rate_type_nm": "단리"
                    }
                ]
            }
        }

public_data_service = PublicDataService()
