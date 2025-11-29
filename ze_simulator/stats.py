"""
ZE 시뮬레이터 - 스탯 시스템
플레이어의 인간/좀비 스탯 정의 및 생성
"""
import random
from dataclasses import dataclass
from typing import Dict


@dataclass
class HumanStats:
    """인간 스탯"""
    사격_정확도: float = 50.0  # 좀비 맞추는 능력
    이동_점프_능력: float = 50.0  # 이동 속도, 점프맵 숙련
    판단력: float = 50.0  # 도망/방어 판단
    용기: float = 50.0  # 패닉 저항
    팀워크: float = 50.0  # 팀과 뭉쳐 다니는 능력
    유틸_사용_능력: float = 50.0  # 슬로우/넉백 등 활용

    def to_dict(self) -> Dict[str, float]:
        """딕셔너리로 변환"""
        return {
            "사격_정확도": self.사격_정확도,
            "이동_점프_능력": self.이동_점프_능력,
            "판단력": self.판단력,
            "용기": self.용기,
            "팀워크": self.팀워크,
            "유틸_사용_능력": self.유틸_사용_능력
        }

    def apply_modifier(self, modifiers: Dict[str, float]) -> 'HumanStats':
        """환경 보정치 적용 (새 인스턴스 반환)"""
        return HumanStats(
            사격_정확도=self.사격_정확도 * modifiers.get("사격_정확도", 1.0),
            이동_점프_능력=self.이동_점프_능력 * modifiers.get("이동_점프_능력", 1.0),
            판단력=self.판단력 * modifiers.get("판단력", 1.0),
            용기=self.용기 * modifiers.get("용기", 1.0),
            팀워크=self.팀워크 * modifiers.get("팀워크", 1.0),
            유틸_사용_능력=self.유틸_사용_능력 * modifiers.get("유틸_사용_능력", 1.0)
        )


@dataclass
class ZombieStats:
    """좀비 스탯"""
    내구력: float = 50.0  # 총 맞고 버티는 정도
    감염력: float = 50.0  # 닿았을 때 감염 확률
    이동_점프_능력: float = 50.0  # 접근 능력
    공격성: float = 50.0  # 돌진 빈도
    집단_협력_능력: float = 50.0  # 협공 효과

    def to_dict(self) -> Dict[str, float]:
        """딕셔너리로 변환"""
        return {
            "내구력": self.내구력,
            "감염력": self.감염력,
            "이동_점프_능력": self.이동_점프_능력,
            "공격성": self.공격성,
            "집단_협력_능력": self.집단_협력_능력
        }

    def apply_modifier(self, modifiers: Dict[str, float]) -> 'ZombieStats':
        """환경 보정치 적용 (새 인스턴스 반환)"""
        return ZombieStats(
            내구력=self.내구력 * modifiers.get("내구력", 1.0),
            감염력=self.감염력 * modifiers.get("감염력", 1.0),
            이동_점프_능력=self.이동_점프_능력 * modifiers.get("이동_점프_능력", 1.0),
            공격성=self.공격성 * modifiers.get("공격성", 1.0),
            집단_협력_능력=self.집단_협력_능력 * modifiers.get("집단_협력_능력", 1.0)
        )


def generate_random_human_stats() -> HumanStats:
    """랜덤한 인간 스탯 생성 (30~90 범위, 정규분포)"""
    return HumanStats(
        사격_정확도=max(30, min(90, random.gauss(60, 15))),
        이동_점프_능력=max(30, min(90, random.gauss(60, 15))),
        판단력=max(30, min(90, random.gauss(60, 15))),
        용기=max(30, min(90, random.gauss(60, 15))),
        팀워크=max(30, min(90, random.gauss(60, 15))),
        유틸_사용_능력=max(30, min(90, random.gauss(60, 15)))
    )


def generate_random_zombie_stats() -> ZombieStats:
    """랜덤한 좀비 스탯 생성 (30~90 범위, 정규분포)"""
    return ZombieStats(
        내구력=max(30, min(90, random.gauss(60, 15))),
        감염력=max(30, min(90, random.gauss(60, 15))),
        이동_점프_능력=max(30, min(90, random.gauss(60, 15))),
        공격성=max(30, min(90, random.gauss(60, 15))),
        집단_협력_능력=max(30, min(90, random.gauss(60, 15)))
    )
