<script setup lang="ts"></script>

<template>
  <Header class="header" />
  <div class="content__">
    <slot />
  </div>
</template>

<style lang="scss" scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: calc(54px * var(--root-scale));
  z-index: 3000;
}

.content__ {
  margin-top: calc(54px * var(--root-scale));
  --margin-top: calc(54px * var(--root-scale));
}
</style>
