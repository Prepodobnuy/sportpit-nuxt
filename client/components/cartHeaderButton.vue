<script setup lang="ts">
const { total } = storeToRefs(useCartStore());
</script>

<template>
  <div class="wrapper">
    <div v-if="total > 0" class="total">{{ total }}</div>
    <UiButton
      leading="hugeicons:shopping-basket-01"
      variant="ghost"
      label="Корзина"
      @click="navigateTo('/cart')"
      :fw="false"
    />
  </div>
</template>

<style lang="scss" scoped>
.wrapper {
  position: relative;
}

.total {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background-color: var(--error-bg);
  color: var(--error-fg);
  z-index: 1000;
  border-radius: var(--br);

  max-width: var(--hg);
  min-width: calc(var(--hg) / 2.2);
  height: calc(var(--hg) / 2.2);

  right: 0;
  top: 0;
}
</style>
