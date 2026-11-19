# 会员空间平台 · 小程序品牌主题（#1835）

一套可审计、可再生成的小程序视觉主题：以 `tokens.json`（W3C Design Tokens / DTCG）为唯一来源，生成 TDesign 小程序 CSS 变量、Figma 变量集合、对比度检查表和 Web 预览截图。

- 任务：#1835【S3-BRAND-001】小程序主题设计变量与 TDesign 主题映射
- 范围：色彩、字号/行高/字重、圆角、间距、阴影、动效；不含业务页面开发
- 数据：全部为虚构示例，不含客户名、手机号、邮箱、身份证等 PII
- 技术：Python 3.12 + Node.js（仅截图用 Playwright/Edge）；产物为纯静态文件
- 交付仓库：https://github.com/Gupeat/memberspace-brand-theme-1835
- 在线 Figma：https://www.figma.com/design/U3n0qOCgViDDfdSnOWIw5n/MemberSpace-Brand-Theme-1835---v2?node-id=0-1
- 发布资产：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/tag/v2.1.0

## 交付物

| 文件 | 说明 |
| --- | --- |
| `tokens.json` | 74 个 W3C DTCG 令牌；7 个别名；color 38、font 16、radius 4、space 5、shadow 3、motion 8 |
| `theme.wxss` | 64 个 TDesign 1.18.0 实际消费的 CSS 变量，选择器为 `page, .td-theme` |
| `figma/figma-variables.json` | 74 个 Figma 变量（COLOR/FLOAT/STRING），名称与令牌路径逐一对应 |
| `figma/figma-import.tokens.json` + `figma/Light.tokens.json` | 可直接导入 Figma Variables 的嵌套 DTCG 数据；`Light.tokens.json` 用于让 mode 名为 Light |
| `figma/create-variables.js` + `figma/manifest.json` | Figma 开发插件（备选路径）：导入清单后一键创建/更新同名变量集合 |
| `evidence/figma-online/` | 在线 Figma 的导出快照、截图、README 与 `verify.json` |
| `docs/FIGMA-VARIABLES.md` | 74 行 Figma 变量 ↔ tokens.json 1:1 对照表 |
| `docs/CONTRAST.md` | 57 组正文文字/背景组合的 WCAG 对比度表，最低 4.66:1 |
| `demo/index.html` + `demo/demo.css` | TDesign 风格示例页（按钮、标签、cell、输入、提示、变量卡） |
| `artifacts/example-page.png` | 750×2269 示例页截图；由脚本生成并做像素/计算样式断言 |
| `scripts/` | build / validate / capture / acceptance / reverse drill |
| `tests/test_tokens.py` | 15 项 pytest，覆盖 token、别名、对比度、主题映射、Figma（含导入文件）、文档、校验脚本 |

## 快速开始

在 `repo/` 下执行：

```powershell
# 1) 从 tokens.json 重新生成 theme.wxss、Figma 变量、对比度表、对照表
python scripts/build.py

# 2) 8 项产物校验（DTCG、scale、别名、WCAG、新鲜度、Figma 1:1、demo、文档）
python scripts/validate.py

# 3) 单元测试（15 passed）
python -m pytest -q tests

# 4) 校验在线 Figma 的导出快照与 tokens.json 74/74 一致
python scripts/verify_figma_export.py

# 5) Web 预览截图（需要 Node + playwright-core + Microsoft Edge）
npm install playwright-core   # 首次
node scripts/capture.mjs

# 6) 完整两轮验收（清空生成物后重建，并输出 acceptance-<label>.log / ACCEPTANCE-<label>.md）
python scripts/run_acceptance.py --label round1
python scripts/run_acceptance.py --label round2
```

截图脚本默认使用 Microsoft Edge，可用 `EDGE` 环境变量覆盖；Node 可用 `NODE` 环境变量覆盖。

## tokens.json 结构

顶层按 DTCG 分类并声明 `$type`：

- `color`：`brand` 6 阶、`accent` 2 阶、`neutral` 50–900 共 10 阶、`text` 5、`bg` 4、`border` 2、`semantic` 4 色 + 4 浅底、`focus` 1
- `font`：`family.sans`；`size.24/28/32/36/40/48`（rpx）；对应 `lineHeight`；`weight.regular/medium/semibold`
- `radius`：`small` 8rpx、`default` 16rpx、`large` 24rpx、`round` 9999rpx
- `space`：16/24/32/48/64rpx
- `shadow`：`sm/md/lg` 三级；`motion`：`duration` 4 档 + `easing` 4 条
- 7 个别名（如 `color.text.primary` → `color.neutral.900`），构建时统一解析

