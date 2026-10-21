# 插件文档中心

Minecraft 服务端插件的文档总站。**只放文档，不放插件源码** —— 每个插件的代码、构建、Release 都在自己的仓库里，这里负责把它们讲清楚。

**在线地址**：<https://zhaobuobuo114.github.io/plugin-wiki/>

## 这里有什么

- 插件库：所有在维护的插件，含版本、适用服务端、状态与标签
- 每个插件一套完整文档：安装部署、指令权限、配置详解、经济联动、常见问题、更新日志
- 全文搜索（按 `/` 或 `Ctrl+K`）、侧边栏导航、深色主题、移动端适配

当前收录：

| 插件 | 适用版本 | 版本 | 文档 |
| --- | --- | --- | --- |
| QianDao 签到插件 | 1.12.2 | v1.1.4 | [查看](https://zhaobuobuo114.github.io/plugin-wiki/qiantao/) |

## 仓库结构

```text
docs-src/                 文档源文件
├─ site.json              站点配置：插件清单、导航分组
├─ pages/                 Markdown 页面（每个插件一个目录）
└─ assets/                CSS / JS / 图标

tools/build_wiki.py       构建脚本：Markdown → docs/
docs/                     GitHub Pages 发布目录（自动生成，不要手改）
```

## 本地构建

需要 Python 3 与 `markdown`：

```bash
python -m pip install markdown
python tools/build_wiki.py
python -m http.server 8000 -d docs
```

访问 `http://localhost:8000`。搜索与筛选依赖 `fetch`，所以要起本地服务，不能直接双击 HTML。

## 新增一个插件

1. 在 `docs-src/site.json` 的 `plugins` 里登记（名称、版本、适用服务端、简介、标签、文档路径、仓库与下载地址）
2. 复制 `docs-src/pages/_template/` 到 `docs-src/pages/<id>/`，改内容
3. 在 `site.json` 的 `groups` 里加一个可折叠分组
4. `python tools/build_wiki.py`，提交并推送

首页卡片、插件库、导航、搜索索引都会自动更新，不需要手写 HTML。详细字段说明见站内「文档维护指南」。

## 发布

Push 到 `main` 后 GitHub Pages 自动重新构建，约一分钟生效。

---

插件定制：QQ `1071576270` · 邮箱 `1071576270@qq.com`
