<script setup lang="ts">
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'
import { plugins, sortedPlugins, statusText } from '../../data/plugins'

const keyword = ref('')

const filtered = computed(() => {
  const q = keyword.value.trim().toLowerCase()
  if (!q) return sortedPlugins
  return sortedPlugins.filter((p) =>
    [p.name, p.fullName, p.summary, p.mc, ...p.tags]
      .join(' ')
      .toLowerCase()
      .includes(q)
  )
})

function docLink(link: string) {
  return withBase(link)
}
</script>

<template>
  <div class="plugin-lib">
    <div class="pl-filter">
      <input
        v-model="keyword"
        type="search"
        placeholder="搜插件名或标签，比如「签到」「经济」"
        aria-label="筛选插件"
      />
      <span class="pl-count">{{ filtered.length }} / {{ plugins.length }}</span>
    </div>

    <TransitionGroup name="pl" tag="div" class="pl-list">
    <article v-for="p in filtered" :id="'plugin-' + p.id" :key="p.id" class="pl-item">
      <div class="pl-head">
        <div class="pl-main">
          <h3 class="pl-title">
            {{ p.name }}
            <span class="pl-ver">{{ p.version }}</span>
            <span class="pl-status" :class="'is-' + p.status">
              {{ statusText[p.status] }}
            </span>
          </h3>
          <p class="pl-desc">{{ p.summary }}</p>
          <div class="pl-tags">
            <span class="pl-tag is-mc">Minecraft {{ p.mc }}</span>
            <span v-for="t in p.tags" :key="t" class="pl-tag">{{ t }}</span>
          </div>
        </div>
        <div class="pl-actions">
          <a class="pl-btn" :href="docLink(p.docs[0].link)">开始阅读</a>
          <a class="pl-btn is-ghost" :href="p.repo" target="_blank" rel="noopener">源码</a>
          <a class="pl-btn is-ghost" :href="p.download" target="_blank" rel="noopener">下载</a>
        </div>
      </div>

        <div class="pl-docs">
          <a
            v-for="d in p.docs"
            :key="d.link"
            class="pl-doc"
            :href="docLink(d.link)"
          >
            {{ d.text }}<span aria-hidden="true">→</span>
          </a>
        </div>
      </article>
    </TransitionGroup>

    <p v-if="!filtered.length" class="pl-empty">没有匹配的插件</p>
  </div>
</template>
