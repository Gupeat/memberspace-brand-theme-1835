# #1835 提交材料（rework v2.2.0）

- 任务：#1835【S3-BRAND-001】小程序主题设计变量与 TDesign 主题映射
- 金额：7000 USD；agent 1688（craftmesh-v7.env）
- 状态：v1 已于 2026-11-19T10:46:33.421669Z 提交；平台随后 request-rework（rework_count=1）。rework v2.2.0 已完成实现、微信开发者工具真实截图、在线 Figma、两轮 7 步验收、证据与文档；**尚未提交**，等待用户审核与明确批准。
- 更新时间：2026-11-20 11:35（Asia/Shanghai）

## 1. rework v2.2.0 相对 v1 的修改

1. 新增微信开发者工具真实运行证据：miniprogram-demo 使用 t-button / t-tag，app.wxss 引入生成的 theme.wxss；DevTools 2.02.2609250 Stable、沙箱 AppID wx65dda5a642890a95、libVersion 3.4.10；模拟器与完整 IDE 两张截图；verify_devtools_evidence.py 18/18 PASS。
2. theme.wxss 从 68 收敛到 64 个 TDesign 1.18.0 实际消费变量：移除 --td-line-height、--td-anim-duration-moderate、--td-anim-duration-slow、--td-anim-time-fn-ease-in；对应 token 保留。
3. 在线 Figma 文件：collection Theme、mode Light、74 变量、Anyone can edit；可导入 DTCG（figma-import.tokens.json / Light.tokens.json，74 项，字节相同）；verify_figma_export.py 74/74 校验。
4. 测试从 14 增至 16；新增 miniprogram theme 同源测试与 DevTools 证据校验；验收从 6 步扩展到 7 步。
5. Figma 插件保持非破坏性：不删除任何既有变量，类型冲突跳过，未匹配变量保留并提示。
6. 交付通道为 GitHub 公开仓库 + Release 资产，不使用 filebin；包内不含 project-docs，避免包 SHA 与文档互相引用。

## 2. 交付清单

1. repo/tokens.json：74 个 W3C DTCG token，7 个别名，覆盖色彩/字号/行高/字重/圆角/间距/阴影/动效。
2. repo/theme.wxss：64 个 TDesign 1.18.0 实际消费的 CSS 变量，选择器 page, .td-theme。
3. repo/figma/figma-variables.json：74 个 Figma 变量，名称与 tokens.json 1:1。
4. repo/figma/figma-import.tokens.json + Light.tokens.json：Figma Variables 可直接导入的嵌套 DTCG（74 项，字节相同）。
5. repo/figma/create-variables.js + manifest.json：非破坏性 Figma Plugin API 导入脚本。
6. repo/evidence/figma-online/：在线 Figma 导出快照、verify.json、登录态/共享/匿名截图与 README。
7. repo/evidence/devtools/：真实微信开发者工具截图、run.json（版本/AppID/页面/截图哈希/计算样式）、verify.json（18/18）。
8. repo/miniprogram-demo/：可直接在 DevTools 打开的最小 TDesign 小程序（t-button / t-tag，引用生成的 theme.wxss）。
9. repo/docs/FIGMA-VARIABLES.md：74 行 1:1 对照表；docs/FIGMA-ONLINE.md、docs/WECHAT-DEVTOOLS.md、docs/USAGE.md。
10. repo/docs/CONTRAST.md：57 组对比度，全部 ≥4.5:1，最小 4.66:1。
11. repo/demo/ + repo/artifacts/example-page.png：完整 TDesign 风格 Web 预览，750×2269。
12. repo/tests/test_tokens.py + scripts/validate.py + verify_figma_export.py + verify_devtools_evidence.py：16 tests、8/8 校验、Figma 74/74、DevTools 18/18。
13. repo/artifacts/acceptance-round1.log、round2.log、ACCEPTANCE-*.md：两轮 7 步从零验收。
14. repo/artifacts/reverse-drill.log：3/3 变异命中。
15. 项目文档 00/01/02/03/STATUS；本文件与 submission-solution-v2.txt；GitHub 仓库 project-docs/ 同版存档。
16. GitHub Release v2.2.0 与归档 zip（见第 6 节）。

## 3. rework 六项逐条答复

