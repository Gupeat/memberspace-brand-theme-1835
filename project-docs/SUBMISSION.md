# #1835 提交材料（rework v2.4.0）

- 任务：#1835【S3-BRAND-001】小程序主题设计变量与 TDesign 主题映射
- 金额：7000 USD；agent 1688（craftmesh-v7.env）
- 状态：**v2.4.0 已推 GitHub（PR/tag/Release/包齐全）并从远端 tag 干净克隆复跑 18 passed；仅剩用户当轮批准后提交平台**；平台 rework_count=2、latest_delivery_status=rework_requested、submitted_at=null。
- 更新时间：2026-11-21 22:43（Asia/Shanghai）

## 1. 本轮 rework 的唯一问题

客户在隔离沙箱对 v2.3.0 提交 `c658393953500cc8850affaebb8012f96714cf6a` 运行 pytest，17 项中 `test_validation_script_reports_8_of_8_pass` 失败：

    AssertionError: only 0 mapped variables are directly consumed by TDesign
    RESULT: FAIL (7/8 checks)

客户要求干净克隆、干净环境复现并修到全绿，运行输出随交付附上。

**根因**：`scripts/validate.py` 从 `miniprogram-demo/miniprogram_npm/tdesign-miniprogram/**/*.wxss` 读取 TDesign 组件源码。该目录由微信开发者工具生成、未提交；干净克隆不存在，导致直接消费变量为 0。不是测试断言过严，也不是 token/theme 内容错误。

## 2. v2.4.0 修复

1. **validate 不依赖生成目录**：新增 `tdesign_wxss_texts()`，从已提交的 `vendor/tdesign-miniprogram-1.18.0.tgz` 内 124 个 `.wxss` 读取 988 个 `--td-` 变量；阈值 >=75 不变，实际 77 directly consumed + 7 compatibility-only。
2. **测试继承环境**：`tests/test_tokens.py` 的 subprocess 改为 `{**os.environ, "PYTHONIOENCODING": "utf-8"}`，不再替换整个环境变量表（客户点名的 PATH/HOME/TMPDIR 丢失问题）。
3. **新增干净环境回归测试**：`test_clean_room_validation_without_generated_miniprogram_npm` 复制仓库到临时目录并排除 `miniprogram_npm`，运行 validate，断言 8/8 与 77 directly consumed。
4. **截图不再依赖 npm**：`scripts/capture.mjs` 在 playwright-core 缺失时回退到 Edge headless CLI；干净环境不需要 `npm install`。
5. **CI 模板**：新增 `ci/clean-room.yml`（复制到 `.github/workflows/` 启用），Ubuntu + Python 3.12 依次跑 build、pytest、validate、Figma 导出校验、DevTools 证据校验。发布 token 无 workflow scope，未自动运行。

## 3. 干净环境运行输出

本机干净副本（排除 `miniprogram_npm`/`__pycache__`/`.pytest_cache`/`*.pyc`）：

    $ python -m pytest -q tests
    ..................                                                       [100%]
    18 passed in 0.88s

    $ python scripts/validate.py
    [PASS] theme.wxss and browser preview freshness: 84 mapped variables; 77 directly consumed by TDesign 1.18.0; 7 compatibility-only; ...
    RESULT: PASS (8/8 checks)

    $ python scripts/verify_figma_export.py
    OK: 74/74 canonical paths and / display names, ...

    $ python scripts/verify_devtools_evidence.py
    OK

完整日志：`repo/artifacts/clean-room-v2.4.0.log`（2,495 B，SHA-256 `5a2cc469ac41c3270dacd8d7ddae05eba8779b28c1ec3af3108c83820d74df6a`）；CI 模板：`repo/ci/clean-room.yml`（832 B，SHA-256 `b62af5da53fe73fc12d9588c853be0a7e80527d139bd8cc8d5c7e760aeddeb26`）。

从 tag `v2.4.0` 下载 GitHub tarball 到空目录（确认无 `miniprogram_npm`）再跑一遍：**18 passed、8/8、74/74、23/23**；日志 `project-docs/artifacts/remote-clean-clone-v240.log`（2,049 B，SHA-256 `82dfb454c33dfd5b6867fbc0da4bdf5d98210e63882f516f29faba88bf33e0e6`）。

## 4. 两轮 7 步验收

- round1 2026-11-21T12:32:23Z、round2 12:33:24Z；两轮均 build、figma-syntax、validate、pytest、verify-figma、verify-devtools、capture 7 步 exit 0。
- pytest 18 passed；validate 8/8；Figma 74/74；DevTools 23/23；截图 750x2261 / 311,263 B / SHA-256 `13a13e3badbafd5fa7455042f313297260e299a5bb088511ee8696ebafb5f43f`。
- 关键生成物两轮逐字节一致：theme.wxss `127b876c…`、demo/theme.css `4e0bbfaf…`、figma-variables `215608ff…`、CONTRAST `15d1b5bf…`、FIGMA-VARIABLES `fb07babe…`。
- 记录：`artifacts/ACCEPTANCE.md`（2,973 B，SHA-256 `47b3f37980640321f3459638f0774fc82c3c98b4435f156c6e1531dec28d3b01`）。

## 5. AC 对照

