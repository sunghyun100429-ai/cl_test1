"""
ZE 시뮬레이터 - 메인 시뮬레이션 엔진
틱 기반으로 게임을 진행하며 모든 이벤트를 처리
"""
import random
from typing import List, Dict, Tuple
from .player import Player, create_players, select_initial_zombies
from .phase import Phase
from .environment import EnvironmentModifiers
from .formulas import (
    calculate_infection_probability,
    calculate_troll_probability,
    calculate_fall_probability,
    calculate_crowd_factor,
    calculate_crowd_density,
    roll_event,
    get_random_troll_type
)


class SimulationLogger:
    """시뮬레이션 로그 관리"""

    def __init__(self):
        self.logs = []
        self.event_counts = {
            "감염": 0,
            "트롤": 0,
            "낙사": 0,
            "함정": 0,
            "침수": 0
        }

    def log(self, message: str):
        """로그 추가"""
        self.logs.append(message)
        print(message)

    def log_event(self, event_type: str, message: str):
        """이벤트 로그 및 카운트"""
        if event_type in self.event_counts:
            self.event_counts[event_type] += 1
        self.log(f"[{event_type}] {message}")

    def get_summary(self) -> Dict:
        """이벤트 요약 반환"""
        return self.event_counts.copy()


class ZESimulator:
    """ZE 시뮬레이터 메인 클래스"""

    def __init__(self, map_phases: List[Phase], player_count: int = 64):
        """
        Args:
            map_phases: 맵의 페이즈 리스트
            player_count: 플레이어 수 (기본 64명)
        """
        self.phases = map_phases
        self.players = create_players(player_count)
        self.current_phase_index = 0
        self.current_tick = 0
        self.phase_tick = 0
        self.logger = SimulationLogger()
        self.game_over = False
        self.winner = None

        # 초기 좀비 선정
        select_initial_zombies(self.players, count=2)
        self.logger.log("=== ZE 시뮬레이션 시작 ===")
        self.logger.log(f"플레이어 수: {player_count}명")
        self.logger.log(f"초기 좀비: {[p.name for p in self.players if p.is_zombie]}")

    def run(self):
        """시뮬레이션 실행"""
        for phase in self.phases:
            if self.game_over:
                break

            self.logger.log(f"\n{'='*50}")
            self.logger.log(f"페이즈 {phase.phase_number}: {phase.name}")
            self.logger.log(f"타입: {phase.phase_type.value} | 환경: {phase.environment.value}")
            self.logger.log(f"설명: {phase.description}")
            self.logger.log(f"{'='*50}\n")

            self.run_phase(phase)
            self.current_phase_index += 1

        # 최종 결과
        self.print_final_results()

    def run_phase(self, phase: Phase):
        """단일 페이즈 실행"""
        self.phase_tick = 0

        # 환경 보정치 적용
        self.apply_environment_modifiers(phase)

        # 페이즈 진행
        while self.phase_tick < phase.duration_ticks and not self.game_over:
            self.phase_tick += 1
            self.current_tick += 1

            self.run_tick(phase)

            # 승패 판정
            if self.check_game_over():
                break

        # 페이즈 종료
        alive_humans = self.get_alive_humans()
        zombies = self.get_zombies()
        self.logger.log(f"\n[페이즈 {phase.phase_number} 종료] 생존 인간: {len(alive_humans)}명 | 좀비: {len(zombies)}명\n")

    def run_tick(self, phase: Phase):
        """단일 틱 실행"""
        alive_humans = self.get_alive_humans()
        zombies = self.get_zombies()

        if len(alive_humans) == 0:
            return

        # 1. 뒤쳐짐 판정 (RUN, JUMP 페이즈)
        if phase.phase_type.value in ["RUN", "JUMP"]:
            self.process_stragglers(alive_humans)

        # 2. 트롤 사고 판정
        self.process_troll_events(alive_humans, phase)

        # 트롤 사고 후 생존자 갱신
        alive_humans = self.get_alive_humans()
        if len(alive_humans) == 0:
            return

        # 3. 감염 판정
        self.process_infections(alive_humans, zombies, phase)

        # 감염 후 생존자 갱신
        alive_humans = self.get_alive_humans()
        if len(alive_humans) == 0:
            return

        # 4. 낙사 판정 (JUMP 페이즈)
        if phase.phase_type.value == "JUMP":
            self.process_falls(alive_humans, phase)

        # 낙사 후 생존자 갱신
        alive_humans = self.get_alive_humans()
        if len(alive_humans) == 0:
            return

        # 5. 특수 환경 이벤트
        self.process_special_events(alive_humans, phase)

    def apply_environment_modifiers(self, phase: Phase):
        """환경 보정치를 모든 플레이어에 적용"""
        human_mods = EnvironmentModifiers.get_human_modifiers(phase.environment)
        zombie_mods = EnvironmentModifiers.get_zombie_modifiers(phase.environment)

        for player in self.players:
            player.apply_environment_modifiers(human_mods, zombie_mods)

    def process_stragglers(self, alive_humans: List[Player]):
        """뒤쳐짐 판정 (위치 기반)"""
        # 랜덤하게 일부 플레이어가 뒤쳐짐
        for human in alive_humans:
            if random.random() < 0.1:  # 10% 확률로 뒤쳐짐
                human.position = max(0, human.position - 10)

    def process_troll_events(self, alive_humans: List[Player], phase: Phase):
        """트롤 사고 판정"""
        crowd_density = calculate_crowd_density(len(alive_humans))
        env_mods = EnvironmentModifiers.get_special_modifiers(phase.environment)

        for human in alive_humans:
            troll_prob = calculate_troll_probability(
                human,
                crowd_density=crowd_density,
                env_factor=1.0,
                phase_factor=phase.troll_factor
            )

            if roll_event(troll_prob):
                troll_type = get_random_troll_type()
                human.kill(f"트롤_{troll_type}")
                self.logger.log_event("트롤", f"Tick {self.current_tick}: {human.name} - {troll_type}으로 사망")

    def process_infections(self, alive_humans: List[Player], zombies: List[Player], phase: Phase):
        """감염 판정"""
        if len(zombies) == 0:
            return

        crowd_factor = calculate_crowd_factor(len(zombies), len(alive_humans))
        env_mods = EnvironmentModifiers.get_special_modifiers(phase.environment)

        # 랜덤하게 좀비-인간 매칭
        infection_attempts = min(len(zombies), len(alive_humans) // 2)

        for _ in range(infection_attempts):
            if len(alive_humans) == 0:
                break

            zombie = random.choice(zombies)
            human = random.choice(alive_humans)

            infection_prob = calculate_infection_probability(
                human,
                zombie,
                crowd_factor=crowd_factor,
                env_factor=1.0,
                phase_factor=phase.infection_factor
            )

            if roll_event(infection_prob):
                human.infect(self.current_tick)
                self.logger.log_event("감염", f"Tick {self.current_tick}: {human.name} 감염됨 (by {zombie.name})")
                alive_humans.remove(human)

    def process_falls(self, alive_humans: List[Player], phase: Phase):
        """낙사 판정"""
        crowd_density = calculate_crowd_density(len(alive_humans))

        for human in alive_humans[:]:  # 복사본으로 순회
            fall_prob = calculate_fall_probability(
                human,
                env_factor=1.0,
                phase_factor=phase.fall_factor,
                crowd_density=crowd_density,
                troll_influence=1.0
            )

            if roll_event(fall_prob):
                human.kill("낙사")
                self.logger.log_event("낙사", f"Tick {self.current_tick}: {human.name} 낙사")

    def process_special_events(self, alive_humans: List[Player], phase: Phase):
        """특수 환경 이벤트 (함정, 침수 등)"""
        special_mods = EnvironmentModifiers.get_special_modifiers(phase.environment)

        # 함정 이벤트 (신전)
        if "함정_계수" in special_mods:
            trap_factor = special_mods["함정_계수"]
            for human in alive_humans[:]:
                # 판단력이 낮을수록 함정에 걸릴 확률 증가
                trap_prob = (100 - human.current_human_stats.판단력) / 100 * 0.05 * trap_factor
                if roll_event(trap_prob):
                    human.kill("함정")
                    self.logger.log_event("함정", f"Tick {self.current_tick}: {human.name} 함정에 피격")

        # 침수 이벤트 (감옥)
        if "침수_계수" in special_mods:
            flood_factor = special_mods["침수_계수"]
            for human in alive_humans[:]:
                # 이동 능력이 낮을수록 침수 위험 증가
                flood_prob = (100 - human.current_human_stats.이동_점프_능력) / 100 * 0.04 * flood_factor
                if roll_event(flood_prob):
                    human.kill("침수")
                    self.logger.log_event("침수", f"Tick {self.current_tick}: {human.name} 침수로 사망")

    def check_game_over(self) -> bool:
        """게임 종료 판정"""
        alive_humans = self.get_alive_humans()

        if len(alive_humans) == 0:
            self.game_over = True
            self.winner = "좀비"
            self.logger.log("\n[게임 종료] 좀비 승리! 모든 인간이 감염되거나 사망했습니다.")
            return True

        # 마지막 페이즈 완료 시 인간 승리
        if self.current_phase_index >= len(self.phases) - 1 and self.phase_tick >= self.phases[-1].duration_ticks:
            self.game_over = True
            self.winner = "인간"
            self.logger.log("\n[게임 종료] 인간 승리! 생존자가 탈출에 성공했습니다!")
            return True

        return False

    def get_alive_humans(self) -> List[Player]:
        """생존 인간 리스트 반환"""
        return [p for p in self.players if not p.is_zombie and p.is_alive]

    def get_zombies(self) -> List[Player]:
        """좀비 리스트 반환"""
        return [p for p in self.players if p.is_zombie and p.is_alive]

    def print_final_results(self):
        """최종 결과 출력"""
        self.logger.log("\n" + "="*50)
        self.logger.log("=== 최종 결과 ===")
        self.logger.log("="*50)

        alive_humans = self.get_alive_humans()
        zombies = self.get_zombies()

        self.logger.log(f"\n승리: {self.winner}")
        self.logger.log(f"생존 인간: {len(alive_humans)}명")
        self.logger.log(f"좀비: {len(zombies)}명")

        # 이벤트 통계
        self.logger.log("\n=== 이벤트 통계 ===")
        summary = self.logger.get_summary()
        for event_type, count in summary.items():
            self.logger.log(f"{event_type}: {count}회")

        # 생존자 명단
        if len(alive_humans) > 0:
            self.logger.log("\n=== 생존자 명단 ===")
            for human in alive_humans:
                self.logger.log(f"  - {human.name}")

        self.logger.log("\n" + "="*50)
