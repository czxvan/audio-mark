<template>
  <ul class="layout-menu">
    <template
      v-for="(item, i) in model"
      :key="item">
      <app-menu-item
        v-if="!item.separator"
        :item="item"
        :index="i"/>
      <li
        v-if="item.separator"
        class="menu-separator"></li>
    </template>
  </ul>
</template>

<script setup>
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    {
        label: 'Audio-Mark',
        icons: 'pi pi-fw pi-th-large',
        items:[
            { label: 'generate', icon: 'pi pi-fw pi-home', to: '/ADMK/generate' },
            { label: 'detect', icon: 'pi pi-fw pi-home', to: '/ADMK/detect' },
        ]
    },

]);
</script>

<style lang="scss" scoped></style>
