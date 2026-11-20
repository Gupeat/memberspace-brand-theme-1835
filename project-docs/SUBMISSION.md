# #1835 提交材料（rework v2.3.0）

- 任务：#1835【S3-BRAND-001】小程序主题设计变量与 TDesign 主题映射
- 金额：7000 USD；agent 1688（craftmesh-v7.env）
- 状态：v1 已于 2026-11-19T10:46:33.421669Z 提交；平台随后 request-rework（rework_count=1）。v2.3.0 已完成实现、严格 DTCG、微信开发者工具真实截图、在线 Figma、62 组对比度、17 tests、23 项 DevTools、两轮 7 步验收、GitHub Release；**尚未提交**，等待用户审核与明确批准。
- 更新时间：2026-11-20 20:40（Asia/Shanghai）

## 1. rework v2.3.0 相对 v1 的修改

1. **严格 W3C DTCG**：38 个 color 全部改为 `{colorSpace:"srgb",components:[r,g,b],hex:"#RRGGBB"}` 对象；21 个 dimension 改为 px；3 个 shadow 改为含 color 对象和四边 dimension 的复合对象；7 个 alias 全部可解析。validate.py 检查 1 与 tests/test_tokens.py 覆盖严格值类型。
2. **TDesign 语义浅底与组合字体**：theme.wxss 从 64 个映射扩展到 84 个（77 个被 TDesign 1.18.0 直接消费，7 个兼容别名）。新增 `--td-tag-success-light-color` / `--td-tag-warning-light-color` / `--td-tag-danger-light-color`，修复 TDesign 标签只换文字色、浅底仍是默认色的问题；新增 mark/body/title/headline 的 `--td-font-size-*` 与 `--td-line-height-*`，修复组合字体不采用 24/28/32/36/40/48 阶梯的问题；删除会改变语义的 `--td-font-size-xxl`。
3. **Figma 显示名统一**：在线文件 74 个变量、collection Theme / mode Light、Anyone can edit；Figma 显示名为 `color/brand/primary` 这类 `/` 分组，canonical tokenPath 为 `color.brand.primary` 点分路径，逐段 1:1。对照表、插件 JSON、插件脚本、导入 DTCG 全部统一；verify_figma_export.py 同时校验 74/74 tokenPath 与 74/74 显示名。
4. **对比度表补齐**：62 组正文组合，最低 4.66:1；新增语义标签实际浅底组合：success #0E7A5F on #E7F7F0=4.78、warning #9A5B00 on #FFF4E5=4.99、error #B42318 on #FEE9E9=5.65、info #0B5C8A on #E6F3FB=6.38、accent #0F766E on #E6F4F1=4.84。
5. **微信开发者工具真实截图**：DevTools 2.02.2609250 Stable、沙箱 AppID wx65dda5a642890a95、libVersion 3.4.10、页面 pages/index/index；t-button/t-tag 真实计算样式为品牌色、语义浅底与 16px/12px 字号；模拟器 488x941 与 IDE 1564x1250 两张截图；verify_devtools_evidence.py 23/23 PASS。
6. **交付通道**：GitHub 公开仓库 + Release v2.3.0 资产（1,959,220 B / SHA-256 3544c2d0…），下载回验一致；不使用 filebin。包内不含 project-docs，避免包 SHA 与文档互相引用。

## 2. 交付清单

1. repo/tokens.json：74 个严格 DTCG token，7 个别名；覆盖色彩、字号/行高/字重、圆角、间距、阴影、动效。
2. repo/theme.wxss：84 个 TDesign 小程序 CSS 变量映射；由 tokens.json 生成；与 miniprogram-demo/theme.wxss 字节相同。
3. repo/figma/figma-variables.json：74 个变量定义（tokenPath 点分 + `/` 显示名）；create-variables.js + manifest.json 为桌面插件备选路径。
4. repo/figma/figma-import.tokens.json 与 Light.tokens.json：Figma Variables 可直接导入的嵌套 DTCG；74 项，两份字节相同。
5. repo/docs/CONTRAST.md：62 组正文对比度表，全部 >=4.5:1。
6. repo/docs/FIGMA-VARIABLES.md：74 行对照表（tokenPath + 显示名）；docs/FIGMA-ONLINE.md：在线/导入/导出说明。
7. repo/docs/WECHAT-DEVTOOLS.md：DevTools 打开、截图、复现与限制。
8. repo/evidence/devtools/：两张截图、run.json、verify.json。
9. repo/evidence/figma-online/：Theme.zip、Light.tokens.json、verify.json、登录/共享/匿名截图。
10. repo/scripts/：build.py、validate.py、verify_figma_export.py、verify_devtools_evidence.py、capture.mjs、run_acceptance.py、reverse_drill.py。
11. repo/tests/test_tokens.py：17 项测试；repo/README.md 与 docs/USAGE.md：使用、替换品牌色、Figma 导入、验证说明。
12. 交付包：1835-s3-brand-001-rework-v2.3.0.zip；GitHub Release v2.3.0。

## 3. AC 对照与证据

