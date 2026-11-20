# #1835 实施计划

更新时间：2026-11-20 20:35（Asia/Shanghai）
状态：**v2.3.0 已于 2026-11-20T15:04:45.916268Z 提交**（用户当轮明确批准）。v1 于 2026-11-19T10:46:33Z 提交后被要求 rework（rework_count=1）。v2.3.0 已完成严格 DTCG、84 个 TDesign 映射（77 直接消费 + 7 兼容）、语义浅底与组合字体、Figma 显示名统一、62 组对比度、17 tests、23 项 DevTools、两轮验收；包 1,959,220 B / SHA 3544c2d0…，Release v2.3.0 下载回验通过；九次预检 deterministic 通过、defects=[]、critic outage（would_pass=null），已如实披露。平台 status=submitted、latest_delivery_status=submitted；delivery_check=checked（AC1/AC3/AC4 matched、AC2 unclear）。

## 1. 里程碑

| 里程碑 | 内容 | 验收方式 | 状态 |
| --- | --- | --- | --- |
| M0 | 任务深读、00/01/02、目录 | 文档齐 | DONE |
| M1 | token 体系：色彩/字号/圆角/间距/阴影/动效 | tokens.json 74 token、7 别名、严格 DTCG 校验通过 | DONE |
| M2 | theme.wxss 生成器与 TDesign 变量映射 | 84 个映射，77 个被 TDesign 1.18.0 直接消费，7 个兼容；重新生成逐字节一致 | DONE |
| M3 | 示例页与截图 | 750x2261 截图；按钮/标签计算样式与 PNG 尺寸断言 | DONE |
| M4 | Figma 变量 JSON、插件、1:1 对照表 | 74 tokenPath + 74 显示名；node --check 通过 | DONE |
| M5 | 对比度、测试、两轮、变异、README/USAGE | 17 tests；8/8；两轮（7 步）；3/3 变异 | DONE |
| M6 | 在线 Figma、微信 DevTools、交付包、提交正文 | 在线 74/74；DevTools 23/23；包 MANIFEST/隐私/下载回验 | DONE |
| M7 | solution precheck | 九次只读预检；deterministic 通过、defects=[]，critic outage（would_pass=null），如实记录 | DONE |
| M8 | 用户审核、提交、WorkStatus | 用户当轮明确批准后 submit；记录 submitted_at/version | DONE（2026-11-20T15:04:45Z submitted） |

## 2. 依赖图

M0 -> M1 -> M2 -> M3 -> M4 -> M5 -> M6 -> M7 -> M8

- M2 依赖 token 结构与命名；M3 依赖 theme.wxss；M4 依赖 token 路径；M5 依赖全部实现；M6/M7 依赖验收证据；M8 依赖用户明确批准。
- 对比度计算在 M1 后即可跑，但作为 M5 的硬门禁。

## 3. 模块边界

| 模块 | 文件 | 职责 | 不负责 |
| --- | --- | --- | --- |
| token 源 | tokens.json | 唯一事实源；严格 DTCG 结构 | 不写 CSS、不写 Figma |
| 构建 | scripts/build.py | 解析 alias，生成 theme.wxss/figma JSON/插件/对比度表/对照表 | 不修改 token 值 |
| 校验 | scripts/validate.py | 结构/类型/别名/对比度/映射/1:1/新鲜度 | 不生成产物 |
| 示例页 | demo/ | 用 theme 变量渲染 TDesign 风格组件 | 不实现业务逻辑 |
| Figma | figma/ + evidence/figma-online/ | 在线文件、导入 DTCG、Plugin API 脚本、导出快照与校验 | 不伪造变量或链接 |
| 测试 | tests/ | 固化上述断言 | 不做视觉主观判断 |
| 验收 | scripts/run_acceptance.py | 清空生成物、跑 7 步、写日志与证据 | 不修改业务源码 |
| 变异 | scripts/reverse_drill.py | 临时副本注入 3 类缺陷，证明闸门有效 | 不改工作树 |

## 4. 验证计划（实际执行）

1. 严格 DTCG：每个叶子有 $value；$type 合法；color 使用 color 对象（colorSpace/components/hex）；dimension 使用 px；shadow 使用复合对象；duration 使用 {value,unit:"ms"}。
2. 必填分类：品牌主/辅色、中性 10 阶、4 语义色、6 字号、4 圆角、5 间距、3 阴影、3 时长、2 缓动。
3. alias：7 个别名全部可解析；无环；引用存在。
4. 对比度：62 组正文组合，逐条 WCAG 2.1；最低 4.66:1。
5. theme.wxss：由 build.py 生成；重新生成逐字节一致；84 个变量可追溯到 token；77 个直接消费，7 个兼容别名。
6. 示例页：Edge headless 截图 750x2261；按钮背景/标签文字为品牌主色；标签浅底为品牌浅色；PNG 宽 750 且高>=1500。
7. DevTools：真实模拟器截图 488x941 + 完整 IDE 1564x1250；计算样式覆盖 button/tag 品牌色、语义浅底与字号；23 项校验。
8. Figma：figma-variables.json 的 tokenPath 集合 == token 路径集合；74 个；显示名 74 个；导入 DTCG 74 个；在线文件 74 个；导出快照 verify 74/74（tokenPath + display name）；插件按同名创建；manifest 可导入。
9. 两轮从零：删除生成物后重新 build+figma-syntax+validate+pytest+verify-figma+verify-devtools+capture；两轮均通过，关键哈希稳定。
10. 变异：改中性色、删品牌映射、改 Figma 名称，对应校验必须失败（3/3）。
11. 单测：17 项 pytest 覆盖上述硬门禁。

