# #1835 证据

- 任务：#1835【S3-BRAND-001】小程序主题设计变量与 TDesign 主题映射
- 金额：7000 USD；agent 1688（craftmesh-v7.env）；assigned_to_me=true；escrow funded；deadline 2026-12-14T15:59:59Z；assignment_deadline 2026-11-22T01:07:49Z；platform_only
- 更新时间：2026-11-20 20:40（Asia/Shanghai）
- 平台状态：v1 已于 2026-11-19T10:46:33.421669Z 提交，status=submitted、assigned_to_me=true；平台随后要求 rework（rework_count=1，latest_delivery_status=rework_requested）。v2.3.0 已完成并上传 Release，尚未提交；本文件记录 v2.3.0 的生成、校验、两轮验收、变异、DevTools、包与 Release 证据。

## E1 环境

- Windows；Python 3.12.14（bundled），Pillow 12.3.0；Node v24.21.0；Microsoft Edge headless；playwright-core 1.65.1。
- Figma：已有账号（凭证只在本机 .clawhunt/figma-account.txt，不进仓库/包）；在线文件 collection Theme / mode Light / 74 变量，共享 Anyone can edit；匿名可查看，匿名视图不显示 Variables 编辑面板。
- 微信开发者工具 2.02.2609250 Stable（Windows），沙箱 AppID wx65dda5a642890a95，libVersion 3.4.10；真实模拟器运行见 E17。
- 无 git/docker；GitHub 通过 REST API 提交，不是本地 git/PR；Web 预览仍是 2rpx=1px，仅作完整示例页补充。
- 所有数据均为虚构；仓库与文档不含客户名、真实企业、手机号、邮箱或身份证。

## E2 生成

命令（repo 根）：

    python scripts/build.py

退出码 0，输出：

    {"tokens": 74, "themeVariables": 84, "figmaVariables": 74, "figmaImportVariables": 74, "contrastPairs": 62, "minContrast": 4.66, "tokensHash": "4e5dc3b3c3e31a0ecebee9f4e030966233f4599984d7b204aaa3174a9f0b0b35"}

- 生成 tokens 索引、theme.wxss、demo/theme.css、figma/figma-variables.json、figma/figma-import.tokens.json、figma/Light.tokens.json、figma/create-variables.js、docs/CONTRAST.md、docs/FIGMA-VARIABLES.md。
- 重新运行 build.py 后关键生成物逐字节一致；theme.wxss 与 miniprogram-demo/theme.wxss 字节相同。

## E3 校验 8/8

命令：`python scripts/validate.py`，退出码 0。

    [PASS] DTCG structure and value types: 74 tokens; strict DTCG value types valid (color objects, px dimensions, composite shadows)
    [PASS] required token categories and scales: 33 required tokens; 6 sizes; 10 neutrals; 4 semantics
    [PASS] alias resolution: 7 aliases resolve without cycles
    [PASS] WCAG contrast >= 4.5:1: 62 pairs, minimum 品牌主色文字 / 品牌浅底 4.66:1
    [PASS] theme.wxss and browser preview freshness: 84 mapped variables; 77 directly consumed by TDesign 1.18.0; 7 compatibility-only; miniprogram-demo/theme.wxss matches; 10 preview extensions; browser preview is 2x rpx->px
    [PASS] Figma variables 1:1: 74 Figma variables with / display names; 74 DTCG import variables; canonical tokenPath values exactly equal tokens.json dot paths
    [PASS] demo references and variables: 42 theme variables used by demo, all defined
    [PASS] contrast documentation: 62 documented pairs, no FAIL

    RESULT: PASS (8/8 checks)

日志：repo/artifacts/validation.log（980 B，SHA-256 e9a25e14…）与 validation.json（1,614 B，SHA-256 2ed7ebf4…）。

## E4 对比度

- docs/CONTRAST.md 62 组：4 个正文色 x 11 个浅底、反白色 x 9 个深底、品牌链接 x 3，以及品牌主色/辅助色/语义色浅底组合。
- 最低 4.66:1（品牌主色文字 / 品牌浅底）；全部正文组合 >= 4.5:1。
- 新增语义浅底：success #0E7A5F on #E7F7F0 = 4.78；warning #9A5B00 on #FFF4E5 = 4.99；error #B42318 on #FEE9E9 = 5.65；info #0B5C8A on #E6F3FB = 6.38；accent #0F766E on #E6F4F1 = 4.84。
- 由 build.py 计算，validate.py 检查 4 与检查 8 双重校验；测试 test_all_62_body_text_pairs_meet_wcag_aa。

