# 主线有限复核的复现布局

固定只读引擎输入PR23 `7a1dfbc92efa2a54bb85175cc251856bb2cdb4d3`，其原文件保持不变。复现时建立独立本地目录，在其中放同版本完整 `engine/`；把本目录ROYAL_PROBE.ts放在engine旁，把main-review-dom-probe.ts复制到engine/scripts/hero-pilot/。其余证据留在同层；不要把本研究导出加入产品模块或覆盖试点未回传代码。

命令与环境见INTAKE_REPORT。DOM脚本沿原作者dom-smoke的jsdom路径约定运行；先核当前依赖是否实际可用，缺依赖如实记录，不把缺环境写成通过。scripts中的测试导出只加到临时模块副本，原web源码不改。本次脚本使用作者合成中局并调用实际DOM处理器，未验证浏览器布局/触摸，也不声明自然完整棋谱可达。

这里保存的是主线委派审查的原证据，不替代试点的RETURN_TO_MAIN或自己新任务已读回执。修复后由试点在自己的分支记录新证据，保留这些固定旧输出。

保存的DOM复现脚本只调整一处汇总输出路径为旁侧MAIN_REVIEW_DOM_SMOKE.json，以免覆盖原作者review/hero-pilot/DOM_SMOKE.json；处理器、fixture和观察逻辑与实际运行版本相同。原实际输出证据保持不改。
