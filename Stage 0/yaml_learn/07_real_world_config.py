"""
07_real_world_config.py
真实项目配置读写示例

学习目标：
1. 模拟一个完整的项目配置文件（数据库、日志、服务器、功能开关）
2. 封装读取配置的函数，方便业务代码复用
3. 体验配置文件在项目中的典型用法
"""

import yaml
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
CONFIG_FILE = OUTPUT_DIR / "project_config.yaml"


def load_config(path: Path) -> dict:
    """安全地加载 YAML 配置文件，文件不存在时返回空字典。"""
    if not path.exists():
        print(f"⚠️ 配置文件不存在：{path}，将使用默认空配置")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_config(path: Path, config: dict) -> None:
    """把配置保存为 YAML 文件。"""
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            config,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )


# 第一步：创建一个接近真实项目的初始配置
project_config = {
    "project": {
        "name": "First Demo",
        "env": "development",
        "version": "2.0.0",
    },
    "server": {
        "host": "127.0.0.1",
        "port": 8000,
        "workers": 4,
    },
    "database": {
        "driver": "mysql",
        "host": "localhost",
        "port": 3306,
        "username": "root",
        "password": "secret",  # 真实项目中不要把密码提交到 Git！
        "database": "first_demo",
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "logs/app.log",
    },
    "features": {
        "enable_cache": True,
        "enable_metrics": False,
        "allowed_hosts": ["localhost", "127.0.0.1"],
    },
}

save_config(CONFIG_FILE, project_config)
print(f"✅ 项目配置已生成：{CONFIG_FILE}")
print()
print("--- 生成的 YAML ---")
print(CONFIG_FILE.read_text(encoding="utf-8"))

# 第二步：加载配置
config = load_config(CONFIG_FILE)

# 第三步：从配置中提取参数（带默认值，增强健壮性）
print("--- 业务代码中使用配置 ---")
host = config.get("server", {}).get("host", "0.0.0.0")
port = config.get("server", {}).get("port", 8000)
log_level = config.get("logging", {}).get("level", "DEBUG")
cache_enabled = config.get("features", {}).get("enable_cache", False)

print(f"启动服务器：{host}:{port}")
print(f"日志级别：{log_level}")
print(f"缓存开关：{cache_enabled}")
print()

# 第四步：修改配置并保存（模拟用户通过管理后台改配置）
config["features"]["enable_metrics"] = True
config["features"]["allowed_hosts"].append("192.168.1.100")
config["project"]["env"] = "production"

save_config(CONFIG_FILE, config)
print("--- 更新后的 YAML ---")
print(CONFIG_FILE.read_text(encoding="utf-8"))

print()
print("提示：真实项目中，密码等敏感信息建议放在环境变量或专门的 secrets 管理工具中。")
