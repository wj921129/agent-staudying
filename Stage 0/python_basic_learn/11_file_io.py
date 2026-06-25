# ============ 11 文件读写 ============
# 知识点：open()、read()、readlines()、write()、append、close()、with 语句
import os

# 使用当前文件同目录下的临时文件进行演示
file_path = os.path.join(os.path.dirname(__file__), "temp_demo.txt")

# --- 1. 写入文件（w 模式：覆盖写入） ---
f = open(file_path, "w", encoding="utf-8")
f.write("第一行内容\n")
f.write("第二行内容\n")
f.write("第三行内容\n")
f.close()
print(f"文件已写入：{file_path}")

# --- 2. 追加写入（a 模式：追加到末尾） ---
f = open(file_path, "a", encoding="utf-8")
f.write("第四行（追加）\n")
f.close()
print("追加写入完成")

# --- 3. 读取文件（r 模式） ---
# read() 一次性读取全部内容
f = open(file_path, "r", encoding="utf-8")
content = f.read()
print(f"\n--- read() 全部读取 ---\n{content}")
f.close()

# readlines() 按行读取为列表
f = open(file_path, "r", encoding="utf-8")
lines = f.readlines()
print("--- readlines() 按行读取 ---")
for line in lines:
    print(f"  → {line.strip()}")  # strip() 去掉末尾换行符
f.close()

# --- 4. 推荐写法：with 语句自动关闭文件 ---
# with 语句会在代码块结束后自动调用 close()，避免忘记关闭
print("\n--- with 语句读取 ---")
with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        print(f"  → {line.strip()}")

# --- 5. 读取项目中的其他文件 ---
# 读取 main.py 示例
main_path = os.path.join(os.path.dirname(__file__), '..', 'main.py')
with open(main_path, "r", encoding="utf-8") as f:
    print(f"\n--- main.py 内容 ---\n{f.read()}")

# 清理临时文件
os.remove(file_path)
print("临时文件已清理")
