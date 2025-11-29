"""
ZE 시뮬레이터 - 핵심 공식
감염, 트롤, 낙사 확률 계산
"""
import random
from typing import List
from .player import Player
from .stats import HumanStats, ZombieStats
from .traits import (
    HumanTrait,
    get_trait_infection_modifier,
    get_trait_fall_modifier,
    get_trait_troll_modifier
)


def calculate_infection_probability(
    human: Player,
    zombie: Player,
    crowd_factor: float = 1.0,
    env_factor: float = 1.0,
    phase_factor: float = 1.0
) -> float:
    """
    감염 확률 계산

    Args:
        human: 인간 플레이어
        zombie: 좀비 플레이어
        crowd_factor: 군중 계수 (좀비 수에 따라 증가)
        env_factor: 환경 계수
        phase_factor: 페이즈 계수

    Returns:
        최종 감염 확률 (0.0 ~ 1.0)
    """
    h_stats = human.current_human_stats
    z_stats = zombie.current_zombie_stats

    # 공격 점수 (좀비)
    attack_score = (
        z_stats.감염력 * 0.5 +
        z_stats.이동_점프_능력 * 0.2 +
        z_stats.공격성 * 0.2 +
        z_stats.집단_협력_능력 * 0.1
    )

    # 방어 점수 (인간)
    defense_score = (
        h_stats.이동_점프_능력 * 0.4 +
        h_stats.용기 * 0.3 +
        h_stats.팀워크 * 0.2 +
        h_stats.판단력 * 0.1
    )

    # 비율 계산
    ratio = attack_score / (attack_score + defense_score)

    # 기본 감염 확률
    base_prob = 0.2 + 0.6 * ratio

    # 특성 보정
    trait_modifier = get_trait_infection_modifier(human.human_traits)

    # 최종 감염 확률
    final_prob = base_prob * crowd_factor * env_factor * phase_factor * trait_modifier

    return max(0.0, min(1.0, final_prob))


def calculate_troll_probability(
    human: Player,
    crowd_density: float = 1.0,
    env_factor: float = 1.0,
    phase_factor: float = 1.0
) -> float:
    """
    트롤 사고 확률 계산

    Args:
        human: 인간 플레이어
        crowd_density: 혼잡도 계수
        env_factor: 환경 계수
        phase_factor: 페이즈 계수

    Returns:
        최종 트롤 사고 확률 (0.0 ~ 1.0)
    """
    h_stats = human.current_human_stats

    # 트롤 기본 점수 (가해자)
    troll_score = (
        (100 - h_stats.팀워크) * 0.5 +
        (100 - h_stats.판단력) * 0.3 +
        (100 - h_stats.용기) * 0.2
    )

    # 방어 점수
    defense_score = (
        h_stats.이동_점프_능력 * 0.4 +
        h_stats.판단력 * 0.3 +
        h_stats.용기 * 0.3
    )

    # 트롤 비율
    troll_ratio = troll_score / (troll_score + defense_score)

    # 기본 트롤 확률
    base_prob = 0.15 + 0.3 * (troll_ratio - 0.5)

    # 특성 보정
    trait_modifier = get_trait_troll_modifier(human.human_traits)

    # 최종 트롤 확률
    final_prob = base_prob * env_factor * phase_factor * crowd_density * trait_modifier

    return max(0.0, min(1.0, final_prob))


def calculate_fall_probability(
    human: Player,
    env_factor: float = 1.0,
    phase_factor: float = 1.0,
    crowd_density: float = 1.0,
    troll_influence: float = 1.0,
    C: float = 0.8
) -> float:
    """
    낙사 확률 계산

    Args:
        human: 인간 플레이어
        env_factor: 환경 계수
        phase_factor: 페이즈 계수
        crowd_density: 혼잡도
        troll_influence: 트롤 영향
        C: 기본 계수 (기본값 0.8)

    Returns:
        최종 낙사 확률 (0.0 ~ 1.0)
    """
    h_stats = human.current_human_stats

    # 안전 점수
    safety_score = (
        h_stats.이동_점프_능력 * 0.5 +
        h_stats.판단력 * 0.3 +
        h_stats.용기 * 0.2
    )

    # 실수 점수
    mistake_score = 100 - safety_score
    X = mistake_score / 100

    # 기본 낙사 확률
    base_prob = (X ** 2) * C

    # 특성 보정
    trait_modifier = get_trait_fall_modifier(human.human_traits)

    # 최종 낙사 확률
    final_prob = base_prob * env_factor * phase_factor * crowd_density * troll_influence * trait_modifier

    return max(0.0, min(1.0, final_prob))


def calculate_crowd_factor(zombie_count: int, human_count: int) -> float:
    """
    군중 계수 계산 (좀비 수에 따라 감염 확률 증가)

    Args:
        zombie_count: 좀비 수
        human_count: 인간 수

    Returns:
        군중 계수
    """
    if human_count == 0:
        return 1.0

    ratio = zombie_count / (zombie_count + human_count)

    # 좀비가 많을수록 계수 증가 (1.0 ~ 1.5)
    crowd_factor = 1.0 + 0.5 * ratio

    return crowd_factor


def calculate_crowd_density(alive_humans: int, max_humans: int = 64) -> float:
    """
    혼잡도 계수 계산 (인간이 많을수록 트롤/낙사 증가)

    Args:
        alive_humans: 생존 인간 수
        max_humans: 최대 인간 수

    Returns:
        혼잡도 계수
    """
    if max_humans == 0:
        return 1.0

    ratio = alive_humans / max_humans

    # 인간이 많을수록 혼잡도 증가 (0.7 ~ 1.3)
    density = 0.7 + 0.6 * ratio

    return density


def roll_event(probability: float) -> bool:
    """
    확률에 따라 이벤트 발생 여부 결정

    Args:
        probability: 발생 확률 (0.0 ~ 1.0)

    Returns:
        True if event occurs
    """
    return random.random() < probability


def get_random_troll_type() -> str:
    """랜덤한 트롤 사고 타입 반환"""
    types = ["길막", "밀침", "연쇄끼임"]
    weights = [0.4, 0.35, 0.25]  # 길막이 가장 흔함
    return random.choices(types, weights=weights)[0]
