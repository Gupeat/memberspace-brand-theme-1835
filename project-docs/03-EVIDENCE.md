# #1835 证据

- 任务：#1835【S3-BRAND-001】小程序主题设计变量与 TDesign 主题映射
- 金额：7000 USD；agent 1688（craftmesh-v7.env）；assigned_to_me=true；escrow funded；deadline 2026-12-14T15:59:59Z；assignment_deadline 2026-11-22T01:07:49Z；platform_only
- 更新时间：2026-11-19 21:20（Asia/Shanghai）
- 平台状态：v1 已于 2026-11-19T10:46:33.421669Z 提交，status=submitted、latest_delivery_version=1、rework_count=0；本文件记录 v2 返工与本地证据，未重复提交。

## E1 环境

- Windows；Python 3.12.14（bundled），Pillow 12.3.0；Node v24.21.0；Microsoft Edge headless；playwright-core 1.65.1。
- 无 Figma 账号/Token、无微信开发者工具、无 git/docker；因此不伪造 Figma 链接或真机截图，交付可导入 JSON、Figma Plugin API 脚本与 1:1 对照表，示例页为 TDesign 变量/组件外观的 Web 预览（2rpx=1px）。
- 所有数据均为虚构；仓库与文档不含客户名、真实企业、手机号、邮箱或身份证。

## E2 生成

命令（repo 根）：

    python scripts/build.py

退出码 0，输出：

    {"tokens": 74, "themeVariables": 64, "figmaVariables": 74, "contrastPairs": 57, "minContrast": 4.66, "tokensHash": "63972f37c08d0e6a28b88579a8e0880503ce0c43770b7fdf12f2e7f89fe3f6ef"}

生成物：tokens.json（74 token；color 38、font 16、radius 4、space 5、shadow 3、motion 8；7 别名）、theme.wxss（64 个 TDesign 1.18.0 实际消费变量）、demo/theme.css（64+10 个预览扩展，2x 换算）、figma/figma-variables.json（74 变量）、figma/create-variables.js（幂等创建/更新）、docs/CONTRAST.md（57 组）、docs/FIGMA-VARIABLES.md（74 行）。

## E3 校验 8/8

命令：

    python scripts/validate.py

输出摘要（完整日志见 repo/artifacts/validation.log，773 B）：

    [PASS] DTCG structure and value types: 74 tokens; types and values valid
    [PASS] required token categories and scales: 33 required tokens; 6 sizes; 10 neutrals; 4 semantics
    [PASS] alias resolution: 7 aliases resolve without cycles
    [PASS] WCAG contrast >= 4.5:1: 57 pairs, minimum 品牌主色文字 / 品牌浅底 4.66:1
    [PASS] theme.wxss and browser preview freshness: 64 TDesign-consumed variables; 10 documented preview extensions; browser preview is 2x rpx->px
    [PASS] Figma variables 1:1: 74 Figma variables, names exactly equal tokens.json paths
    [PASS] demo references and variables: 42 theme variables used by demo, all defined
    [PASS] contrast documentation: 57 documented pairs, no FAIL

    RESULT: PASS (8/8 checks)

## E4 对比度

- 57 组：4 个正文色 × 11 个浅底 = 44；反白色 × 9 个深底 = 9；品牌链接 × 3；品牌主色文字 / 品牌浅底 = 1。
- 全部 ≥ 4.5:1，最小 4.66:1（品牌主色 #1F5EFF 文字 / 品牌浅底 #F1F4FF）。
- 白色文字 / 品牌主色 #1F5EFF = 5.12:1；正文主色 / 页面底色 12.66:1。
- 明细见 repo/docs/CONTRAST.md（57 行，无 FAIL）。

## E5 单测

命令：

    python -m pytest -q tests

结果：14 passed in 0.22s。覆盖：74 token 计数与类型、64 个 TDesign 消费变量与 THEME_MAP 集合相等、禁止旧非法变量名、theme/demo 与 render 输出逐字节一致、57 组对比度、74 个 Figma 变量 1:1、Figma 插件使用 getLocalVariableCollections/variableCollectionId、demo 42 个变量全部已定义、CONTRAST 57 行、返工 token（brand.disabled、motion.duration.moderate、两个缓动）存在。

## E6 示例页截图

命令：

    node scripts/capture.mjs

结果：repo/artifacts/example-page.png，750×2269，300,034 B，SHA-256 eccf75328d60d6f201e08b872740c786ba4abd3fade4bed05e43d0e8418db23a。

计算样式断言：

- [data-accent=button] 背景 rgb(31, 94, 255)。
- [data-accent=tag] 文字 rgb(31, 94, 255)，背景 rgb(241, 244, 255)，圆角 9999px。
- 字体包含 sans-serif；demo 根宽 750。
- PNG IHDR 宽 750、高 ≥1500。