| # | 平台要求 | 交付与证据 |
| --- | --- | --- |
| 1 [blocker] | GitHub 仓库或 PR，README 写运行/测试，包含 tokens、theme、校验脚本、demo、文档 | https://github.com/Gupeat/memberspace-brand-theme-1835（public，可直接克隆）；README「快速开始」7 条命令；tokens.json、theme.wxss、scripts/、miniprogram-demo/、demo/、docs/ 全部在仓库 |
| 2 [blocker] | Figma 变量集合链接，实际建立与 tokens.json 同名变量 | https://www.figma.com/design/U3n0qOCgViDDfdSnOWIw5n/MemberSpace-Brand-Theme-1835---v2?node-id=0-1；collection Theme / mode Light / 74 变量 / Anyone can edit；evidence/figma-online/verify.json 74/74 |
| 3 [major] | theme.wxss 应用到 TDesign 小程序组件的截图，必须在微信开发者工具或真机中截取 | evidence/devtools/miniprogram-simulator.png（488×941，仅模拟器）与 miniprogram-devtools.png（1564×1250，完整 IDE）；run.json 记录 DevTools 2.02.2609250、页面 pages/index/index；verify.json 18/18；README 与 docs/WECHAT-DEVTOOLS.md 引用 |
| 4 [major] | Figma 变量名与 tokens.json 一一对应，且与 Figma 文件实际一致 | docs/FIGMA-VARIABLES.md 74 行；figma/figma-variables.json 74 个；evidence/figma-online/verify.json 74/74（名称/类型/别名/值/描述） |
| 5 [major] | tokens.json 通过 W3C DTCG 校验，提交校验脚本与输出 | scripts/validate.py 第 1 项 DTCG；artifacts/validation.log、validation.json（8/8 PASS）；pytest test_token_index_has_74_valid_tokens |
| 6 [minor] | 对比度检查表所有正文组合 ≥4.5:1，完整表含前景/背景/比值/用途 | docs/CONTRAST.md 57 组（前景、背景、比值、用途），最小 4.66:1；validate.py 第 4/8 项；pytest test_all_57_body_text_pairs_meet_wcag_aa |

## 4. 客户 AC 逐条对照

| 编号 | 客户验收标准 | 结果 | 证据 |
| --- | --- | --- | --- |
| AC1 | tokens.json 通过 W3C Design Tokens 格式校验 | PASS | validate.py 检查 1；artifacts/validation.log；pytest test_token_index_has_74_valid_tokens |
| AC2 | 对比度检查表所有正文组合 ≥4.5:1 | PASS | docs/CONTRAST.md 57 组，min 4.66:1；validate.py 检查 4；pytest test_all_57_body_text_pairs_meet_wcag_aa |
| AC3 | theme.wxss 应用到 TDesign 组件示例页后按钮/标签使用新品牌色 | PASS | 微信开发者工具真实截图 evidence/devtools/*.png；run.json 计算样式；verify.json 18/18；pytest test_miniprogram_demo_uses_the_generated_theme |
| AC4 | Figma 变量名与 tokens.json 名称一一对应 | PASS | 在线 74 变量；evidence/figma-online/verify.json 74/74；docs/FIGMA-VARIABLES.md 74 行；validate.py 检查 6 |

## 5. 复现命令

在 repo/ 下执行：

    python scripts/build.py
    python scripts/validate.py
    python -m pytest -q tests
    python scripts/verify_figma_export.py
    python scripts/verify_devtools_evidence.py
    node scripts/capture.mjs
    python scripts/run_acceptance.py --label round1
    python scripts/run_acceptance.py --label round2

## 6. 交付包与 Release

- 本地路径：clawhunt/projects/1835/artifacts/1835-s3-brand-001-rework-v2.2.0.zip
- 仓库：https://github.com/Gupeat/memberspace-brand-theme-1835
- Release：PENDING_RELEASE_URL
- 资产：PENDING_ASSET_URL
- 字节：PENDING_BYTES
- SHA-256：PENDING_SHA
- 包内：repo 源码/生成物/测试/证据（含 miniprogram-demo 与 evidence/devtools）+ README-PACKAGE.txt + MANIFEST.txt；项目文档在 GitHub project-docs/。
- 下载回验：PENDING_VERIFY。

## 7. 平台状态与提交记录

- v1：2026-11-19T10:46:33.421669Z 提交成功；instant_review needs_changes（启发式语义打分）；平台随后 request-rework，rework_count=1、latest_delivery_status=rework_requested。
- v2.2.0：**未提交**。提交必须等用户审核并明确批准；批准后执行：

    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "clawhunt\clawhunt.ps1" submit -ProblemId 1835 -EnvFile "craftmesh-v7.env" -TextFile "clawhunt\projects\1835\submission-solution-v2.txt"

- 提交后 WorkStatus 回写 submitted，记录 submitted_at 与 latest_delivery_version；绝不重复提交。

## 8. 提交检查表（v2.2.0）

- [x] 平台已 request-rework（rework_count=1）
- [x] 16 tests、8/8 校验、Figma 74/74、DevTools 18/18
- [x] 两轮 7 步从零验收、3/3 变异
- [x] 交付包已打包并本地自检
- [ ] 回填包 URL/字节/SHA-256 并下载回验
- [ ] 预检 would_pass=true、defects=[]
- [ ] 用户审核并明确批准
- [ ] 执行 submit 并记录 submitted_at/version
- [ ] 提交后 WorkStatus submitted；绝不重复提交

## 9. 已知限制

- 微信开发者工具截图使用沙箱测试号与模拟器（iPhone 12/13 Pro），不是真机截图；不同 IDE 版本/设备模拟器可能导致 PNG 字节不同。
- Figma 免费版；匿名查看者不显示 Variables 编辑面板，变量证据以登录态截图与导出快照为准。
- miniprogram-demo 只演示 t-button/t-tag 的品牌色、圆角与字号，不代表全部 TDesign 组件。
- 57 组对比度是颜色组合校验，不等同完整 UI 无障碍审计。
- 本机无 git 客户端，GitHub 通过 REST API 提交，不是 git CLI 生成的 PR。
