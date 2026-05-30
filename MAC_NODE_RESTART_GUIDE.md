# Mac 安装 Node.js 后重新启动项目说明

这份文档只针对 Mac 电脑，用来解决安装 Node.js 后，项目仍然报 `/api/install-tiktok-panel 500` 或 TikTok 浮窗无法启动的问题。

## 1. 不要在 Chrome 控制台输入 Node 命令

下面这个命令必须在 Mac 的“终端”里输入：

```bash
node --version
```

不要在 Chrome 开发者工具的“控制台”里输入。Chrome 控制台只能执行 JavaScript，输入 `node --version` 会出现类似错误：

```text
Uncaught SyntaxError: Unexpected identifier 'version'
```

这个错误不代表 Node.js 坏了，只是输错地方了。

## 2. 打开 Mac 终端

可以用任意一种方式打开：

1. 按 `Command + Space`
2. 输入 `终端`
3. 回车打开

也可以打开：

```text
应用程序 > 实用工具 > 终端
```

## 3. 检查 Node.js 是否安装成功

在终端输入：

```bash
node --version
```

如果看到类似下面的内容，说明 Node.js 已经安装成功：

```text
v20.0.0
```

版本号不一定完全一样，只要能显示 `v` 开头的版本号就可以。

如果提示：

```text
command not found: node
```

说明 Node.js 没装好，或者当前终端还没识别到 Node.js。

可以去 Node.js 官网下载 LTS 版本：

```text
https://nodejs.org
```

安装完成后，必须关闭当前终端窗口，再重新打开一个新的终端窗口。

## 4. 停止旧的项目服务

如果项目之前已经在运行，先回到运行项目的终端窗口，按：

```text
Ctrl + C
```

看到命令行可以重新输入内容，就说明旧服务已经停止。

如果找不到之前运行项目的终端窗口，可以直接重新打开一个终端继续下面步骤。旧服务如果还占用端口，后面会有处理方法。

## 5. 重新进入项目文件夹

假设项目在桌面，并且文件夹名是：

```text
novelty-product-scout-skill
```

在终端输入：

```bash
cd ~/Desktop/novelty-product-scout-skill
```

如果你是下载 ZIP 解压的，文件夹名可能是：

```text
novelty-product-scout-skill-main
```

那就输入：

```bash
cd ~/Desktop/novelty-product-scout-skill-main
```

如果不确定文件夹在哪里，可以把项目文件夹直接拖进终端窗口，终端会自动填入路径。

## 6. 在项目文件夹里再次确认 Node

进入项目文件夹后，再输入一次：

```bash
node --version
```

如果能看到版本号，再继续下一步。

如果这里还是提示 `command not found: node`，说明 Node.js 还没有被当前终端识别，需要重新安装 Node.js，或者关闭终端后重新打开。

## 7. 重新启动项目

在项目文件夹里输入：

```bash
python3 scripts/web_app.py
```

看到下面内容说明启动成功：

```text
Novelty Product Scout web app: http://127.0.0.1:8765
Press Ctrl+C to stop.
```

启动成功后，不要关闭这个终端窗口。

## 8. 打开网页

打开 Chrome，访问：

```text
http://127.0.0.1:8765
```

如果之前打开过旧页面，建议强制刷新一次：

```text
Command + Shift + R
```

## 9. 如果要使用 TikTok 页面浮窗

TikTok 网站浮窗还需要打开 Chrome 的一个权限。

在 Mac 顶部菜单栏里找到 Chrome 的菜单，点击：

```text
查看 > 开发者 > 允许 Apple 事件中的 JavaScript
```

英文版 Chrome 是：

```text
View > Developer > Allow JavaScript from Apple Events
```

如果没有开启这个权限，TikTok 浮窗可能无法注入到页面。

## 10. 测试 TikTok 浮窗

1. 保持项目终端窗口不要关闭。
2. Chrome 打开 `http://127.0.0.1:8765`。
3. 在网页里点击“开始选品分析”。
4. 结果出来后，点击一个 TikTok 证据链接。
5. Chrome 会打开 TikTok 页面。
6. 如果正常，TikTok 页面右侧会出现筛选浮窗。

## 11. 常见问题

### 问题 1：还是出现 `/api/install-tiktok-panel 500`

先确认是在终端里运行：

```bash
node --version
```

不是在 Chrome 控制台里运行。

如果终端里能看到 Node 版本，但页面还是报 500，请看运行 `python3 scripts/web_app.py` 的终端窗口，那里会显示更具体的错误。

### 问题 2：`favicon.ico 404`

这个可以忽略。

这是浏览器在找网站图标，不影响项目运行，也不是 TikTok 浮窗失败的原因。

### 问题 3：端口 8765 被占用

说明旧项目可能还在运行。

可以换一个端口启动：

```bash
python3 scripts/web_app.py 8766
```

然后浏览器打开：

```text
http://127.0.0.1:8766
```

### 问题 4：TikTok 页面打开了，但是没有浮窗

按顺序检查：

1. 是否用的是 Google Chrome。
2. 是否已经安装 Node.js。
3. 是否在终端里能运行 `node --version`。
4. 是否开启了 `允许 Apple 事件中的 JavaScript`。
5. 是否保持本地项目还在运行。
6. 是否重新点击了一次 TikTok 结果链接。

## 12. 最短操作流程

如果只想照着做，按这个流程：

1. 安装 Node.js。
2. 关闭所有终端窗口。
3. 重新打开终端。
4. 输入 `node --version`，确认有版本号。
5. 进入项目文件夹。
6. 输入 `python3 scripts/web_app.py`。
7. Chrome 打开 `http://127.0.0.1:8765`。
8. 按 `Command + Shift + R` 强制刷新。
9. 如果要用 TikTok 浮窗，开启 Chrome 的 `允许 Apple 事件中的 JavaScript`。
10. 点击选品结果里的 TikTok 链接测试浮窗。