目视复核：按钮、标签、cell、输入、成功/警告提示、设计变量四行均完整显示，无截断或错位。

## E7 Figma 变量

- figma/figma-variables.json：74 个变量，名称与 tokens.json 路径严格 1:1。
- figma/create-variables.js：Figma Plugin API 脚本，按集合创建/更新同名变量；**不删除集合内已有变量**，类型冲突跳过并提示，未匹配变量保留并报告；Node --check 通过。
- figma/manifest.json：插件清单，可在 Figma 桌面端 Import plugin from manifest 运行。
- docs/FIGMA-VARIABLES.md：74 行 1:1 对照表。
- 限制：本机无 Figma 账号/Token，无法生成在线 Figma 文件链接；交付的是可导入包与脚本，不伪造链接。

## E8 两轮从零验收（rework-v2）

- round1：2026-11-19T13:56:03Z；round2：2026-11-19T13:56:08Z；均 exit 0。
- 每轮 5 步：build、figma-syntax、validate、pytest、capture。
- 两轮均：build 0.12s；validate 0.13s；pytest 0.91–0.93s（14 passed）；capture 2.72–2.78s；截图 750×2269、300,034 B；8/8 PASS。
- 两轮关键哈希完全一致：tokens 63972f37…；theme.wxss 0835f0c0…；demo/theme.css 350cc8d9…；figma-variables 9717a2ab…；CONTRAST 45768f03…；FIGMA-VARIABLES 0acb6395…；截图 eccf7532…。
- 日志：repo/artifacts/acceptance-round1.log（2,458 B）、acceptance-round2.log（2,458 B）；ACCEPTANCE-round1.md、ACCEPTANCE-round2.md（各 2,484 B）。

## E9 变异（反向）演练

脚本：scripts/reverse_drill.py；在临时副本注入 3 类缺陷，验证闸门能发现：

- A：neutral.500 改为 #D5DAE2 → 对比度失败（1.40/1.34）。
- B：删除 --td-brand-color 映射 → demo 变量未定义（6/8 失败）。
- C：重命名 Figma 变量 → 1:1 失败（7/8 失败）。

结果：3/3 DETECTED。日志：repo/artifacts/reverse-drill.log（1,033 B，SHA-256 6a1657ea7cf5ea9dba414b7cfec8c0ed95c3410c09e7ef99b04dd0f0c64fc716）。

## E10 隐私与脱敏

- 验收日志与文档中的本机用户名/目录已替换为 <home>/<tmp>；artifacts 与本文件不再包含用户名、绝对用户目录或系统临时目录路径。
- 全仓扫描手机号、邮箱、身份证号、API 凭据、授权头、访问令牌与口令等敏感模式：0 命中。
- 所有示例数据均为虚构。

## E11 关键文件哈希

