# #1835 验收记录（round1）

- 生成时间：2026-11-19T15:27:10Z
- tokens.json SHA-256：`63972f37c08d0e6a28b88579a8e0880503ce0c43770b7fdf12f2e7f89fe3f6ef`
- theme.wxss SHA-256：`0835f0c080c3a48a0d400a37a9822b715e4ee29ad1db033650cccfa503030b28`
- Figma 变量集 SHA-256：`9717a2ab957beff8f76deb43f29ad4d14b7ebd32b5baa7b525a069be0f815dfc`
- 截图：`artifacts/example-page.png`，750x2269，300034 B，SHA-256：`eccf75328d60d6f201e08b872740c786ba4abd3fade4bed05e43d0e8418db23a`
- 单测：15 passed
- 校验：8/8 PASS
- token / TDesign 变量 / 对比度组合：74 / 64 / 57（最小 4.66:1）
- Figma 在线导出：74/74 名称 1:1，collection Theme / mode Light

| 步骤 | 命令 | exit | 秒 |
| --- | --- | ---: | ---: |
| build | `<home>\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe <home>\Documents\deepseek-harness\default-workspace\clawhunt\projects\1835\repo\scripts\build.py` | 0 | 0.13 |
| figma-syntax | `<home>/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/node/bin/node.exe --check <home>\Documents\deepseek-harness\default-workspace\clawhunt\projects\1835\repo\figma\create-variables.js` | 0 | 0.14 |
| validate | `<home>\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe <home>\Documents\deepseek-harness\default-workspace\clawhunt\projects\1835\repo\scripts\validate.py` | 0 | 0.14 |
| pytest | `<home>\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe -m pytest -q tests` | 0 | 1.03 |
| verify-figma | `<home>\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe <home>\Documents\deepseek-harness\default-workspace\clawhunt\projects\1835\repo\scripts\verify_figma_export.py` | 0 | 0.12 |
| capture | `<home>/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/node/bin/node.exe <home>\Documents\deepseek-harness\default-workspace\clawhunt\projects\1835\repo\scripts\capture.mjs` | 0 | 3.68 |

## 校验明细

- [PASS] DTCG structure and value types：74 tokens; types and values valid
- [PASS] required token categories and scales：33 required tokens; 6 sizes; 10 neutrals; 4 semantics
- [PASS] alias resolution：7 aliases resolve without cycles
- [PASS] WCAG contrast >= 4.5:1：57 pairs, minimum 品牌主色文字 / 品牌浅底 4.66:1
- [PASS] theme.wxss and browser preview freshness：64 TDesign-consumed variables; 10 documented preview extensions; browser preview is 2x rpx->px
- [PASS] Figma variables 1:1：74 Figma variables + 74 DTCG import variables, names exactly equal tokens.json paths
- [PASS] demo references and variables：42 theme variables used by demo, all defined
- [PASS] contrast documentation：57 documented pairs, no FAIL

## 结论

全部命令 exit 0；8/8 校验通过；15 项 pytest 通过；Figma 在线导出 74/74 校验通过；截图为 750px 宽。
