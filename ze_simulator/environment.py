"""
ZE 시뮬레이터 - 환경 보정치 시스템
각 환경별 플레이어 스탯 보정치
"""
from enum import Enum
from typing import Dict


class EnvironmentType(Enum):
    """환경 타입"""
    넓은_지형 = "넓은_지형"
    좁은_복도 = "좁은_복도"
    낭떠러지 = "낭떠러지"
    최종_홀딩 = "최종_홀딩"
    침수_지형 = "침수_지형"
    함정_복도 = "함정_복도"


class EnvironmentModifiers:
    """환경 보정치 컬렉션"""

    @staticmethod
    def get_modifiers(env_type: EnvironmentType) -> Dict[str, Dict[str, float]]:
        """환경 타입에 따른 보정치 반환"""
        modifiers = {
            EnvironmentType.넓은_지형: {
                "인간": {
                    "사격_정확도": 0.85,
                    "이동_점프_능력": 1.1
                },
                "좀비": {
                    "이동_점프_능력": 0.9,
                    "내구력": 0.95
                },
                "특수": {}
            },
            EnvironmentType.좁은_복도: {
                "인간": {
                    "사격_정확도": 1.2,
                    "이동_점프_능력": 0.8
                },
                "좀비": {
                    "내구력": 0.8,
                    "집단_협력_능력": 1.1
                },
                "특수": {}
            },
            EnvironmentType.낭떠러지: {
                "인간": {
                    "이동_점프_능력": 1.1,
                    "판단력": 0.9
                },
                "좀비": {
                    "이동_점프_능력": 1.1
                },
                "특수": {}
            },
            EnvironmentType.최종_홀딩: {
                "인간": {
                    "사격_정확도": 1.0,
                    "팀워크": 1.1
                },
                "좀비": {
                    "내구력": 1.1,
                    "감염력": 1.05
                },
                "특수": {}
            },
            EnvironmentType.침수_지형: {
                "인간": {
                    "이동_점프_능력": 0.75,
                    "판단력": 0.95,
                    "용기": 0.9
                },
                "좀비": {
                    "이동_점프_능력": 0.85,
                    "감염력": 1.1
                },
                "특수": {
                    "침수_계수": 1.4  # 침수 낙사 확률 증가
                }
            },
            EnvironmentType.함정_복도: {
                "인간": {
                    "이동_점프_능력": 0.9,
                    "판단력": 0.9
                },
                "좀비": {
                    "이동_점프_능력": 0.8
                },
                "특수": {
                    "함정_계수": 1.6  # 함정 피격 확률 증가
                }
            }
        }
        return modifiers.get(env_type, {
            "인간": {},
            "좀비": {},
            "특수": {}
        })

    @staticmethod
    def get_human_modifiers(env_type: EnvironmentType) -> Dict[str, float]:
        """인간 보정치만 반환"""
        mods = EnvironmentModifiers.get_modifiers(env_type)
        return mods.get("인간", {})

    @staticmethod
    def get_zombie_modifiers(env_type: EnvironmentType) -> Dict[str, float]:
        """좀비 보정치만 반환"""
        mods = EnvironmentModifiers.get_modifiers(env_type)
        return mods.get("좀비", {})

    @staticmethod
    def get_special_modifiers(env_type: EnvironmentType) -> Dict[str, float]:
        """특수 보정치 반환 (침수 계수, 함정 계수 등)"""
        mods = EnvironmentModifiers.get_modifiers(env_type)
        return mods.get("특수", {})


def normalize_stat_modifiers(modifiers: Dict[str, float]) -> Dict[str, float]:
    """
    스탯 보정치를 정규화
    키 이름을 변환 (예: "사격 정확도" -> "사격_정확도")
    """
    normalized = {}
    key_mapping = {
        "사격 정확도": "사격_정확도",
        "이동/점프 능력": "이동_점프_능력",
        "유틸 사용 능력": "유틸_사용_능력",
        "집단 협력 능력": "집단_협력_능력"
    }

    for key, value in modifiers.items():
        new_key = key_mapping.get(key, key)
        normalized[new_key] = value

    return normalized
