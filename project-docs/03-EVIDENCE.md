# #1835 证据（v2.4.0 干净环境修复）

- 任务：#1835【S3-BRAND-001】小程序主题设计变量与 TDesign 主题映射
- 金额：7000 USD；agent 1688（craftmesh-v7.env）；assigned_to_me=true；escrow funded；deadline 2026-12-14T15:59:59Z；platform_only
- 更新时间：2026-11-21 22:43（Asia/Shanghai）
- 平台状态（2026-11-21 22:43 只读查询）：status=in_progress、rework_count=2、max_rework_rounds=3、latest_delivery_status=rework_requested、submitted_at=null、delivery_check=null。
- 当前交付：**v2.4.0 已发布 GitHub**（PR #1/#2、tag `v2.4.0`、Release、包），并从远端 tag 干净克隆复跑 18 passed；待用户当轮批准后提交平台，尚未提交。
- 历史：v2.3.0 于 2026-11-20T15:04:45.916268Z 提交（commit 2da1d8e、17 tests、包 1,959,220 B），随后被要求第 2 轮 rework；其数字只作历史，不得作为 v2.4.0 证据引用。

## E1 客户 blocker 与复现

客户在隔离沙箱对 v2.3.0 提交 `c658393953500cc8850affaebb8012f96714cf6a` 运行：

    python -m pytest -q tests

17 项中 1 项失败：

    AssertionError: only 0 mapped variables are directly consumed by TDesign
    RESULT: FAIL (7/8 checks)

测试名：`tests/test_tokens.py::test_validation_script_reports_8_of_8_pass`。交付说明与 README 当时写“17 项 pytest 通过”，与沙箱结果矛盾。

本机把该 commit 下载到干净目录 `C:/Users/xibei/AppData/Local/Temp/1835-clean-c658393/...` 后运行 `python -m pytest -q tests`，得到 16 passed、1 failed，失败输出与客户一致。证明不是客户环境特例。

## E2 根因

`scripts/validate.py` 原第 230-233 行读取：

    ROOT/miniprogram-demo/miniprogram_npm/tdesign-miniprogram/**/*.wxss

该目录由微信开发者工具“构建 npm”生成，未提交到仓库；干净克隆不存在，因此：

- `consumed` 集合为空；
- 检查 5 报 `only 0 mapped variables are directly consumed by TDesign`；
- validate 退出码 1，pytest 的 subprocess 断言失败。

第二个可移植性问题：`tests/test_tokens.py` 的 subprocess 传 `env={"PYTHONIOENCODING": "utf-8"}`，替换整个环境变量表，丢失 PATH/HOME/TMPDIR/SYSTEMROOT；客户已点名。它不是本次唯一失败的主因，但同样必须修。

## E3 修复

1. `scripts/validate.py`：新增 `tdesign_wxss_texts() -> list[str]`，从 `ROOT/vendor/tdesign-miniprogram-1.18.0.tgz` 读取所有 `.wxss` 成员并 UTF-8 解码；缺失或为空抛 AssertionError。检查 5 改为遍历该函数返回的 wxss 文本。tgz 内 124 个 `.wxss`、988 个 `--td-` 变量；直接消费 77 个，阈值 >=75 不变。
2. `tests/test_tokens.py`：`env = {**os.environ, "PYTHONIOENCODING": "utf-8"}`；新增 `test_clean_room_validation_without_generated_miniprogram_npm(tmp_path)`：`shutil.copytree(ROOT, clean, ignore=ignore_patterns("miniprogram_npm","__pycache__",".pytest_cache","*.pyc"))`，断言不存在 `miniprogram-demo/miniprogram_npm`，subprocess 跑 `clean/scripts/validate.py`，断言 exit 0、`RESULT: PASS (8/8 checks)`、`77 directly consumed`。
3. `scripts/capture.mjs`：playwright-core 缺失时回退到 Edge headless CLI（`--headless=new --window-size=750,2261`），干净环境不需要 `npm install`；有 playwright-core 时仍走原计算样式断言。
4. `ci/clean-room.yml`（GitHub Actions 模板，复制到 `.github/workflows/` 启用）：Ubuntu + Python 3.12；`actions/checkout@v4`、`actions/setup-python@v5`；依次执行 build、pytest、validate、verify_figma_export、verify_devtools_evidence。不含 capture/Edge，不含 `git diff --exit-code`（生成文件在 Windows 为 CRLF，Linux 构建为 LF，diff 会误红）。

## E4 干净副本运行输出

