# 插件文档中心

Minecraft 服务端插件的文档总站。**只放文档，不放插件源码** —— 每个插件的代码、构建、Release 都在自己的仓库里，这里负责把它们讲清楚。

**在线地址**：<https://zhaobuobuo114.github.io/plugin-wiki/>

基于 [VitePress](https://vitepress.dev/) 构建，深色主题，内置全文搜索（按 `/` 或 `Ctrl+K`）。

## 这里有什么

- **插件库**：所有在维护的插件，含版本、适用服务端、状态、标签，以及每个插件的完整文档入口
- **文档页**：安装部署、指令权限、配置详解、经济联动、常见问题、更新日志
- **全文搜索**：标题、正文、配置项都能搜
- **插件定制**：接单范围、交付内容与联系方式

当前收录：

| 插件 | 适用版本 | 版本 | 文档 |
| --- | --- | --- | --- |
| [klkhk]plugin_qiandao_1.12.2 | 1.12.2 | v1.1.4 | [查看](https://zhaobuobuo114.github.io/plugin-wiki/qiantao/) |

## 仓库结构

```text
wiki/                       VitePress 源文件
├─ .vitepress/
│  ├─ config.mts            导航、侧边栏、搜索配置
│  └─ theme/
│     ├─ index.ts           注册组件
│     ├─ custom.css         配色与组件样式（青蓝主题）
│     └─ PluginLibrary.vue  插件库列表组件
├─ data/plugins.ts          插件数据源
├─ index.md                 首页
├─ plugins.md               插件库
├─ custom.md                插件定制
├─ maintain.md              维护指南
└─ qiantao/                 每个插件一个目录

docs/                       构建产物（GitHub Pages 发布目录）
```

## 本地开发

```bash
npm install
npm run dev       # http://localhost:5173/plugin-wiki/
npm run build     # 输出到 docs/
npm run preview   # 预览构建结果
```

## 新增插件

1. `wiki/<id>/` 下新建 Markdown 页面
2. 在 `wiki/data/plugins.ts` 的 `plugins` 数组登记（名称、版本、标签、文档链接）
3. 在 `wiki/.vitepress/config.mts` 的 `sidebar` 加一个 `'/<id>/'` 分组
4. `npm run build`，提交 `wiki/` 与 `docs/`

详细字段说明见站内「文档维护指南」。

## 发布

推送到 `main` 后，GitHub Pages 从 `docs/` 目录发布，约一分钟生效。

---

插件定制：QQ `1071576270` · 邮箱 `1071576270@qq.com`
