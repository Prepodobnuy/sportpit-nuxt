<script setup lang="ts">
import { useCartStore } from "~/stores/useCartStore";

const { id, mod = false } = defineProps<{
  id: number;
  mod?: boolean;
}>();

const store = useProductStore(id);
const cart = useCartStore();

const in_cart_count = cart.product_in_cart_count(id);

const increment = () => {
  cart.add_product(id);
};
const decrement = () => {
  cart.remove_product(id);
};

const config = useRuntimeConfig();
const cover = `${config.public.apiBase}/api/client/product/${id}/cover`;

const handleSelfClick = () => {
  if (mod) {
    navigateTo(`/admin/edit/product/${id}`);
    return;
  }
  navigateTo(`/product/${id}`);
};
</script>

<template>
  <article
    v-if="store.data"
    @click.self="handleSelfClick"
    class="flex gap-4 p-2 bg-gray-800 border light:bg-gray-100 light:border-gray-300 border-gray-700 rounded-[8px] items-center h-max w-full"
  >
    <img
      class="pic rounded-[6px] w-24 h-24"
      :src="cover"
      @click="handleSelfClick"
    />

    <div class="flex-1 min-w-0" @click="handleSelfClick">
      <p class="font-bold text-lg">{{ store.data.cost }} $</p>
      <p class="text-wrap line-clamp-2 text-clip overflow-hidden">
        {{ store.data.name }}
      </p>
    </div>

    <footer class="flex items-center gap-1 ml-auto">
      <UButton
        v-if="in_cart_count <= 0 && !mod"
        leading-icon="hugeicons:shopping-basket-01"
        class="w-max"
        size="xl"
        @click="increment"
      />
      <div v-else-if="!mod" class="inline-flex gap-1 items-center">
        <p class="w-[20px] flex items-center justify-center">
          {{ in_cart_count }}
        </p>
        <UButton
          color="neutral"
          leading-icon="hugeicons:minus-sign"
          class="w-max"
          variant="subtle"
          size="xl"
          @click="decrement"
        />
        <UButton
          color="neutral"
          leading-icon="hugeicons:plus-sign"
          class="w-max"
          variant="subtle"
          size="xl"
          @click="increment"
        />
      </div>
      <div v-if="mod" class="inline-flex gap-1">
        <UButton
          color="success"
          leading-icon="hugeicons:plus-sign"
          class="w-max"
          variant="subtle"
          size="xl"
          @click="navigateTo(`/admin/edit/product/${id}`)"
        />
        <UButton
          color="error"
          leading-icon="hugeicons:delete-01"
          class="w-max"
          variant="subtle"
          size="xl"
          @click="store.deletee()"
        />
      </div>
    </footer>
  </article>
</template>

<style lang="scss" scoped>
.pic {
  width: 96px;
  height: 96px;
  object-fit: cover;
}
</style>