执行脚本（临时副本排除 `miniprogram_npm`/`__pycache__`/`.pytest_cache`/`*.pyc`）：

    $ python scripts/build.py
    {"tokens": 74, "themeVariables": 84, "figmaVariables": 74, "figmaImportVariables": 74, "contrastPairs": 62, "minContrast": 4.66, "tokensHash": "4e5dc3b3c3e31a0ecebee9f4e030966233f4599984d7b204aaa3174a9f0b0b35"}
    $ python -m pytest -q tests
    ..................                                                       [100%]
    18 passed in 0.88s
    $ python scripts/validate.py
    [PASS] theme.wxss and browser preview freshness: 84 mapped variables; 77 directly consumed by TDesign 1.18.0; 7 compatibility-only; miniprogram-demo/theme.wxss matches; 10 preview extensions; browser preview is 2x rpx->px
    RESULT: PASS (8/8 checks)
    $ python scripts/verify_figma_export.py
    OK: 74/74 canonical paths and / display names, type counts, aliases, values and descriptions match; export snapshot is fresh.
    $ python scripts/verify_devtools_evidence.py
    OK

日志：`repo/artifacts/clean-room-v2.4.0.log`，2,495 B，SHA-256 `5a2cc469ac41c3270dacd8d7ddae05eba8779b28c1ec3af3108c83820d74df6a`。日志中命令统一写作 `python scripts/...`，不含本机绝对路径。

## E5 测试

- `python -m pytest -q tests`：**18 passed**（新增干净环境回归测试 1 项）。
- `python scripts/validate.py`：**8/8 PASS**，第 5 项 77 directly consumed + 7 compatibility-only。
- `python scripts/verify_figma_export.py`：74/74 tokenPath、74/74 显示名，ok=true。
- `python scripts/verify_devtools_evidence.py`：23/23，ok=true。
- 全量测试文件：`repo/tests/test_tokens.py`，9,260 B，SHA-256 `acb111c8ae51b9a7f2ef01d6e89175f7b95b2e62ac740ffc0054d89f196eb5e5`。

## E6 两轮 7 步验收

`python scripts/run_acceptance.py --label round1` 与 `--label round2`，每轮先删除生成物，再跑 build、figma-syntax、validate、pytest、verify-figma、verify-devtools、capture。

- round1 2026-11-21T12:32:23Z；round2 2026-11-21T12:33:24Z；两轮 7 步均 exit 0。
- 每轮 pytest 18 passed、validate 8/8、Figma 74/74、DevTools 23/23、截图 750x2261。
- 截图：`artifacts/example-page.png`，311,263 B，SHA-256 `13a13e3badbafd5fa7455042f313297260e299a5bb088511ee8696ebafb5f43f`。
- 两轮关键生成物逐字节一致：theme.wxss `127b876c07ec5ea75bc4441d20510169e517f75c7726507853a01f516c7d1f3f`、demo/theme.css `4e0bbfaff8a88c66282b9d3fdfa76f096e954e5248e6b4d803fd01fa3e29af36`、figma/figma-variables.json `215608ff444c16a66771ce950086b5bcb5bfcf6ebf38b488e7abd26ee9249e03`、docs/CONTRAST.md `15d1b5bfed826a80437974b51fce1016c441f10567cd7507b7c2e6fb098db7e6`、docs/FIGMA-VARIABLES.md `fb07babeb59e26d2787b064b5e1a1e59e61133b4aca0b9d4bf444a0e9de76f34`。
- 记录：`artifacts/ACCEPTANCE.md`，2,973 B，SHA-256 `47b3f37980640321f3459638f0774fc82c3c98b4435f156c6e1531dec28d3b01`；round1 `c666322d56a383f3c8a57a22b49ac4ca21798aa56a48be0e2dad8fe5ca7b03f1`，round2 与 ACCEPTANCE 相同。

## E7 CI 模板与远端干净克隆

新增 `ci/clean-room.yml`，832 B，SHA-256 `b62af5da53fe73fc12d9588c853be0a7e80527d139bd8cc8d5c7e760aeddeb26`：

- `on: push: branches: [main]; pull_request; workflow_dispatch`
- `runs-on: ubuntu-latest`，Python 3.12
- 步骤：build → pytest → validate → verify_figma_export → verify_devtools_evidence
- 设计取舍：不跑 capture（Linux runner 无 Edge/playwright），不加 `git diff --exit-code`（CRLF/LF 差异）。
- 该文件是可直接启用的模板，复制到 `.github/workflows/clean-room.yml` 生效；GitHub 发布 token 无 workflow scope，因此没有自动在 Actions 运行。

从 tag `v2.4.0` 下载 GitHub tarball 到空目录（无 `miniprogram_npm`）后实跑：

    $ python -m pytest -q tests
    18 passed in 0.97s
    $ python scripts/validate.py
    RESULT: PASS (8/8 checks)
    $ python scripts/verify_figma_export.py
    OK: 74/74 ...
    $ python scripts/verify_devtools_evidence.py
    OK

日志：`project-docs/artifacts/remote-clean-clone-v240.log`，2,049 B，SHA-256 `82dfb454c33dfd5b6867fbc0da4bdf5d98210e63882f516f29faba88bf33e0e6`。

## E8 当前关键文件哈希

