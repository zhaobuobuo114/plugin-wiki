<script setup lang="ts">
import { sortedPlugins } from '../../data/plugins'
</script>

<template>
  <nav class="plugin-outline" aria-label="插件目录">
    <div class="po-title">
      <span>插件目录</span>
      <span class="po-count">{{ sortedPlugins.length }}</span>
    </div>
    <ul class="po-list">
      <li v-for="p in sortedPlugins" :key="p.id">
        <a :href="'#plugin-' + p.id">{{ p.name }}</a>
      </li>
    </ul>
  </nav>
</template>
