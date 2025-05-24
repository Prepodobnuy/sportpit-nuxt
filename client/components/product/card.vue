<script setup lang="ts">
import type { Product } from "~/types/orders";
const { coverUrl } = useProduct();
const { product } = defineProps<{ product: Product }>();
const getStoredState = () => {
  return product.count > 0 ? "instock" : "nostock";
};
const cart = useCartStore();
</script>

<template>
  <div v-if="product" class="card-wrapper">
    <UiFallbackImg
      style="aspect-ratio: 600/400"
      :src="coverUrl(product.id)"
      fallback="empty-card.png"
    />
    <div class="card-content">
      <div class="top-line">
        <h5 class="title">{{ product.name }}</h5>
        <p class="storage" :class="getStoredState()">
          {{ product.count > 0 ? "В наличии" : "Отсутствует" }}
        </p>
      </div>
      <div class="bottom-line">
        <UiButton
          v-if="!cart.inCart(product.id)"
          @click="cart.addProduct(product.id)"
          leading="hugeicons:shopping-cart-add-02"
          size="sm"
          :fw="false"
          icon
        />
        <div v-else class="action">
          <p>{{ cart.inCartCount(product.id) }}</p>
          <UiButton
            @click="cart.removeProduct(product.id)"
            leading="hugeicons:minus-sign"
            size="sm"
            color="error"
            variant="outline"
            :fw="false"
            icon
          />
          <UiButton
            @click="
              () => {
                if (product.count - cart.inCartCount(product.id) > 0) {
                  cart.addProduct(product.id);
                }
              }
            "
            leading="hugeicons:plus-sign"
            size="sm"
            color="success"
            variant="outline"
            :fw="false"
            icon
          />
        </div>
        <p class="cost">{{ product.cost }}</p>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.card-wrapper {
  border-radius: var(--br);
  overflow: hidden;

  .card-content {
    display: flex;
    flex-direction: column;
    padding: var(--pd);
    gap: calc(var(--gap));
    width: 100%;

    .top-line {
      display: inline-flex;
      justify-content: space-between;
      align-items: center;

      * {
        font-size: 0.85em;
      }

      .title {
        font-weight: 600;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      p {
        font-weight: 400;

        &.instock {
          color: var(--success-bg);
        }
        &.nostock {
          color: var(--error-bg);
        }
        &.soon {
          color: var(--warning-bg);
        }
      }
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

      .action {
        display: inline-flex;
        align-items: center;
        gap: calc(var(--gap) / 2);
      }
    }
  }
}

.storage {
  flex-shrink: 0;
}
</style>
