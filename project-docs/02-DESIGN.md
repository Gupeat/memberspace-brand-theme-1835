# #1835 设计说明

更新时间：2026-11-20 20:10（Asia/Shanghai）

## 1. 方案选型

| 方案 | 说明 | 结论 |
| --- | --- | --- |
| A 单一 token 源 + 生成器（采用） | tokens.json 为唯一事实源，脚本生成 theme.wxss、Figma JSON、插件、对比度表、对照表 | 采用：无漂移、可复现、可替换品牌 |
| B 手写 tokens + 手写 wxss | 两份文件各自维护 | 弃：必然漂移，AC1/AC3 难同时满足 |
| C 直接依赖 TDesign 默认主题 | 只覆盖少量变量 | 弃：中性 10 阶、阴影、动效、Figma 1:1 不完整 |
| D 引入第三方 token 工具链 | 需要 npm 依赖与网络 | 弃：交付环境无稳定 npm，增加不可复现风险 |

## 2. 色彩体系

品牌主色 #1F5EFF（白字对比度 5.12:1），hover #1748D6，active #1239B0，light #F1F4FF，lightHover #EDF1FF，disabled #B5C7FF；辅助色 #0F766E + 浅底 #E6F4F1；焦点环为实心品牌色 #1F5EFF（避免透明叠加后不可见）。

中性 10 阶：

| step | 色值 | 用途 |
| --- | --- | --- |
| neutral.50 | #F8FAFC | 页面浅底 |
| neutral.100 | #F1F5F9 | 分组底 |
| neutral.200 | #E2E8F0 | 分隔/边框 |
| neutral.300 | #CBD5E1 | 强边框/禁用边 |
| neutral.400 | #94A3B8 | 占位/图标弱 |
| neutral.500 | #57677C | 正文弱化（所有浅底组合 ≥4.5:1） |
| neutral.600 | #475569 | 三级正文 |
| neutral.700 | #334155 | 二级正文 |
| neutral.800 | #1E293B | 标题 |
| neutral.900 | #0F172A | 主文字/反白底 |

语义色使用深色版保证白字或浅底文字对比度：成功 #0E7A5F + 浅底 #E7F7F0；警告 #9A5B00 + #FFF4E5；错误 #B42318 + #FEE9E9；信息 #0B5C8A + #E6F3FB。TDesign 标签浅底变量已映射，真实 DevTools 计算样式为 #E7F7F0/#FFF4E5/#FEE9E9。

## 3. 字号与排版

六档：24/28/32/36/40/48 rpx；行高分别 36/40/44/48/56/64 rpx。字重 400/500/600。字体栈 PingFang SC、Helvetica Neue、Microsoft YaHei、sans-serif；生成 CSS 时对 generic family 不加引号，避免浏览器把它当成字体名。

TDesign 映射同时覆盖旧别名（`--td-font-size-s/base/m/l/xl`）与组合字体的底层变量（`--td-font-size-mark-*`、`--td-font-size-body-*`、`--td-font-size-title-*`、`--td-font-size-headline-small` 及对应 `--td-line-height-*`）；DevTools 实测 button 字号 16px、tag 字号 12px。

## 4. 圆角、间距、阴影、动效

- 圆角：8/16/24 rpx、9999rpx（全圆）。
- 间距：16/24/32/48/64 rpx，4 的倍数，覆盖 8pt 栅格。
- 阴影：sm 0 2rpx 8rpx rgba(15,23,42,0.06)；md 0 8rpx 24rpx rgba(15,23,42,0.10)；lg 0 16rpx 48rpx rgba(15,23,42,0.14)。
- 动效：fast 120ms、base 200ms、moderate 240ms、slow 320ms；standard cubic-bezier(0.2,0,0,1)、emphasized cubic-bezier(0.3,0,0,1)、decelerate cubic-bezier(0,0,0.15,1)、accelerate cubic-bezier(0.82,0,1,0.9)。

## 5. token 结构（严格 W3C DTCG）

顶层按类别分组：color、font、radius、space、shadow、motion。叶子为 { "$value": ..., "$type": ... }。

