# #1835 状态

- 任务：#1835【S3-BRAND-001】小程序主题设计变量与 TDesign 主题映射
- 金额：7000 USD；agent 1688（craftmesh-v7.env）；assigned_to_me=true；escrow funded；deadline 2026-12-14T15:59:59Z；platform_only
- 更新时间：2026-11-21 22:43（Asia/Shanghai）
- 平台状态（2026-11-21 22:43 只读查询）：status=in_progress、rework_count=2、max_rework_rounds=3、latest_delivery_status=rework_requested、submitted_at=null、delivery_check=null、deadline 2026-12-14T15:59:59。
- 本地状态：**v2.4.0 已推 GitHub（tag/Release/包）并从远端 tag 干净克隆复跑 18 passed；仅剩用户当轮批准后提交平台。** 尚未提交，不重复提交。

## 本轮唯一 blocker（客户原文）

客户在隔离沙箱对 v2.3.0 提交 `c658393953500cc8850affaebb8012f96714cf6a` 运行 `python -m pytest -q tests`，17 项中 `test_validation_script_reports_8_of_8_pass` 失败，而交付说明与 README 写 17 项全部通过。要求干净克隆、干净环境复现并修到全绿，运行输出随交付附上。

## 根因与修复

**根因**：`scripts/validate.py` 从 `miniprogram-demo/miniprogram_npm/tdesign-miniprogram/**/*.wxss` 读取 TDesign 组件源码。该目录由微信开发者工具生成、未提交，干净克隆不存在，因此 `directly consumed` 为 0，检查 5 失败，validate 输出 7/8。

1. `scripts/validate.py`：新增 `tdesign_wxss_texts()`，从已提交的 `vendor/tdesign-miniprogram-1.18.0.tgz` 内 124 个 `.wxss` 读取 988 个 `--td-` 变量；不再依赖生成的 `miniprogram_npm`。直接消费变量仍为 77，阈值 >=75 不变。
2. `tests/test_tokens.py`：subprocess 环境改为 `{**os.environ, "PYTHONIOENCODING": "utf-8"}`，不再替换整个环境变量表；新增 `test_clean_room_validation_without_generated_miniprogram_npm`，在排除 `miniprogram_npm` 的临时副本上运行 validate，要求 8/8。
3. `scripts/capture.mjs`：playwright-core 缺失时自动回退到 Edge headless CLI，干净环境不再需要 npm 依赖；截图 750x2261。
4. `ci/clean-room.yml`：GitHub Actions 模板（复制到 `.github/workflows/` 启用）；Ubuntu + Python 3.12，执行 build、pytest、validate、Figma 导出校验、DevTools 证据校验。发布 token 无 workflow scope，未自动运行；不把它写成“CI 已跑”。

## 验收结果

- 本机干净副本（排除 `miniprogram_npm`/`__pycache__`/`.pytest_cache`）：build 0、pytest **18 passed**、validate **8/8 PASS**（77 directly consumed）、Figma 74/74、DevTools 23/23；日志 `repo/artifacts/clean-room-v2.4.0.log`（2,495 B / SHA-256 `5a2cc469…`）。
- 两轮 7 步验收：round1 2026-11-21T12:32:23Z、round2 12:33:24Z，均 exit 0；pytest 18 passed；截图 750x2261 / 311,263 B / SHA-256 `13a13e3b…`；关键产物哈希两轮一致。
- 远端干净克隆：从 tag `v2.4.0` 下载 GitHub tarball 到空目录（确认无 `miniprogram_npm`），实跑 **18 passed、8/8、74/74、23/23**；日志 `project-docs/artifacts/remote-clean-clone-v240.log`（2,049 B / SHA-256 `82dfb454…`）。
- 未改 tokens.json、theme.wxss、对比度、Figma 变量与 DevTools 证据，因此 AC1–AC4 的业务产物不变，只修可移植性。

## GitHub 与包

- 仓库：https://github.com/Gupeat/memberspace-brand-theme-1835
- 代码合并提交（tag v2.4.0）：`a7f8722f83f781e46df2432f73978d4e05d31da4`
- PR：#1（干净环境修复，merged）、#2（CI 模板，merged）
- tag：`v2.4.0` → `a7f8722f83f781e46df2432f73978d4e05d31da4`
- Release：https://github.com/Gupeat/memberspace-brand-theme-1835/releases/tag/v2.4.0
- 包：`1835-s3-brand-001-rework-v2.4.0.zip`，1,976,416 B，SHA-256 `6af7be676b482764aafd3d6191f57e0e2c5033ae185f3fc77d27018b2ecc116d`；MANIFEST 1,251 文件、missing/extra 0、隐私扫描 0 命中；Release 资产 state=uploaded。
- 项目文档（00/01/02/03/STATUS/SUBMISSION/task + 预检/远端复跑）在仓库 `project-docs/`，不放入 zip。

## 待办

1. 已构建/校验 zip，已推 GitHub、建 PR/tag/Release，已远端干净克隆复跑 18 passed。
2. 已更新 SUBMISSION/03-EVIDENCE/submission-solution-v3.txt 的 commit/PR/tag/包哈希/远端复跑。
3. 向用户汇报并取得**当轮明确批准**后，执行：
   `powershell -File clawhunt\clawhunt.ps1 submit -ProblemId 1835 -EnvFile craftmesh-v7.env -TextFile clawhunt\projects\1835\submission-solution-v3.txt`
4. 提交后记录 submitted_at、instant_review、delivery_check，补 03-EVIDENCE E10。

## 关键本地哈希（v2.4.0）

| 文件 | 字节 | SHA-256 |
| --- | ---: | --- |
| repo/tests/test_tokens.py | 9,260 | acb111c8ae51b9a7f2ef01d6e89175f7b95b2e62ac740ffc0054d89f196eb5e5 |
| repo/scripts/validate.py | 18,608 | 170122746655a2b7dfb3aa66f9330cd7843fb7c27ce06a9b6478520000668530 |
| repo/scripts/capture.mjs | 4,214 | 2634d9e7156d0c9a27103fe5d8bb5b8b86b4ca508022a412a78e7008372493f8 |
| repo/ci/clean-room.yml | 832 | b62af5da53fe73fc12d9588c853be0a7e80527d139bd8cc8d5c7e760aeddeb26 |
| repo/artifacts/clean-room-v2.4.0.log | 2,495 | 5a2cc469ac41c3270dacd8d7ddae05eba8779b28c1ec3af3108c83820d74df6a |
| repo/artifacts/example-page.png | 311,263 | 13a13e3badbafd5fa7455042f313297260e299a5bb088511ee8696ebafb5f43f |
| repo/artifacts/ACCEPTANCE.md | 2,973 | 47b3f37980640321f3459638f0774fc82c3c98b4435f156c6e1531dec28d3b01 |
| repo/README.md | 17,736 | 00a481461bdb0c31c857e0261b27d9b1a348ee604abb4eb67988d810c6296a54 |
| repo/README-PACKAGE.txt | 1,391 | c093f59de2e2a09f42aaa34fb40560c8c4667ca82fc8110f2ccd93608d8a08f0 |

## 历史

v2.3.0 于 2026-11-20T15:04:45.916268Z 提交（status=submitted、rework_count=1），随后被要求第 2 轮 rework；其 17 tests、commit 2da1d8e、包 1,959,220 B 等数字只属于历史，不得作为 v2.4.0 证据引用。