## E5 单测

命令：`python -m pytest -q tests`，退出码 0。

    17 passed

覆盖严格 DTCG 值类型、74 token 索引、7 alias、84 映射、62 对比度、Figma tokenPath 与 `/` 显示名、导入 DTCG 字节一致、miniprogram-demo 主题同源、验证脚本 8/8。

## E6 示例页截图

- 命令：`node scripts/capture.mjs`；Edge headless + playwright-core；750px 宽、按 scrollHeight 裁剪。
- 输出：repo/artifacts/example-page.png，750x2261，296,124 B，SHA-256 8d7b49c30b61938d8e64156efde62d9ecb39f5aa2fc1fc76ae398040b0ddc4c4。
- 断言：按钮背景 rgb(31, 94, 255)、标签文字 rgb(31, 94, 255)、标签浅底 rgb(241, 244, 255)、PNG 宽 750 且高 >= 1500。
- 该 Web 预览是完整示例页补充；AC3 的真实 TDesign 证据见 E17，不用 Web 截图冒充 DevTools。

## E7 在线 Figma 变量（74/74）

- 在线文件：https://www.figma.com/design/U3n0qOCgViDDfdSnOWIw5n/MemberSpace-Brand-Theme-1835---v2?node-id=0-1；collection Theme、mode Light、74 变量、Anyone can edit。
- 导出快照：evidence/figma-online/Theme.zip（28,607 B，SHA-256 f9bc2c8c…），解包 Light.tokens.json（28,475 B，SHA-256 7ee62794…）。
- verify_figma_export.py 实跑 ok=true、checked 74；74 tokenPath 点分集合与 tokens.json 完全相等，74 个 `/` 显示名逐项映射，类型/别名/值/描述一致；import_fresh=true、light_identical=true。
- evidence/figma-online/verify.json（3,169 B，SHA-256 632641e6…）；登录态、共享、匿名截图见同目录。
- 命名口径：Figma 显示名为 `color/brand/primary` 这类 `/` 分组；canonical tokenPath 为 `color.brand.primary` 点分路径；两者逐段 1:1，不声称显示名字符串等于点号字符串。

## E8 两轮从零验收（v2.3.0 最终）

命令：`python scripts/run_acceptance.py --label round1` 与 `--label round2`；每次清空生成物后跑 7 步。

- round1 generatedAt 2026-11-20T12:08:00Z；round2 2026-11-20T12:08:06Z；两轮 7 步均 exit 0。
- 每轮：pytest 17 passed、validate 8/8、Figma 74/74、DevTools 23、Web 截图 750x2261 / 296,124 B / SHA 8d7b49c3…；capture 3.05s / 3.33s。
- 日志：artifacts/acceptance-round1.log 3,495 B / SHA e4449cef…；round2 3,495 B / SHA e2aab8ab…。
- 记录：ACCEPTANCE-round1.md 2,973 B / SHA 4e17bee3…；ACCEPTANCE-round2.md 与 ACCEPTANCE.md 均 2,973 B / SHA f63cd9fd…。
- 哈希稳定性：两轮 theme.wxss 127b876c…、demo/theme.css 4e0bbfaf…、figma-variables 215608ff…、CONTRAST 15d1b5bf…、FIGMA-VARIABLES fb07babe… 完全一致。

## E9 变异（反向）演练

脚本：scripts/reverse_drill.py；在临时副本注入 3 类缺陷，验证闸门能发现：

- A：color.neutral.500 的 DTCG `$value.hex` 改为 #D5DAE2，并同步 components -> 对比度失败（1.40/1.34 等）。
- B：删除 `--td-brand-color` 映射 -> demo 变量未定义，validate 7/8 FAIL。
- C：重命名 Figma 变量 -> 1:1 失败，validate 7/8 FAIL。

结果：3/3 DETECTED；日志：repo/artifacts/reverse-drill.log（1,033 B，SHA-256 c08681569f425c72cbf34dc5b97aa8e8445e1555e988d0ad2a8435917e828c66）。
注意：v2.3.0 改为严格 DTCG 后，旧的字符串替换变异目标已不存在；本轮修复 reverse_drill.py 以 JSON 方式同时修改 hex 与 components，重新得到 3/3。

## E10 隐私与脱敏

