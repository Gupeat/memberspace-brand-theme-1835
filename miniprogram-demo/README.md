# miniprogram-demo

TDesign 小程序组件示例页，用于验证 theme.wxss 的品牌变量。所有文案与数据均为虚构。

## 依赖准备

仓库不提交 miniprogram_npm（体积大、可由 npm 包重建）。在 repo 根目录执行：

    mkdir -p /tmp/tdesign-miniprogram
    tar -xzf vendor/tdesign-miniprogram-1.18.0.tgz -C /tmp/tdesign-miniprogram
    mkdir -p miniprogram-demo/miniprogram_npm/tdesign-miniprogram
    cp -r /tmp/tdesign-miniprogram/package/miniprogram_dist/* miniprogram-demo/miniprogram_npm/tdesign-miniprogram/

Windows PowerShell 可用 tar 命令；也可用 7-Zip 解压 vendor 下的 tgz 与内部 tar。

## 在微信开发者工具打开

1. 导入目录 miniprogram-demo。
2. AppID 使用测试号/沙箱号（本机截图使用 wx65dda5a642890a95，libVersion 3.4.10）；没有 AppID 时选择“测试号”。
3. 编译后页面路径 pages/index/index，应看到品牌主色 #1F5EFF 的 t-button 与 t-tag。

证据：evidence/devtools/ 下的截图、run.json 与 verify.json；运行说明见 docs/WECHAT-DEVTOOLS.md。
