# 新奇特选品雷达部署运行说明

这份文档给完全不懂技术的人使用。目标是：在自己的电脑上把这个 Skill 跑起来，打开一个网页界面，然后完成一次选品分析。

项目地址：

```text
https://github.com/OwenZhao9/novelty-product-scout-skill
```

本项目是本地运行的网页工具，不需要购买服务器，也不需要前端打包。电脑里只要有 Python，就可以启动。

## 1. 你需要准备什么

请先准备：

- 一台电脑：Mac 或 Windows 都可以
- 一个浏览器：推荐 Chrome
- Python 3：推荐 Python 3.10 或以上
- 网络连接：用于采集公开网页信号
- Git：可选，如果不会用 Git，也可以直接下载 ZIP

不需要准备：

- 不需要服务器
- 不需要数据库
- 不需要 Node.js
- 不需要 API Key
- 不需要付费数据源

## 2. 安装 Python

### Mac

打开“终端”，输入：

```bash
python3 --version
```

如果能看到类似下面的内容，说明 Python 已经装好：

```text
Python 3.10.0
```

如果提示找不到命令，可以去 Python 官网下载安装：

```text
https://www.python.org/downloads/
```

### Windows

打开 PowerShell，输入：

```powershell
python --version
```

或者：

```powershell
py --version
```

如果提示找不到命令，去 Python 官网下载安装：

```text
https://www.python.org/downloads/
```

安装 Windows 版本 Python 时，建议勾选：

```text
Add python.exe to PATH
```

## 3. 获取项目代码

有两种方式，任选一种。

### 方式 A：直接下载 ZIP，适合小白

1. 打开项目地址：

```text
https://github.com/OwenZhao9/novelty-product-scout-skill
```

2. 点击绿色按钮 `Code`
3. 点击 `Download ZIP`
4. 下载完成后解压
5. 进入解压后的文件夹

解压后的文件夹名字通常类似：

```text
novelty-product-scout-skill-main
```

### 方式 B：使用 Git 下载，适合会一点命令行的人

Mac 终端或 Windows PowerShell 输入：

```bash
git clone https://github.com/OwenZhao9/novelty-product-scout-skill.git
cd novelty-product-scout-skill
```

## 4. 启动网页版本

### Mac 启动方式

先进入项目文件夹。假设项目放在桌面，可以这样进入：

```bash
cd ~/Desktop/novelty-product-scout-skill
```

如果你是下载 ZIP 解压的，文件夹名可能是：

```bash
cd ~/Desktop/novelty-product-scout-skill-main
```

然后启动：

```bash
python3 scripts/web_app.py
```

看到类似下面的内容，就说明启动成功：

```text
Novelty Product Scout web app: http://127.0.0.1:8765
Press Ctrl+C to stop.
```

### Windows 启动方式

先进入项目文件夹。假设项目放在桌面，可以这样进入：

```powershell
cd Desktop\novelty-product-scout-skill
```

如果你是下载 ZIP 解压的，文件夹名可能是：

```powershell
cd Desktop\novelty-product-scout-skill-main
```

然后启动：

```powershell
python scripts\web_app.py
```

如果上面命令不行，试试：

```powershell
py scripts\web_app.py
```

看到类似下面的内容，就说明启动成功：

```text
Novelty Product Scout web app: http://127.0.0.1:8765
Press Ctrl+C to stop.
```

## 5. 打开网页

启动成功后，不要关闭终端或 PowerShell。

打开浏览器，访问：

```text
http://127.0.0.1:8765
```

如果页面能打开，说明部署成功。

## 6. 如何完成一次选品分析

进入网页后，按下面步骤操作：

1. 选择市场，例如泰国、越南、菲律宾、马来西亚、新加坡、美国等。
2. 选择平台，例如 TikTok 小店。
3. 选择人群，如果没有明确人群，可以勾选“不限”。
4. 选择类目，例如饰品配件、宠物用品、家居清洁、厨房工具等。
5. 设置价格带，最低值可以填 `0`，最高值可以留空或填一个较大的数字。
6. 选择货币单位，例如泰铢、人民币、越南盾、新加坡元、美金、菲律宾比索、马来西亚币。
7. 输入种子关键词，建议用英文，例如：

