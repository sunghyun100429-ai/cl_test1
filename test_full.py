#!/usr/bin/env python3
"""
ZE 시뮬레이터 - 전체 테스트 (64명)
"""
from ze_simulator.simulator import ZESimulator
from ze_simulator.maps.factory import get_factory_map, get_factory_info


def test_full_simulation():
    """전체 64명 시뮬레이션"""
    print("\n전체 시뮬레이션 테스트: 공장 탈출 맵 (64명)")
    print("="*60)

    phases = get_factory_map()
    simulator = ZESimulator(phases, player_count=64)
    simulator.run()


if __name__ == "__main__":
    test_full_simulation()
