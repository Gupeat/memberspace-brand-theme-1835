# #1835 实施计划

更新时间：2026-11-20 11:56（Asia/Shanghai）
状态：v1 已于 2026-11-19T10:46:33Z 提交；rework-v2 已把 theme 变量从 68 收敛到 64，完成两轮验收、变异、安全修复、在线 Figma 变量交付、微信开发者工具真实截图与 GitHub Release v2.2.0，未重复提交。

## 1. 里程碑

| 里程碑 | 内容 | 验收方式 | 状态 |
| --- | --- | --- | --- |
| M0 | 任务深读、00/01/02、目录 | 文档齐 | ✅ |
| M1 | token 体系：色彩/字号/圆角/间距/阴影/动效 | tokens.json 74 token、7 别名、DTCG 校验通过 | ✅ |
| M2 | theme.wxss 生成器与 TDesign 变量映射 | 64 个 TDesign 消费变量，重新生成逐字节一致 | ✅ |
| M3 | 示例页与截图 | 750×2269 截图；按钮/标签计算样式与 PNG 尺寸断言 | ✅ |
| M4 | Figma 变量 JSON、插件、1:1 对照表 | 74 名称完全相等；node --check 通过 | ✅ |
| M5 | 对比度、测试、两轮、变异、README/USAGE | 16 tests；8/8；两轮（7 步）；3/3 变异 | ✅ |
| M6 | 在线 Figma、微信 DevTools、交付包、提交正文、WorkStatus | 在线 74/74；DevTools 18/18；包校验 + 用户批准后提交 | v1 已于 2026-11-19T10:46:33Z 提交；v2.2.0 已发布 GitHub Release、在线 Figma 与 DevTools 截图，等待用户审核批准 |

## 2. 依赖图

M0 -> M1 -> M2 -> M3 -> M4 -> M5 -> M6

- M2 依赖 token 结构与命名；M3 依赖 theme.wxss；M4 依赖 token 路径；M5 依赖全部实现；M6 依赖验收证据。
- 对比度计算在 M1 后即可跑，但作为 M5 的硬门禁。

## 3. 模块边界

| 模块 | 文件 | 职责 | 不负责 |
| --- | --- | --- | --- |
| token 源 | tokens.json | 唯一事实源；W3C 结构 | 不写 CSS、不写 Figma |
| 构建 | scripts/build.py | 解析 alias，生成 theme.wxss/figma JSON/插件/对比度表/对照表 | 不修改 token 值 |
| 校验 | scripts/validate.py | 结构/类型/别名/对比度/映射/1:1/新鲜度 | 不生成产物 |
| 示例页 | demo/ | 用 theme 变量渲染 TDesign 风格组件 | 不实现业务逻辑 |
| Figma | figma/ + evidence/figma-online/ | 在线文件、导入 DTCG、Plugin API 脚本、导出快照与校验 | 不伪造变量或链接 |
| 测试 | tests/ | 固化上述断言 | 不做视觉主观判断 |
| 验收 | scripts/run_acceptance.py | 清空生成物、跑 7 步、写日志与证据 | 不修改业务源码 |

## 4. 验证计划（实际执行）

1. W3C 结构：每个叶子有 $value；$type 合法；dimension/duration 用 {value,unit}；color 用 #RRGGBB；shadow 字段齐。
2. 必填分类：品牌主/辅色、中性 10 阶、4 语义色、6 字号、4 圆角、5 间距、3 阴影、3 时长、2 缓动。
3. alias：7 个别名全部可解析；无环；引用存在。
4. 对比度：57 组正文组合，逐条 WCAG 2.1；最低 4.66:1。
5. theme.wxss：由 build.py 生成；重新生成逐字节一致；64 个变量均可追溯到 token。
6. 示例页：Edge headless 截图 750×2269；按钮背景/标签文字为品牌主色；标签浅底为品牌浅色；PNG 宽 750 且高≥1500。
7. Figma：figma-variables.json 的变量名集合 == token 路径集合；74 个；导入 DTCG 74 个；在线文件 74 个；导出快照 verify 74/74；插件按同名创建；manifest 可导入。
8. 两轮从零：删除生成物后重新 build+figma-syntax+validate+pytest+verify-figma+capture；两轮均通过，关键哈希稳定。
9. 变异：改中性色、删品牌映射、改 Figma 名称，对应校验必须失败（3/3）。
10. 单测：15 项 pytest 覆盖上述硬门禁。

## 5. 验收对照

| AC | 命令/证据 | 结果 |
| --- | --- | --- |
| AC1 | `python scripts/validate.py` 检查 1；`pytest tests/test_tokens.py::test_token_index_has_74_valid_tokens` | PASS |
| AC2 | `docs/CONTRAST.md` 57 组；`pytest ...test_all_57_body_text_pairs_meet_wcag_aa` | PASS，min 4.66:1 |
| AC3 | `node scripts/capture.mjs`；`artifacts/example-page.png`；计算样式断言 | PASS，750×2269 |
| AC4 | 在线 Figma 74 变量；`evidence/figma-online/verify.json`；`figma/figma-variables.json`；`docs/FIGMA-VARIABLES.md`；`pytest ...test_figma_variables_are_exactly_1_to_1` | PASS，74/74 |

## 6. 冗余与降级

- 生成物可重建：tokens.json 是唯一源；theme.wxss/figma JSON/CONTRAST 全部由 build.py 生成。
- 截图失败不影响 token 校验；AC3 必须有截图，capture 失败即验收失败，不伪造。
- Figma 免费版：在线变量与共享链接可用；匿名查看者无 Variables 编辑面板，变量证据以登录态截图与导出快照为准。
- 无微信开发者工具：用 TDesign 变量名与外观的 Web 预览；README 注明不是真机截图。
- 字体不可用：回退 PingFang SC / Microsoft YaHei / sans-serif；不下载字体。
- 本机路径：验收日志统一替换为 `<home>`，避免泄露用户名。

## 7. 时间检查点

- 2026-11-19 13:25：M0–M2 完成。
- 2026-11-19 18:20：TDesign 映射返工；当时 68 个映射、57 组对比度、14 tests、两轮与 3/3 变异完成。
- 2026-11-19 18:26：M6 文档/证据更新。
- 2026-11-19 21:40：修复 Figma 插件破坏性删除与公共托管两项 safety blocker；改为 GitHub 仓库 + Release 交付。
- 2026-11-19 18:46：经用户明确批准提交；平台 status=submitted、assigned_to_me=true；WorkStatus submitted。
- 2026-11-19 21:20 起：rework-v2，移除 4 个 TDesign 1.18.0 未消费映射，theme 变量 68→64。
- 2026-11-19 22:55–23:20：在线 Figma 导入 74 变量（collection Theme / mode Light），导出快照并校验 74/74；新增 figma-import.tokens.json 生成与第 15 个测试。
- 2026-11-20 11:20–11:40：新增微信开发者工具真实截图与 verify_devtools_evidence.py（18/18）、miniprogram-demo 主题同源测试（第 16 个测试）；两轮 7 步验收（round1 03:40:14Z、round2 03:40:22Z）均 exit 0；16 tests、8/8、Figma 74/74、DevTools 18/18。
- 2026-11-20 11:47：GitHub Release v2.2.0 与资产上传、下载回验完成（1,954,726 B，SHA-256 12375a15…8156）。
- 提交必须用户当轮明确批准；本单不自动提交。