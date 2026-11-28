<!-- Profile README for HtLimite -->

<p align="center">
  <img src="./assets/profile-hero.svg" alt="HtLimite — Frontend Engineering, Full-stack Practice and AI-assisted Development" />
</p>

<h1 align="center">Hi, I'm HtLimite (Reiki)</h1>
<p align="center">前端开发 · 供应链与企业级系统 · 平时折腾全栈与 AI 工具</p>
<p align="center">
  <a href="https://wyy.hair/">博客</a> ·
  <a href="https://wyy.hair/projects/">作品集</a> ·
  <a href="https://github.com/HtLimite?tab=repositories">公开仓库</a>
</p>

## 关于我

主力做前端开发，平时写得最多的是供应链和企业级业务系统（TMS、WMS、SRM），覆盖 PC、PDA、H5、微信小程序和飞书内嵌应用——日常打交道最多的是复杂表格表单、配置化规则、ERP 对接、OAuth 鉴权以及 Git Submodule / CI/CD 这类工程交付细节。

工作之外喜欢把生活里的痛点做成能用起来的小工具，后端、服务器部署、日志监控和 AI 应用基本都是这么一路折腾出来的。个人项目和踩坑记录大多沉淀在 [技术博客](https://wyy.hair/)。

## 技术栈

| 方向 | 常用技术与工具 |
| :--- | :--- |
| **前端与多端** | React、Vue 3、TypeScript、Next.js、Umi、Vite、uni-app、微信小程序、Vant、Cocos Creator |
| **后端与存储** | Node.js、Spring Boot、FastAPI、Python、PostgreSQL（pgvector）、MySQL、Redis、Supabase、MinIO |
| **AI 与 Agent** | RAG、Embedding、Tool Calling、SSE、工作流编排、Codex、Claude Code、Antigravity、MCP、Skills |
| **工程与部署** | Git、pnpm、ESLint、GitHub Actions、Jenkins、Linux、Docker、Nginx、Caddy、Rancher、Kubernetes |
| **可观测性** | Grafana、Loki、日志分析、服务健康检查 |

> 前端是主力工作方向，后端、AI 与运维更多来自个人项目和实际排查需求。

## 折腾过的项目

### [AgentFlow-AI](https://github.com/HtLimite/AgentFlow-AI) `公开仓库`
面向 AI Agent、知识库与工作流的全栈实验项目，把常见 AI 链路做成了一套本地可跑、可验证的平台。
- 文档解析切片、RAG 问答及引用溯源，支持多模型供应商与 Prompt 评测
- Agent 工具调用、可视化工作流画布、调用审计与本地服务健康检查
- `Next.js` `TypeScript` `FastAPI` `PostgreSQL` `pgvector` `Redis` `Docker`

### [AI 书签导航](https://wyy.hair/posts/9a7b6388/) `项目笔记`
给自己做的云端书签工具，专门治一治浏览器收藏夹越攒越乱、存完就找不到的毛病。
- 支持 Chrome 书签导入并保留原目录层级、搜索筛选与游标分页
- 后台 Worker 异步抓取生成网站缩略图，带并发控制与云端同步
- `Next.js` `React` `TypeScript` `Supabase` `Vercel` `Docker`

### [脑洞侦察社](https://wyy.hair/posts/f5d41a8d/) `重构笔记`
一款微信益智小游戏，也是一次用 AI 驱动存量重构的实战——从原生 Canvas 迁到 Cocos Creator + TypeScript。
- 拆分玩法逻辑与渲染层，通过 Command、Snapshot 与领域事件约束代码边界
- 配套资源生命周期管理与自动化校验脚本，兜底高频 AI 迭代
- `Cocos Creator` `TypeScript` `Node.js` `微信小游戏` `AI Coding`

### [记忆之词](https://wyy.hair/posts/2910840a/) `项目笔记`
从大学一路重构到现在的背单词与实时对战应用，覆盖多端适配、实时通信与前后端长期维护。
- `uni-app` `Vue 3` `TypeScript` `Spring Boot` `WebSocket`

### 其他公开仓库
- **家政系统练习：** [housekeep-admin-vue](https://github.com/HtLimite/housekeep-admin-vue) · [housekeep-api](https://github.com/HtLimite/housekeep-api) · [housekeep-foundations](https://github.com/HtLimite/housekeep-foundations) · [housekeep-customer](https://github.com/HtLimite/housekeep-customer)
- **实验与存档：** [credit](https://github.com/HtLimite/credit) · [ai-gemini-report](https://github.com/HtLimite/ai-gemini-report) · [Vue](https://github.com/HtLimite/Vue) · [library](https://github.com/HtLimite/library) · [HtLimite.github.io](https://github.com/HtLimite/HtLimite.github.io)（早年 Todo List 静态页）

<sub>部分个人项目仍在迭代暂未开源，相关方案和排障记录会直接写在博客里。</sub>

## AI 协作习惯

日常深度使用 Codex、Claude Code、Antigravity，也折腾终端自动化、MCP 和 Skills。相比一次性让模型生成一大堆代码，更习惯这样做：

- 用 `AGENTS.md` 写明目录边界与约束规则，先拆任务和验收标准再动手
- 改动前先摸清现有实现，尽量保持最小范围修改，防止 Agent 顺手改崩无关逻辑
- 靠 Lint、Typecheck、单测和真实接口日志做阶段验证，不盲信生成结果
- 把高频重复操作和排障步骤沉淀成脚本或 Skills

## GitHub 统计

<p align="center">
  <img src="./assets/github-profile-stats.svg" alt="Public repository statistics and followers" />
  <img src="./assets/top-languages.svg" alt="Language shares by code bytes in public non-fork repositories" />
  <img src="./assets/github-streak.svg" alt="Contribution streak and totals for the displayed period" />
  <img src="./assets/contribution-activity.svg" alt="Daily GitHub contribution activity for the last 90 calendar days" />
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./profile-3d-contrib/profile-night-rainbow.svg" />
    <source media="(prefers-color-scheme: light)" srcset="./profile-3d-contrib/profile-green.svg" />
    <img src="./profile-3d-contrib/profile-green.svg" alt="3D GitHub contribution profile" />
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/github-contribution-grid-snake-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="./assets/github-contribution-grid-snake.svg" />
    <img src="./assets/github-contribution-grid-snake.svg" alt="GitHub contribution snake" />
  </picture>
</p>

<p align="center">
  <sub>统计仅涵盖公开仓库，由 GitHub Actions 定期更新</sub>
</p>

---

<p align="center"><b>Stay curious, keep building.</b></p>
