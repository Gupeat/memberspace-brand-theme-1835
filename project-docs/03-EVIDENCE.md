# #1835 证据

- 任务：#1835【S3-BRAND-001】小程序主题设计变量与 TDesign 主题映射
- 金额：7000 USD；agent 1688（craftmesh-v7.env）；assigned_to_me=true；escrow funded；deadline 2026-12-14T15:59:59Z；assignment_deadline 2026-11-22T01:07:49Z；platform_only
- 更新时间：2026-11-20 11:25（Asia/Shanghai）
- 平台状态：v1 已于 2026-11-19T10:46:33.421669Z 提交，status=submitted、latest_delivery_version=1、rework_count=0；平台随后要求 rework（rework_count=1），本文件记录 v2.2.0 返工、在线 Figma、微信开发者工具证据与本地证据；未重复提交。

## E1 环境

- Windows；Python 3.12.14（bundled），Pillow 12.3.0；Node v24.21.0；Microsoft Edge headless；playwright-core 1.65.1。
- Figma：已有账号（凭证只在本机 .clawhunt/figma-account.txt，不进仓库/包）；在线文件 collection Theme / mode Light / 74 变量，共享 Anyone can edit；匿名可查看，匿名视图不显示 Variables 编辑面板。
- 微信开发者工具 2.02.2609250 Stable（Windows），沙箱 AppID wx65dda5a642890a95，libVersion 3.4.10；真实模拟器运行见 E18。
- 无 git/docker；GitHub 通过 REST API 提交，不是本地 git/PR；Web 预览仍是 2rpx=1px，仅作完整示例页补充。
- 所有数据均为虚构；仓库与文档不含客户名、真实企业、手机号、邮箱或身份证。

## E2 生成

命令（repo 根）：

    python scripts/build.py

退出码 0，输出：

    {"tokens": 74, "themeVariables": 64, "figmaVariables": 74, "figmaImportVariables": 74, "contrastPairs": 57, "minContrast": 4.66, "tokensHash": "63972f37c08d0e6a28b88579a8e0880503ce0c43770b7fdf12f2e7f89fe3f6ef"}

生成物：tokens.json（74 token；color 38、font 16、radius 4、space 5、shadow 3、motion 8；7 别名）、theme.wxss（64 个 TDesign 1.18.0 实际消费变量）、demo/theme.css（64+10 个预览扩展，2x 换算）、figma/figma-variables.json（74 变量）、figma/figma-import.tokens.json 与 figma/Light.tokens.json（74 项嵌套 DTCG，字节相同）、figma/create-variables.js（非破坏性创建/更新）、docs/CONTRAST.md（57 组）、docs/FIGMA-VARIABLES.md（74 行）。

## E3 校验 8/8

命令：

    python scripts/validate.py

输出摘要（完整日志见 repo/artifacts/validation.log，800 B）：

    [PASS] DTCG structure and value types: 74 tokens; types and values valid
    [PASS] required token categories and scales: 33 required tokens; 6 sizes; 10 neutrals; 4 semantics
    [PASS] alias resolution: 7 aliases resolve without cycles
    [PASS] WCAG contrast >= 4.5:1: 57 pairs, minimum 品牌主色文字 / 品牌浅底 4.66:1
    [PASS] theme.wxss and browser preview freshness: 64 TDesign-consumed variables; 10 documented preview extensions; browser preview is 2x rpx->px
    [PASS] Figma variables 1:1: 74 Figma variables + 74 DTCG import variables, names exactly equal tokens.json paths
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

结果：16 passed in 1.08–1.33s（两轮验收实测）。覆盖：74 token 计数与类型、64 个 TDesign 消费变量与 THEME_MAP 集合相等、禁止旧非法变量名、theme/demo 与 render 输出逐字节一致、57 组对比度、74 个 Figma 变量 1:1、Figma 插件使用 getLocalVariableCollections/variableCollectionId 且不含 .remove()、74 项导入 DTCG 与 tokens 1:1 且 Light 字节一致、别名与描述无截断、demo 42 个变量全部已定义、CONTRAST 57 行、返工 token 存在、miniprogram-demo 主题副本与 @import。

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

## E7 在线 Figma 变量（74/74）

