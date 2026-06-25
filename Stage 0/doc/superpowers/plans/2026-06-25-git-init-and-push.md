# Git 仓库初始化与推送 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 初始化当前项目目录为 Git 仓库，保留现有代码，配置忽略文件，并推送至远程仓库。

**Architecture:** 本计划通过在本地执行 `git init`，创建 `.gitignore` 排除 IDE 配置文件（如 `.idea`），添加现有文件并创建首次提交。接着请求老板提供远程仓库 URL，最后关联并推送代码。

**Tech Stack:** Git, PowerShell

## Global Constraints
- 必须保留当前目录下的全部代码。
- 必须配置 `.gitignore` 以防止提交垃圾文件（如 `.idea/`）。
- 推送前必须与老板确认远程仓库地址。

---

### Task 1: 初始化本地仓库与配置忽略文件

**Files:**
- Create: `.gitignore`

**Interfaces:**
- Consumes: 当前项目目录结构
- Produces: 初始化后的本地 Git 仓库，且包含 `.gitignore` 规则

- [ ] **Step 1: 初始化 Git 仓库**

运行命令：
```powershell
git init
```
预期输出：包含 "Initialized empty Git repository" 的信息。

- [ ] **Step 2: 创建并配置 `.gitignore` 文件**

在根目录下创建 `.gitignore` 文件，排除 PyCharm 配置文件 `.idea` 及 Python 缓存：
```text
.idea/
__pycache__/
*.pyc
```

- [ ] **Step 3: 检查待提交的文件状态**

运行命令：
```powershell
git status
```
预期输出：显示未跟踪的文件，且 `.idea/` 目录已被成功忽略。

- [ ] **Step 4: 添加并提交代码**

运行命令：
```powershell
git add .
git commit -m "feat: 首次提交，保留现有代码"
```
预期输出：显示添加的文件列表及提交成功信息。

---

### Task 2: 关联远程仓库并推送代码

**Files:**
- Modify: 本地 Git 配置

**Interfaces:**
- Consumes: 老板提供的远程 Git 仓库 URL
- Produces: 远程仓库中包含推送的代码

- [ ] **Step 1: 关联远程仓库**

一旦提供 URL（假设为 `<REMOTE_URL>`），运行：
```powershell
git remote add origin <REMOTE_URL>
```

- [ ] **Step 2: 推送代码到远程仓库**

运行命令：
```powershell
git branch -M main
git push -u origin main
```
预期输出：推送进度及成功信息。
