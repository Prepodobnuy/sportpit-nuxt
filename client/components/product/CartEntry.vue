<script setup lang="ts">
import type { Product } from "~/types/orders";

const { coverUrl } = useProduct();
const { product_id, count } = defineProps<{
  product_id: number;
  count: number;
}>();
const cart = useCartStore();

const fetchProduct = async (): Promise<Product | null> => {
  const config = useRuntimeConfig();
  const { data } = await useFetch<Product>(
    `/api/client/product/${product_id}`,
    {
      method: "GET",
      baseURL: config.public.apiBase,
    },
  );
  return data.value;
};

const product = await fetchProduct();
</script>

<template>
  <div class="card-wrapper" v-if="product !== null">
    <div class="left">
      <UiFallbackImg
        class="cover"
        style="aspect-ratio: 600/400"
        :src="coverUrl(product.id)"
        fallback="empty-card.png"
      />
      <div class="col">
        <div class="grid-row title">
          <div class="name">Название</div>
          <div class="cost">Цена за ед.</div>
          <div class="total">Итоговая цена</div>
        </div>
        <div class="grid-row">
          <div class="name">{{ product.name }}</div>
          <div class="cost">{{ product.cost }}</div>
          <div class="total">
            {{ Number(product.cost) * count }}
          </div>
        </div>
      </div>
    </div>
    <div class="right">
      <p>{{ count }}</p>
      <UiButton
        @click="cart.removeProduct(product_id)"
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
            if (product.count - cart.inCartCount(product_id) > 0) {
              cart.addProduct(product_id);
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
  </div>
</template>

<style lang="scss" scoped>
.col {
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  width: 100%;
  flex-shrink: 1;
  height: var(--hg);

  .grid-row {
    display: inline-flex;
    gap: var(--gap);
    width: 100%;
    font-size: 0.9em;

    * {
      font-size: 1em;
      opacity: 0.9;
    }

    &.title {
      * {
        font-size: 0.8em;
        opacity: 0.9;
      }
    }

    .name,
    .cost,
    .total {
      min-width: 10px;
      max-width: 100px;
      width: 100%;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .cost,
    .total {
      max-width: 220px;
      width: 100%;
      flex-shrink: 1;
      white-space: nowrap;
      overflow: visible;
    }

    .name {
      width: 600px;
      flex-shrink: 1;
    }
  }
}

.card-wrapper {
  position: relative;
  width: 100%;
  display: inline-flex;
  gap: var(--gap);
  align-items: start;
  justify-content: space-between;
  height: var(--hg);

  .left {
    height: var(--hg);
    display: inline-flex;
    gap: var(--gap);
    align-items: start;
    justify-content: start;
    .cover {
      height: 100%;
      width: unset;
    }
  }

  .right {
    height: 100%;
    position: absolute;
    right: 0;
    top: 0;
    background-color: var(--window-bg);
    gap: var(--gap);
    display: inline-flex;
    align-items: center;
    justify-content: end;
  }
}
</style>
