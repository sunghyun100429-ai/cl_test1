#!/usr/bin/env python3
"""
ZE 시뮬레이터 - 테스트 스크립트
빠른 테스트를 위한 자동화된 스크립트
"""
from ze_simulator.simulator import ZESimulator
from ze_simulator.maps.factory import get_factory_map, get_factory_info


def test_factory_map():
    """공장 맵 테스트"""
    print("\n테스트 시작: 공장 탈출 맵")
    print("="*60)

    map_info = get_factory_info()
    print(f"맵: {map_info['맵_이름']}")
    print(f"난이도: {map_info['난이도']}")

    # 8명으로 빠른 테스트
    phases = get_factory_map()
    simulator = ZESimulator(phases, player_count=8)
    simulator.run()

    print("\n테스트 완료!")


if __name__ == "__main__":
    test_factory_map()