- 打包前发现 acceptance-round1/2.log 含本机路径（JSON 转义双反斜杠），原因是 run_acceptance.py 只替换单反斜杠 HOME；已修复为按 ROOT/HOME 的单反斜杠、双反斜杠、正斜杠三种写法替换为 <repo>/<home>。
- verify_devtools_evidence.py 输出改为相对路径 evidence/devtools/verify.json；最终日志无用户名、绝对用户目录或系统临时目录路径。
- 全仓与包扫描：C:/Users、/Users/、xibei、craftmesh、ghp_/github_pat_/sk-、邮箱、手机号等模式 0 命中；Figma 账号凭证只在本机 .clawhunt/figma-account.txt，不进仓库/包。
- 包内 1,249 个文本/代码文件扫描 0 命中；所有示例数据均为虚构。

## E11 关键文件哈希

| 文件 | 字节 | SHA-256 |
| --- | ---: | --- |
| repo/tokens.json | 16,690 | 4e5dc3b3c3e31a0ecebee9f4e030966233f4599984d7b204aaa3174a9f0b0b35 |
| repo/theme.wxss | 3,442 | 127b876c07ec5ea75bc4441d20510169e517f75c7726507853a01f516c7d1f3f |
| repo/miniprogram-demo/theme.wxss | 3,442 | 127b876c07ec5ea75bc4441d20510169e517f75c7726507853a01f516c7d1f3f |
| repo/demo/theme.css | 3,814 | 4e0bbfaff8a88c66282b9d3fdfa76f096e954e5248e6b4d803fd01fa3e29af36 |
| repo/demo/index.html | 3,833 | fd9fcc1572ffe3e6ffc7368cfbdffb11bf4ec08bb6648938b62fdf0882418662 |
| repo/demo/demo.css | 6,934 | 951dab78abceb1cc97e746c9b62e5222eddaeddd7760bd65ad126e30a6fd26fc |
| repo/figma/figma-variables.json | 15,936 | 215608ff444c16a66771ce950086b5bcb5bfcf6ebf38b488e7abd26ee9249e03 |
| repo/figma/figma-import.tokens.json | 16,450 | 505525ec378605cb5e6a8f41fa80a9897a73406a3d2c5fc6e8e6737c9c24d95b |
| repo/figma/Light.tokens.json | 16,450 | 505525ec378605cb5e6a8f41fa80a9897a73406a3d2c5fc6e8e6737c9c24d95b |
| repo/figma/create-variables.js | 14,785 | dfb8f19f710393a5c2db4e68443bcc6c2ce1b9778ec7c6accff1c17de006cd98 |
| repo/figma/manifest.json | 137 | a2f0776ffc3b2a6fe2e60732a0b04154d2795de2947c3714c6401afdbeabd037 |
| repo/docs/CONTRAST.md | 5,195 | 15d1b5bfed826a80437974b51fce1016c441f10567cd7507b7c2e6fb098db7e6 |
| repo/docs/FIGMA-VARIABLES.md | 7,335 | fb07babeb59e26d2787b064b5e1a1e59e61133b4aca0b9d4bf444a0e9de76f34 |
| repo/docs/FIGMA-ONLINE.md | 3,483 | b90f2eab01868897a8508f241b6d2fbea044657271c6b6ca04cac4c6950f1fc5 |
| repo/docs/WECHAT-DEVTOOLS.md | 5,445 | c9798d29df9531100eaaad45c7d11e4473a5d8bf07c955a779381f217032d205 |
| repo/docs/USAGE.md | 7,591 | bdcb1fedb149e3af1f21328c38bda98c26132bdbe5c1468587f8a035c06ae5b6 |
| repo/README.md | 15,879 | 572db99ff13c7a2e6f77917f1b124a688c144255fddaef76043c7cd752469d67 |
| repo/README-PACKAGE.txt | 1,180 | 5e3e4a4f881a3663314a9c08f9fff7bc7eb2d5bedcd2aa3231ba8c7df939ab9f |
| repo/miniprogram-demo/README.md | 1,078 | 309a57e4d6074005ef562b335f16b559dba83ccc8e85c9c5f4d044d59e90d9ae |
| repo/miniprogram-demo/project.config.json | 1,339 | 16a92d87587bebfc4ed2c2d0fc153c0efd58c6fe9f642b90544164da18651223 |
| repo/artifacts/example-page.png | 296,124 | 8d7b49c30b61938d8e64156efde62d9ecb39f5aa2fc1fc76ae398040b0ddc4c4 |
| repo/artifacts/validation.log | 980 | e9a25e1494dc6e4cb70098ffa5962a22b98b90a8b88467e1f184ecb43327839f |
| repo/artifacts/validation.json | 1,614 | 2ed7ebf4a6c4050ea4ee5826087273d8676d020d48cbd5a1348cd125d7fe9505 |
| repo/artifacts/acceptance-round1.log | 3,495 | e4449cef4d520b5d63c5e26cb5062dd4e5675ccd228a9f39c057aefba44dd9fc |
| repo/artifacts/acceptance-round2.log | 3,495 | e2aab8ab80c7fc046c63c80c2b66b330d12bd4089d9cf0409c6df460d900cc70 |
| repo/artifacts/ACCEPTANCE-round1.md | 2,973 | 4e17bee39f4586a033fc1ceb4f4e0936902367eaf6381ad9eaed4600f6921973 |
| repo/artifacts/ACCEPTANCE-round2.md | 2,973 | f63cd9fdd919eb51b163f0df0a76d001b1b460b6177e3586a6f83fc24757ffd8 |
| repo/artifacts/ACCEPTANCE.md | 2,973 | f63cd9fdd919eb51b163f0df0a76d001b1b460b6177e3586a6f83fc24757ffd8 |
| repo/artifacts/reverse-drill.log | 1,033 | c08681569f425c72cbf34dc5b97aa8e8445e1555e988d0ad2a8435917e828c66 |
| repo/tests/test_tokens.py | 8,499 | ca80c8a1a9fa1196aef73e81c4d8e688a8de2a652b5f6830caacc358faec00b5 |
| repo/scripts/build.py | 28,098 | cf00de85ba5118817fa8c447c62c55ab58e9ae6194b354bd3f9cca3a195d88f0 |
| repo/scripts/validate.py | 17,936 | 27b33510f8d81bb5bacaaaee47b06e54f11baeb4149be7d31611f9c6540d5127 |
| repo/scripts/verify_figma_export.py | 6,745 | aa70df32e239f928c200560914789407ca83d1cbe80056b71ba3c94e15fda62a |
| repo/scripts/verify_devtools_evidence.py | 4,790 | 06306caec7840ff7fbe39d0314fc7c3e42e0c974984375d782ed702fef1b8159 |
| repo/scripts/capture.mjs | 3,371 | 76f2b7e6f319b89f41aff9350dd96f97cb16fc28a73ea3174a60cbb946a26b4b |
| repo/scripts/run_acceptance.py | 8,726 | df91405f5b8385bb6ce67d7eddee58222aae02a22d4fc1db1776e2e47a5be9f2 |
| repo/scripts/reverse_drill.py | 4,459 | 548ea9e0039656918e35bedc5c2c767f7aa331e0626974a6dda8cd6dcd349241 |
| repo/evidence/devtools/miniprogram-simulator.png | 101,266 | 3df9ec5a364e7067953609beecac54bb65591607c02f733192a84900ebc2a187 |
| repo/evidence/devtools/miniprogram-devtools.png | 179,074 | 97d49831578538a6bab2e839a951c47c0c2faad995a91327be4b41e1f893e8fe |
| repo/evidence/devtools/run.json | 3,264 | 67358e4daa4e5b94ee8ebd90f8698380149a09995d9906ff42c3a68c68cfcf74 |
| repo/evidence/devtools/verify.json | 3,342 | efd5e18a88e2c1a1e379c825c3d36a245a1445426feeb9d3c099f5b82e91990a |
| repo/evidence/figma-online/Theme.zip | 28,607 | f9bc2c8c35a798fca9d9fb7097868645870e1930f0d0f1f1a00e4673cb091ccc |
| repo/evidence/figma-online/Light.tokens.json | 28,475 | 7ee627941bc69c1699b66a4cce0cf57efebda79175db873f20ffc60c61b56ed8 |
| repo/evidence/figma-online/verify.json | 3,169 | 632641e6a657c7cee3bb82f5da3c7e8a4a5e43a2a1b52302309cfb6b2e0f21b9 |
| repo/evidence/figma-online/figma-online-final.png | 49,218 | f611bec12d0339f15fd9d86e7c66024ee07d74fc86953b78b70dbef34cfcb699 |
| repo/evidence/figma-online/figma-shared-final.png | 60,161 | 1c4b3a46b8abfe0742cbc5cc67b5cb06818814d3817cdf0c61bfb352f7ea85a5 |
| repo/evidence/figma-online/figma-anon-public.png | 23,804 | 828b060d557296b3092bdd8ba07deeb3ffde9ae28dbf96cb3bb11df774de24dd |

