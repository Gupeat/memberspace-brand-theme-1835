# 使用说明（#1835 品牌主题）

本说明面向三类使用者：设计师、小程序开发者、设计系统维护者。所有命令都在 `repo/` 目录执行。

## 1. 设计师：改颜色/字号/圆角

1. 只编辑 `tokens.json`，不要手改 `theme.wxss`、`demo/theme.css`、`figma/*.json`、`docs/CONTRAST.md`、`docs/FIGMA-VARIABLES.md`；这些都是生成物。
2. 颜色值用 6 位十六进制（如 `#1F5EFF`）；需要透明时用 8 位（`#RRGGBBAA`）。
3. 尺寸用 DTCG dimension 对象：`{ "value": 28, "unit": "rpx" }`。
4. 别名写成 `{color.neutral.900}`；构建时会解析，循环引用会直接失败。
5. 运行：

   ```powershell
   python scripts/build.py
   python scripts/validate.py
   ```

6. 对比度不达标时，`validate.py` 会打印具体组合与比值；必须 ≥4.5:1。不要通过删检查项“修复”。
7. 重新截取示例页：`node scripts/capture.mjs`（需要 Edge 与 playwright-core）。

### 加新令牌

- 在对应分类下添加带 `$value` 的对象，必要字段写 `$description`。
- 如果它需要映射到 TDesign，在 `scripts/build.py` 的 `THEME_MAP` 加一行 `("--td-xxx", "path.to.token")`。
- 如果它用于示例页，在 `demo/demo.css` 用 `var(--td-xxx)` 引用，`validate.py` 会检查变量已定义。
- 重跑 build/validate/pytest；Figma 变量会自动增加。

### 改品牌色

至少成组修改：`brand.primary`、`hover`、`active`、`light`、`lightHover`，以及依赖它们的 `focus.ring`。改完检查：

```powershell
python scripts/validate.py
python -m pytest -q tests
node scripts/capture.mjs
```

截图应显示按钮主色、标签文字色与新品牌色一致。

## 2. 小程序开发者：接入 TDesign

1. 复制 `theme.wxss` 到小程序项目。
2. 在 `app.wxss` 顶部引入：

   ```css
   @import "theme.wxss";
   ```

3. 变量已挂在 `page` 和 `.td-theme` 上，TDesign 组件直接继承，不需要逐组件传色值。
4. 页面局部想覆盖主题时，在容器加 `class="td-theme"`，或在该容器内重设 `--td-*` 变量。
5. 使用变量而不是硬编码：

   ```css
   .cta {
     background: var(--td-brand-color);
     border-radius: var(--td-radius-default);
     font-size: var(--td-font-size-base);
   }
   ```

6. 字号是 rpx，原则：正文 `--td-font-size-base`（28rpx），辅助 `--td-font-size-s`（24rpx），标题按 32/36/40/48rpx。

### 组件对照

| 场景 | 变量 |
| --- | --- |
| 主按钮/主链接 | `--td-brand-color`、`--td-brand-color-active`、`--td-brand-color-disabled`、`--td-brand-color-focus`、`--td-brand-color-light`、`--td-brand-color-light-active`、`--td-text-color-brand` |
| 成功/警告/错误 | `--td-success-color`、`--td-warning-color`、`--td-error-color`（信息色见 02-DESIGN，TDesign 小程序无独立 info 变量） |
| 正文/次要/占位/禁用/反白 | `--td-text-color-primary/secondary/placeholder/disabled/anti` |
| 页面/卡片/悬停 | `--td-bg-color-page/container/container-active/secondarycontainer` |
| 边框 | `--td-component-stroke`、`--td-border-color`、`--td-border-level-1-color`、`--td-border-level-2-color`、`--td-component-border` |
| 圆角 | `--td-radius-small/default/large/round` |
| 间距 | `--td-spacer`、`--td-spacer-1/2/3/4` |
| 阴影 | `--td-shadow-1/2/3` |
| 动效 | `--td-anim-duration-base`、`--td-anim-time-fn-easing/ease-out` |

完整清单见 `theme.wxss`（64 项）。

## 3. 设计系统维护者：生成物与闸门

### 唯一来源

`tokens.json` → `build.py` → 以下生成物：

- `theme.wxss`
- `demo/theme.css`（rpx 换成 px 的 2x 浏览器预览）
- `figma/figma-variables.json`
- `figma/create-variables.js`、`figma/manifest.json`
- `docs/CONTRAST.md`
- `docs/FIGMA-VARIABLES.md`

### 每次改动的最短流程

```powershell
python scripts/build.py
python scripts/validate.py
python -m pytest -q tests
```

提交/交付前再跑两轮从零验收：

```powershell
python scripts/run_acceptance.py --label round1
python scripts/run_acceptance.py --label round2
```

`run_acceptance.py` 会删除生成物后重建，校验 8 项、14 项 pytest、截图尺寸/色彩，并写出：

- `artifacts/acceptance-<label>.log`（每条命令、stdout、stderr）
- `artifacts/ACCEPTANCE-<label>.md`、`artifacts/ACCEPTANCE.md`

### 变异演练

```powershell
python scripts/reverse_drill.py
```

它复制仓库到临时目录，注入三类缺陷（改中性色导致对比度失败、删品牌映射、改 Figma 名称），确认闸门能捕获。日志 `artifacts/reverse-drill.log`，输出 3/3 DETECTED。临时副本会删除，不影响仓库。

### 常见问题

| 现象 | 原因/处理 |
| --- | --- |
| `theme.wxss 或 demo/theme.css 不是最新` | 改了 tokens 但没跑 build；重跑 build |
| 对比度 FAIL | 调整前景/背景色，直到 ≥4.5:1；不要改阈值 |
| Figma 1:1 失败 | 检查 Tokens 路径是否被改名；重跑 build 生成变量与文档 |
| demo 变量未定义 | `demo.css` 用了 THEME_MAP 未映射的 `--td-*`；补映射或改用已有变量 |
| 截图失败 | 确认 Edge 路径、`playwright-core` 已安装；可用 `EDGE` 环境变量 |
| GIF/截图字节不同 | 字体/渲染差异；以像素与计算样式断言为准，不要求字节稳定 |
| Figma 插件无法导入 | 选择 `figma/manifest.json` 而不是 JS 文件；需要在桌面端开发插件菜单 |

### 不变量

- `tokens.json` 是唯一真源；生成物不得手改。
- 74 个 token、64 个 TDesign 消费变量、74 个 Figma 变量、57 组对比度必须保持一致。
- 最低正文对比度 4.66:1。
- 示例页 750px 宽、2x 预览、截图高 ≥1500。
- 所有示例数据为虚构，不含 PII、API Key、Token。