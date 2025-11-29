"""
ZE 시뮬레이터 - 특성(Traits) 시스템
플레이어의 특수 능력 및 보정치
"""
import random
from enum import Enum
from typing import Dict, List


class HumanTrait(Enum):
    """인간 특성"""
    팀_리더 = "팀_리더"  # 팀워크 +20%, 주변 플레이어 사기 상승
    점프_달인 = "점프_달인"  # 이동/점프 +30%, 낙사 확률 -50%
    점프_초보 = "점프_초보"  # 이동/점프 -20%, 낙사 확률 +30%
    이기적_성향 = "이기적_성향"  # 팀워크 -30%, 트롤 사고 유발 +40%
    라스트_스탠드 = "라스트_스탠드"  # 인간 20명 이하일 때 모든 스탯 +15%
    희생정신 = "희생정신"  # 뒤쳐진 아군 엄호 시도, 감염 위험 +20% 하지만 팀 생존률 향상


class ZombieTrait(Enum):
    """좀비 특성"""
    암살자형 = "암살자형"  # 이동 +25%, 단독 감염력 +20%
    브루저 = "브루저"  # 내구력 +30%, 이동 -10%
    웨이브_콜러 = "웨이브_콜러"  # 집단 협력 +40%, 군중 계수 추가 증가
    자폭_돌격형 = "자폭_돌격형"  # 공격성 +50%, 내구력 -30%


def get_human_trait_modifiers(trait: HumanTrait) -> Dict[str, float]:
    """인간 특성의 스탯 보정치 반환"""
    modifiers = {
        HumanTrait.팀_리더: {
            "팀워크": 1.2,
            "용기": 1.1
        },
        HumanTrait.점프_달인: {
            "이동_점프_능력": 1.3
        },
        HumanTrait.점프_초보: {
            "이동_점프_능력": 0.8
        },
        HumanTrait.이기적_성향: {
            "팀워크": 0.7
        },
        HumanTrait.라스트_스탠드: {
            # 조건부 적용 (시뮬레이터에서 처리)
        },
        HumanTrait.희생정신: {
            "용기": 1.15,
            "팀워크": 1.1
        }
    }
    return modifiers.get(trait, {})


def get_zombie_trait_modifiers(trait: ZombieTrait) -> Dict[str, float]:
    """좀비 특성의 스탯 보정치 반환"""
    modifiers = {
        ZombieTrait.암살자형: {
            "이동_점프_능력": 1.25,
            "감염력": 1.2
        },
        ZombieTrait.브루저: {
            "내구력": 1.3,
            "이동_점프_능력": 0.9
        },
        ZombieTrait.웨이브_콜러: {
            "집단_협력_능력": 1.4
        },
        ZombieTrait.자폭_돌격형: {
            "공격성": 1.5,
            "내구력": 0.7
        }
    }
    return modifiers.get(trait, {})


def assign_random_human_traits(count: int = 1) -> List[HumanTrait]:
    """랜덤한 인간 특성 부여 (30% 확률로 특성 없음)"""
    if random.random() < 0.3:
        return []

    # 70% 확률로 특성 1개
    available_traits = list(HumanTrait)
    return random.sample(available_traits, min(count, len(available_traits)))


def assign_random_zombie_traits(count: int = 1) -> List[ZombieTrait]:
    """랜덤한 좀비 특성 부여 (30% 확률로 특성 없음)"""
    if random.random() < 0.3:
        return []

    # 70% 확률로 특성 1개
    available_traits = list(ZombieTrait)
    return random.sample(available_traits, min(count, len(available_traits)))


def get_trait_infection_modifier(traits: List[HumanTrait]) -> float:
    """특성에 따른 감염 확률 보정치"""
    modifier = 1.0
    for trait in traits:
        if trait == HumanTrait.희생정신:
            modifier *= 1.2  # 감염 위험 +20%
        elif trait == HumanTrait.점프_달인:
            modifier *= 0.95  # 약간 감소
    return modifier


def get_trait_fall_modifier(traits: List[HumanTrait]) -> float:
    """특성에 따른 낙사 확률 보정치"""
    modifier = 1.0
    for trait in traits:
        if trait == HumanTrait.점프_달인:
            modifier *= 0.5  # 낙사 확률 -50%
        elif trait == HumanTrait.점프_초보:
            modifier *= 1.3  # 낙사 확률 +30%
    return modifier


def get_trait_troll_modifier(traits: List[HumanTrait]) -> float:
    """특성에 따른 트롤 사고 확률 보정치"""
    modifier = 1.0
    for trait in traits:
        if trait == HumanTrait.이기적_성향:
            modifier *= 1.4  # 트롤 사고 +40%
        elif trait == HumanTrait.팀_리더:
            modifier *= 0.8  # 트롤 사고 -20%
    return modifier