| 文件 | 字节 | SHA-256 |
| --- | ---: | --- |
| repo/tests/test_tokens.py | 9,260 | acb111c8ae51b9a7f2ef01d6e89175f7b95b2e62ac740ffc0054d89f196eb5e5 |
| repo/scripts/validate.py | 18,608 | 170122746655a2b7dfb3aa66f9330cd7843fb7c27ce06a9b6478520000668530 |
| repo/scripts/capture.mjs | 4,214 | 2634d9e7156d0c9a27103fe5d8bb5b8b86b4ca508022a412a78e7008372493f8 |
| repo/scripts/run_acceptance.py | 8,726 | f2f75776e48cfaf9d55d6868c1662e581f0dcdb913d12cdf27e92a807c1b240d |
| repo/ci/clean-room.yml | 832 | b62af5da53fe73fc12d9588c853be0a7e80527d139bd8cc8d5c7e760aeddeb26 |
| repo/artifacts/clean-room-v2.4.0.log | 2,495 | 5a2cc469ac41c3270dacd8d7ddae05eba8779b28c1ec3af3108c83820d74df6a |
| repo/artifacts/example-page.png | 311,263 | 13a13e3badbafd5fa7455042f313297260e299a5bb088511ee8696ebafb5f43f |
| repo/artifacts/ACCEPTANCE.md | 2,973 | 47b3f37980640321f3459638f0774fc82c3c98b4435f156c6e1531dec28d3b01 |
| repo/README.md | 17,736 | 00a481461bdb0c31c857e0261b27d9b1a348ee604abb4eb67988d810c6296a54 |
| repo/README-PACKAGE.txt | 1,391 | c093f59de2e2a09f42aaa34fb40560c8c4667ca82fc8110f2ccd93608d8a08f0 |
| repo/tokens.json | 16,690 | 4e5dc3b3c3e31a0ecebee9f4e030966233f4599984d7b204aaa3174a9f0b0b35 |
| repo/theme.wxss | 3,442 | 127b876c07ec5ea75bc4441d20510169e517f75c7726507853a01f516c7d1f3f |

业务产物（tokens/theme/Figma/对比度/DevTools）本轮未改，因此 AC1–AC4 证据沿用；只修可移植性。

## E9 交付包与 GitHub

- 包：`1835-s3-brand-001-rework-v2.4.0.zip`，1,976,416 B，SHA-256 `6af7be676b482764aafd3d6191f57e0e2c5033ae185f3fc77d27018b2ecc116d`。
- zip 1,252 entries；MANIFEST 1,251 个文件；逐文件 SHA-256/字节校验 0 错误；zip 无 missing/extra；testzip 无错误；隐私扫描 0 命中。
- MANIFEST 含 `ci/clean-room.yml` 与 `artifacts/clean-room-v2.4.0.log`；包内 README-PACKAGE 为 v2.4.0。
- 仓库：https://github.com/Gupeat/memberspace-brand-theme-1835
- 代码合并提交（v2.4.0 tag）：`a7f8722f83f781e46df2432f73978d4e05d31da4`
- PR：#1 https://github.com/Gupeat/memberspace-brand-theme-1835/pull/1（干净环境修复，merged）、#2 https://github.com/Gupeat/memberspace-brand-theme-1835/pull/2（CI 模板，merged）
- tag：`v2.4.0` → `a7f8722f83f781e46df2432f73978d4e05d31da4`
- Release：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/tag/v2.4.0
- 远端干净克隆复跑：tarball 无 `miniprogram_npm`；18 passed、8/8、74/74、23/23，日志 `project-docs/artifacts/remote-clean-clone-v240.log`（2,049 B，SHA-256 `82dfb454c33dfd5b6867fbc0da4bdf5d98210e63882f516f29faba88bf33e0e6`）。

## E10 平台提交记录

- 提交命令：`powershell -File clawhunt\clawhunt.ps1 submit -ProblemId 1835 -EnvFile craftmesh-v7.env -TextFile clawhunt\projects\1835\submission-solution-v3.txt`
- 状态：**待用户当轮明确批准**；尚未提交。
- 提交后记录：submitted_at `__SUBMITTED_AT__`、instant_review `__INSTANT__`、delivery_check `__DELIVERY__`。

## E11 限制

- 微信开发者工具截图是模拟器（iPhone 12/13 Pro），不是真机；沙箱 AppID 不是客户 AppID。
- Figma 免费版；匿名查看不显示 Variables 编辑面板，变量证据以登录态截图与导出快照为准。
- 62 组对比度是颜色组合校验，不等同完整 UI 无障碍审计。
- clean-room 日志来自 Windows 干净副本与从 tag 下载的 GitHub tarball；CI 模板未在 GitHub Actions 自动运行，因此没有 Linux runner 结果。
- 本机无 git 客户端，GitHub 通过 REST API 提交；不是 git CLI 生成的 PR。
