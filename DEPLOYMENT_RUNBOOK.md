# 新奇特选品雷达部署运行说明

这份文档给不熟悉技术部署的人使用。目标是：在自己的电脑上把这个 Skill 跑起来，打开一个网页界面，完成一次选品分析，并能正常使用 TikTok 页面浮窗。

项目地址：

```text
https://github.com/OwenZhao9/novelty-product-scout-skill
```

本项目是本地运行的网页工具，不需要购买服务器，也不需要前端打包。

如果只使用选品分析网页，电脑里有 Python 就可以启动。

如果要使用“点击 TikTok 链接后自动打开 TikTok 页面并显示右侧浮窗”，还需要额外准备 Node.js、Google Chrome，并开启 Chrome 的 AppleScript JavaScript 权限。

## 1. 你需要准备什么

请先准备：

- 一台电脑：Mac 或 Windows 都可以
- 一个浏览器：推荐 Chrome
- Python 3：推荐 Python 3.10 或以上
- Node.js：用于 TikTok 页面浮窗
- 网络连接：用于采集公开网页信号
- Git：可选，如果不会用 Git，也可以直接下载 ZIP

不需要准备：

- 不需要服务器
- 不需要数据库
- 不需要 API Key
- 不需要付费数据源

特别说明：

- 普通选品分析：Mac 和 Windows 都可以。
- TikTok 页面右侧浮窗：当前版本只支持 macOS + Google Chrome，因为它复用了小红书 Skill 的 AppleScript 注入方式。
- 如果是 Windows，可以正常使用选品分析和工具内 TikTok 证据过滤，但不能使用“注入到 TikTok 网站页面的浮窗”。

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

## 3. 安装 Node.js

如果只做选品分析，可以先跳过这一节。

如果要使用 TikTok 页面右侧浮窗，必须安装 Node.js。否则点击 TikTok 链接时，浏览器控制台会看到：

```text
/api/install-tiktok-panel 500 (Internal Server Error)
```

### Mac

打开“终端”，输入：

```bash
node --version
```

如果能看到类似下面的内容，说明 Node.js 已经装好：

```text
v20.0.0
```

如果提示找不到命令，可以用 Homebrew 安装：

```bash
brew install node
```

如果没有 Homebrew，也可以直接去 Node.js 官网下载 LTS 版本：

```text
https://nodejs.org
```

### Windows

打开 PowerShell，输入：

```powershell
node --version
```

如果提示找不到命令，去 Node.js 官网下载 LTS 版本：

```text
https://nodejs.org
```

安装完成后，关闭并重新打开终端或 PowerShell，再运行：

```bash
node --version
```

确认能看到版本号。

## 4. 开启 Chrome 的 TikTok 浮窗权限

如果只使用网页里的选品分析，可以先跳过这一节。

如果要让工具把浮窗安装到 TikTok 网站页面，必须使用 macOS 的 Google Chrome，并打开下面这个权限。

打开 Google Chrome，点击系统菜单栏：

```text
查看 > 开发者 > 允许 Apple 事件中的 JavaScript
```

英文版 Chrome 是：

```text
View > Developer > Allow JavaScript from Apple Events
```

注意：

- 这个开关是 Chrome 级别的，不是项目设置。
- 如果不开，点击 TikTok 链接时 `/api/install-tiktok-panel` 会失败。
- 第一次使用时，macOS 可能会弹出权限提示，允许终端或 Python 控制 Chrome 即可。
- Windows 目前不能使用这个 TikTok 网站注入浮窗，因为 Windows 没有 macOS AppleScript。

## 5. 获取项目代码

有两种方式，任选一种。

### 方式 A：直接下载 ZIP，适合不使用命令行的人

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

## 6. 如果以前运行过旧版本，先更新项目

如果这台电脑以前运行过旧版本，建议先做一次更新。否则浏览器里可能还在用旧页面缓存，或者后端还是旧代码。

### 使用 Git 下载的人

进入项目文件夹后运行：

```bash
git pull
```

如果项目还在运行，先回到运行项目的终端，按：

```text
Ctrl + C
```

然后重新启动项目。

### 使用 ZIP 下载的人

如果是下载 ZIP 的方式，不会自动更新。建议：

1. 重新打开 GitHub 项目页。
2. 重新点击 `Code > Download ZIP`。
3. 解压新的 ZIP。
4. 用新的文件夹启动项目。

### 更新后刷新浏览器

项目启动后，浏览器打开页面时建议强制刷新一次：

Mac：

```text
Command + Shift + R
```

Windows：

```text
Ctrl + F5
```

这样可以避免浏览器继续使用旧版本的网页文件。

## 7. 启动网页版本

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

## 8. 打开网页

启动成功后，不要关闭终端或 PowerShell。

打开浏览器，访问：

```text
http://127.0.0.1:8765
```

