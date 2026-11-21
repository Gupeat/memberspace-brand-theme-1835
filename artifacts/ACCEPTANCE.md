# #1835 验收记录（round2）

- 生成时间：2026-11-21T15:26:17Z
- tokens.json SHA-256：`4e5dc3b3c3e31a0ecebee9f4e030966233f4599984d7b204aaa3174a9f0b0b35`
- theme.wxss SHA-256：`127b876c07ec5ea75bc4441d20510169e517f75c7726507853a01f516c7d1f3f`
- Figma 变量集 SHA-256：`215608ff444c16a66771ce950086b5bcb5bfcf6ebf38b488e7abd26ee9249e03`
- demo/theme.css SHA-256：`4e0bbfaff8a88c66282b9d3fdfa76f096e954e5248e6b4d803fd01fa3e29af36`
- docs/CONTRAST.md SHA-256：`15d1b5bfed826a80437974b51fce1016c441f10567cd7507b7c2e6fb098db7e6`
- docs/FIGMA-VARIABLES.md SHA-256：`fb07babeb59e26d2787b064b5e1a1e59e61133b4aca0b9d4bf444a0e9de76f34`
- miniprogram-demo/theme.wxss SHA-256：`127b876c07ec5ea75bc4441d20510169e517f75c7726507853a01f516c7d1f3f`
- 截图：`artifacts/example-page.png`，750x2261，311263 B，SHA-256：`13a13e3badbafd5fa7455042f313297260e299a5bb088511ee8696ebafb5f43f`
- 单测：18 passed
- 校验：8/8 PASS
- token / TDesign 变量 / 对比度组合：74 / 84 / 62（最小 4.66:1）
- Figma 在线导出：74/74 名称 1:1，collection Theme / mode Light
- 微信开发者工具：微信开发者工具 2.02.2609250 Stable (Windows)，23 项证据校验通过

| 步骤 | 命令 | exit | 秒 |
| --- | --- | ---: | ---: |
| build | `<home>\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe <repo>\scripts\build.py` | 0 | 0.14 |
| figma-syntax | `<home>/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/node/bin/node.exe --check <repo>\figma\create-variables.js` | 0 | 0.13 |
| validate | `<home>\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe <repo>\scripts\validate.py` | 0 | 0.25 |
| pytest | `<home>\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe -m pytest -q tests` | 0 | 1.45 |
| verify-figma | `<home>\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe <repo>\scripts\verify_figma_export.py` | 0 | 0.12 |
| verify-devtools | `<home>\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe <repo>\scripts\verify_devtools_evidence.py` | 0 | 0.11 |
| capture | `<home>/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/node/bin/node.exe <repo>\scripts\capture.mjs` | 0 | 2.46 |

## 校验明细

- [PASS] DTCG structure and value types：74 tokens; strict DTCG value types valid (color objects, px dimensions, composite shadows)
- [PASS] required token categories and scales：33 required tokens; 6 sizes; 10 neutrals; 4 semantics
- [PASS] alias resolution：7 aliases resolve without cycles
- [PASS] WCAG contrast >= 4.5:1：62 pairs, minimum 品牌主色文字 / 品牌浅底 4.66:1
- [PASS] theme.wxss and browser preview freshness：84 mapped variables; 77 directly consumed by TDesign 1.18.0; 7 compatibility-only; miniprogram-demo/theme.wxss matches; 10 preview extensions; browser preview is 2x rpx->px
- [PASS] Figma variables 1:1：74 Figma variables with / display names; 74 DTCG import variables; canonical tokenPath values exactly equal tokens.json dot paths
- [PASS] demo references and variables：42 theme variables used by demo, all defined
- [PASS] contrast documentation：62 documented pairs, no FAIL

## 结论

全部 7 步命令 exit 0；8/8 校验通过；18 项 pytest 通过；Figma 在线导出 74/74 校验通过；微信开发者工具证据 23 项通过；Web 截图为 750px 宽。
