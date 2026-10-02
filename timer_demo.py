# 简化版锦标赛计时器（教学用，仿 WTGB 比赛引擎的思路）
# 作者：教学示例

# 盲注结构：每一级持续多少分钟，小盲/大盲各是多少
BLIND_LEVELS = [
    {"duration_min": 10, "small_blind": 10, "big_blind": 20},
    {"duration_min": 10, "small_blind": 20, "big_blind": 40},
    {"duration_min": 15, "small_blind": 50, "big_blind": 100},
]

# 用「时间戳」记录比赛状态：这样 App 切到后台再回来，时间依然准确
import time

class TournamentClock:
    def __init__(self, levels, speed=1):
        # speed 是测试加速开关：1 = 正常速度（分钟就是分钟），120 = 测试模式（1秒当2分钟）
        self.levels = levels
        self.speed = speed
        self.level_index = 0          # 当前在第几级盲注
        self.level_started_at = time.time()   # 本级开始的时刻（秒）

    def current_level(self):
        return self.levels[self.level_index]

    def seconds_remaining(self):
        """本级还剩多少秒（考虑加速倍数后的「表上秒数」）"""
        level = self.current_level()
        elapsed = time.time() - self.level_started_at
        total = level["duration_min"] * 60 / self.speed
        return max(0, total - elapsed)

    def is_level_over(self):
        return self.seconds_remaining() == 0

    def advance_if_needed(self):
        """如果当前级打完了，自动升到下一级；返回是否升了"""
        if not self.is_level_over():
            return False
        if self.level_index < len(self.levels) - 1:
            self.level_index += 1
            self.level_started_at = time.time()
            return True
        return False   # 已经是最后一级，不再升


def run_match(clock):
    """比赛进行模式：每秒报时，到点升盲，打完收工"""
    level = clock.current_level()
    print(f"比赛开始！当前盲注: 小盲{level['small_blind']}/大盲{level['big_blind']}")

    while True:
        remaining = clock.seconds_remaining()

        # 先判断「最后一级也打完了」——是的话直接收工，不再报时
        if remaining == 0 and not clock.advance_if_needed():
            print("比赛结束！")
            break

        print(f"剩余 {remaining:.0f} 秒")
        if remaining == 0:   # advance_if_needed 刚升了一级
            level = clock.current_level()
            print(f"===== 升盲！现在是 小盲{level['small_blind']}/大盲{level['big_blind']} =====")

        # 每次循环 = 表上时间走1秒；speed 已经折算在 seconds_remaining 里，
        # 所以这里固定睡真实1秒即可（测试模式下1秒=表上120秒）
        time.sleep(1)


clock = TournamentClock(BLIND_LEVELS, speed=120)   # speed=120：测试加速，约18秒看完全场
run_match(clock)
