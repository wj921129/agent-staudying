# ============ 08 基础类 ============
# 知识点：class 定义、__init__ 构造方法、__str__ 字符串表示、self


# --- 1. 用户信息类 ---
class User:
    """用户信息类：演示构造方法与字符串表示"""

    def __init__(self, name, id_card, phone):
        self.name = name          # 用户姓名
        self.id_card = id_card    # 身份证号
        self.phone = phone        # 手机号

    def __str__(self):
        """定义对象的字符串表示，方便 print 输出"""
        return f"User(name={self.name}, id_card={self.id_card}, phone={self.phone})"


# 创建对象并打印
user = User("张三", "110101199001011234", "13800138000")
print(user)  # 自动调用 __str__


# --- 2. ATM 取款机类 ---
class ATM:
    """ATM 取款机类：演示存款、取款、查询余额"""

    def __init__(self, bank_name, user, balance=0.0):
        self.bank_name = bank_name    # 所属银行名称
        self.user = user              # 用户信息对象（组合）
        self.balance = balance        # 账户余额

    def save_money(self, amount):
        """存款"""
        if amount <= 0:
            print("存款金额必须大于0")
            return
        self.balance += amount
        print(f"{self.user.name} 成功存入 {amount} 元，当前余额：{self.balance} 元")

    def fetch_money(self, amount):
        """取款"""
        if amount <= 0:
            print("取款金额必须大于0")
            return
        if amount > self.balance:
            print(f"余额不足！当前余额仅 {self.balance} 元，无法取出 {amount} 元")
            return
        self.balance -= amount
        print(f"{self.user.name} 成功取出 {amount} 元，当前余额：{self.balance} 元")

    def check_balance(self):
        """查询余额"""
        print(f"【{self.bank_name}】{self.user.name} 的账户余额为：{self.balance} 元")

    def __str__(self):
        return f"ATM(bank_name={self.bank_name}, user={self.user}, balance={self.balance})"


# 使用 ATM 类
user = User("李磊", "4300", "131")
atm = ATM("中国银行", user, 1000.0)
atm.save_money(500.0)
atm.fetch_money(500.0)
atm.check_balance()
print(atm)