修改令牌后必须重跑 `build.py`；`validate.py` 会拦截主题/预览/对比度文档与 token 不一致的陈旧产物。

## theme.wxss 用法

在 `app.wxss` 中引入：

```css
@import "theme.wxss";
```

变量挂在 `page` 与 `.td-theme` 上，TDesign 组件会继承：

```css
page, .td-theme {
  --td-brand-color: #1F5EFF;
  --td-brand-color-active: #1239B0;
  --td-font-size-base: 28rpx;
  --td-radius-default: 16rpx;
  /* 其余 60 个变量见 theme.wxss */
}
```

品牌映射示例：

| TDesign 变量 | tokens.json |
| --- | --- |
| `--td-brand-color` | `color.brand.primary` |
| `--td-brand-color-active` | `color.brand.active` |
| `--td-brand-color-disabled` | `color.brand.disabled` |
| `--td-brand-color-focus` | `color.focus.ring` |
| `--td-brand-color-light` | `color.brand.light` |
| `--td-brand-color-light-active` | `color.brand.lightHover` |
| `--td-text-color-brand` | `color.brand.hover` |
| `--td-text-color-primary` | `color.text.primary` |
| `--td-bg-color-page` | `color.bg.page` |
| `--td-font-size-base` | `font.size.28` |
| `--td-radius-default` | `radius.default` |

完整 64 项见 `theme.wxss`；构建脚本中的 `THEME_MAP` 是唯一映射来源。

## Figma 变量

**在线文件（可直接查看）**：https://www.figma.com/design/U3n0qOCgViDDfdSnOWIw5n/MemberSpace-Brand-Theme-1835---v2?node-id=0-1

- 文件：`MemberSpace Brand Theme 1835 - v2`；共享设置为 **Anyone / can edit**（匿名可查看画布；匿名视图不显示 Variables 编辑面板，这是 Figma 权限设计）。
- 变量：collection `Theme`、mode `Light`、**74 个变量**（color 38 / number 28 / string 8），名称与 `tokens.json` 点分路径严格 1:1。
- 导入源：`figma/Light.tokens.json`（与 `figma/figma-import.tokens.json` 字节相同）。
- 导入后导出快照：`evidence/figma-online/Theme.zip`；解包后的 `Light.tokens.json` 由 `scripts/verify_figma_export.py` 与 `tokens.json` 逐项比对（名称、类型、别名、值、描述），结果写入 `evidence/figma-online/verify.json`。
- 证据截图：`evidence/figma-online/figma-online-final.png`（collection Theme / 74 变量 / mode Light）、`figma-shared-final.png`（共享设置）、`figma-anon-public.png`（匿名可查看）。

重新导入步骤（Figma 网页版或桌面端）：

1. Variables 面板 → Import variables → 选择 `figma/Light.tokens.json`（文件名决定 mode 名 `Light`）。
2. 把新 collection 重命名为 `Theme`；导入后应有 74 个变量。
3. 设计稿中按名称绑定颜色/字号/圆角/间距/阴影变量。

桌面插件是备选路径：`Plugins → Development → Import plugin from manifest...`，选择 `figma/manifest.json`，运行 “1835 Brand Theme Variables”；插件只创建/更新同名变量，不删除集合内已有变量，类型冲突与未匹配变量保留并提示。

`docs/FIGMA-VARIABLES.md` 逐行列出令牌路径、Figma 名称、类型、值；`docs/FIGMA-ONLINE.md` 记录在线文件、共享、导入/导出与校验细节。

## 示例页截图

- `demo/index.html` 是 Web 预览，不是微信开发者工具或真机截图；数据全部虚构。
- 预览采用 2rpx = 1px，因此 750px 宽截图等价于 375pt 设备 @2x。
- `scripts/capture.mjs` 断言：按钮背景 `rgb(31, 94, 255)`、标签文字同色且浅底 `rgb(241, 244, 255)`、应用宽度 750、PNG 宽 750 且高 ≥1500，然后才写出截图。
- 产物：`artifacts/example-page.png`（750×2269）。

## 交付与复现

- 仓库：https://github.com/Gupeat/memberspace-brand-theme-1835 （public，全部为虚构数据）
- Release v2.1.0：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/tag/v2.1.0
- 归档资产：`1835-s3-brand-001-rework-v2.zip`；资产页含字节数与 SHA-256，可与提交正文交叉核对。
- 评审可直接在仓库根目录执行“快速开始”的 6 条命令复现 15 passed / 8/8 PASS / Figma 74/74 / 750×2269 截图。

## 验收对照

