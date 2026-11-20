# 1835 S3-BRAND-001 交付包（v2.3.0）

- 任务：小程序主题设计变量与 TDesign 主题映射（7000 USD）
- 版本：v2.3.0（严格 DTCG 值类型、TDesign 语义浅底与组合字体映射、Figma slash 显示名、62 组对比度与 23 项 DevTools 证据）
- 入口：README.md、tokens.json、theme.wxss、docs/、figma/、demo/、miniprogram-demo/、vendor/、tests/、scripts/、artifacts/、evidence/（figma-online + devtools）
- 校验：本包内 MANIFEST.txt 列出每个文件的 SHA-256 与字节数；可用 Python zipfile 解包后逐行核对。
- 在线 Figma：见 README.md 与 docs/FIGMA-ONLINE.md（collection Theme / mode Light / 74 变量）。
- 微信开发者工具：见 docs/WECHAT-DEVTOOLS.md 与 evidence/devtools/（真实模拟器截图 + 23 项校验）。
- miniprogram_npm 已随包附带；用 vendor/tdesign-miniprogram-1.18.0.tgz 可重建。
- 项目文档（00/01/02/03/STATUS/SUBMISSION/task-1835.json）在 GitHub 仓库的 project-docs/ 下，不放入本 zip，避免包内文档与包 SHA 互相引用。
- 数据：全部为虚构数据；包内不含客户名、PII、API Key、访问令牌或本机用户目录。
