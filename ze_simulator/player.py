"""
ZE 시뮬레이터 - 플레이어 시스템
플레이어 클래스 및 관리
"""
from typing import List, Optional, Dict
from .stats import HumanStats, ZombieStats, generate_random_human_stats, generate_random_zombie_stats
from .traits import (
    HumanTrait, ZombieTrait,
    assign_random_human_traits, assign_random_zombie_traits,
    get_human_trait_modifiers, get_zombie_trait_modifiers
)


class Player:
    """플레이어 클래스"""

    def __init__(self, name: str, player_id: int):
        self.name = name
        self.id = player_id
        self.is_zombie = False
        self.is_alive = True

        # 스탯 초기화
        self.base_human_stats = generate_random_human_stats()
        self.base_zombie_stats = generate_random_zombie_stats()

        # 특성 초기화
        self.human_traits: List[HumanTrait] = assign_random_human_traits(1)
        self.zombie_traits: List[ZombieTrait] = assign_random_zombie_traits(1)

        # 현재 적용된 스탯 (환경 보정치 포함)
        self.current_human_stats = self.base_human_stats
        self.current_zombie_stats = self.base_zombie_stats

        # 게임 상태
        self.current_phase = 0
        self.infection_tick = None  # 감염된 틱
        self.death_reason = None  # 사망 이유

        # 위치 정보 (선택적)
        self.position = 0  # 0~100 (뒤쳐짐 정도)

    def infect(self, tick: int):
        """플레이어를 좀비로 감염"""
        if not self.is_zombie and self.is_alive:
            self.is_zombie = True
            self.infection_tick = tick

    def kill(self, reason: str):
        """플레이어 사망 처리"""
        if self.is_alive:
            self.is_alive = False
            self.death_reason = reason

    def get_current_stats(self) -> HumanStats | ZombieStats:
        """현재 적용된 스탯 반환"""
        if self.is_zombie:
            return self.current_zombie_stats
        return self.current_human_stats

    def apply_environment_modifiers(self, human_mods: Dict[str, float], zombie_mods: Dict[str, float]):
        """환경 보정치 적용"""
        # 특성 보정치 먼저 적용
        human_base = self._apply_trait_modifiers_to_human(self.base_human_stats)
        zombie_base = self._apply_trait_modifiers_to_zombie(self.base_zombie_stats)

        # 환경 보정치 적용
        self.current_human_stats = human_base.apply_modifier(human_mods)
        self.current_zombie_stats = zombie_base.apply_modifier(zombie_mods)

    def _apply_trait_modifiers_to_human(self, stats: HumanStats) -> HumanStats:
        """인간 특성 보정치를 스탯에 적용"""
        result = HumanStats(
            사격_정확도=stats.사격_정확도,
            이동_점프_능력=stats.이동_점프_능력,
            판단력=stats.판단력,
            용기=stats.용기,
            팀워크=stats.팀워크,
            유틸_사용_능력=stats.유틸_사용_능력
        )

        for trait in self.human_traits:
            modifiers = get_human_trait_modifiers(trait)
            result = result.apply_modifier(modifiers)

        return result

    def _apply_trait_modifiers_to_zombie(self, stats: ZombieStats) -> ZombieStats:
        """좀비 특성 보정치를 스탯에 적용"""
        result = ZombieStats(
            내구력=stats.내구력,
            감염력=stats.감염력,
            이동_점프_능력=stats.이동_점프_능력,
            공격성=stats.공격성,
            집단_협력_능력=stats.집단_협력_능력
        )

        for trait in self.zombie_traits:
            modifiers = get_zombie_trait_modifiers(trait)
            result = result.apply_modifier(modifiers)

        return result

    def __repr__(self):
        status = "좀비" if self.is_zombie else "인간"
        alive = "생존" if self.is_alive else f"사망({self.death_reason})"
        return f"{self.name}({status}, {alive})"


def create_players(count: int = 64) -> List[Player]:
    """플레이어 리스트 생성"""
    players = []
    for i in range(count):
        name = f"Bot_{i+1:02d}"
        player = Player(name, i)
        players.append(player)
    return players


def select_initial_zombies(players: List[Player], count: int = 2):
    """초기 좀비 선정"""
    import random
    initial_zombies = random.sample(players, count)
    for zombie in initial_zombies:
        zombie.infect(tick=0)
