# #1835【S3-BRAND-001】小程序主题设计变量与 TDesign 主题映射 · 理解与范围

更新时间：2026-11-19 21:36（Asia/Shanghai）
状态：v1 已于 2026-11-19T10:46:33Z 提交（submitted，rework_count=0）；rework-v2 已完成实现、两轮验收、变异、安全修复与 GitHub 仓库/Release 交付，等平台 rework 或用户明确指示；未重复提交。

## 1. 平台事实

| 项 | 值 |
| --- | --- |
| 任务 | #1835【S3-BRAND-001】会员空间平台 · 小程序主题设计变量与 TDesign 主题映射 |
| 报价 / 托管 | 7000 USD / escrow funded |
| 归属 | agent 1688（craftmesh-v7.env），assigned_to_me=true |
| 平台状态 | submitted（2026-11-19T10:46:33Z），assigned_to_me=true，escrow funded，latest_delivery_version=1，rework_count=0；v2 待平台 rework 后提交 |
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
3. Figma 同名变量集合：交付可导入变量 JSON、Figma 开发插件（manifest + 脚本）与一一对照表；本机无 Figma 账号与 Token，无法直接生成 Figma 链接，文档明确限制。
4. 对比度检查表：所有正文文字组合 ≥ 4.5:1；附计算口径与结果。
5. TDesign 组件示例页截图：按钮、标签、单元格、输入框、提示等使用新品牌色。
6. 使用说明：如何替换品牌色、如何新增 token、如何导入 Figma、如何验证。

## 3. 验收对照（实际证据）

| AC | 原文 | 交付证据 |
| --- | --- | --- |
| AC1 | tokens.json 通过 W3C Design Tokens 格式校验 | `scripts/validate.py` 检查 1（74 token、类型/值/别名）；`tests/test_tokens.py::test_token_index_has_74_valid_tokens`；`artifacts/validation.log` |
| AC2 | 对比度检查表中所有正文文字组合 ≥ 4.5:1 | `docs/CONTRAST.md` 57 组，最低 4.66:1；`scripts/validate.py` 检查 4；`tests/test_tokens.py::test_all_57_body_text_pairs_meet_wcag_aa` |
| AC3 | theme.wxss 应用到 TDesign 组件示例页后的截图中按钮、标签使用新品牌色 | `artifacts/example-page.png`（750×2269）；`scripts/capture.mjs` 断言按钮背景/标签文字为 rgb(31,94,255)、标签浅底 rgb(241,244,255)；`tests/test_tokens.py::test_theme_has_64_tdesign_consumed_variables_and_is_fresh`、`test_browser_preview_is_same_theme_at_2x` |
| AC4 | Figma 变量名与 tokens.json 中的名称一一对应（对照表） | `figma/figma-variables.json` 74 个；`figma/create-variables.js` + `figma/manifest.json`；`docs/FIGMA-VARIABLES.md` 74 行；`scripts/validate.py` 检查 6；`tests/test_tokens.py::test_figma_variables_are_exactly_1_to_1`、`test_figma_plugin_and_doc_cover_every_token` |

## 4. 设计边界与假设

- 色彩：品牌主色、辅助色；中性色 10 阶；成功/警告/错误/信息四种语义色；文字、背景、边框、焦点环。
- 字号：24 / 28 / 32 / 36 / 40 / 48 rpx 六档，每档对应行高；字重 400/500/600。
- 圆角：8 / 16 / 24 rpx 与全圆；间距：16 / 24 / 32 / 48 / 64 rpx。
- 阴影 3 级；动效 fast/base/moderate/slow 四档时长与 standard/emphasized/decelerate/accelerate 四条缓动。
- 单位：小程序使用 rpx；Figma 变量使用 2rpx = 1px 的换算值（375pt 视口），在变量描述与 README 中注明。
- 命名：tokens 使用点分路径（如 color.brand.primary），Figma 变量名完全一致（点号保留，不转成“/”分组），TDesign 变量映射表显式列出。
- S2-BRAND 对接：当前品牌色是占位值；替换 tokens.json 中 color.brand.* 后重新运行 scripts/build.py 即可生成新的 theme.wxss 与 Figma 变量。README/USAGE 写明对接字段。

## 5. Top 5 风险（含实际处置）

| 风险 | 影响 | 应对与实际结果 |
| --- | --- | --- |
| 无 Figma 账号/Token，无法生成 Figma 链接 | AC4 交付形态受限 | 交付可导入变量 JSON + Figma 插件（manifest + 脚本）+ 1:1 对照表；README/SUBMISSION 明确限制，不用虚假链接。已完成。 |
| 对比度只算主色，漏语义色/浅底组合 | AC2 不达标 | 脚本枚举 57 组正文组合并断言；最低 4.66:1。已完成。 |
| theme.wxss 手写与 tokens 漂移 | AC3/维护性 | theme.wxss 由 build.py 生成；validate.py 比对新鲜度；两轮从零重建哈希一致。已完成。 |
| Figma 变量名与 token 路径不一致 | AC4 不达标 | 生成器统一从 token 路径取名；校验 1:1 与数量；插件语法 `node --check` 通过。已完成。 |
| 示例页只是网页，不是微信开发者工具 | AC3 说服力 | 用 TDesign 变量名与组件外观的 Web 预览，截图 + 声明不是真机截图；README 与证据都写清。已完成。 |

## 6. Out of Scope

- 不修改 S2-BRAND 源文件；不交付标志/字体授权。
- 不实现小程序业务页面、不接后端、不做登录。
- 不发布 Figma 文件到 Community；不购买字体。
- 不引入境外 SDK；不采集任何真实用户数据。

## 7. Definition of Done

- [x] tokens.json 通过结构、类型、别名、必填分类校验。
- [x] 对比度表全部正文组合 ≥ 4.5:1，且有计算脚本。
- [x] theme.wxss 覆盖品牌色/语义色/文字/背景/圆角/字号/阴影/动效变量，且由 token 生成。
- [x] 示例页截图可见按钮、标签使用品牌色，并有计算样式与 PNG 尺寸断言。
- [x] Figma 变量名与 token 路径 1:1，附对照表、插件与导入清单。
- [x] build 幂等、两轮从零演练、变异演练（3/3 DETECTED）。
- [x] README/USAGE 完整、可复现。
- [x] v2 交付包已发布到 GitHub Releases 并回验（343,925 B；SHA-256 24e6348c…；https://github.com/Gupeat/memberspace-brand-theme-1835/releases/tag/v2.0.0）。
- [x] 用户 2026-11-19 明确批准后提交；提交后绝不重复提交。