以上哈希按 2026-11-20 20:20 最终工作树重新计算；包内对应文件逐项一致。

## E12 交付包与 GitHub Release v2.3.0

- 仓库：https://github.com/Gupeat/memberspace-brand-theme-1835（public，main 分支；源码 commit 2da1d8e…；project-docs 同步在 main）
- Release：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/tag/v2.3.0
- 资产：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/download/v2.3.0/1835-s3-brand-001-rework-v2.3.0.zip
- 本地路径：clawhunt/projects/1835/artifacts/1835-s3-brand-001-rework-v2.3.0.zip
- 字节数：1,959,220 B
- SHA-256：3544c2d089b74bfc91e993d2c6ec56bc04449d5d2e352478ba55e72d878a0c65
- GitHub asset：id 771731043；digest sha256:3544c2d0…0c65；上传后 curl -L 下载 1,959,220 B，SHA-256 完全一致。
- 内容：repo 源码/生成物/测试/证据（tokens.json、theme.wxss、figma/、docs/、evidence/figma-online/、evidence/devtools/、artifacts/、miniprogram-demo/ 全量 miniprogram_npm、vendor/tdesign-miniprogram-1.18.0.tgz）+ README-PACKAGE.txt + MANIFEST.txt；zip 1,250 entries，MANIFEST 覆盖 1,249 个文件；排除 node_modules、.git、缓存、临时文件、precheck-* 与 project.config.json.bak*。
- 校验：MANIFEST 1,249/1,249 个文件 SHA-256/字节匹配；zip 无 missing/extra；testzip 无错误；隐私扫描 0 命中；上传后下载回验字节与 SHA 一致。
- 项目文档不放入 zip，放在 GitHub 仓库 project-docs/，避免包内文档与包 SHA 互相引用。