- 在线文件：https://www.figma.com/design/U3n0qOCgViDDfdSnOWIw5n/MemberSpace-Brand-Theme-1835---v2?node-id=0-1
- collection Theme、mode Light、74 变量；分组 color 38（brand 6、accent 2、neutral 10、text 5、bg 4、border 2、semantic 8、focus 1）、font 16、radius 4、space 5、shadow 3、motion 8。
- 导入源：figma/Light.tokens.json（与 figma-import.tokens.json 字节相同，74 项嵌套 DTCG；颜色 sRGB，尺寸 2rpx=1px，duration ms，fontWeight int，别名保留 {path}）。
- 导出快照：evidence/figma-online/Theme.zip 与解包 Light.tokens.json；verify.json 记录 ok=true、checked=74、counts 38/28/8、missing/extra 空、import_fresh=true、light_identical=true。
- 校验脚本：scripts/verify_figma_export.py，将导出快照与 build.render_figma_import(INDEX) 逐项比对名称、类型、别名、值与描述；失败 exit 1。实跑 PASS 74/74。
- 截图：evidence/figma-online/figma-online-final.png（collection Theme 74 / mode Light）、figma-shared-final.png（Anyone can edit）、figma-anon-public.png（匿名可查看）。
- docs/FIGMA-VARIABLES.md：74 行 1:1 对照表；docs/FIGMA-ONLINE.md：导入/导出/匿名限制说明。

## E8 两轮从零验收（v2.2.0）

- round1：2026-11-20T03:19:21Z；round2：2026-11-20T03:19:40Z；均 exit 0。
- 每轮 7 步：build、figma-syntax、validate、pytest、verify-figma、verify-devtools、capture。
- 两轮均：build 0.18/0.15s；figma-syntax 0.14/0.14s；validate 0.17/0.15s；pytest 1.33/1.08s（16 passed）；verify-figma 0.13/0.12s；verify-devtools 0.12/0.12s；capture 3.97/3.39s；8/8 PASS；Figma 74/74；DevTools 18 项；Web 截图 750×2269、300,034 B。
- 两轮关键哈希完全一致：tokens 63972f37…；theme.wxss 与 miniprogram-demo/theme.wxss 均 0835f0c0…；demo/theme.css 350cc8d9…；figma-variables 9717a2ab…；figma-import/Light ebc70a2a…；CONTRAST 45768f03…；FIGMA-VARIABLES 976603e1…；example-page eccf7532…。
- 日志：repo/artifacts/acceptance-round1.log（3,864 B，SHA-256 0ccce1fa55f8b382671ded99bc3a653972fa02fcaeec9ef13246e90258501b60）、acceptance-round2.log（3,864 B，aa29e21c9a31004ea80778210a1df260aafdb02256fd92c1f220ae68894dd0de）；ACCEPTANCE-round2.md / ACCEPTANCE.md（各 3,268 B，7871c97de86944934bb0c07f5f4eec4b75673e69578cc0b0f63d51a35217b813）。

## E9 变异（反向）演练

脚本：scripts/reverse_drill.py；在临时副本注入 3 类缺陷，验证闸门能发现：

- A：neutral.500 改为 #D5DAE2 → 对比度失败（1.40/1.34）。
- B：删除 --td-brand-color 映射 → demo 变量未定义（6/8 失败）。
- C：重命名 Figma 变量 → 1:1 失败（7/8 失败）。

结果：3/3 DETECTED。日志：repo/artifacts/reverse-drill.log（1,033 B，SHA-256 6a1657ea7cf5ea9dba414b7cfec8c0ed95c3410c09e7ef99b04dd0f0c64fc716）。

## E10 隐私与脱敏

