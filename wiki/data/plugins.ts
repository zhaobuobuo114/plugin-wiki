export interface PluginDoc {
  text: string
  link: string
}

export interface Plugin {
  id: string
  name: string
  fullName: string
  version: string
  mc: string
  status: 'stable' | 'beta' | 'wip'
  updated: string
  summary: string
  tags: string[]
  repo: string
  download: string
  docs: PluginDoc[]
}

export const statusText: Record<Plugin['status'], string> = {
  stable: '稳定',
  beta: '测试',
  wip: '开发中'
}

export const plugins: Plugin[] = [
  {
    id: 'qiantao',
    name: '[klkhk]plugin_qiandao_1.12.2',
    fullName: '[klkhk]plugin_qiandao_1.12.2',
    version: 'v1.1.4',
    mc: '1.12.2',
    status: 'stable',
    updated: '2026-10-21',
    summary: '七日周期签到，断签能补，连续有奖，金币直接进 ZPoints / PlayerPoints / Vault。',
    tags: ['签到', '补签卡', '排行榜', '经济联动', 'GUI'],
    repo: 'https://github.com/zhaobuobuo114/klkhk-plugin_qiandao',
    download: 'https://github.com/zhaobuobuo114/klkhk-plugin_qiandao/releases/latest',
    docs: [
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