## E13 限制与边界

- Figma 免费版：在线变量与共享链接可用；匿名查看者不显示 Variables 编辑面板，变量证据以登录态截图与导出快照为准。
- 微信开发者工具截图使用沙箱测试号与模拟器（iPhone 12/13 Pro），不是真机截图；不同 IDE 版本、设备模拟器与字体渲染可能导致 PNG 字节不同。
- Web 预览仍是 2rpx=1px，仅作完整示例页补充，不能替代 E17 的 DevTools 证据。
- color.semantic.info 保留在 tokens.json，但 TDesign 小程序官方变量集无独立 info 变量，未伪造映射；业务可直接使用该 token。
- 本机无 git 客户端：使用 GitHub REST API 提交；交付为公开仓库 + Release 资产 + SHA-256，不是 git CLI 生成的 PR。
- 交付仓库为 public，仅含虚构数据、源码、生成物与证据；不含客户名、PII、API Key 或访问令牌。
- 62 组对比度是颜色组合校验，不等同于完整 UI 无障碍审计。
- TDesign 1.18.0 核对：v2.3.0 映射 84 个变量，77 个直接消费、7 个兼容别名；--td-font-size-xxl 已删除（TDesign 默认指向 headline-large 72rpx），旧别名 s/base/m/l/xl 保留。

## E14 提交记录（v1，已发生）

- 提交时间：2026-11-19T10:46:33.421669Z；平台返回 status=submitted、assigned_to_me=true。
- 平台随后要求 rework：rework_count=1，latest_delivery_status=rework_requested。
- v1 不可改写；v2.3.0 只能作为 rework 重新提交，不能覆盖 v1。

## E15 rework 六项对照（v2.3.0）

| 客户要求 | v2.3.0 证据 |
| --- | --- |
| GitHub 仓库 | public repo https://github.com/Gupeat/memberspace-brand-theme-1835；README 快速开始 7 条命令；源码/生成物/测试/证据齐全 |
| Figma 链接 | https://www.figma.com/design/U3n0qOCgViDDfdSnOWIw5n/MemberSpace-Brand-Theme-1835---v2?node-id=0-1；collection Theme / mode Light / 74 变量 / Anyone can edit |
| 微信开发者工具截图 | DevTools 2.02.2609250 Stable、沙箱 AppID、libVersion 3.4.10；模拟器 488x941 与 IDE 1564x1250；23 项校验 |
| Figma 名称 1:1 | 74 个 `/` 显示名 + 74 个点分 tokenPath；verify_figma_export.py 双向校验；对照表 docs/FIGMA-VARIABLES.md |
| DTCG 校验 | 严格 DTCG：38 color 对象、21 dimension px、3 shadow 复合；validate.py 检查 1；17 tests |
| 对比度表 | 62 组正文组合，min 4.66:1；含语义标签实际浅底组合；docs/CONTRAST.md |

