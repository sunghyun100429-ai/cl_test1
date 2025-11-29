"""
ZE_지하 감옥 탈출 (Underground Prison Escape)
난이도: 중상급
"""
from typing import List
from ..phase import Phase, PhaseType, PhaseBuilder
from ..environment import EnvironmentType


def get_prison_map() -> List[Phase]:
    """지하 감옥 탈출 맵 데이터 반환"""
    phases = [
        # 페이즈 1: 감옥 정문 디펜스
        PhaseBuilder.create_phase(
            phase_number=1,
            name="감옥 정문 디펜스",
            phase_type=PhaseType.DEFEND,
            environment=EnvironmentType.넓은_지형,
            duration_ticks=30,
            description="감옥 정문을 지켜라. 죄수 좀비들이 몰려온다!"
        ),

        # 페이즈 2: 철창 복도 런
        PhaseBuilder.create_phase(
            phase_number=2,
            name="철창 복도",
            phase_type=PhaseType.RUN,
            environment=EnvironmentType.좁은_복도,
            duration_ticks=25,
            description="좁은 철창 복도를 달려라. 좀비가 양 옆에서 공격한다!"
        ),

        # 페이즈 3: 침수 지하도 런
        PhaseBuilder.create_phase(
            phase_number=3,
            name="침수 지하도",
            phase_type=PhaseType.RUN,
            environment=EnvironmentType.침수_지형,
            duration_ticks=30,
            description="물에 잠긴 지하도. 이동 속도가 느려지고 침수 낙사 위험이 높다!"
        ),

        # 페이즈 4: 옥상 헬기 홀딩
        PhaseBuilder.create_phase(
            phase_number=4,
            name="옥상 헬기 홀딩",
            phase_type=PhaseType.HOLD,
            environment=EnvironmentType.최종_홀딩,
            duration_ticks=40,
            description="옥상에서 헬기가 올 때까지 40초간 버텨라!"
        )
    ]

    return phases


def get_prison_info() -> dict:
    """지하 감옥 맵 정보 반환"""
    return {
        "맵_이름": "ZE_지하 감옥 탈출",
        "맵_코드": "ze_prison_escape",
        "난이도": "중상급",
        "페이즈_수": 4,
        "예상_시간": "약 125틱 (약 2분 5초)",
        "특징": [
            "감옥 정문 디펜스",
            "좁은 철창 복도",
            "침수 지형 (이동 속도 감소)",
            "옥상 헬기 홀딩"
        ],
        "특수_메커니즘": {
            "침수_지형": "페이즈 3에서 침수 계수 1.4배 적용, 이동 속도 25% 감소"
        }
    }
