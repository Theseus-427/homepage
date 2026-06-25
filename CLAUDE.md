# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

史浩均的学术个人主页。基于 Astro 5 纯静态构建，部署在 GitHub Pages 子路径 `/homepage/`，后续计划绑定自定义域名。

- 仓库: `Theseus-427/homepage`
- 线上: https://theseus-427.github.io/homepage/

## 常用命令

```bash
npm run dev       # 开发服务器，http://localhost:4321，热重载
npm run build     # 生产构建 → dist/
npm run preview   # 本地预览 dist/ 构建产物
```

## 架构

```
src/pages/
  index.astro      # 首页，单页包含所有板块（Research/Publications/Projects/Experience/Contact）
  cv.astro         # 简历页，window.print() 打印 PDF
  projects.astro   # 项目展示
src/styles/
  global.css       # 全局样式，三个页面共享
public/assets/     # 静态资源，原样复制到 dist/
```

所有页面内容（出版物、项目、经历等）定义在 `.astro` 文件 frontmatter 的 JS 对象中，模板部分遍历渲染。

## 关键规则：所有内部路径必须用 BASE_URL

**这是本项目最重要的规则。** Astro 的 `base` 配置不会自动转换 `.astro` 模板中手写的 `href="/..."` 或 `src="/..."`。所有内部路径必须用 `import.meta.env.BASE_URL` 拼接：

```astro
---
const base = import.meta.env.BASE_URL;  // 当前为 "/homepage/"，自定义域名时变 "/"
---

<!-- 正确 -->
<a href={`${base}cv/`}>CV</a>
<img src={`${base}assets/photo.png`} />

<!-- 错误 — 子路径下会 404 -->
<a href="/cv/">CV</a>
<img src="/assets/photo.png" />
```

同样适用于 `public/` 目录下的静态资源引用和 CSS 中的 `url()`。

## 配置

`astro.config.mjs`:
- `site`: `"https://theseus-427.github.io"` — 绑定自定义域名后修改
- `base`: `"/homepage/"` — 项目站点子路径，自定义域名后删除
- `output`: `"static"` — 纯静态生成

绑定自定义域名时：删掉 `base`，`site` 改为新域名，`BASE_URL` 自动变为 `/`，所有路径无需改代码。

## 部署

push 到 `main` 分支 → GitHub Actions 自动构建并部署到 Pages。Workflow 在 `.github/workflows/deploy.yml`。

如需手动触发 Pages 创建（首次或重置后）：
```bash
gh api repos/Theseus-427/homepage/pages -X POST -f build_type=workflow
```

## 开发笔记

`dev-notes.md` 记录了踩过的坑和解决方案，遇到新问题时参考并更新。
