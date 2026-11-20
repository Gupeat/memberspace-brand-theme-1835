# #1835【S3-BRAND-001】小程序主题设计变量与 TDesign 主题映射 · 理解与范围

更新时间：2026-11-20 20:10（Asia/Shanghai）
状态：v1 已于 2026-11-19T10:46:33Z 提交；平台随后要求 rework（rework_count=1，latest_delivery_status=rework_requested）。v2.3.0 已完成严格 DTCG 修复、TDesign 语义浅底与组合字体映射、Figma 显示名统一、62 组对比度、23 项 DevTools 证据、两轮 7 步验收；交付包已生成并自检（1,959,220 B，SHA-256 3544c2d0…），源码已推送 GitHub（源码 commit 2da1d8e…；project-docs 已同步到 main 分支），GitHub Release v2.3.0 与下载回验完成；solution precheck 已执行（deterministic checks passed、defects=[]，LLM critic outage、would_pass=null，待重试）；**尚未提交**，等待用户审核与明确批准。

## 1. 平台事实

| 项 | 值 |
| --- | --- |
| 任务 | #1835【S3-BRAND-001】会员空间平台 · 小程序主题设计变量与 TDesign 主题映射 |
| 报价 / 托管 | 7000 USD / escrow funded |
| 归属 | agent 1688（craftmesh-v7.env），assigned_to_me=true |
| 平台状态 | v1 submitted（2026-11-19T10:46:33Z）；rework_count=1；latest_delivery_status=rework_requested；v2.3.0 待用户批准后提交 |
| 交付截止 | 2026-12-14T15:59:59Z |
| 开工期限 | 2026-11-22T01:07:49Z |
| 交付通道 | platform_only |
| 阶段 | Stage iii 业务框架与小程序 · 小程序视觉主题 |
| 依赖 | S2-BRAND（品牌标志与规范）；本机无 S2-BRAND 交付物，按任务给的色系范围自建可替换的虚构品牌 token，并在 README 写明对接点 |
| 数据 | 全部虚构；占位品牌名「会员空间平台」；无客户名、无真实 PII |

## 2. 任务范围

做一个设计变量层，不是做完整小程序页面：

1. tokens.json：W3C Design Tokens（DTCG）格式，覆盖色彩、字体字号/行高/字重、圆角、间距、阴影、动效。
2. theme.wxss：把 token 映射为 TDesign 小程序组件的 CSS 变量。
3. Figma 同名变量集合：交付在线 Figma 文件（collection Theme / mode Light / 74 变量、Anyone can edit）、可直接导入的 DTCG 文件、Figma 开发插件（manifest + 脚本）与一一对照表；匿名查看者不显示 Variables 编辑面板，属 Figma 权限设计。
4. 对比度检查表：所有正文文字组合 ≥ 4.5:1；附计算口径与结果。
5. TDesign 组件示例页截图：按钮、标签使用新品牌色；真实微信开发者工具截图，不是 Web 伪造。
6. 使用说明：如何替换品牌色、如何新增 token、如何导入 Figma、如何验证。

## 3. 验收对照（实际证据）

| AC | 原文 | 交付证据 |
| --- | --- | --- |
| AC1 | tokens.json 通过 W3C Design Tokens 格式校验 | 严格 DTCG：38 个 color 为 `{colorSpace,components,hex}` 对象；21 个 dimension 为 px；3 个 shadow 为复合对象。`scripts/validate.py` 检查 1（74 token、类型/值/别名）；`tests/test_tokens.py::test_tokens_use_strict_dtcg_value_shapes`、`test_token_index_has_74_valid_tokens`；`artifacts/validation.log` |
| AC2 | 对比度检查表中所有正文文字组合 ≥ 4.5:1 | `docs/CONTRAST.md` 62 组，最低 4.66:1；`scripts/validate.py` 检查 4；`tests/test_tokens.py::test_all_62_body_text_pairs_meet_wcag_aa` |
| AC3 | theme.wxss 应用到 TDesign 组件示例页后的截图中按钮、标签使用新品牌色 | `artifacts/example-page.png`（750×2261）；`scripts/capture.mjs` 断言按钮背景/标签文字为 rgb(31,94,255)、标签浅底 rgb(241,244,255)；真实 DevTools 证据 `evidence/devtools/`（button/tag 计算样式、语义浅底、字号），23 项校验；`test_miniprogram_demo_uses_the_generated_theme`、`test_browser_preview_is_same_theme_at_2x` |
| AC4 | Figma 变量名与 tokens.json 中的名称一一对应（对照表） | 在线 Figma 74 变量；`evidence/figma-online/verify.json` 74/74 tokenPath 与 74/74 显示名（`color/brand/primary` 这类 `/` 分组）；`figma/figma-variables.json` 74 个；`figma/create-variables.js` + `figma/manifest.json`；`docs/FIGMA-VARIABLES.md` 74 行；`scripts/validate.py` 检查 6；`test_figma_variables_are_exactly_1_to_1`、`test_figma_plugin_and_doc_cover_every_token`、`test_figma_import_file_is_nested_dtcg_and_matches_tokens` |

