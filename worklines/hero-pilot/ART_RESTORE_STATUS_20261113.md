# 司衡原工程恢复与发布断点｜2026-11-13

原工作树实际可访问，本轮只读检查后复制到隔离目录。没有重画人物、重建七个实现文件或重新编码四张导出；所有原实现/导出SHA与旧ART_VALIDATION/ART_ASSET_MANIFEST一致。原三个stdout日志也已找到，SHA逐一匹配旧ART_RUN_LOG记录。原工作树保留未动。

## 实际找回

- 七个实现文件：web/hero-art.ts、web/app.ts、web/style.css、scripts/serve-web.ts、scripts/hero-pilot/dom-smoke.ts、scripts/hero-pilot/package-art.cjs、scripts/hero-pilot/verify-art.cjs。
- 原生成母版：art/hero-pilot/siheng-portrait-v1.png、siheng-avatar-master-v1.png；提示词与README同目录。
- 原WebP：web/assets/hero-pilot/siheng-portrait-v1.webp（768×1152，124242 bytes）；siheng-avatar-64-v1.webp（1834）、128（5188）、256（14694）。合计145958 bytes，约142.5 KiB。
- 原验证正文与检查板：review/hero-pilot/ART_VALIDATION.json、ART_ASSET_MANIFEST.json、ART_DELIVERY_CHECK.json、ART_RUN_LOG.txt、ART_QA_CONTACT.png。
- 三份原日志与四份本轮复核日志：review/hero-pilot/art-recovery-logs/。恢复证据：review/hero-pilot/ART_RECOVERY.json。日志原被.gitignore排除，本轮已显式纳入待发布清单。

## 两张用户上传原图的核对

精确原文件名沿用前收束。头像与原生成母版解码成RGBA后完全一致，PNG编码/字节数不同。立绘alpha通道完全一致，RGB原字节不完全相同；其中含透明区差异。按公共alpha合成到相同任意底色，浮点RGB最大差异0.9961/255；视觉检查为同一人物与剪影，不推定未证的编码成因。保留原工作树母版与四张原导出，上传原件也完整保留；不把两版写成字节相同。公开记录不放私有文件ID、私有链接或上传原件哈希。

## 本轮实际复核

| 检查 | 结果 |
| --- | --- |
| 相关Web测试（web-gameplay-v4、web-layout、web-messages） | 56通过，0失败 |
| 原生产模块DOM交互脚本 | 14通过；技能段用明确合成中局，不冒充真人或浏览器 |
| npm run build:web | 通过；最终构建在DOM脚本结束后执行，排除临时测试钩子 |
| verify-art.cjs | 六个文件身份、四个构建复制及四个实际HTTP 200/MIME/哈希通过 |
| 48/64/96px检查板 | 已实际查看浅/深两底，面容与深灰/米白/深青色块可辨 |

1025全套、18局演练、155换轨回归、三项王安全探针没有重跑，历史证据继续绑定原版本。真实浏览器画面/触摸、真人强度、全面独立QA和动画仍未完成。

## 已保全与未发布

完整私有恢复包：`siheng-art-recovery-20261113.zip`。包含完整engine源码快照、31个增量文件清单、两个用户上传PNG原件、原/新日志；排除.git、dist与外部依赖。已实测ZIP CRC和增量SHA，且持久保存成功。文件库按精确文件名即可恢复；公共GitHub不记录私有ID。

自动审批审核拒绝了向公开仓库上传64px头像blob，理由为仓库及图片披露授权未确立。随后已核实两仓库属于aaaycc931-droid、公开且连接有push权限；历史授权支持自主制作/实现/保存，但未取得审核要求的明确图片公开披露确认。没有改道、重试图片上传或借文本夹带图片；本次只更新获授权的交接状态文字。

因此引擎专属分支与draft PR23仍为`5ab688c96f4960aad70467e7e4c15c21dc55a2e1`，没有新美术提交。恢复包和本地验证不等于仓库发布、主线接收或上线。目标仅为`aaaycc931-droid/jieqi-engine`的`codex/autonomous-hero-01-20261113`，不合并部署。

## 下一步

明确允许将包内司衡生成母版、运行时图片、检查板及配套工程提交到上述公开仓库后，读取最新HEAD，核恢复清单，增量发布并逐项读回，更新PR23与本线状态。无需再找图、重建代码或无理由重跑本批测试；真人/浏览器等未验项独立继续。主线接收由主线自行回执。
