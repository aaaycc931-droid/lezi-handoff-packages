# 当前图稿复现

从包根目录执行node scripts/compose-ui-from-layers.cjs；需sharp（可通过CODEX_PRIMARY_RUNTIME_NODE_MODULES指定已安装目录），输出到rerenders/，不覆盖images/。仅复现现有版本，不表示新图自动获批。

验证示例：python scripts/verify_pixel_diff.py inherited_dispatch/ui-return/images/lezi-bluetooth-B1-v1.png images/lezi-bluetooth-B1-v2.png --regions evidence/b1-v2-font-pixel-check.json。需Pillow。核对母版摘要可加--expected-source-sha256，精确保护矩形内部纹理可加二值蒙版--mask。

render_sources_original/保持生成当时脚本字节，里面绝对工作路径仅作历史证据；使用归档底层＋文字层复现更稳妥，不重新抹字。不把局部估计底层称为原始隐藏纸纹。
