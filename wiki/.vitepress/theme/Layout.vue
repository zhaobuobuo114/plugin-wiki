<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import PluginOutline from './PluginOutline.vue'

const route = useRoute()

const isPluginsPage = computed(() => {
  const path = route.path.replace(/\.html$/, '').replace(/\/+$/, '')
  return path.endsWith('/plugins')
})
</script>

<template>
  <DefaultTheme.Layout>
    <template #aside-outline-after>
      <PluginOutline v-if="isPluginsPage" />
    </template>
  </DefaultTheme.Layout>
</template>
