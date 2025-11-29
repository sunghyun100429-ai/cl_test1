#!/usr/bin/env python3
"""
ZE 시뮬레이터 - 메인 실행 파일
3개 맵(공장/신전/감옥)을 선택하여 시뮬레이션 실행
"""
import sys
from ze_simulator.simulator import ZESimulator
from ze_simulator.maps.factory import get_factory_map, get_factory_info
from ze_simulator.maps.temple import get_temple_map, get_temple_info
from ze_simulator.maps.prison import get_prison_map, get_prison_info


def print_menu():
    """메인 메뉴 출력"""
    print("\n" + "="*60)
    print("    ZE 시뮬레이터 v1.0 - 텍스트 기반 Zombie Escape")
    print("="*60)
    print("\n맵 선택:")
    print("  1. ZE_공장 탈출 (난이도: 중간)")
    print("  2. ZE_고대 신전 탈출 (난이도: 상급)")
    print("  3. ZE_지하 감옥 탈출 (난이도: 중상급)")
    print("  4. 모든 맵 순차 실행")
    print("  0. 종료")
    print("="*60)


def print_map_info(map_info: dict):
    """맵 정보 출력"""
    print("\n" + "-"*60)
    print(f"맵 이름: {map_info['맵_이름']}")
    print(f"맵 코드: {map_info['맵_코드']}")
    print(f"난이도: {map_info['난이도']}")
    print(f"페이즈 수: {map_info['페이즈_수']}")
    print(f"예상 시간: {map_info['예상_시간']}")
    print("\n특징:")
    for feature in map_info['특징']:
        print(f"  - {feature}")
    if '특수_메커니즘' in map_info:
        print("\n특수 메커니즘:")
        for key, value in map_info['특수_메커니즘'].items():
            print(f"  - {key}: {value}")
    print("-"*60 + "\n")


def run_map(map_phases, map_info, player_count=64):
    """맵 실행"""
    print_map_info(map_info)
    input("엔터를 눌러 시뮬레이션을 시작하세요...")

    simulator = ZESimulator(map_phases, player_count=player_count)
    simulator.run()


def main():
    """메인 함수"""
    while True:
        print_menu()
        choice = input("\n선택 (0-4): ").strip()

        if choice == "0":
            print("\n시뮬레이터를 종료합니다.")
            sys.exit(0)

        elif choice == "1":
            run_map(get_factory_map(), get_factory_info())

        elif choice == "2":
            run_map(get_temple_map(), get_temple_info())

        elif choice == "3":
            run_map(get_prison_map(), get_prison_info())

        elif choice == "4":
            print("\n모든 맵을 순차적으로 실행합니다.\n")
            input("엔터를 눌러 시작...")

            # 공장
            print("\n\n### 1/3: 공장 탈출 ###")
            run_map(get_factory_map(), get_factory_info())
            input("\n다음 맵으로 진행하려면 엔터를 누르세요...")

            # 신전
            print("\n\n### 2/3: 고대 신전 탈출 ###")
            run_map(get_temple_map(), get_temple_info())
            input("\n다음 맵으로 진행하려면 엔터를 누르세요...")

            # 감옥
            print("\n\n### 3/3: 지하 감옥 탈출 ###")
            run_map(get_prison_map(), get_prison_info())

            print("\n모든 맵 시뮬레이션이 완료되었습니다!")

        else:
            print("\n잘못된 선택입니다. 0-4 사이의 숫자를 입력하세요.")

        input("\n메인 메뉴로 돌아가려면 엔터를 누르세요...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n시뮬레이터가 중단되었습니다.")
        sys.exit(0)