| AC | 原文 | 交付证据 |
| --- | --- | --- |
| AC1 | tokens.json 通过 W3C Design Tokens 格式校验 | 严格 DTCG：38 个 color 对象、21 个 px dimension、3 个复合 shadow；validate.py 8/8 检查 1 通过；tests/test_tokens.py 严格值类型测试；artifacts/validation.log |
| AC2 | 对比度检查表中所有正文文字组合 >= 4.5:1 | docs/CONTRAST.md 62 组，最低 4.66:1；validate.py 检查 4/8；test_all_62_body_text_pairs_meet_wcag_aa |
| AC3 | theme.wxss 应用到 TDesign 组件示例页后的截图中按钮、标签使用新品牌色 | artifacts/example-page.png 750x2261；DevTools 真实截图 + 23 项计算样式；button background rgb(31,94,255)、tag 浅底 #E7F7F0/#FFF4E5/#FEE9E9、字号 16px/12px |
| AC4 | Figma 变量名与 tokens.json 中的名称一一对应（对照表） | 74 个 `/` 显示名 + 74 个点分 tokenPath；verify_figma_export.py 74/74+74/74；docs/FIGMA-VARIABLES.md；figma-variables.json；在线 Theme/Light |

## 4. 复现命令

在 repo 根目录：

    python scripts/build.py
    python scripts/validate.py
    python -m pytest -q tests
    python scripts/verify_figma_export.py
    python scripts/verify_devtools_evidence.py
    node scripts/capture.mjs
    python scripts/reverse_drill.py
    python scripts/run_acceptance.py --label round1

实测：build `{"tokens":74,"themeVariables":84,"figmaVariables":74,"figmaImportVariables":74,"contrastPairs":62,"minContrast":4.66,"tokensHash":"4e5dc3b3…"}`；validate 8/8 PASS；pytest 17 passed；Figma 74/74；DevTools 23/23；两轮 7 步均 exit 0；变异 3/3 DETECTED。

## 5. 交付包与 GitHub Release

- 仓库：https://github.com/Gupeat/memberspace-brand-theme-1835（public；main 2da1d8e…）
- Release：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/tag/v2.3.0
- 资产：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/download/v2.3.0/1835-s3-brand-001-rework-v2.3.0.zip
- 字节：1,959,220 B；SHA-256：3544c2d089b74bfc91e993d2c6ec56bc04449d5d2e352478ba55e72d878a0c65；asset id 771731043。
- zip 1,250 entries；MANIFEST 覆盖 1,249 个文件；逐文件 SHA-256/字节校验 0 错误；无 missing/extra；testzip 无错误；隐私扫描 0 命中。
- 上传后 curl -L 下载 1,959,220 B，SHA-256 与上传一致。

## 6. 沙箱/隐私

- 所有数据均为虚构：占位品牌名「会员空间平台」，无客户名、真实企业、手机号、邮箱、身份证。
- Figma 账号凭证只在本机 .clawhunt/figma-account.txt，不进仓库/包/提交文本。
- 微信开发者工具使用个人沙箱测试号，不是客户 AppID；不上传、不预览、不连接后端。
- 仓库和包不含 API Key、token、Cookie、授权头或 PII；验收日志已按 ROOT/HOME 三种写法脱敏，含 JSON 转义双反斜杠。
- 包扫描 C:/Users、/Users/、xibei、craftmesh、ghp_/github_pat_/sk-、邮箱、手机号 0 命中。

## 7. 质量闸门

- [x] build 幂等；theme.wxss 与 miniprogram-demo/theme.wxss 字节相同
- [x] validate.py 8/8 PASS
- [x] pytest 17 passed
- [x] 严格 DTCG：38 color 对象、21 px dimension、3 复合 shadow
- [x] 84 映射：77 直接消费 + 7 兼容；标签语义浅底与组合字体在真实 DevTools 生效
- [x] Figma 74 tokenPath + 74 显示名；在线文件 74 变量
- [x] 62 组对比度，最小 4.66:1
- [x] 两轮 7 步从零验收 exit 0
- [x] 变异 3/3 DETECTED
- [x] 包 MANIFEST/zip/隐私/下载回验通过
- [ ] v2.3.0 solution precheck would_pass=true、defects=[]（2026-11-20T12:30Z/12:33Z 两次：deterministic 通过、defects=[]；critic outage、would_pass=null，待重试）
- [ ] 用户审核并明确批准
- [ ] 执行 submit 并记录 submitted_at/version

## 8. 已知限制

- 微信开发者工具截图使用沙箱测试号与模拟器（iPhone 12/13 Pro），不是真机截图；不同 IDE 版本/设备模拟器可能导致 PNG 字节不同。
- Figma 免费版；匿名查看者不显示 Variables 编辑面板，变量证据以登录态截图与导出快照为准。
- miniprogram-demo 只演示 t-button/t-tag 的品牌色、语义浅底与字号，不代表全部 TDesign 组件；完整组件外观见 demo/index.html（Web 预览）。
- 62 组对比度是颜色组合校验，不等同完整 UI 无障碍审计。
- 本机无 git 客户端，GitHub 通过 REST API 提交，不是 git CLI 生成的 PR。
- 项目文档不放入 zip；GitHub 仓库 project-docs 为文档快照。
