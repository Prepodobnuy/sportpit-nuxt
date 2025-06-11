<script setup lang="ts">
const mobile = isMobile();
</script>

<template>
  <div class="layout">
    <Header
      class="header fixed left-0 h-12 z-1000 bg-gray-800 light:bg-gray-200"
      :class="mobile ? 'bottom-0' : 'top-0'"
    />
    <div :class="mobile ? 'mb-12' : 'mt-12'">
      <slot />
    </div>
  </div>
</template>
