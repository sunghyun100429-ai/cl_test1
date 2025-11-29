"""
ZE_공장 탈출 (Factory Escape)
난이도: 중간
"""
from typing import List
from ..phase import Phase, PhaseType, PhaseBuilder
from ..environment import EnvironmentType


def get_factory_map() -> List[Phase]:
    """공장 탈출 맵 데이터 반환"""
    phases = [
        # 페이즈 1: 넓은 창고 디펜스
        PhaseBuilder.create_phase(
            phase_number=1,
            name="창고 디펜스",
            phase_type=PhaseType.DEFEND,
            environment=EnvironmentType.넓은_지형,
            duration_ticks=30,
            description="넓은 창고에서 30초간 좀비를 막아야 한다. 문이 열릴 때까지 버텨라!"
        ),

        # 페이즈 2: 좁은 복도 런
        PhaseBuilder.create_phase(
            phase_number=2,
            name="복도 탈출",
            phase_type=PhaseType.RUN,
            environment=EnvironmentType.좁은_복도,
            duration_ticks=25,
            description="좁은 복도를 달려 탈출하라. 뒤쳐지면 감염된다!"
        ),

        # 페이즈 3: 컨베이어 점프
        PhaseBuilder.create_phase(
            phase_number=3,
            name="컨베이어 점프",
            phase_type=PhaseType.JUMP,
            environment=EnvironmentType.낭떠러지,
            duration_ticks=20,
            description="움직이는 컨베이어 벨트를 점프로 건너야 한다. 낙사 주의!"
        ),

        # 페이즈 4: 화물열차 최종 홀딩
        PhaseBuilder.create_phase(
            phase_number=4,
            name="화물열차 홀딩",
            phase_type=PhaseType.HOLD,
            environment=EnvironmentType.최종_홀딩,
            duration_ticks=40,
            description="화물열차가 출발할 때까지 40초간 버텨라. 최후의 방어선이다!"
        )
    ]

    return phases


def get_factory_info() -> dict:
    """공장 맵 정보 반환"""
    return {
        "맵_이름": "ZE_공장 탈출",
        "맵_코드": "ze_factory_escape",
        "난이도": "중간",
        "페이즈_수": 4,
        "예상_시간": "약 115틱 (약 2분)",
        "특징": [
            "넓은 지형 디펜스",
            "좁은 복도 런",
            "컨베이어 점프 구간",
            "화물열차 최종 홀딩"
        ]
    }
