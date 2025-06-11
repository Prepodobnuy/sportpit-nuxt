<script setup lang="ts">
import { ClientOnly } from "#components";
import { VueMarkdown } from "vue-markdown-x";

const route = useRoute();
const id = Number(route.params.id);

const config = useRuntimeConfig();
const cover = `${config.public.apiBase}/api/client/product/${id}/cover`;

// Используем ваш store
const store = useProductStore(id);
const product = computed(() => store.data);

// Работа с корзиной
const cart = useCartStore();
const in_cart_count = computed(() => cart.product_in_cart_count(id));

const addToCart = () => {
  cart.add_product(id);
};

const removeFromCart = () => {
  cart.remove_product(id);
};
// Заглушка для похожих товаров
const similarProducts = ref([{ id: 1 }, { id: 2 }, { id: 3 }, { id: 4 }]);
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Кнопка назад -->
      <UButton
        icon="i-heroicons-arrow-left-20-solid"
        color="neutral"
        variant="ghost"
        class="mb-6"
        @click="navigateTo('/')"
      >
        Назад
      </UButton>

      <!-- Основной контент -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Левая колонка - изображение -->
        <div
          class="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden"
        >
          <img
            :src="cover"
            :alt="product?.name"
            class="w-full h-auto max-h-[500px] object-contain"
          />
        </div>

        <!-- Правая колонка - информация -->
        <div class="space-y-6">
          <!-- Заголовок и цена -->
          <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
              {{ product?.name }}
            </h1>
            <div class="mt-4 flex items-center">
              <span
                class="text-2xl font-bold text-primary-600 dark:text-primary-400"
              >
                {{ product?.cost }} $
              </span>
            </div>
          </div>

          <!-- Кнопки действий -->
          <div class="flex flex-wrap gap-4 pt-4">
            <UButton
              v-if="in_cart_count <= 0"
              icon="i-heroicons-shopping-basket"
              size="xl"
              color="primary"
              @click="addToCart"
            >
              Добавить в корзину
            </UButton>

            <div v-else class="flex items-center gap-4">
              <UButton
                icon="i-heroicons-minus"
                color="gray"
                variant="outline"
                size="xl"
                @click="removeFromCart"
              />
              <span class="text-lg font-medium dark:text-white">
                {{ in_cart_count }} в корзине
              </span>
              <UButton
                icon="i-heroicons-plus"
                color="gray"
                variant="outline"
                size="xl"
                @click="addToCart"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Описание товара -->
      <div
        v-if="product && product.description"
        class="prose dark:prose-invert max-w-none text-[1.2em] p-4"
      >
        <VueMarkdown :md="product.description" />
      </div>
    </div>
  </div>
</template>

<style>
.prose {
  color: #374151; /* gray-700 */
  line-height: 1.6;
}

.prose h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.prose p {
  margin-bottom: 1rem;
}

.prose ul {
  list-style-type: disc;
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}

.prose a {
  color: #3b82f6; /* blue-500 */
  text-decoration: underline;
}

.dark .prose {
  color: #e5e7eb; /* gray-200 */
}

.dark .prose a {
  color: #60a5fa; /* blue-400 */
}
</style>