- 验收日志与文档中的本机用户名/目录已替换为 <home>/<tmp>；artifacts 与本文件不再包含用户名、绝对用户目录或系统临时目录路径。
- 全仓扫描手机号、邮箱、身份证号、API 凭据、授权头、访问令牌与口令等敏感模式：0 命中。
- Figma 账号凭证只在本机 .clawhunt/figma-account.txt；仓库、包与本文档均不含邮箱或密码。
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
| repo/figma/figma-import.tokens.json | 16,490 | ebc70a2aa0ae018f8907137a3759e96055d35f6c9f40eb490d12438719523029 |
| repo/figma/Light.tokens.json | 16,490 | ebc70a2aa0ae018f8907137a3759e96055d35f6c9f40eb490d12438719523029 |
| repo/figma/create-variables.js | 14,825 | 99aff3862f18113a7e33202bdb83573ccc5c4a51e8e33b2b71f4c15870e001cb |
| repo/figma/manifest.json | 137 | a2f0776ffc3b2a6fe2e60732a0b04154d2795de2947c3714c6401afdbeabd037 |
| repo/docs/CONTRAST.md | 4,549 | 45768f03698255463f0c4e1d7b18f1c45abd139d70e857a0c2b7d6e023f999b8 |
| repo/docs/FIGMA-VARIABLES.md | 7,131 | 976603e1eef0d6e6ec022c94b0f4651a00ad5a0d6e662ed8e7721de3b58c872e |
| repo/docs/FIGMA-ONLINE.md | 3,246 | ef60210e9513699c82672f54f3db5fc1160e5e6eb6ccb9454e8aa71dd0c2d8d4 |
| repo/docs/USAGE.md | 7,062 | 34b69f590c6bfd3b1145cf62541107f99d7935d7c394fe68b0e9488da31298e3 |
| repo/README.md | 12,300 | b0b16027a285d2073915aae7ec40cfbbb4e7117759d260ea2eae66c2c97cb9d7 |
| repo/artifacts/example-page.png | 300,034 | eccf75328d60d6f201e08b872740c786ba4abd3fade4bed05e43d0e8418db23a |
| repo/artifacts/validation.log | 800 | 0b00277faee450e5f3573dc58d3f012390fc99c8dc693d6fb0bd3306077629f2 |
| repo/artifacts/validation.json | 1,434 | 129b90626888f57074a2fceac2a73d733bd86309e7d4d0e64aa4276e84a061ec |
| repo/artifacts/acceptance-round1.log | 2,995 | 516e5a1fe800559e01192b3ff41857457e3865a58e297573fa12f2d6f99c133d |
| repo/artifacts/acceptance-round2.log | 2,995 | 2ca6197269bdca9acf4ef0831345e80176b0b04a5e5631ef63f2ab6403eceacd |
| repo/artifacts/ACCEPTANCE-round1.md | 2,844 | f10effd341a96527cbdf3e5f627db2a8da08a1f36cd11b074de20fd7bb442fa5 |
| repo/artifacts/ACCEPTANCE-round2.md | 2,844 | 70682496d8e82ea3f4062d712f1fc2c508396f48a362ae78f81a8ba2839cbb4f |
| repo/artifacts/ACCEPTANCE.md | 2,844 | 70682496d8e82ea3f4062d712f1fc2c508396f48a362ae78f81a8ba2839cbb4f |
| repo/artifacts/reverse-drill.log | 1,033 | 6a1657ea7cf5ea9dba414b7cfec8c0ed95c3410c09e7ef99b04dd0f0c64fc716 |
| repo/tests/test_tokens.py | 6,195 | f4cc2650325d43f2f5794dec0cb798242db42afaaad3ccd04196e98b3bcf1560 |
| repo/scripts/build.py | 24,181 | 356456361b7a04a45be384dc69de889cdf9170d22904680698a90fe2fb2687e0 |
| repo/scripts/validate.py | 16,078 | f76b6bacbaf506c2496044465e19d36fef818ecfcf98b066ef4b0295baa51fdf |
| repo/scripts/verify_figma_export.py | 5,881 | d1dc9bc2862bb4e53d6a7c631c62dd1f733e02278c0c042d52524051784d7be1 |
| repo/scripts/capture.mjs | 3,371 | 76f2b7e6f319b89f41aff9350dd96f97cb16fc28a73ea3174a60cbb946a26b4b |
| repo/scripts/run_acceptance.py | 7,745 | 9a4d85a83ff69852f91e46ef96a9e4811720f952e44c70f0ed9b655364ffccef |
| repo/scripts/reverse_drill.py | 4,124 | f622b3ebb7f41f4d2dc0b026ea62cbdcba7bed50ae1222c44c09bc6f6e5b9965 |

以上哈希均按 2026-11-19 23:33 最终工作树重新计算；README 在 23:30 改一处 Release 链接后哈希为 b0b16027…。

## E12 交付包（v2.1.0，GitHub Release）

- 仓库：https://github.com/Gupeat/memberspace-brand-theme-1835
- Release：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/tag/v2.1.0
- 资产：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/download/v2.1.0/1835-s3-brand-001-rework-v2.1.0.zip
- 本地路径：clawhunt/projects/1835/artifacts/1835-s3-brand-001-rework-v2.1.0.zip
- 字节数：489,536 B
- SHA-256：8264e580ca09f88c273e6e057d4bca4c85b5269e91ddae0d5e3038750c6f09e2
- 内容：repo 下 40 个源码/生成物/证据文件（含 evidence/figma-online 的 7 个文件）+ README-PACKAGE.txt + MANIFEST.txt，共 42 个条目；排除 node_modules、缓存、临时文件、数据库。项目文档不放入 zip，放在 GitHub 仓库 project-docs/，避免包内文档与包 SHA 互相引用。
- 校验：MANIFEST 逐文件 SHA-256/字节匹配；testzip 无错误；无未列条目；隐私扫描 0 命中；上传后 curl -L 下载回验字节与 SHA-256。

## E13 限制与边界