## 5. 验收对照

| AC | 命令/证据 | 结果 |
| --- | --- | --- |
| AC1 | `python scripts/validate.py` 检查 1；`pytest tests/test_tokens.py::test_tokens_use_strict_dtcg_value_shapes` | PASS |
| AC2 | `docs/CONTRAST.md` 62 组；`pytest ...test_all_62_body_text_pairs_meet_wcag_aa` | PASS，min 4.66:1 |
| AC3 | `node scripts/capture.mjs`；`artifacts/example-page.png`；DevTools 23 项；计算样式断言 | PASS，750x2261；button 16px、tag 12px |
| AC4 | 在线 Figma 74 变量；`evidence/figma-online/verify.json`；`figma/figma-variables.json`；`docs/FIGMA-VARIABLES.md`；`pytest ...test_figma_variables_are_exactly_1_to_1` | PASS，74/74 tokenPath + 74/74 显示名 |

## 6. 冗余与降级

- 生成物可重建：tokens.json 是唯一源；theme.wxss/figma JSON/CONTRAST 全部由 build.py 生成。
- 截图失败不影响 token 校验；AC3 必须有截图，capture 失败即验收失败，不伪造。
- Figma 免费版：在线变量与共享链接可用；匿名查看者无 Variables 编辑面板，变量证据以登录态截图与导出快照为准。
- 无微信开发者工具时：Web 预览仍可作为完整示例页补充；但 AC3 以真实 DevTools 证据为准，不用 Web 冒充。
- 字体不可用：回退 PingFang SC / Microsoft YaHei / sans-serif；不下载字体。
- 本机路径：验收日志按 ROOT/HOME 的三种写法替换为 <repo>/<home>，包括 JSON 转义的双反斜杠，避免泄露用户名。

## 7. 时间检查点

- 2026-11-19 13:25：M0-M2 完成。
- 2026-11-19 18:20：TDesign 映射返工；当时 68 个映射、57 组对比度、14 tests（历史值，已被 v2.3.0 取代）。
- 2026-11-19 18:46：经用户明确批准提交 v1；平台 status=submitted、assigned_to_me=true。
- 2026-11-19 21:20 起：rework-v2，移除 4 个 TDesign 1.18.0 未消费映射，theme 变量 68->64（历史值）。
- 2026-11-19 22:55-23:20：在线 Figma 导入 74 变量（collection Theme / mode Light），导出快照并校验 74/74。
- 2026-11-20 11:20-11:40：新增微信开发者工具真实截图与 verify_devtools_evidence.py（18/18，历史）；miniprogram-demo 主题同源测试。
- 2026-11-20 11:47：GitHub Release v2.2.0 与资产上传、下载回验完成（1,954,726 B，SHA-256 12375a15...；历史版本，已被 v2.3.0 取代）。
- 2026-11-20 19:20-20:00：按对抗审核报告修复严格 DTCG、Figma 显示名、tag 语义浅底、组合字体、64 口径、62 对比度；DevTools 重截并扩到 23 项；修复验收日志双反斜杠路径泄露；两轮重跑（round1 11:58:27Z、round2 11:58:32Z）。
- 2026-11-20 20:08：最终两轮重跑（round1 12:08:00Z、round2 12:08:06Z），17/84/62/23/74/8-8 全绿。
- 2026-11-20 20:12：源码推送 GitHub main 15a0869...（初版 v2.3.0 文档/源码）。
- 2026-11-20 20:20：修复 reverse_drill.py 的 DTCG color 变异目标，变异恢复 3/3；重打包 1,959,220 B / 3544c2d0...；源码推送 main 2da1d8e...。
- 2026-11-20 20:30：GitHub Release v2.3.0 创建并上传资产 771731043；下载回验 1,959,220 B / SHA 3544c2d0... 一致。
- 提交必须用户当轮明确批准；本单不自动提交。

## 8. 下一步

1. ~~重试 v2.3.0 solution precheck~~：已九次，critic 持续 outage；用户已明确批准按 deterministic 证据提交。
2. ~~汇报用户并等待批准~~：已完成，用户 23:04 明确批准。
3. ~~批准后 submit~~：已于 2026-11-20T15:04:45Z 提交，status=submitted；不重复提交，等评审。
