<script setup lang="ts">
import type { Product } from "~/types/orders";
const { coverUrl, deleteProduct, refresh } = useProduct();
const { product } = defineProps<{ product: Product }>();
const getStoredState = () => {
  return product.count > 0 ? "instock" : "nostock";
};
</script>

<template>
  <div v-if="product" class="entry-wrapper">
    <UiFallbackImg
      style="aspect-ratio: 600/400; width: 200px"
      :src="coverUrl(product.id)"
      fallback="empty-card.png"
    />
    <div class="entry-content">
      <h5>Название</h5>
      <p class="title">{{ product.name }}</p>
      <h5>Количество</h5>
      <p class="count">{{ product.count }}</p>
      <h5>Цена</h5>
      <p class="cost">{{ product.count }}</p>
      <div class="bottom-line">
        <UiButton
          leading="hugeicons:edit-02"
          label="редактировать"
          size="xs"
          :fw="false"
          @click="navigateTo(`/admin/product/${product.id}/edit`)"
        />
        <UiButton
          leading="hugeicons:delete-02"
          size="xs"
          :fw="false"
          icon
          variant="outline"
          color="error"
          @click="deleteProduct(product.id)"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.entry-wrapper {
  border-radius: var(--br);
  overflow: hidden;

  .entry-content {
    display: flex;
    flex-direction: column;
    padding: var(--pd);
    width: 100%;

    h5 {
      font-size: 0.8em;
    }
    p {
      font-size: 0.75em;
      margin-bottom: 0.25em;
    }

    .bottom-line {
      display: inline-flex;
      flex-direction: row-reverse;
      justify-content: space-between;
      align-items: center;

      width: 100%;

      .cost {
        font-weight: 600;
      }
    }
  }
}

.storage {
  flex-shrink: 0;
}
</style>
