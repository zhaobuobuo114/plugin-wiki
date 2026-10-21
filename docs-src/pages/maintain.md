# 文档维护指南

这份文档写给以后要往站点里加插件的自己。整套站点是静态生成的：没有数据库，没有后台，改完跑一条命令就发布。

---

## 一、站点是怎么工作的

```text
docs-src/                 文档源文件（编辑这里）
├─ site.json              站点配置：导航分组 + 插件清单
├─ pages/
│  ├─ home.md             首页（开屏介绍）
│  ├─ plugins.md          插件库
│  ├─ custom.md           插件定制
│  ├─ maintain.md         本文
│  ├─ _template/          新插件模板
│  └─ qiantao/            每个插件一个目录
│     ├─ intro.md
│     ├─ install.md
│     └─ ...

tools/build_wiki.py       构建：Markdown → docs/ 静态站
docs/                     GitHub Pages 发布目录（自动生成，不要手改）
```

侧边栏只放固定入口：首页、插件库、插件定制、维护指南。**插件的页面不进侧边栏**，而是收在插件库里，进入插件后由顶部页签切换 —— 插件再多，左边也不会变长。

构建命令：

```bash
python tools/build_wiki.py
```

## 二、新增一个插件（三步）

### 第 1 步：复制模板

```bash
cp -r docs-src/pages/_template docs-src/pages/dailyquest
```

模板里有四个文件：介绍、安装、指令、FAQ。改内容即可。

### 第 2 步：在 `site.json` 的 `plugins` 里登记

```json
{
  "id": "dailyquest",
  "name": "DailyQuest",
  "fullName": "DailyQuest 每日任务",
  "version": "v1.0.0",
  "mc": "1.12.2",
  "status": "stable",
  "updated": "2026-10-21",
  "summary": "一句话说清它解决什么问题，别写形容词。",
  "tags": ["任务", "活跃度", "奖励"],
  "repo": "https://github.com/you/DailyQuest",
  "download": "https://github.com/you/DailyQuest/releases/latest",
  "pages": [
    { "title": "插件介绍", "short": "介绍", "slug": "dailyquest/index.html", "source": "dailyquest/intro.md", "alias": ["DailyQuest-介绍"] },
    { "title": "安装部署", "short": "安装", "slug": "dailyquest/install.html", "source": "dailyquest/install.md", "alias": ["DailyQuest-安装"] },
    { "title": "指令与权限", "short": "指令", "slug": "dailyquest/commands.html", "source": "dailyquest/commands.md", "alias": ["DailyQuest-指令"] },
    { "title": "常见问题", "short": "FAQ", "slug": "dailyquest/faq.html", "source": "dailyquest/faq.md", "alias": ["DailyQuest-FAQ"] }
  ]
}
```

| 字段 | 作用 |
| --- | --- |
| `status` | `stable` / `beta` / `wip`，显示为「稳定 / 测试 / 开发中」 |
| `repo` / `download` | 该插件自己的仓库与发布页，条目上的「源码 / 下载」用 |
| `pages` | 该插件的全部文档页，顺序就是页签顺序 |
| `short` | 页签上的短名，不填就用 `title` |
| `slug` | 生成的 HTML 路径，第一页习惯用 `index.html` |
| `source` | 对应的 Markdown 文件（相对 `pages/`） |
| `alias` | 站内链接别名，写 `[安装](DailyQuest-安装)` 就能跳 |

登记完，插件库条目、文档页签、搜索索引、首页统计都会自动生成。

### 第 3 步：构建并发布

```bash
python tools/build_wiki.py
git add -A
git commit -m "docs: 新增 DailyQuest 文档"
git push
```

推送后 GitHub Pages 自动重新发布，大约一分钟。

## 三、页面里能用的占位符

在 Markdown 里单独一行写占位符，构建时替换成生成的 HTML（前后要留空行）：

| 占位符 | 生成内容 |
| --- | --- |
| `[[STATS]]` | 插件数 / 文档数 / 最近更新 |
| `[[PLUGINS]]` | 带搜索框的插件条目列表（插件库用） |
| `[[META:dailyquest]]` | 该插件的版本、适用版本、状态、更新时间、源码与下载 |

首页只用 `[[STATS]]`，不再重复列插件 —— 插件一律去插件库看。

## 四、写作规范

- **先给结论，再给原因**。比如「升级前先删 config.yml」放在前面，为什么放后面。
- **配置项写清默认值**，读者不用回去翻文件。
- **命令用表格**：指令 / 作用 / 权限，三列够了。
- **坑要标出来**。容易翻车的地方单独写一句，别埋在段落里。
- **站内链接用别名**，如 `[配置详解](QianDao-配置详解)`，构建时自动转成正确路径。
- **外部链接自动新开标签页**，不用手写 `target`。

## 五、本地预览

直接双击 `docs/index.html` 能看排版；搜索和插件筛选依赖 `fetch`，要起个本地服务：

```bash
python -m http.server 8000 -d docs
```

然后访问 `http://localhost:8000`。

## 六、常见问题

**改了 Markdown，网站没变？**
先跑 `python tools/build_wiki.py`，再提交 `docs/`。只改 `docs-src/` 不构建，线上不会变。

**页面 404？**
检查 `slug` 与生成路径是否一致，`source` 文件是否存在。

**插件页签顺序不对？**
`pages` 数组的顺序就是页签顺序。

**想换配色？**
改 `docs-src/assets/style.css` 顶部的 CSS 变量（`--accent`、`--bg`、`--panel`）。

**条目上的版本号和实际不符？**
改 `plugins[].version`，这是唯一数据源。

---

[返回首页](Home) · [插件库](插件总览)
