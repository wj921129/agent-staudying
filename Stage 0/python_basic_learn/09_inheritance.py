# ============ 09 继承 ============
# 知识点：继承、super() 调用父类、方法重写、新增属性和方法


# --- 1. 父类 ---
class User:
    """用户信息类"""

    def __init__(self, name, id_card, phone):
        self.name = name
        self.id_card = id_card
        self.phone = phone

    def __str__(self):
        return f"User(name={self.name}, id_card={self.id_card}, phone={self.phone})"


# --- 2. 子类继承父类 ---
class LiLei(User):
    """LiLei 继承 User，新增 house 属性"""

    def __init__(self, name, id_card, phone, house):
        # super() 调用父类的 __init__ 方法
        super().__init__(name, id_card, phone)
        self.house = house  # 新增属性：房子地址

    def house_address(self):
        """新增方法：打印房子地址"""
        print(f"{self.name} 的房子在 {self.house}")


# 创建子类对象
lilei = LiLei("李磊", "456", "131", "阿龙太")

# 继承自父类的 __str__ 方法
print(lilei)

# 调用子类新增的方法
lilei.house_address()

# 继承自父类的属性依然可用
print(f"姓名：{lilei.name}，身份证：{lilei.id_card}，手机：{lilei.phone}")


# --- 3. 多态示例 ---
class Student(User):
    """Student 继承 User，新增 school 属性"""

    def __init__(self, name, id_card, phone, school):
        super().__init__(name, id_card, phone)
        self.school = school

    def __str__(self):
        # 重写父类的 __str__ 方法
        return f"Student(name={self.name}, school={self.school})"


# 多态：不同子类对同一方法有不同实现
users = [
    LiLei("李磊", "456", "131", "阿龙太"),
    Student("小红", "789", "132", "北京大学"),
]

for u in users:
    print(u)  # 自动调用各自重写的 __str__