| 文件 | 字节 | SHA-256 |
| --- | ---: | --- |
| repo/tokens.json | 10,320 | 63972f37c08d0e6a28b88579a8e0880503ce0c43770b7fdf12f2e7f89fe3f6ef |
| repo/theme.wxss | 2,639 | 0835f0c080c3a48a0d400a37a9822b715e4ee29ad1db033650cccfa503030b28 |
| repo/demo/theme.css | 3,028 | 350cc8d9517a7aa5c461a460bbadce19df45b524452c0533879baa944f7c7339 |
| repo/demo/index.html | 3,833 | fd9fcc1572ffe3e6ffc7368cfbdffb11bf4ec08bb6648938b62fdf0882418662 |
| repo/demo/demo.css | 6,923 | 3feb96901db6498cae02cc466a72e5e5274d721f1ea8991c4586225aafaaff8d |
| repo/figma/figma-variables.json | 15,976 | 9717a2ab957beff8f76deb43f29ad4d14b7ebd32b5baa7b525a069be0f815dfc |
| repo/figma/create-variables.js | 14,825 | 99aff3862f18113a7e33202bdb83573ccc5c4a51e8e33b2b71f4c15870e001cb |
| repo/figma/manifest.json | 137 | a2f0776ffc3b2a6fe2e60732a0b04154d2795de2947c3714c6401afdbeabd037 |
| repo/docs/CONTRAST.md | 4,549 | 45768f03698255463f0c4e1d7b18f1c45abd139d70e857a0c2b7d6e023f999b8 |
| repo/docs/FIGMA-VARIABLES.md | 6,776 | 0acb63953da46d441f1439a06759e6eccbe8b1703cbe8afb7795de8f7c7ef03a |
| repo/docs/USAGE.md | 5,771 | 49617ee53c133ff6397eddc889376f95bb224429d147e5d3cffb4894a699a777 |
| repo/README.md | 10,371 | b0bc3f5334f5dca548faa926f688ce93a8342818117c9c5897cb01135fff752d |
| repo/artifacts/example-page.png | 300,034 | eccf75328d60d6f201e08b872740c786ba4abd3fade4bed05e43d0e8418db23a |
| repo/artifacts/validation.log | 773 | c89f58a93ea048c350f180fb8d12f5b389314d60d9672ea53c8cd25a88861ce8 |
| repo/artifacts/validation.json | 1,407 | af73909011f601d665d2708e38d47f1204624fbec2cada09f8963d288cbf61a5 |
| repo/artifacts/acceptance-round1.log | 2,458 | a1fece4fc81842dadbde1b248c8b2d5ef3c73b579afd4324be317ddeafc8a3ba |
| repo/artifacts/acceptance-round2.log | 2,458 | 1e295b724cf4e937309dde22ad44b74964c1732ea34b64d5fac42c384b58cf41 |
| repo/artifacts/ACCEPTANCE-round1.md | 2,484 | 9c0ea686df0fbf2d6ca0ee5d3e61f592ce982bb1c674ce51d68ab54290d37d14 |
| repo/artifacts/ACCEPTANCE-round2.md | 2,484 | cc393388a6bacea62a777adf59c8bf1463641b49d292ea8c6aada72eb410affd |
| repo/artifacts/reverse-drill.log | 1,033 | 6a1657ea7cf5ea9dba414b7cfec8c0ed95c3410c09e7ef99b04dd0f0c64fc716 |
| repo/tests/test_tokens.py | 5,627 | f79b2c93dec411ca1af3193e24fbb0373b1176de86a051f9843283736117e3b3 |
| repo/scripts/build.py | 20,107 | c9d34b5a9926cc1883938d083b7b7626dc12a6cd7f3eb5aed13acb214aa19262 |
| repo/scripts/validate.py | 14,465 | 526cda0fc91cd5dbf67da0ae64b5ab4546012785fba1bdd7309763a9ae6b778b |
| repo/scripts/capture.mjs | 3,371 | 76f2b7e6f319b89f41aff9350dd96f97cb16fc28a73ea3174a60cbb946a26b4b |
| repo/scripts/run_acceptance.py | 6,998 | e7f53a3f06b2725bf333e2713e83f4b16603ddef00cb6f8eb49d2ead4dcb6fe8 |
| repo/scripts/reverse_drill.py | 4,124 | f622b3ebb7f41f4d2dc0b026ea62cbdcba7bed50ae1222c44c09bc6f6e5b9965 |

以上哈希均由最终工作树（2026-11-19 21:55 之后）重新计算；README/create-variables.js/build.py/test_tokens.py 的旧值已刷新。

## E12 交付包（rework-v2，GitHub Release）

- 本地路径：clawhunt/projects/1835/artifacts/1835-s3-brand-001-rework-v2.zip
- 字节数：343,925 B
- SHA-256：24e6348c7c8b379ed5aa4191de1199725e2b6883a743883ab67fa88ef8ec60e2
- 仓库：https://github.com/Gupeat/memberspace-brand-theme-1835
- Release：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/tag/v2.0.0
- 资产：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/download/v2.0.0/1835-s3-brand-001-rework-v2.zip
- 内容：30 个条目（repo 下 28 个源码/生成物/证据文件 + README-PACKAGE.txt + MANIFEST.txt）；MANIFEST 29 个文件逐一 SHA-256/字节匹配；testzip 无错误；无缓存、依赖目录、临时文件或 v1 zip。
- 可重复性：固定 ZipInfo 时间戳；同一工作树连续两次打包字节与 SHA-256 相同。
- 回验：本地重新读取 343,925 B，SHA-256 与上表一致；GitHub 上传后再次下载核对。
- 隐私扫描：包内文本 0 命中用户名、用户目录、系统临时目录、手机号、邮箱、身份证号、API 凭据、授权头、访问令牌、口令。
- 说明：zip 只包含 repo 内容；项目文档（00/01/02/03/STATUS/task-1835.json）在 GitHub 仓库的 project-docs/ 下，不放进 zip，避免包内文档快照与最终 SHA 互相引用。

## E13 限制与边界