- color：`{ "colorSpace": "srgb", "components": [r,g,b], "hex": "#RRGGBB" }`，可选 `alpha`；38 个 color 全部为对象，不再使用裸 hex 字符串。
- dimension：`{ "value": 14, "unit": "px" }`；21 个 dimension 全部 px（DTCG 允许 px/rem）。
- shadow：复合对象，`color` 为 color 对象，`offsetX/offsetY/blur/spread` 为 dimension。
- duration：`{ "value": 200, "unit": "ms" }`；cubicBezier：四元数组；fontWeight：整数。
- alias：`{color.brand.primary}` 形式字符串，构建时解析；无环。
- token 路径即 canonical 路径（点分展示）；Figma 显示名使用 `/` 分组，逐段 1:1。

## 6. TDesign 映射

theme.wxss 输出 page 级 84 个变量：77 个被 TDesign 1.18.0 直接消费；7 个为兼容别名（`--td-brand-color-focus`、`--td-text-color-link`、`--td-success-color-light`、`--td-warning-color-light`、`--td-error-color-light`、`--td-bg-color-secondarycomponent-active`、`--td-border-level-2-color`）。覆盖：

- 品牌：--td-brand-color、--td-brand-color-active、--td-brand-color-disabled、--td-brand-color-focus、--td-brand-color-light、--td-brand-color-light-active、--td-text-color-brand、--td-text-color-link。
- 语义：--td-success-color/-light、--td-warning-color/-light、--td-error-color/-light；新增 --td-tag-success-light-color / --td-tag-warning-light-color / --td-tag-danger-light-color，修复 TDesign 标签浅底只换文字的问题。`color.semantic.info` 保留在 tokens.json 供业务样式直接使用，TDesign 小程序官方变量集无独立 info 变量，不伪造映射。
- 文字：--td-text-color-primary/secondary/placeholder/disabled/anti。
- 背景：--td-bg-color-page/container/container-active/secondarycontainer/-active/component/-active/-disabled/secondarycomponent/-active/specialcomponent。
- 边框：--td-component-stroke、--td-border-color、--td-border-level-1-color、--td-border-level-2-color、--td-component-border。
- 字体：--td-font-family、旧别名 --td-font-size-s/base/m/l/xl、组合字体底层 --td-font-size-mark-*/body-*/title-*/headline-small 与 --td-line-height-*；`--td-font-size-xxl` 已删除（TDesign 默认指向 headline-large 72rpx，保留会改变语义）。
- 圆角：--td-radius-small/default/large/round。
- 间距：--td-spacer、--td-spacer-1/2/3/4。
- 阴影：--td-shadow-1/2/3。
- 动效：--td-anim-duration-base、--td-anim-time-fn-easing/ease-out；moderate/slow/ease-in 未被 TDesign 1.18.0 消费，已从映射移除，token 仍保留。

所有值来自 token；CSS 中不出现硬编码颜色/尺寸（生成器输出除外）。除 7 个兼容别名外，其余 77 个都在 TDesign 1.18.0 的 124 个 wxss 中被直接引用。

## 7. Figma 变量策略

在线交付与可重建证据并行：

1. 在线文件：MemberSpace Brand Theme 1835 - v2（https://www.figma.com/design/U3n0qOCgViDDfdSnOWIw5n/MemberSpace-Brand-Theme-1835---v2?node-id=0-1），collection Theme、mode Light、74 变量、Anyone can edit；匿名可看画布，匿名视图不显示 Variables 编辑面板。
2. `figma/figma-import.tokens.json` + `figma/Light.tokens.json`：Figma Variables 可直接导入的嵌套 DTCG；文件名决定 mode 名 Light；颜色 sRGB，尺寸 px，别名保留 {path}。两份文件字节相同。
3. `figma/figma-variables.json` + `figma/create-variables.js` + `figma/manifest.json`：机器可读定义与桌面插件备选路径；插件非破坏性，按同名创建/更新，不删除既有变量；name 使用 `/` 显示名，tokenPath 保留点分路径。
4. `evidence/figma-online/`：导入后导出快照 Theme.zip、解包 Light.tokens.json、登录态/共享/匿名截图、README 与 verify.json。
5. `scripts/verify_figma_export.py`：将导出快照与 tokens.json 的 74 个路径逐项比对，同时校验 74 个 `/` 显示名；`run_acceptance.py` 把它作为第 5 步；失败即验收失败。
6. `docs/FIGMA-VARIABLES.md` 与 `docs/FIGMA-ONLINE.md`：74 行对照表（tokenPath 与显示名）+ 在线文件/导入/导出/校验说明。

## 8. 对比度方法

