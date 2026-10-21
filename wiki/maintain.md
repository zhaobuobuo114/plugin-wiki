---
title: 文档维护指南
---

# 文档维护指南

写给以后要加插件的自己。站点是 VitePress 生成的静态站，没有数据库、没有后台，改完跑一条命令就发布。

## 一、结构

```text
wiki/                        VitePress 源文件
├─ .vitepress/
│  ├─ config.mts             导航、侧边栏、搜索、页脚
│  └─ theme/
│     ├─ index.ts            注册自定义组件
│     ├─ custom.css          配色与组件样式
│     └─ PluginLibrary.vue   插件库列表组件
├─ data/plugins.ts           插件数据（名称、版本、标签、文档链接）
├─ index.md                  首页
├─ plugins.md                插件库
├─ custom.md                 插件定制
├─ maintain.md               本文
└─ qiantao/                  每个插件一个目录
   ├─ index.md
   ├─ install.md
   └─ ...

site/                        构建产物（GitHub Pages 发布目录）
```

侧边栏只在插件页面出现，内容是**当前插件**的页面。首页、插件库、定制页没有侧边栏 —— 插件再多，左侧也不会变长。

## 二、新增一个插件

### 1. 建页面

```bash
mkdir wiki/dailyquest
```

复制 `wiki/qiantao/` 里的 Markdown 改内容即可。每个文件顶部加 frontmatter：

```markdown
---
title: 安装部署
---
```

### 2. 登记数据

编辑 `wiki/data/plugins.ts`，往 `plugins` 数组里加一项：

```ts
{
  id: 'dailyquest',
  name: 'DailyQuest',
  fullName: 'DailyQuest 每日任务',
  version: 'v1.0.0',
  mc: '1.12.2',
  status: 'stable',          // stable | beta | wip
  updated: '2026-10-21',
  summary: '一句话说清它解决什么问题，别写形容词。',
  tags: ['任务', '活跃度', '奖励'],
  repo: 'https://github.com/you/DailyQuest',
  download: 'https://github.com/you/DailyQuest/releases/latest',
  docs: [
    { text: '插件介绍', link: '/dailyquest/' },
    { text: '安装部署', link: '/dailyquest/install' },
    { text: '指令与权限', link: '/dailyquest/commands' },
    { text: '常见问题', link: '/dailyquest/faq' }
  ]
}
```

插件库条目、状态标签、文档链接都会自动生成，不用碰 HTML。

### 3. 加侧边栏

编辑 `wiki/.vitepress/config.mts` 的 `themeConfig.sidebar`：

```ts
sidebar: {
  '/qiantao/': [ /* ... */ ],
  '/dailyquest/': [
    {
      text: 'DailyQuest 每日任务',
      items: [
        { text: '插件介绍', link: '/dailyquest/' },
        { text: '安装部署', link: '/dailyquest/install' },
        { text: '指令与权限', link: '/dailyquest/commands' },
        { text: '常见问题', link: '/dailyquest/faq' }
      ]
    }
  ]
}
```

### 4. 构建发布

```bash
npm run build
git add -A
git commit -m "docs: 新增 DailyQuest 文档"
git push
```

产物在 `site/`，推送后 GitHub Pages 自动发布，约一分钟。

## 三、写作规范

- **先给结论，再给原因。** 「升级前先删 config.yml」放前面，为什么放后面。
- **配置项写清默认值**，读者不用回去翻文件。
- **命令用表格**：指令 / 作用 / 权限，三列够了。
- **坑单独标出来**，别埋在段落里。
- **站内链接用绝对路径**，如 `[配置详解](/qiantao/config)`，VitePress 会自动加 base。
- **外部链接自动新开标签页**，不用手写 `target`。

## 四、本地预览

```bash
npm install        # 第一次
npm run dev        # 开发预览，热更新
npm run build      # 构建到 site/
npm run preview    # 预览构建结果
```

## 五、常见问题

**改了 Markdown 线上没变？**
先 `npm run build`，再提交 `site/`。只改 `wiki/` 不构建，线上不会变。

**页面 404？**
检查 `docs` 里的 `link` 是否与实际文件路径一致；`index.md` 对应目录根路径。

**插件条目顺序不对？**
`plugins` 数组的顺序就是显示顺序。

**想换主色？**
改 `wiki/.vitepress/theme/custom.css` 顶部的 `--vp-c-brand-1/2/3`。
