# ============ 07 lambda 与高阶函数 ============
# 知识点：lambda 匿名函数、函数作为参数传递、复合操作
import sys
import os

# 将项目根目录加入路径，以便导入 shop 模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shop import User, ATM


# --- 准备：创建 ATM 实例 ---
class LiLei(User):
    def __init__(self):
        super().__init__("李磊")


li_lei = LiLei()
atm = ATM(li_lei)


# --- 1. 基础函数封装 ---
def enter_card():
    print("欢迎使用ATM机")


def save_money(amount):
    atm.saveMoney(amount)


def fetch_money(amount):
    atm.fetchMoney(amount)


def exit_card():
    print("谢谢使用")


def check_balance():
    atm.getBalance()


# --- 2. 通用操作：函数作为参数 ---
def common_operation(opera, amount):
    """通用操作：先查余额，再执行具体操作"""
    check_balance()
    opera(amount)


# --- 3. 复合操作 v1：函数数组 ---
def composite_operation(comm_opera_arr, card_opera_arr, amount):
    """复合操作：入卡 → 批量操作 → 出卡"""
    card_opera_arr[0]()
    for opera in comm_opera_arr:
        common_operation(opera, amount)
    card_opera_arr[1]()


comm_opera_arr = [save_money, save_money, fetch_money]
card_opera_arr = [enter_card, exit_card]

print("=== composite_operation v1 ===")
composite_operation(comm_opera_arr, card_opera_arr, 500)


# --- 4. 复合操作 v2：lambda 替代具名函数 ---
def composite_operation2(comm_opera_arr, card_opera1, card_opera2, amount):
    """复合操作：用 lambda 传入匿名函数"""
    card_opera1()
    for opera in comm_opera_arr:
        common_operation(opera, amount)
    card_opera2()


print("\n=== composite_operation2 (lambda) ===")
composite_operation2(
    comm_opera_arr,
    lambda: print("欢迎使用ATM机"),
    lambda: print("谢谢使用"),
    500
)


# --- 5. 复合操作 v3：lambda 更复杂 ---
# 支持多参数、条件逻辑、字典映射、操作日志
def composite_operation3(comm_opera_arr, enter_card, exit_card, amount, log_opera):
    """复合操作3：自定义入卡问候、出卡总结、操作日志"""
    enter_card(atm.user.name, amount)
    for opera in comm_opera_arr:
        log_msg = log_opera(opera, amount)
        print(f"[日志] {log_msg}")
        common_operation(opera, amount)
    exit_card(atm.user.name, amount)


# 操作名称映射
opera_label = {save_money: "存款", fetch_money: "取款"}

print("\n=== composite_operation3 (复杂 lambda) ===")
composite_operation3(
    comm_opera_arr,
    lambda name, amt: print(f"✦ {name} 您好！本次计划操作 {amt} 元，请确认 ✦"),
    lambda name, amt: print(f"✦ {name} 本次操作总额 {amt} 元，感谢使用ATM ✦"),
    500,
    lambda opera, amt: f"{opera_label[opera]} {amt}元 → 执行中..." if amt > 0 else f"{opera_label[opera]} 金额异常"
)
