"""
ZE_고대 신전 탈출 (Ancient Temple Escape)
난이도: 상급
"""
from typing import List
from ..phase import Phase, PhaseType, PhaseBuilder
from ..environment import EnvironmentType


def get_temple_map() -> List[Phase]:
    """고대 신전 탈출 맵 데이터 반환"""
    phases = [
        # 페이즈 1: 석상 디펜스
        PhaseBuilder.create_phase(
            phase_number=1,
            name="석상 디펜스",
            phase_type=PhaseType.DEFEND,
            environment=EnvironmentType.넓은_지형,
            duration_ticks=35,
            description="고대 신전 입구의 넓은 광장. 석상이 움직일 때까지 35초간 방어하라!"
        ),

        # 페이즈 2: 함정 복도 런
        PhaseBuilder.create_phase(
            phase_number=2,
            name="함정 복도",
            phase_type=PhaseType.RUN,
            environment=EnvironmentType.함정_복도,
            duration_ticks=30,
            description="화살 함정과 낙석이 있는 복도. 함정에 맞으면 즉사한다!"
        ),

        # 페이즈 3: 발판 점프
        PhaseBuilder.create_phase(
            phase_number=3,
            name="발판 점프",
            phase_type=PhaseType.JUMP,
            environment=EnvironmentType.낭떠러지,
            duration_ticks=25,
            description="무너지는 발판을 점프로 건너라. 점프 실력이 생존을 결정한다!"
        ),

        # 페이즈 4: 신전 입구 홀딩
        PhaseBuilder.create_phase(
            phase_number=4,
            name="신전 입구 홀딩",
            phase_type=PhaseType.HOLD,
            environment=EnvironmentType.최종_홀딩,
            duration_ticks=45,
            description="신전 출구가 열릴 때까지 45초간 버텨라. 좀비 웨이브가 몰려온다!"
        )
    ]

    return phases


def get_temple_info() -> dict:
    """고대 신전 맵 정보 반환"""
    return {
        "맵_이름": "ZE_고대 신전 탈출",
        "맵_코드": "ze_temple_escape",
        "난이도": "상급",
        "페이즈_수": 4,
        "예상_시간": "약 135틱 (약 2분 15초)",
        "특징": [
            "석상 디펜스",
            "함정 복도 (즉사 위험)",
            "무너지는 발판 점프",
            "긴 최종 홀딩"
        ],
        "특수_메커니즘": {
            "함정_피격": "페이즈 2에서 함정 계수 1.6배 적용"
        }
    }
