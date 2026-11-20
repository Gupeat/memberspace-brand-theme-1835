# 微信开发者工具运行与截图（#1835）

本文件说明如何在**真实微信开发者工具**中打开 `miniprogram-demo`，验证 `theme.wxss` 对 TDesign 组件（t-button / t-tag）的品牌色生效，并复现 `evidence/devtools/` 中的证据。所有数据均为虚构示例。

## 1. 环境

- 微信开发者工具：2.02.2609250 Stable（Windows）
- 基础库：3.4.10
- AppID：个人沙箱测试号 `wx65dda5a642890a95`（不是客户 AppID，仅用于本地模拟器）
- 页面：`pages/index/index`；设备：iPhone 12/13 (Pro)
- TDesign 小程序组件：`tdesign-miniprogram` 1.18.0；仓库提供 `vendor/tdesign-miniprogram-1.18.0.tgz`，按第 2.1 节重建 `miniprogram_npm/tdesign-miniprogram/`

## 2. 目录与主题注入

```text
miniprogram-demo/
├─ app.json / app.js / app.wxss
├─ theme.wxss                 # 由 scripts/build.py 从 tokens.json 生成
├─ project.config.json        # appid / libVersion / miniprogramRoot
├─ pages/index/{index.json,index.wxml,index.wxss,index.js}
└─ miniprogram_npm/tdesign-miniprogram/
```

- `app.wxss` 第一行是 `@import "./theme.wxss";`
- `miniprogram-demo/theme.wxss` 与仓库根 `theme.wxss` **字节相同**；`build.py` 同步写入，`verify_devtools_evidence.py` 会校验
- 页面只使用 `t-button` 与 `t-tag`，并直接引用 `--td-brand-color`、`--td-brand-color-light` 等变量

### 2.1 重建 miniprogram_npm

仓库不提交 1,191 个依赖文件，改用随仓库提供的 npm 包重建：

```powershell
mkdir "$env:TEMP\tdesign-miniprogram" -Force
tar -xzf vendor/tdesign-miniprogram-1.18.0.tgz -C "$env:TEMP\tdesign-miniprogram"
New-Item -ItemType Directory -Force miniprogram-demo/miniprogram_npm/tdesign-miniprogram | Out-Null
Copy-Item "$env:TEMP\tdesign-miniprogram\package\miniprogram_dist\*" miniprogram-demo/miniprogram_npm/tdesign-miniprogram -Recurse -Force
```

完成后 `miniprogram-demo/miniprogram_npm/tdesign-miniprogram/` 应存在 `button/`、`tag/` 等组件目录。

## 3. 打开项目

```powershell
# 启动 IDE 前清除该环境变量，否则 Electron 会以 Node 模式退出
Remove-Item Env:ELECTRON_RUN_AS_NODE -ErrorAction SilentlyContinue

# 启动 IDE（如已启动可跳过）
& "C:\Program Files (x86)\Tencent\微信web开发者工具\微信开发者工具.exe"

# 等 IDE 服务端口就绪后用 CLI 打开项目
& "C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat" open `
  --project "<repo>\miniprogram-demo" --port 24728 --lang zh
```

> 首次使用 CLI 需要在 IDE 的“设置 → 安全设置”中开启服务端口。若 IDE 未登录，CLI 会提示登录；本项目只使用沙箱 AppID，不需要真实小程序账号。

## 4. 预期画面

模拟器中应看到：

- 顶部蓝色品牌头图（`--td-brand-color` = `#1F5EFF`）
- “立即报名”主按钮：蓝底白字，圆角 8px
- “查看详情”浅色按钮：浅蓝底（`#F1F4FF`）、品牌色文字
- “联系顾问”默认按钮
- 品牌 / 成功 / 警告 / 危险四种 `t-tag`
- 页脚“示例说明”：本页在微信开发者工具中运行，引用 `repo/theme.wxss` 生成的 TDesign 变量

## 5. 证据与校验

| 文件 | 说明 |
| --- | --- |
| `evidence/devtools/miniprogram-simulator.png` | 仅模拟器画面，488×941，101,266 B，SHA-256 `3df9ec5a364e7067953609beecac54bb65591607c02f733192a84900ebc2a187` |
| `evidence/devtools/miniprogram-devtools.png` | 完整 IDE 窗口（文件树、模拟器、调试器），1564×1250，179,074 B，SHA-256 `97d49831578538a6bab2e839a951c47c0c2faad995a91327be4b41e1f893e8fe` |
| `evidence/devtools/run.json` | 工具版本、AppID、页面、设备、截图尺寸/字节/哈希、计算样式、复现命令 |
| `evidence/devtools/verify.json` | 23 项校验结果（截图、AppID、主题副本、`@import`、WXML 组件、计算样式、语义浅底与字号） |

```powershell
python scripts/verify_devtools_evidence.py
# {"ok": true, "checked": 23, ...}
```

计算样式（真实渲染，随工具版本可能有机差异）：

```text
button_primary.background = rgb(31, 94, 255)
button_primary.color      = rgb(255, 255, 255)
button_primary.fontSize   = 16px
button_light.background   = rgb(241, 244, 255)
tag_brand.background      = rgb(241, 244, 255)
tag_brand.color           = rgb(31, 94, 255)
tag_brand.fontSize        = 12px
tag_success.background    = rgb(231, 247, 240)
tag_success.color         = rgb(14, 122, 95)
tag_warning.background    = rgb(255, 244, 229)
tag_warning.color         = rgb(154, 91, 0)
tag_danger.background     = rgb(254, 233, 233)
tag_danger.color          = rgb(180, 35, 24)
```

## 6. 限制

- 这是**模拟器截图**，不是真机截图；真机需要真实 AppID 与微信登录，本项目不涉及。
- 使用沙箱测试号；不同 IDE 版本、设备模拟器、字体渲染可能导致 PNG 字节不同。`run.json` 绑定本次证据的字节与哈希，重新截图后需同步更新。
- `miniprogram-demo` 只证明主题变量对 t-button / t-tag 生效，不代表全部 TDesign 组件；完整组件外观见 `demo/index.html`（Web 预览，2rpx=1px）。
- 模拟器不连接后端，页面无网络请求；所有文案与数据均为虚构。
- 截图由运行中的 DevTools 远程调试端口导出，不是网页截图；不要在无 IDE 的环境下伪造同名文件，`verify_devtools_evidence.py` 会校验 AppID、主题副本与计算样式。