- Figma 免费版：在线变量与共享链接可用；匿名查看者不显示 Variables 编辑面板，变量证据以登录态截图与导出快照为准。
- 微信开发者工具截图使用沙箱测试号与模拟器（iPhone 12/13 Pro），不是真机截图；不同 IDE 版本、设备模拟器与字体渲染可能导致 PNG 字节不同。
- Web 预览仍是 2rpx=1px，仅作完整示例页补充，不能替代 E18 的 DevTools 证据。
- color.semantic.info 保留在 tokens.json，但 TDesign 小程序官方变量集无独立 info 变量，未伪造映射；业务可直接使用该 token。
- 本机无 git 客户端：使用 GitHub REST API 提交；交付为公开仓库 + Release 资产 + SHA-256，不是 git CLI 生成的 PR。
- 交付仓库为 public，仅含虚构数据、源码、生成物与证据；不含客户名、PII、API Key 或访问令牌。
- 57 组对比度是颜色组合校验，不等同于完整 UI 无障碍审计。
- TDesign 1.18.0 核对：v2 已将映射收敛为 64 个实际消费变量；--td-line-height、--td-anim-duration-moderate、--td-anim-duration-slow、--td-anim-time-fn-ease-in 已从 theme 映射移除，对应 token 仍保留，供业务样式或未来版本使用。

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
- 安全修复：Figma 插件不再删除任何既有变量；类型冲突跳过并提示，未匹配变量保留并报告；测试断言插件不含 .remove()。
- 交付方式：由 filebin 公共主机改为 GitHub 公开仓库 + Release 资产；仓库只含虚构数据、源码与证据。
- 平台状态未变：submitted、rework_count=0。平台没有修改已提交 solution_text 的接口；v2 包与正文已备，等待平台 request-rework 或用户明确指示后提交；未执行重复提交。

## E16 提交前预检（v2，历史）

- 预检命令（只读，不提交）：POST https://clawhunt.store/api/v1/problems/1835/solution/precheck，body = submission-solution-v2.txt 全文 + assets（GitHub 仓库 + Release 资产）。
- 结果（2026-11-19T14:10Z 左右，HTTP 200，耗时 88,054 ms）：would_pass=true、defects=[]、critic.passed=true、critic.score=7、blocked_by=[]、reason="passed adversarial critique"；note="dry-run only — nothing was submitted; the formal review may still differ"。
- 原始响应：repo/artifacts/precheck-v2.json。
- 历史失败已修复：旧版正文 + filebin/data URI 方案被 safety critic 拦截；v2 已改为非破坏性插件 + GitHub 仓库/Release 资产，预检通过。

## E17 v2.2.0 提交前预检

- 待 v2.2.0 打包与 Release 上传后执行；结果回填于本文件与项目 STATUS.md，不提交。

## E18 微信开发者工具真实运行证据（v2.2.0）

- 工具：微信开发者工具 2.02.2609250 Stable（Windows）；基础库 3.4.10；沙箱 AppID wx65dda5a642890a95；页面 pages/index/index；设备 iPhone 12/13 (Pro)。
- 项目：repo/miniprogram-demo（TDesign 1.18.0，t-button / t-tag）；app.wxss 引入 ./theme.wxss；miniprogram-demo/theme.wxss 与 repo/theme.wxss 字节相同（构建同步）。
- 打开命令：cli.bat open --project "<repo>/miniprogram-demo" --port 24728 --lang zh；执行前清除 ELECTRON_RUN_AS_NODE。
- 截图 1：evidence/devtools/miniprogram-simulator.png，488×941，101,264 B，SHA-256 210ec05728a5e8d835189d0ac10dd7eb4e6b2032a54fac39f1f7f122722c0fde（仅模拟器）。
- 截图 2：evidence/devtools/miniprogram-devtools.png，1564×1250，176,635 B，SHA-256 fce1d407dfb94168dadb2c07670f8fe65551c702a6b8a3044000be8d88dac2b6（完整 IDE 窗口）。
- run.json：2,693 B，SHA-256 3cf66112393d04c14fa060954866213f3c3c387f82c2605519fbbce284ed499d；记录工具版本、AppID、页面、设备、截图元数据、计算样式与命令。
- 真实渲染计算样式：主按钮 rgb(31, 94, 255)；浅色按钮 rgb(241, 244, 255)、文字 rgb(31, 94, 255)；品牌标签浅底 rgb(241, 244, 255)、文字 rgb(31, 94, 255)；成功 rgb(227, 249, 233)/rgb(14, 122, 95)；警告 rgb(255, 241, 233)/rgb(154, 91, 0)；危险 rgb(255, 240, 237)/rgb(180, 35, 24)。
- 校验：scripts/verify_devtools_evidence.py 读 run.json，校验截图存在/字节/哈希/尺寸、AppID/libVersion、主题副本字节一致、app.wxss @import、WXML 含 t-button/t-tag、计算样式；实跑 18/18 PASS，结果 evidence/devtools/verify.json（2,808 B，SHA-256 8e57278ab2db0189874c87cea75f8822cfa0c0e6a379aec80ac7d465ea942d49）。
- 运行步骤、预期画面与限制见 repo/docs/WECHAT-DEVTOOLS.md。
- 这是模拟器截图，不是真机截图；不连接后端，所有文案与数据均为虚构。

