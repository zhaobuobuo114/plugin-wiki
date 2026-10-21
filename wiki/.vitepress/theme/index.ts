import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import PluginLibrary from './PluginLibrary.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('PluginLibrary', PluginLibrary)
  }
} satisfies Theme