- 无 Figma 账号/Token：不能生成在线 Figma 链接；交付 JSON、Plugin API 脚本、manifest 与 1:1 表。若验收方要求在线链接，需要用户提供 Figma 账号/Token。
- 无微信开发者工具：示例页截图是 Web 预览（2rpx=1px），不是微信小程序真机截图；变量映射与组件外观已按 TDesign 小程序官方变量名核对。
- color.semantic.info 保留在 tokens.json，但 TDesign 小程序官方变量集无独立 info 变量，未伪造映射；业务可直接使用该 token。
- 交付形态为 GitHub 公开仓库 + Release 资产 + SHA-256；本机无 git 客户端，使用 GitHub REST API 提交。
- 交付仓库为 public，仅含虚构数据、源码、生成物与证据；不含客户名、PII、API Key 或访问令牌。
- 57 组对比度是颜色组合校验，不等同于完整 UI 无障碍审计。
- TDesign 1.18.0 核对：rework-v2 已将映射收敛为 64 个实际消费变量；--td-line-height、--td-anim-duration-moderate、--td-anim-duration-slow、--td-anim-time-fn-ease-in 已从 theme 映射移除，但对应 token 仍保留，供业务样式或未来版本使用。

## E14 提交记录（v1，已发生）

- 提交时间：2026-11-19T10:46:33.421669Z；agent 1688（craftmesh-v7.env）；ProblemId 1835。
- 命令：powershell.exe -NoProfile -ExecutionPolicy Bypass -File "clawhunt\clawhunt.ps1" submit -ProblemId 1835 -EnvFile "craftmesh-v7.env" -TextFile "clawhunt\projects\1835\submission-solution.txt"
- 返回：{"problem_id":1835,"status":"submitted","submitted_at":"2026-11-19T10:46:33.421669","message":"Solution submitted, awaiting review"}
- instant_review：status=needs_changes、passed=false；relevance 0.72、substance 0.94、feasibility 0.67、acceptance 0.14、evidence 0.23；criterion 0.53/0.66/0.50/0.64；elapsed 257ms；model jev-1.13.0；settlement_authorized=false。
- delivery_check：status=checked、read=text_only、repositories=[]；4 条 criteria 均 unclear；relevance/substance/feasibility matched，acceptance unclear，evidence not_matched。
- 说明：instant_review 是启发式语义打分，低分不等于交付无效；提交后不可改写，不为分数反复改写或重提。
- 平台复核：status=submitted、assigned_to_me=true、price=7000、escrow=funded、latest_delivery_status=submitted、latest_delivery_version=1、rework_count=0。
- WorkStatus 已回写 submitted（ok: work_status #1835 -> submitted）。
- submission-solution.txt 为 v1 提交时原文（2,132 字符）；文中末句“当前未提交”是提交前表述，提交事实以本记录与平台状态为准。

## E15 rework-v2 记录

- 2026-11-19 21:20 起：根据用户要求把不完美处修到可交付，完成 rework-v2。
- 修复内容：移除 4 个 TDesign 1.18.0 未消费映射；theme.wxss 68→64；demo/theme.css 68+10→64+10；测试/校验/验收脚本计数同步为 64；README/USAGE/00/01/02 文档口径同步。
- 重新生成并复验：build 74/64/74/57/4.66；validate 8/8；pytest 14 passed；两轮从零（13:56:03Z、13:56:08Z）exit 0；变异 3/3；截图 750×2269/300,034 B，哈希不变。
- 安全修复：Figma 插件不再删除任何既有变量；类型冲突跳过并提示，未匹配变量保留并报告；测试断言插件不含 .remove()。
- 交付方式：由 filebin 公共主机改为 GitHub 公开仓库 + Release 资产；仓库只含虚构数据、源码与证据。
- 平台状态未变：submitted、rework_count=0。平台没有修改已提交 solution_text 的接口；v2 包与正文已备，等待平台 request-rework 或用户明确指示后提交；未执行重复提交。

## E16 提交前预检（dry-run）

- 预检命令（只读，不提交）：POST https://clawhunt.store/api/v1/problems/1835/solution/precheck，body = submission-solution-v2.txt 全文 + assets（GitHub 仓库 + Release 资产）。
- 结果（2026-11-19T14:10Z 左右，HTTP 200，耗时 88,054 ms）：
  - `would_pass=true`
  - `defects=[]`
  - `critic.passed=true`、`critic.score=7`、`blocked_by=[]`、reason="passed adversarial critique"
  - note="dry-run only — nothing was submitted; the formal review may still differ"
- 原始响应：repo/artifacts/precheck-v2.json。
- 历史失败已修复：旧版正文 + filebin/data URI 方案被 safety critic 拦截（破坏性插件删除、公共匿名托管、data URI 超 500 字符、无可检查仓库导致 correctness/reproducibility fail）；v2 已改为非破坏性插件 + GitHub 仓库/Release 资产，预检通过。
- 预检结论：PASS（would_pass=true、defects=[]）。仍未提交；等待平台 request-rework 或用户当轮明确指示。
