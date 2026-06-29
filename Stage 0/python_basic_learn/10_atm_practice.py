# ============ 10 ATM 业务实践 ============
# 知识点：类的组合使用、业务逻辑封装、继承扩展
import sys
import os

# 将项目根目录加入路径，以便导入 shop 模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shop import User, ATM


# --- 1. 继承 User 创建具体用户 ---
class LiLei(User):
    def __init__(self):
        super().__init__("李磊")


class ADiao(User):
    def __init__(self):
        super().__init__("阿刁")


# --- 2. 创建用户与 ATM 实例 ---
li_lei = LiLei()
a_diao = ADiao()

atm_li = ATM(li_lei)
atm_diao = ATM(a_diao)

# --- 3. 基本操作 ---
print("=== 李磊的账户 ===")
atm_li.getBalance()
atm_li.saveMoney(500)
atm_li.fetchMoney(200)
atm_li.getBalance()

print("\n=== 阿刁的账户 ===")
atm_diao.getBalance()
atm_diao.saveMoney(1000)
atm_diao.fetchMoney(800)
atm_diao.getBalance()