如果页面能打开，说明部署成功。

## 9. 如何完成一次选品分析

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

## 10. 如何使用 TikTok 页面浮窗

这一节只适用于 macOS + Google Chrome。

如果你只是想在本地工具里看选品结果，不需要做这一节。

使用前确认三件事：

1. 已经安装 Node.js，并且 `node --version` 能显示版本号。
2. 项目正在运行，网页能打开 `http://127.0.0.1:8765`。
3. Chrome 已经开启 `查看 > 开发者 > 允许 Apple 事件中的 JavaScript`。

操作流程：

1. 在本地网页里点击“开始选品分析”。
2. 等结果出来后，点击右侧结果里的 TikTok 证据链接。
3. 系统会用 Chrome 打开 TikTok 页面。
4. 如果注入成功，TikTok 页面右侧会出现一个悬浮筛选面板。

浮窗里可以设置：

- 内容排除词：隐藏标题或描述里包含这些词的内容。
- 必须包含词：只保留包含这些词的内容。
- 账号/作者排除词：隐藏指定账号或作者。
- 日期范围：只看最近一段时间的内容。
- 日期未知也隐藏：看不到发布时间的内容也一起隐藏。

常用按钮：

- `Apply`：应用当前筛选条件。
- `Reset`：清空筛选条件。
- 拖动浮窗顶部：移动浮窗位置。

如果点击 TikTok 链接后没有出现浮窗，先看下面“常见问题”的第 6 到 9 条。

## 11. 如何停止项目

回到正在运行项目的终端或 PowerShell，按：

```text
Ctrl + C
```

看到程序停止后，就可以关闭窗口。

## 12. 如果 8765 端口被占用

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

## 13. 运行命令行演示

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

## 14. 常见问题

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

### 问题 6：页面右上角显示 Error

先看浏览器控制台或启动项目的终端里有没有具体报错。

如果控制台里只有下面这个报错，可以忽略：

```text
favicon.ico 404
```

这是浏览器在找网站图标，不影响项目使用。

如果控制台里出现下面这个报错：

```text
/api/install-tiktok-panel 500 (Internal Server Error)
```

说明 TikTok 浮窗安装接口失败了，优先检查第 7 条。

### 问题 7：点击 TikTok 链接后报 `/api/install-tiktok-panel 500`

最常见原因是没有安装 Node.js，或者启动项目的终端找不到 `node` 命令。

请在同一个终端里运行：

```bash
node --version
```

如果提示找不到命令，就安装 Node.js：

```text
https://nodejs.org
```

安装完成后必须做两件事：

1. 关闭原来的终端或 PowerShell。
2. 重新打开终端，重新运行 `python3 scripts/web_app.py` 或 `python scripts\web_app.py`。

如果 `node --version` 正常，但还是 500，看启动项目的终端窗口，那里会显示更具体的后端报错。

### 问题 8：以前版本能用，更新 TikTok 浮窗后出错

新版本增加了 TikTok 页面浮窗能力，所以多了 Node.js 和 macOS Chrome 权限要求。

按这个顺序处理：

1. 回到运行项目的终端，按 `Ctrl + C` 停止旧服务。
2. 更新项目代码：Git 用户运行 `git pull`，ZIP 用户重新下载 ZIP。
3. 检查 Python：`python3 --version` 或 `python --version`。
4. 如果要用 TikTok 网站浮窗，检查 Node：`node --version`。
5. macOS Chrome 开启 `查看 > 开发者 > 允许 Apple 事件中的 JavaScript`。
6. 重新启动项目。
7. 浏览器强制刷新：Mac 用 `Command + Shift + R`，Windows 用 `Ctrl + F5`。

如果是在 Windows 上使用，选品分析可以正常用，但 TikTok 网站页面浮窗不能用。

### 问题 9：TikTok 打开了，但是没有看到右侧浮窗

按下面顺序排查：

1. 确认使用的是 Google Chrome，不是 Safari、Edge 或系统默认浏览器。
2. 确认是 macOS，Windows 暂不支持注入到 TikTok 网站页面。
3. 确认 `node --version` 能显示版本号。
4. 确认 Chrome 已开启 `允许 Apple 事件中的 JavaScript`。
5. 确认本地项目还在运行，地址是 `http://127.0.0.1:8765`。
6. 回到本地网页，重新点击一次 TikTok 结果链接。

## 15. 这个项目的数据来源说明

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

## 16. 最简单的完整流程

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

如果还要使用 TikTok 网站右侧浮窗，再多做三步：

1. 安装 Node.js，并确认 `node --version` 能显示版本号。
2. 使用 macOS Google Chrome，并开启 `查看 > 开发者 > 允许 Apple 事件中的 JavaScript`。
3. 在分析结果里点击 TikTok 证据链接，等待 Chrome 页面右侧出现浮窗。
