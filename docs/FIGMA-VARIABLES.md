# Figma 变量对照表

在线 Figma 文件（viewer 可看）：https://www.figma.com/design/U3n0qOCgViDDfdSnOWIw5n/MemberSpace-Brand-Theme-1835---v2?node-id=0-1

该文件由 Figma Variables 导入 figma/Light.tokens.json 生成：collection Theme、mode Light、74 个变量；Figma 以 / 分隔嵌套分组，下表 Figma 变量名就是实际显示名，token 路径是 tokens.json 的点分路径，两者逐段一一对应（仅分隔符不同）。
figma/figma-import.tokens.json 为同一 DTCG 数据的通用文件名副本；figma/figma-variables.json 与 figma/create-variables.js 是机器可读定义和桌面插件备选路径，二者也统一使用 / 显示名，并保留 tokenPath 点分路径。

命名规范：Figma 显示名 = token 点分路径将 . 替换为 /；例如 color.brand.primary <=> color/brand/primary。尺寸按 2rpx = 1px 换算为 Figma 数值；别名保留为 {path} 引用。

| # | token 路径 | Figma 变量名（/ 分组） | Figma 类型 | 值 | 说明 |
| ---: | --- | --- | --- | --- | --- |
| 1 | color.brand.primary | color/brand/primary | COLOR | #1F5EFF | 品牌主色 |
| 2 | color.brand.hover | color/brand/hover | COLOR | #1748D6 | 主色悬停 |
| 3 | color.brand.active | color/brand/active | COLOR | #1239B0 | 主色按下 |
| 4 | color.brand.light | color/brand/light | COLOR | #F1F4FF | 主色浅底 |
| 5 | color.brand.lightHover | color/brand/lightHover | COLOR | #EDF1FF | 主色浅底悬停 |
| 6 | color.brand.disabled | color/brand/disabled | COLOR | #B5C7FF | 品牌色禁用态 |
| 7 | color.accent.primary | color/accent/primary | COLOR | #0F766E | 辅助色 |
| 8 | color.accent.light | color/accent/light | COLOR | #E6F4F1 | 辅助色浅底 |
| 9 | color.neutral.50 | color/neutral/50 | COLOR | #F8FAFC | 中性 50 |
| 10 | color.neutral.100 | color/neutral/100 | COLOR | #F1F5F9 | 中性 100 |
| 11 | color.neutral.200 | color/neutral/200 | COLOR | #E2E8F0 | 中性 200 |
| 12 | color.neutral.300 | color/neutral/300 | COLOR | #CBD5E1 | 中性 300 |
| 13 | color.neutral.400 | color/neutral/400 | COLOR | #94A3B8 | 中性 400 |
| 14 | color.neutral.500 | color/neutral/500 | COLOR | #57677C | 中性 500 |
| 15 | color.neutral.600 | color/neutral/600 | COLOR | #475569 | 中性 600 |
| 16 | color.neutral.700 | color/neutral/700 | COLOR | #334155 | 中性 700 |
| 17 | color.neutral.800 | color/neutral/800 | COLOR | #1E293B | 中性 800 |
| 18 | color.neutral.900 | color/neutral/900 | COLOR | #0F172A | 中性 900 |
| 19 | color.text.primary | color/text/primary | COLOR | #0F172A | 主文字（引用 neutral.900） |
| 20 | color.text.secondary | color/text/secondary | COLOR | #334155 | 二级文字（引用 neutral.700） |
| 21 | color.text.tertiary | color/text/tertiary | COLOR | #475569 | 三级文字（引用 neutral.600） |
| 22 | color.text.muted | color/text/muted | COLOR | #57677C | 弱化文字（引用 neutral.500，全浅底 >= 4.5:1） |
| 23 | color.text.anti | color/text/anti | COLOR | #FFFFFF | 反白文字 |
| 24 | color.bg.page | color/bg/page | COLOR | #F8FAFC | 页面背景 |
| 25 | color.bg.surface | color/bg/surface | COLOR | #FFFFFF | 卡片/容器背景 |
| 26 | color.bg.surfaceAlt | color/bg/surfaceAlt | COLOR | #F8FAFC | 次级容器背景（引用 neutral.50） |
| 27 | color.bg.inverse | color/bg/inverse | COLOR | #0F172A | 反色背景 |
| 28 | color.border.default | color/border/default | COLOR | #E2E8F0 | 默认边框（引用 neutral.200） |
| 29 | color.border.strong | color/border/strong | COLOR | #CBD5E1 | 强调边框（引用 neutral.300） |
| 30 | color.semantic.success | color/semantic/success | COLOR | #0E7A5F | 成功 |
| 31 | color.semantic.successLight | color/semantic/successLight | COLOR | #E7F7F0 | 成功浅底 |
| 32 | color.semantic.warning | color/semantic/warning | COLOR | #9A5B00 | 警告 |
| 33 | color.semantic.warningLight | color/semantic/warningLight | COLOR | #FFF4E5 | 警告浅底 |
| 34 | color.semantic.error | color/semantic/error | COLOR | #B42318 | 错误 |
| 35 | color.semantic.errorLight | color/semantic/errorLight | COLOR | #FEE9E9 | 错误浅底 |
| 36 | color.semantic.info | color/semantic/info | COLOR | #0B5C8A | 信息 |
| 37 | color.semantic.infoLight | color/semantic/infoLight | COLOR | #E6F3FB | 信息浅底 |
| 38 | color.focus.ring | color/focus/ring | COLOR | #1F5EFF | 焦点环（实心，避免透明导致不可见） |
| 39 | font.family.sans | font/family/sans | STRING | PingFang SC, Helvetica Neue, Microsoft YaHei, sans-serif | 系统中文字体栈 |
| 40 | font.size.24 | font/size/24 | FLOAT | 12 | 辅助说明 |
| 41 | font.size.28 | font/size/28 | FLOAT | 14 | 正文/基础 |
| 42 | font.size.32 | font/size/32 | FLOAT | 16 | 小标题 |
| 43 | font.size.36 | font/size/36 | FLOAT | 18 | 标题 |
| 44 | font.size.40 | font/size/40 | FLOAT | 20 | 大标题 |
| 45 | font.size.48 | font/size/48 | FLOAT | 24 | 页面主标题 |
| 46 | font.lineHeight.24 | font/lineHeight/24 | FLOAT | 18 | 24 号字行高 |
| 47 | font.lineHeight.28 | font/lineHeight/28 | FLOAT | 20 | 28 号字行高 |
| 48 | font.lineHeight.32 | font/lineHeight/32 | FLOAT | 22 | 32 号字行高 |
| 49 | font.lineHeight.36 | font/lineHeight/36 | FLOAT | 24 | 36 号字行高 |
| 50 | font.lineHeight.40 | font/lineHeight/40 | FLOAT | 28 | 40 号字行高 |
| 51 | font.lineHeight.48 | font/lineHeight/48 | FLOAT | 32 | 48 号字行高 |
| 52 | font.weight.regular | font/weight/regular | FLOAT | 400 | 常规 |
| 53 | font.weight.medium | font/weight/medium | FLOAT | 500 | 中等 |
| 54 | font.weight.semibold | font/weight/semibold | FLOAT | 600 | 半粗 |
| 55 | radius.8 | radius/8 | FLOAT | 4 | 小圆角 |
| 56 | radius.16 | radius/16 | FLOAT | 8 | 默认圆角 |
| 57 | radius.24 | radius/24 | FLOAT | 12 | 大圆角 |
| 58 | radius.full | radius/full | FLOAT | 4999.5 | 全圆 |
| 59 | space.16 | space/16 | FLOAT | 8 | 紧凑间距 |
| 60 | space.24 | space/24 | FLOAT | 12 | 默认间距 |
| 61 | space.32 | space/32 | FLOAT | 16 | 块间距 |
| 62 | space.48 | space/48 | FLOAT | 24 | 大块间距 |
| 63 | space.64 | space/64 | FLOAT | 32 | 页面分区 |
| 64 | shadow.sm | shadow/sm | STRING | 0rpx 2rpx 8rpx 0rpx rgba(15,23,42,0.059) | 轻阴影 |
| 65 | shadow.md | shadow/md | STRING | 0rpx 8rpx 24rpx 0rpx rgba(15,23,42,0.102) | 中阴影 |
| 66 | shadow.lg | shadow/lg | STRING | 0rpx 16rpx 48rpx 0rpx rgba(15,23,42,0.141) | 重阴影 |
| 67 | motion.duration.fast | motion/duration/fast | FLOAT | 120 | 快速反馈 |
| 68 | motion.duration.base | motion/duration/base | FLOAT | 200 | 常规过渡 |
| 69 | motion.duration.moderate | motion/duration/moderate | FLOAT | 240 | 中速过渡 |
| 70 | motion.duration.slow | motion/duration/slow | FLOAT | 320 | 大范围过渡 |
| 71 | motion.easing.standard | motion/easing/standard | STRING | cubic-bezier(0.2, 0, 0, 1) | 标准缓动 |
| 72 | motion.easing.emphasized | motion/easing/emphasized | STRING | cubic-bezier(0.3, 0, 0, 1) | 强调缓动 |
| 73 | motion.easing.decelerate | motion/easing/decelerate | STRING | cubic-bezier(0, 0, 0.15, 1) | 减速缓动（进入） |
| 74 | motion.easing.accelerate | motion/easing/accelerate | STRING | cubic-bezier(0.82, 0, 1, 0.9) | 加速缓动（离开） |
