"""
ZE 시뮬레이터 - 페이즈 시스템
각 페이즈의 타입 및 설정
"""
from enum import Enum
from dataclasses import dataclass
from typing import Dict
from .environment import EnvironmentType


class PhaseType(Enum):
    """페이즈 타입"""
    DEFEND = "DEFEND"  # 디펜스 - 일정 시간 버티기
    RUN = "RUN"  # 런 - 좀비에게 쫓기며 이동
    JUMP = "JUMP"  # 점프 - 점프맵 구간
    HOLD = "HOLD"  # 홀딩 - 최종 방어


@dataclass
class Phase:
    """페이즈 정보"""
    phase_number: int
    name: str
    phase_type: PhaseType
    environment: EnvironmentType
    duration_ticks: int  # 페이즈 지속 시간 (틱)
    description: str = ""

    # 페이즈별 계수
    infection_factor: float = 1.0
    troll_factor: float = 1.0
    fall_factor: float = 1.0

    # 특수 이벤트 (옵션)
    special_events: Dict = None

    def __post_init__(self):
        if self.special_events is None:
            self.special_events = {}


def get_phase_modifiers(phase_type: PhaseType) -> Dict[str, float]:
    """
    페이즈 타입에 따른 이벤트 계수 반환

    Returns:
        {
            "감염_계수": float,
            "트롤_계수": float,
            "낙사_계수": float
        }
    """
    modifiers = {
        PhaseType.DEFEND: {
            "감염_계수": 1.2,  # 근접 방어 -> 감염 높음
            "트롤_계수": 0.8,  # 정적인 상황 -> 트롤 낮음
            "낙사_계수": 0.5  # 고정 방어 -> 낙사 거의 없음
        },
        PhaseType.RUN: {
            "감염_계수": 1.0,  # 도망 -> 감염 중간
            "트롤_계수": 1.3,  # 뒤쳐짐, 밀침 -> 트롤 높음
            "낙사_계수": 0.8  # 이동 중 -> 낙사 중간
        },
        PhaseType.JUMP: {
            "감염_계수": 0.7,  # 점프 중 -> 감염 낮음
            "트롤_계수": 1.5,  # 점프 실수, 밀침 -> 트롤 매우 높음
            "낙사_계수": 2.0  # 점프맵 -> 낙사 매우 높음
        },
        PhaseType.HOLD: {
            "감염_계수": 1.5,  # 최종 방어 -> 감염 매우 높음
            "트롤_계수": 1.0,  # 정적 방어 -> 트롤 중간
            "낙사_계수": 0.6  # 고정 위치 -> 낙사 낮음
        }
    }
    return modifiers.get(phase_type, {
        "감염_계수": 1.0,
        "트롤_계수": 1.0,
        "낙사_계수": 1.0
    })


class PhaseBuilder:
    """페이즈 빌더 헬퍼"""

    @staticmethod
    def create_phase(
        phase_number: int,
        name: str,
        phase_type: PhaseType,
        environment: EnvironmentType,
        duration_ticks: int,
        description: str = ""
    ) -> Phase:
        """페이즈 생성 (자동으로 계수 적용)"""
        modifiers = get_phase_modifiers(phase_type)

        return Phase(
            phase_number=phase_number,
            name=name,
            phase_type=phase_type,
            environment=environment,
            duration_ticks=duration_ticks,
            description=description,
            infection_factor=modifiers["감염_계수"],
            troll_factor=modifiers["트롤_계수"],
            fall_factor=modifiers["낙사_계수"]
        )