## E16 v2.3.0 提交前预检

- 已执行六次：2026-11-20T12:30:34Z（5.4s，5,731 chars）、12:33:35Z（7.4s）、12:36:00Z（6.1s）、12:40:33Z（6.3s，5,768 chars）、12:43:29Z（8.0s，main 引用改为分支后 5,758 chars / 8,769 B）、13:08:25Z（7.3s，仍为 5,758 chars / 8,769 B），调 `POST /api/v1/problems/1835/solution/precheck`（只读，不提交），均 HTTP 200。
- 结果：deterministic checks passed，defects=[]；六次 LLM critic 均 failed to run（outage），would_pass=null，critic.reason="all critic lenses failed to run (outage)"，平台明确说明这不是 fail。记录 attempts[1-6] 在 artifacts/precheck-v230.json。
- 处置：不把 outage 当成通过；本轮 6 次（限流 6/h/agent）已用完，21:30 后可再试，以 would_pass=true、defects=[] 为准；未提交。

## E17 微信开发者工具真实运行证据（v2.3.0）

- 工具/环境：微信开发者工具 2.02.2609250 Stable（Windows），沙箱 AppID wx65dda5a642890a95，基础库 3.4.10，页面 pages/index/index，设备 iPhone 12/13 (Pro)。
- 项目：miniprogram-demo 使用 t-button / t-tag；app.wxss 第一行 @import "./theme.wxss"；theme.wxss 与仓库根字节相同。
- 截图：miniprogram-simulator.png 488x941 / 101,266 B / SHA 3df9ec5a…；miniprogram-devtools.png 1564x1250 / 179,074 B / SHA 97d49831…。
- 计算样式：button_primary background rgb(31,94,255)、color rgb(255,255,255)、radius 8px、fontSize 16px、fontWeight 600；tag_brand background rgb(241,244,255)、color rgb(31,94,255)、fontSize 12px。
- 语义浅底（修复点）：tag_success background rgb(231,247,240)=#E7F7F0，color rgb(14,122,95)；tag_warning background rgb(255,244,229)=#FFF4E5，color rgb(154,91,0)；tag_danger background rgb(254,233,233)=#FEE9E9，color rgb(180,35,24)。
- 校验：verify_devtools_evidence.py 23/23 PASS；结果 evidence/devtools/verify.json（3,342 B，SHA efd5e18a…）。
- 限制：模拟器截图，不是真机；沙箱 AppID 不是客户 AppID；不同 IDE/设备可能导致 PNG 字节不同。

## E18 GitHub 源码与 project-docs

- 源码 commit：2da1d8e509d0689006e7f16b8fa79350afa23d5d（v2.3.0 严格 DTCG/语义浅底/组合字体/Figma 名称/62 对比度/23 DevTools + reverse drill DTCG 修复），tree 938d254999edbfd493637c3d5024683f95796fcb；仓库 68 个源码/文档文件；不跟踪 miniprogram_npm（由 vendor tgz 重建），包内包含全量 miniprogram_npm。
- project-docs：已同步到 main 分支（10 个文件：00/01/02/03/STATUS/SUBMISSION/submission-solution-v2/task-1835/README-PACKAGE/precheck-v230）；因后续文档修订会继续追加提交，此处不锁定 main head，评审以 main 分支最新树为准。
- 旧 Release v2.2.0（1,954,726 B / SHA 12375a15…）仅作历史，不再作为 v2.3.0 提交材料。

## E19 结论

- AC1：严格 DTCG 结构/类型/别名检查通过；AC2：62 组正文组合全部 >=4.5:1，min 4.66；AC3：Web 截图 + 真实 DevTools 23 项，button/tag 品牌色、语义浅底与字号均生效；AC4：74 tokenPath + 74 显示名逐项 1:1。
- 两轮从零验收、8/8 校验、17 tests、3/3 变异、Release 下载回验均通过；未提交，等用户明确批准。