| AC | 要求 | 证据 |
| --- | --- | --- |
| AC1 | tokens.json 通过 W3C Design Tokens 格式校验 | `validate.py` 检查 1；`artifacts/validation.log`；DTCG `$type/$value` 与 74 token 校验；pytest `test_token_index_has_74_valid_tokens` |
| AC2 | 对比度检查表所有正文组合 ≥4.5:1 | `docs/CONTRAST.md` 57 组；最低 4.66:1；`validate.py` 检查 4；pytest `test_all_57_body_text_pairs_meet_wcag_aa` |
| AC3 | theme.wxss 应用到 TDesign 示例页后按钮/标签使用新品牌色 | `artifacts/example-page.png`；`capture.mjs` 计算样式断言；pytest `test_theme_has_64_tdesign_consumed_variables_and_is_fresh`、`test_browser_preview_is_same_theme_at_2x` |
| AC4 | Figma 变量名与 tokens.json 名称一一对应（对照表） | 在线文件 74 变量；`evidence/figma-online/verify.json` 74/74 名称 1:1；`figma/figma-variables.json` 74 个；`docs/FIGMA-VARIABLES.md` 74 行；`validate.py` 检查 6；pytest `test_figma_variables_are_exactly_1_to_1`、`test_figma_plugin_and_doc_cover_every_token`、`test_figma_import_file_is_nested_dtcg_and_matches_tokens` |

## 质量闸门

`scripts/validate.py` 的 8 项检查全部通过（exit 0）：

1. DTCG 结构与值类型
2. 必需分类与字号/中性/语义 scale
3. 7 个别名解析且无环
4. 57 组 WCAG 对比度 ≥4.5:1
5. `theme.wxss` 与 `demo/theme.css` 新鲜度、64 个 TDesign 消费变量
6. Figma 74 个变量名称 1:1
7. demo 使用的 42 个主题变量全部已定义
8. 对比度文档行数与无 FAIL

补充证据：两轮从零重建；3/3 变异演练（改中性色、删品牌映射、改 Figma 名称）均被闸门捕获，日志见 `artifacts/reverse-drill.log`；在线 Figma 导出快照由 `verify_figma_export.py` 校验 74/74，结果见 `evidence/figma-online/verify.json`。

## 已知限制

- Figma 使用免费版：在线文件、变量与共享链接可用；匿名查看者不显示 Variables 编辑面板，变量证据以登录态截图与导出快照为准。不提供暗色模式/多品牌切换。
- 在线 Figma 是手工导入的交付物；`tokens.json` 变更后需重新导入并更新 `evidence/figma-online`，`verify_figma_export.py` 会拦截过期快照。
- 无微信开发者工具；示例页是 TDesign 变量/组件外观的 Web 预览，不是真机截图。
- Figma 变量名称保留点号，不映射为 `/` 分组；这是为了保证与 `tokens.json` 名称严格 1:1。
- 仅提供 Light 模式；未实现暗色主题、动态字体缩放和多品牌切换。
- 示例页面只覆盖按钮、标签、cell、输入、提示与变量卡，不代表全部 TDesign 组件。
- 截图依赖本机 Edge 与 Playwright；不同浏览器/字体渲染可能导致 PNG 字节不同。

## 目录

```text
repo/
├─ tokens.json
├─ theme.wxss
├─ demo/{index.html,demo.css,theme.css}
├─ figma/{figma-variables.json,figma-import.tokens.json,Light.tokens.json,create-variables.js,manifest.json}
├─ evidence/figma-online/{Theme.zip,Light.tokens.json,verify.json,*.png,README.md}
├─ docs/{CONTRAST.md,FIGMA-VARIABLES.md,FIGMA-ONLINE.md,USAGE.md}
├─ scripts/{build.py,validate.py,verify_figma_export.py,capture.mjs,run_acceptance.py,reverse_drill.py}
├─ tests/test_tokens.py
└─ artifacts/{example-page.png,validation.log,ACCEPTANCE*.md,...}
```

## 数据与安全

- 所有文案、企业名、课程名、数字均为虚构示例。
- 不包含真实客户名、手机号、邮箱、身份证、API Key 或访问令牌。
- 构建/校验/截图均在本地执行；示例页不发起网络请求。
- 交付仓库为 public，仅含虚构数据、源码、生成物与证据；不含客户名、PII、API Key 或访问令牌。

## S2-BRAND 对接

- 上游品牌色变化：只改 `tokens.json`，重跑 `build.py` 与验收，不手改生成物。
- 下游小程序：引入 `theme.wxss`，按 `--td-*` 变量使用 TDesign。
- 下游 Figma：直接使用在线文件，或导入 `figma/Light.tokens.json`；设计稿绑定同名变量。
- Figma 在线文件与导入快照是交付物的一部分；令牌变化后重导入、重导出、重跑 `verify_figma_export.py`，不手改变量。