# 在线 Figma 交付（#1835 v2）

## 1. 文件与共享

- 文件：MemberSpace Brand Theme 1835 - v2
- 链接：https://www.figma.com/design/U3n0qOCgViDDfdSnOWIw5n/MemberSpace-Brand-Theme-1835---v2?node-id=0-1
- 共享：Anyone / can edit；匿名可查看画布。匿名视图不显示 Variables 编辑面板，这是 Figma 的权限设计，不是文件缺变量。
- 变量：collection Theme、mode Light、74 个变量（color 38 / number 28 / string 8）。

## 2. 导入源

- figma/Light.tokens.json：Figma Variables 导入文件，嵌套 DTCG；文件名决定 mode 名 Light。
- figma/figma-import.tokens.json：同一份数据的通用文件名副本，与 Light.tokens.json 字节相同。
- 生成方式：python scripts/build.py 从 tokens.json 生成，不手改。
- 尺寸按 2rpx = 1px 换算；颜色导出为 sRGB；别名保留为 {path} 引用。

## 3. 重新导入（Figma 网页版/桌面端）

1. 打开文件 → Variables 面板。
2. Import variables → 选择 figma/Light.tokens.json。
3. 如有旧集合，先确认新集合变量数；把新集合重命名为 Theme，mode 保持 Light。
4. 应看到 74 个变量；分组为 color/font/radius/space/shadow/motion。Figma 显示名是 `color/brand/primary` 这类 `/` 分组路径，与 tokens.json 的点分路径 `color.brand.primary` 逐段 1:1；`scripts/verify_figma_export.py` 同时校验 tokenPath 点分集合与显示名集合。
5. 设计稿中按名称绑定变量。

## 4. 导出与校验

1. Variables 面板 → Export modes → 导出 Theme.zip。
2. 覆盖 evidence/figma-online/Theme.zip，解包出 Light.tokens.json 覆盖同目录文件。
3. 运行 python scripts/verify_figma_export.py。
4. 结果写入 evidence/figma-online/verify.json：74/74 tokenPath 与 74/74 显示名分别 1:1、类型计数 38/28/8、别名、值、描述一致，exit 0。

当前校验结果（2026-11-19）：

- checked 74；counts color 38 / number 28 / string 8；missing/extra 0；value/description mismatch 0。
- Theme.zip SHA-256：f9bc2c8c35a798fca9d9fb7097868645870e1930f0d0f1f1a00e4673cb091ccc（28,607 B）。
- 解包 Light.tokens.json SHA-256：7ee627941bc69c1699b66a4cce0cf57efebda79175db873f20ffc60c61b56ed8。
- figma-online-final.png SHA-256：f611bec12d0339f15fd9d86e7c66024ee07d74fc86953b78b70dbef34cfcb699（1280x720）。

## 5. 匿名访问校验

- 默认 headless UA 访问 Figma 会被 CloudFront 403，不能据此判断文件私有。
- 用 headed Edge + 真实桌面 UA 打开 clean URL：HTTP 200、title 含 MemberSpace Brand Theme 1835、页面出现 Sign up to comment 提示，说明匿名可查看。
- 证据截图：evidence/figma-online/figma-anon-public.png。

## 6. 限制

- Figma 免费版：变量、共享、导出可用；匿名查看者不能打开 Variables 编辑面板。
- 在线文件是手工导入的交付物；tokens.json 变化后必须重新导入/导出，verify_figma_export.py 会拦截过期快照。
- 当前只有 Light 模式；没有暗色模式、多品牌切换或 Code Connect。
- 不包含客户数据；所有 token 值均为虚构品牌值。

## 7. 相关文件

- figma/figma-variables.json：机器可读变量定义（74 项）。
- figma/create-variables.js + figma/manifest.json：桌面插件备选路径（非破坏性创建/更新）。
- docs/FIGMA-VARIABLES.md：74 行 tokenPath（点分）与 Figma 显示名（`/` 分组）对照。
- evidence/figma-online/README.md：证据目录说明与哈希。
