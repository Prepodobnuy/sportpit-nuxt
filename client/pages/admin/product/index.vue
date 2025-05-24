<script setup lang="ts">
import { ProductAdminEntry } from "#components";
import ResponsiveGrid from "~/components/ui/ResponsiveGrid.vue";
import type { Product } from "~/types/orders";

const { categoriesRef, addCategory, updateCategory, deleteCategory } =
  useCathegory();

const { productsRef, addProduct, coverUrl, updateCover, refresh } =
  useProduct();

const filterPrompt = ref("");

const filteredProducts = () => {
  return productsRef.value?.filter((v) =>
    v.name.toLowerCase().includes(filterPrompt.value.toLowerCase()),
  );
};

const { cols } = useGridColumns();
</script>

<template>
  <div class="caths-wrapper">
    <main>
      <div class="top-bar">
        <UiInput
          v-model="filterPrompt"
          placeholder="фильтр"
          style="width: 100%; flex-shrink: 1"
        />
        <UiButton
          leading="hugeicons:add-square"
          @click="navigateTo('/admin/product/create')"
          icon
          :fw="false"
        />
      </div>
      <ResponsiveGrid :cols="cols">
        <ProductAdminEntry v-for="p in filteredProducts()" :product="p" />
      </ResponsiveGrid>
    </main>
  </div>
</template>

<style lang="scss" scoped>
.caths-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;

  main {
    width: 100%;
    max-width: 1100px;
    padding: var(--pd);
    display: flex;
    flex-direction: column;
    gap: var(--gap);

    .top-bar {
      display: inline-flex;
      gap: var(--gap);
    }
  }
}

.cathegory {
  display: inline-flex;
  gap: var(--gap);
}

.child-form {
  display: flex;
  flex-direction: column;
  gap: calc(var(--gap) / 2);

  .bar {
    display: inline-flex;
    flex-direction: row-reverse;
  }
}
</style>