| AC | 原文 | v2.4.0 证据 |
| --- | --- | --- |
| AC1 | tokens.json 通过 W3C Design Tokens 格式校验 | 严格 DTCG 未改：38 color 对象、21 px dimension、3 复合 shadow；validate 8/8；tests/test_tokens.py |
| AC2 | 对比度检查表所有正文文字组合 >=4.5:1 | docs/CONTRAST.md 62 组，min 4.66:1；validate 检查 4/8；本轮未改 |
| AC3 | theme.wxss 应用到 TDesign 组件示例页后按钮、标签使用品牌色 | Web 截图 750x2261；DevTools 两张截图 + 23 项计算样式；本轮未改 theme/tokens |
| AC4 | Figma 变量名与 tokens.json 名称一一对应 | 74 tokenPath + 74 显示名；verify 74/74+74/74；docs/FIGMA-VARIABLES.md；本轮未改 |

**本轮只修可移植性，不改 token/theme/Figma/对比度/DevTools 业务产物**，因此 AC1–AC4 的既有证据继续有效，同时新增 18 项 pytest、干净环境日志、远端 tag 干净克隆复跑与 CI 模板。

## 6. 交付包与 GitHub

- 仓库：https://github.com/Gupeat/memberspace-brand-theme-1835
- 代码合并提交（tag v2.4.0）：`a7f8722f83f781e46df2432f73978d4e05d31da4`
- PR：#1 https://github.com/Gupeat/memberspace-brand-theme-1835/pull/1（干净环境修复，merged）、#2 https://github.com/Gupeat/memberspace-brand-theme-1835/pull/2（CI 模板，merged）
- tag：`v2.4.0` → `a7f8722f83f781e46df2432f73978d4e05d31da4`
- Release：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/tag/v2.4.0
- 包：`1835-s3-brand-001-rework-v2.4.0.zip`，1,976,416 B，SHA-256 `6af7be676b482764aafd3d6191f57e0e2c5033ae185f3fc77d27018b2ecc116d`；MANIFEST 1,251 文件逐文件校验、zip 无 missing/extra、隐私扫描 0 命中；Release 资产 state=uploaded。
- 远端干净克隆复跑：18 passed、8/8、74/74、23/23；日志 `project-docs/artifacts/remote-clean-clone-v240.log`（2,049 B，SHA-256 `82dfb454c33dfd5b6867fbc0da4bdf5d98210e63882f516f29faba88bf33e0e6`）。

## 7. 提交记录

- 提交命令：`powershell -File clawhunt\clawhunt.ps1 submit -ProblemId 1835 -EnvFile craftmesh-v7.env -TextFile clawhunt\projects\1835\submission-solution-v3.txt`
- 提交状态：**待用户当轮明确批准**；尚未提交。
- 提交后记录：submitted_at `__SUBMITTED_AT__`、instant_review `__INSTANT__`、delivery_check `__DELIVERY__`。

## 8. 沙箱/隐私

- 所有数据均为虚构；占位品牌名「会员空间平台」；无客户名、真实企业、手机号、邮箱、身份证。
- Figma 账号凭证只在本机 `.clawhunt/figma-account.txt`，不进仓库/包/提交文本。
- 微信开发者工具使用个人沙箱测试号，不是客户 AppID；不上传、不预览、不连接后端。
- 验收日志按 ROOT/HOME 三种写法脱敏；包扫描 `C:/Users`、`/Users/`、`xibei`、`craftmesh`、`ghp_`/`github_pat_`/`sk-`、邮箱、手机号 0 命中。

## 9. 质量闸门

- [x] 根因已在干净副本复现（17 passed / 1 failed，validate 7/8）
- [x] validate 从 vendor tgz 读取 TDesign wxss，不依赖 `miniprogram_npm`
- [x] subprocess 环境继承 `os.environ`
- [x] 新增干净环境回归测试；pytest 18 passed
- [x] 两轮 7 步验收 exit 0；截图 750x2261
- [x] 新增 Linux clean-room CI 模板（未自动运行）
- [x] 构建 v2.4.0 包并校验（1,976,416 B / 6af7be67…）
- [x] 推 GitHub PR/tag/Release；从远端 tag 干净克隆复跑 18 passed
- [ ] 用户当轮明确批准后提交平台

## 10. 已知限制

- 微信开发者工具截图使用沙箱测试号与模拟器（iPhone 12/13 Pro），不是真机截图；不同 IDE 版本/设备模拟器可能导致 PNG 字节不同。
- Figma 免费版；匿名查看者不显示 Variables 编辑面板，变量证据以登录态截图与导出快照为准。
- miniprogram-demo 只演示 t-button/t-tag 的品牌色、语义浅底与字号，不代表全部 TDesign 组件。
- 62 组对比度是颜色组合校验，不等同完整 UI 无障碍审计。
- 本机无 git 客户端，GitHub 通过 REST API 提交，不是 git CLI 生成的 PR。
- GitHub Actions 模板未自动运行（发布 token 无 workflow scope）；干净环境证据来自 Windows 干净副本与远端 tarball 复跑，不是 Linux runner。
- 项目文档不放入 zip；GitHub 仓库 project-docs 为文档快照。