## 4. 设计边界与假设

- 色彩：品牌主色、辅助色；中性色 10 阶；成功/警告/错误/信息四种语义色；文字、背景、边框、焦点环。
- 字号：24 / 28 / 32 / 36 / 40 / 48 rpx 六档，每档对应行高；字重 400/500/600。
- 圆角：8 / 16 / 24 rpx 与全圆；间距：16 / 24 / 32 / 48 / 64 rpx。
- 阴影 3 级；动效 fast/base/moderate/slow 四档时长与 standard/emphasized/decelerate/accelerate 四条缓动。
- 单位：tokens.json 使用 DTCG 允许的 px；build.py 按 2rpx = 1px 写成 theme.wxss 的 rpx（375pt 视口），Figma 变量使用 px。
- 命名：tokens 使用嵌套 DTCG，路径用点号（如 color.brand.primary）展示；Figma 显示名使用 `/` 分组（如 color/brand/primary），逐段与点分路径 1:1；对照表同时列出两种形式。
- S2-BRAND 对接：当前品牌色是占位值；替换 tokens.json 中 color.brand.* 后重新运行 scripts/build.py 即可生成新的 theme.wxss 与 Figma 变量。README/USAGE 写明对接字段。

## 5. Top 5 风险（含实际处置）

| 风险 | 影响 | 应对与实际结果 |
| --- | --- | --- |
| 严格 DTCG 校验不通过 | AC1 直接失败 | v2.3.0 把 color 改为 color 对象、dimension 改为 px、shadow 改为复合对象；validate.py 第 1 项按严格类型校验；17 tests 覆盖。已完成。 |
| 语义标签只换文字色、浅底仍是 TDesign 默认 | AC3 只完成一半 | theme.wxss 新增 `--td-tag-success-light-color`/`warning`/`danger`；DevTools 实测背景 #E7F7F0/#FFF4E5/#FEE9E9。已完成。 |
| 只覆盖旧 font-size 别名，组合字体不生效 | 字号阶梯对真实组件无效 | 新增 body/title/headline 的 `--td-font-size-*` 与 `--td-line-height-*`；DevTools 实测 button 16px、tag 12px。已完成。 |
| Figma 显示名与 token 路径字符串不相等 | AC4 被严格客户挑战 | 统一为显示名 `/` 分组 + tokenPath 点分路径；verify_figma_export.py 同时校验 74/74 tokenPath 与 74/74 显示名。已完成。 |
| 示例页只是网页，不是微信开发者工具 | AC3 说服力 | 真实 DevTools 2.02.2609250 + 沙箱 AppID；两张截图、run.json 与 23 项校验；README/docs 注明模拟器不是真机。已完成。 |

## 6. Out of Scope

- 不修改 S2-BRAND 源文件；不交付标志/字体授权。
- 不实现小程序业务页面、不接后端、不做登录。
- 不发布 Figma 文件到 Community；不购买字体。
- 不引入境外 SDK；不采集任何真实用户数据。

## 7. Definition of Done

- [x] tokens.json 通过严格 DTCG 结构、类型、别名、必填分类校验。
- [x] 对比度表 62 组全部正文组合 ≥ 4.5:1，且有计算脚本。
- [x] theme.wxss 覆盖品牌色/语义色/文字/背景/圆角/字号/阴影/动效变量，且由 token 生成。
- [x] 示例页截图可见按钮、标签使用品牌色；DevTools 真实计算样式覆盖语义浅底与字号。
- [x] Figma 显示名与 token 路径 1:1，附对照表、插件与导入清单。
- [x] build 幂等、两轮从零演练、变异演练（3/3 DETECTED）。
- [x] README/USAGE 完整、可复现。
- [x] v2.3.0 交付包已生成并通过 MANIFEST/zip/隐私自检；GitHub Release v2.3.0 已创建，资产下载回验通过（见 03-EVIDENCE E12）。
- [ ] v2.3.0 提交前预检 would_pass=true、defects=[] 并记录。
- [x] v1 经用户 2026-11-19 明确批准后提交；v2.3.0 已按平台 rework 完成，待用户审核与明确批准，不重复提交。
