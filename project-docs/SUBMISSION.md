# #1835 提交材料（v2）

- 任务：#1835【S3-BRAND-001】小程序主题设计变量与 TDesign 主题映射
- 金额：7000 USD；agent 1688（craftmesh-v7.env）
- 状态：v1 已于 2026-11-19T10:46:33.421669Z 提交（submitted，rework_count=0）；v2 已完成并发布 GitHub Release，等待平台 request-rework 或用户明确指示。
- 更新时间：2026-11-19 22:05（Asia/Shanghai）

## 1. v2 相对 v1 的修改

1. TDesign 映射从 68 收敛到 64：移除 tdesign-miniprogram 1.18.0 未消费的 --td-line-height、--td-anim-duration-moderate、--td-anim-duration-slow、--td-anim-time-fn-ease-in；对应 token 仍保留。
2. theme.wxss 68→64；demo/theme.css 68+10→64+10；validate.py、tests、run_acceptance.py 的计数与测试名同步。
3. README、USAGE、00、01、02 的变量数量口径同步；03 增加 v2 两轮、变异与安全修复证据。
4. submission-solution-v2.txt 增加“验收标准逐条对照”：客户四条 AC 原文、PASS 结果、命令、测试函数与证据路径。
5. 安全修复：Figma 插件不再删除任何既有变量，类型冲突跳过，未匹配变量保留并提示；交付由公共 filebin 改为 GitHub 仓库 + Release 资产。

## 2. 交付清单

1. repo/tokens.json：74 个 W3C DTCG 变量，7 个别名，覆盖色彩/字号/行高/字重/圆角/间距/阴影/动效。
2. repo/theme.wxss：64 个 TDesign 1.18.0 实际消费的 CSS 变量映射；page 与 .td-theme 选择器。
3. repo/figma/figma-variables.json：74 个 Figma 变量，名称与 tokens.json 1:1。
4. repo/figma/create-variables.js + manifest.json：Figma Plugin API 非破坏性导入脚本。
5. repo/docs/FIGMA-VARIABLES.md：74 行 1:1 对照表。
6. repo/docs/CONTRAST.md：57 组对比度，全部 ≥4.5:1，最小 4.66:1。
7. repo/docs/USAGE.md：安装、变量使用、组件对照、维护者闸门。
8. repo/demo/ + repo/artifacts/example-page.png：TDesign 风格 Web 预览，750×2269，按钮/标签使用新品牌色。
9. repo/tests/test_tokens.py + scripts/validate.py：14 tests、8/8 校验。
10. repo/artifacts/acceptance-round1.log、round2.log、ACCEPTANCE-*.md：v2 两轮从零验收。
11. repo/artifacts/reverse-drill.log：3/3 变异命中。
12. 项目文档 00/01/02/03/STATUS；本文件与 submission-solution-v2.txt；GitHub 仓库 project-docs/ 下同版存档。

## 3. 验收标准逐条对照（客户原文）

| 编号 | 客户验收标准 | 结果 | 复现命令与证据 |
| --- | --- | --- | --- |
| AC1 | 1. tokens.json 通过 W3C Design Tokens 格式校验 | PASS | python scripts/validate.py 第1项；pytest tests/test_tokens.py::test_token_index_has_74_valid_tokens；repo/artifacts/validation.log |
| AC2 | 2. 对比度检查表中所有正文文字组合 ≥ 4.5:1 | PASS | 57 组，最小 4.66:1；python scripts/validate.py 第4项；pytest ...test_all_57_body_text_pairs_meet_wcag_aa；repo/docs/CONTRAST.md |
| AC3 | 3. theme.wxss 应用到 TDesign 组件示例页后的截图中按钮、标签使用新品牌色 | PASS | node scripts/capture.mjs；截图 750×2269、300,034 B；按钮 rgb(31,94,255)，标签 rgb(31,94,255)/rgb(241,244,255)；repo/artifacts/example-page.png |
| AC4 | 4. Figma 变量名与 tokens.json 中的名称一一对应（对照表） | PASS | 74 个变量名称集合与 tokens 路径严格相等；python scripts/validate.py 第6项；pytest ...test_figma_variables_are_exactly_1_to_1；repo/docs/FIGMA-VARIABLES.md 74 行 |

## 4. 复现命令

    cd repo
    python scripts/build.py
    python scripts/validate.py
    python -m pytest -q tests
    node scripts/capture.mjs
    python scripts/run_acceptance.py --label round1
    python scripts/run_acceptance.py --label round2

## 5. v2 交付包（GitHub Release）

- 路径：clawhunt/projects/1835/artifacts/1835-s3-brand-001-rework-v2.zip
- 仓库：https://github.com/Gupeat/memberspace-brand-theme-1835
- Release：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/tag/v2.0.0
- 资产：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/download/v2.0.0/1835-s3-brand-001-rework-v2.zip
- 字节：343,925 B
- SHA-256：24e6348c7c8b379ed5aa4191de1199725e2b6883a743883ab67fa88ef8ec60e2
- 下载回验：343,925 B，SHA-256 一致；30 个条目，MANIFEST 29/29，testzip 无错误，隐私扫描 0。
- 包内：repo 源码/README/docs/tokens/theme/demo/figma/tests/scripts/artifacts + README-PACKAGE.txt + MANIFEST.txt。项目文档在 GitHub 仓库 project-docs/，不放入 zip，避免快照哈希循环。
- 上传后重新下载核对字节与 SHA-256。

## 6. v1 提交记录（历史）

    2026-11-19T10:46:33.421669Z 已执行；返回 status=submitted、submitted_at=2026-11-19T10:46:33.421669、message=Solution submitted, awaiting review。

    instant_review：needs_changes（启发式语义打分，低分不等于交付无效）；delivery_check=checked、text_only。
    平台复核：status=submitted、assigned_to_me=true、latest_delivery_version=1、rework_count=0。

## 7. v2 提交方式（仅在 rework 后执行）

    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "clawhunt\clawhunt.ps1" submit -ProblemId 1835 -EnvFile "craftmesh-v7.env" -TextFile "clawhunt\projects\1835\submission-solution-v2.txt"

前提：平台 status 变为 rework_requested / rework，或客户明确退回；v1 submitted 且 rework_count=0 时禁止执行。

## 8. 提交检查表（v2）

- [ ] 平台已 request-rework 或用户明确指示提交 v2
- [x] v2 包已发布 GitHub Release 并回验
- [x] 回填包 URL/字节/SHA-256
- [ ] 预检 would_pass=true、defects=[]
- [ ] 执行 submit 并记录 submitted_at/version
- [ ] 提交后 WorkStatus submitted；绝不重复提交