WCAG 2.1 相对亮度：sRGB 分量 <=0.04045 时 c/12.92，否则 ((c+0.055)/1.055)^2.4；L=0.2126R+0.7152G+0.0722B；对比度=(L1+0.05)/(L2+0.05)。只把正文文字组合纳入 AC2；装饰色、禁用色不计入正文，但在文档标注。

62 组覆盖 4 个正文色 × 11 个浅底、反白色 × 9 个深底、品牌链接 × 3、品牌主色/品牌浅底，以及语义色浅底组合（success 4.78、warning 4.99、error 5.65、info 6.38、accent 4.84）；最小 4.66。

## 9. 示例页与截图

- 示例页：demo/index.html + demo/demo.css，使用 theme 变量；TDesign 组件外观（按钮、标签、cell、输入、提示、变量卡）；数据虚构。
- 浏览器预览 2rpx=1px：750px 截图 = 375pt 设备 @2x。
- 截图：Edge headless + playwright-core；750 宽，测量 scrollHeight 后按 750 宽裁剪；断言按钮背景 rgb(31,94,255)、标签文字同色、标签浅底 rgb(241,244,255)、PNG 宽 750 且高≥1500；输出 artifacts/example-page.png（750×2261，296,124 B）。
- 真实 DevTools：miniprogram-demo 的 t-button/t-tag，真实计算样式 background/color/fontSize，语义浅底为 #E7F7F0/#FFF4E5/#FEE9E9；23 项证据校验。

## 10. 故障推演

| 故障 | 检测 | 降级 |
| --- | --- | --- |
| tokens.json 语法错 | build.py 立即退出 | 不生成半成品 |
| 严格 DTCG 类型错 | validate.py 检查 1 失败 | 改回 color/dimension/shadow 对象 |
| alias 指向不存在/有环 | validate.py 报路径 | 修复 token |
| 对比度不足 | validate.py 失败 | 调深文字/调浅底 |
| theme.wxss 漂移 | validate.py 新鲜度检查 | 重新生成 |
| 截图失败 | capture 重试/报错 | 保留日志，人工检查 |
| Edge 路径不同 | 环境变量 EDGE | 用 which/默认路径 |
| 字体缺失 | CSS 字体栈回退 | 不影响 token |
| rpx/px 换算错 | 表内同时列 rpx 与 px | 以 tokens 的 px 与 theme 的 2x 换算为准 |
| 截图色差 | 计算样式断言 + 像素尺寸 | 记录实际 RGB |
| Figma 名称不一致 | tokenPath + display name 双重比较 | 重新生成 JSON |
| DevTools 截图 hang | 先 setDeviceMetricsOverride 再 capture | 重试，不伪造 |

## 11. 自审 8 问

1. 覆盖 AC1–AC4？是：严格 DTCG、62 组对比度、真实 DevTools 截图、Figma 双路径 1:1。
2. 单一事实源？是：tokens.json。
3. 可替换品牌？是：改 color.brand.* 后重建。
4. 可复现？是：无网络依赖，脚本 + Edge + DevTools。
5. 对比度可审计？是：脚本枚举 + 表格。
6. Figma 限制说清？是：匿名无 Variables 面板，证据以登录态截图/导出快照为准。
7. 示例页是真实小程序？DevTools 是真实模拟器截图；Web 预览仍是补充，不冒充真机。
8. 有冗余？生成物可重建，截图可重跑，校验可单跑。

## 12. 实际验证结果

- 17 项 pytest 通过：严格 DTCG、84 个映射、62 组对比度、Figma tokenPath + display name、导入 DTCG 字节一致、miniprogram-demo 主题同源、验证脚本 8/8。
- validate.py 8/8 PASS，exit 0；62 组对比度，最低 4.66:1；74 个 Figma 变量 + 74 个导入变量。
- 两轮从零验收：round1 2026-11-20T11:58:27Z、round2 11:58:32Z，均 exit 0；每轮 7 步；Web 截图 750×2261、296,124 B，哈希 8d7b49c3…。
- 微信开发者工具真实模拟器截图（488×941）与完整 IDE 截图（1564×1250），verify_devtools_evidence.py 23/23 PASS。
- 在线 Figma 导出快照：74/74 tokenPath、74/74 显示名、类型、别名、值、描述一致；collection Theme、mode Light。
- 变异演练 3/3 DETECTED：中性色改浅触发对比度失败、删除品牌映射触发 demo 未定义变量、改 Figma 名称触发 1:1 失败。
- 交付包与证据见 03-EVIDENCE.md。
