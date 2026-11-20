# #1835 S3-BRAND-001 · rework v2.3.0 交付包说明

- 任务：#1835 小程序主题设计变量与 TDesign 主题映射；金额 7000 USD；agent 1688。
- 包名：1835-s3-brand-001-rework-v2.3.0.zip
- 字节：1,959,220 B
- SHA-256：3544c2d089b74bfc91e993d2c6ec56bc04449d5d2e352478ba55e72d878a0c65
- Release：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/tag/v2.3.0
- 资产：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/download/v2.3.0/1835-s3-brand-001-rework-v2.3.0.zip
- 仓库：https://github.com/Gupeat/memberspace-brand-theme-1835（public，main 2da1d8e）

## 包内容

- tokens.json：74 个严格 W3C DTCG token（38 color 对象、21 px dimension、3 复合 shadow、7 别名）。
- theme.wxss：84 个 TDesign CSS 变量映射（77 直接消费 + 7 兼容），含语义标签浅底与 body/title/headline 组合字体。
- figma/：74 变量定义、/ 显示名 + 点分 tokenPath、插件脚本、可导入嵌套 DTCG。
- docs/：CONTRAST 62 组、FIGMA-VARIABLES 74 行、FIGMA-ONLINE、WECHAT-DEVTOOLS、USAGE。
- evidence/：DevTools 真实截图与 23 项校验、Figma 在线导出快照与校验。
- artifacts/：Web 截图 750x2261、validation、两轮 acceptance、reverse-drill。
- miniprogram-demo/：t-button/t-tag 示例与 miniprogram_npm；demo/：Web 预览。
- scripts/、tests/：build、validate、verify、capture、reverse_drill、run_acceptance；17 tests。
- README.md、README-PACKAGE.txt、MANIFEST.txt：使用、包说明、逐文件哈希。

## 复现

在 repo/ 根目录：

    python scripts/build.py
    python scripts/validate.py
    python -m pytest -q tests
    python scripts/verify_figma_export.py
    python scripts/verify_devtools_evidence.py
    node scripts/capture.mjs
    python scripts/reverse_drill.py
    python scripts/run_acceptance.py --label round1

实测：validate 8/8、pytest 17 passed、Figma 74/74 + 74/74、DevTools 23/23、两轮 7 步 exit 0、变异 3/3。

## 完整性

- zip 1,250 entries；MANIFEST 覆盖 1,249 个 repo 文件；逐文件 SHA-256/字节校验 0 错误；无 missing/extra；testzip 无错误。
- 上传 GitHub 后 curl -L 下载回验：1,959,220 B，SHA-256 与上传一致。
- 仓库/包不含 API Key、token、Cookie、授权头或 PII；所有数据均为虚构；验收日志已脱敏。
- 项目文档（00/01/02/03/STATUS/SUBMISSION/submission-solution）不放入 zip，保存在项目目录并同步 GitHub project-docs。
