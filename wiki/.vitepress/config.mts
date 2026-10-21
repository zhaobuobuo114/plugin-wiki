import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: '插件文档中心',
  description: 'Minecraft 服务端插件文档总站：安装、配置、指令、经济联动与问题排查。',
  base: '/plugin-wiki/',
  cleanUrls: true,
  appearance: 'force-dark',
  outDir: '../docs',
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/plugin-wiki/icon.svg' }],
    ['meta', { name: 'theme-color', content: '#0a0e14' }]
  ],
  themeConfig: {
    logo: '/icon.svg',
    siteTitle: '插件文档中心',
    nav: [
      { text: '插件库', link: '/plugins' },
      { text: '插件定制', link: '/custom' }
    ],
    sidebar: {
      '/qiantao/': [
        {
          text: '[klkhk]plugin_qiandao_1.12.2',
          items: [
            { text: '插件介绍', link: '/qiantao/' },
            { text: '安装部署', link: '/qiantao/install' },
            { text: '指令与权限', link: '/qiantao/commands' },
            { text: '配置详解', link: '/qiantao/config' },
            { text: '经济联动', link: '/qiantao/economy' },
            { text: '常见问题', link: '/qiantao/faq' },
            { text: '更新日志', link: '/qiantao/changelog' }
          ]
        }
      ]
    },
    search: {
      provider: 'local',
      options: {
        detailedView: true,
        translations: {
          button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' },
          modal: {
            displayDetails: '展开详情',
            resetButtonTitle: '清空',
            backButtonTitle: '返回',
            noResultsText: '没有找到相关内容',
            footer: {
              selectText: '选择',
              selectKeyAriaLabel: '回车',
              navigateText: '切换',
              navigateUpKeyAriaLabel: '上',
              navigateDownKeyAriaLabel: '下',
              closeText: '关闭',
              closeKeyAriaLabel: '退出'
            }
          }
        }
      }
    },
    outline: { level: [2, 3], label: '本页目录' },
    docFooter: { prev: false, next: false },
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单',
    darkModeSwitchLabel: '主题',
    lastUpdated: { text: '最后更新' },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/zhaobuobuo114/plugin-wiki' }
    ],
    footer: {
      message: '承接所有版本 Minecraft 服务端插件定制',
      copyright: 'QQ 1071576270 · 1071576270@qq.com'
    }
  }
})