```text
portable mini cleaner, pet hair remover, travel organizer
```

8. 输入偏好，例如：

```text
轻小件、便携、物流压力低、视觉演示强、合规风险低
```

9. 点击“开始选品分析”。
10. 等待结果生成。

结果页面会展示：

- 候选产品
- 机会评分
- 可信度
- 时效性判断
- 证据链接
- 供应链关键词
- 内容脚本
- 风险提示
- 首测计划

## 7. 如何停止项目

回到正在运行项目的终端或 PowerShell，按：

```text
Ctrl + C
```

看到程序停止后，就可以关闭窗口。

## 8. 如果 8765 端口被占用

如果启动时报错，提示端口已经被占用，可以换一个端口。

Mac：

```bash
python3 scripts/web_app.py 8766
```

Windows：

```powershell
python scripts\web_app.py 8766
```

然后浏览器打开：

```text
http://127.0.0.1:8766
```

## 9. 运行命令行演示

如果你只是想快速确认项目能不能跑，可以运行内置示例。

Mac：

```bash
bash run_demo.sh
```

Windows：

```powershell
python scripts\scout_products.py --market examples\market_profile.json --signals examples\input_signals.csv --output output\report.md --limit 3
```

运行成功后，会生成报告：

```text
output/report.md
```

## 10. 常见问题

### 问题 1：浏览器打不开页面

先确认终端里是否还在运行项目。如果终端关了，网页也会打不开。

正确状态应该能看到：

```text
Novelty Product Scout web app: http://127.0.0.1:8765
Press Ctrl+C to stop.
```

### 问题 2：提示找不到 python 或 python3

说明 Python 没装好，或者没有加入系统路径。

解决方式：

- 重新安装 Python
- Windows 安装时勾选 `Add python.exe to PATH`
- Mac 可以尝试使用 `python3`，Windows 可以尝试使用 `py`

### 问题 3：一直显示正在采集

可能原因：

- 当前网络访问公开搜索结果较慢
- 关键词太窄
- 类目、人群、价格限制太多
- 部分公开网页临时不可访问

处理方式：

- 换更宽的关键词
- 减少筛选条件
- 先用内置示例 CSV 跑一遍
- 重新启动项目后再试

### 问题 4：结果很少或为空

可以这样调整：

- 类目选择“不限”或换成更大的类目
- 人群选择“不限”
- 价格最高值放宽
- 增加英文种子关键词
- 多勾选几个采集源

### 问题 5：结果里有旧内容

这个工具采集的是公开信号，不等于官方实时销量榜。

系统会尽量识别证据里的年份：

- 近期内容会提高时效性判断
- 旧年份内容会被降权
- 无法识别时间的内容会标记为“未识别时间”

实际使用时，建议点击证据链接二次确认。

## 11. 这个项目的数据来源说明

当前版本使用公开网页信号和可选 CSV 数据，不接入付费 API。

它适合做：

- 选品灵感发现
- 首测前机会判断
- 公开证据整理
- 风险初筛
- 内容脚本和供应链关键词生成

它不适合直接当作：

- 官方销量榜
- 实时 GMV 榜
- 确定性爆款预测
- 替代人工选品决策

推荐表达方式是：

```text
这是一个基于公开信号的选品辅助 Skill，用来帮助卖家降低盲目选品成本。
```

不要表达成：

```text
它能保证找到爆款。
```

## 12. 最简单的完整流程

如果你只想照着做一遍，按这个流程：

1. 安装 Python。
2. 从 GitHub 下载项目 ZIP。
3. 解压 ZIP。
4. 打开终端或 PowerShell。
5. 进入项目文件夹。
6. 运行 `python3 scripts/web_app.py`，Windows 可用 `python scripts\web_app.py`。
7. 浏览器打开 `http://127.0.0.1:8765`。
8. 输入市场、类目、关键词、偏好。
9. 点击“开始选品分析”。
10. 查看结果并导出报告。
