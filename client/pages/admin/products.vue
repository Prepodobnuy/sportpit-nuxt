<script setup lang="ts">
import type { Product } from "~/types/orders";
import ProductForm from "~/components/productForm.vue";
import { UiFallbackImg } from "#components";

const { categoriesRef, addCategory, updateCategory, deleteCategory } =
  useCathegory();

const { productsRef, addProduct, coverUrl, updateCover, refresh } =
  useProduct();

const file = ref<File | undefined>(undefined);
const value = reactive<Product>({
  cost: "",
  count: 0,
  name: "",
  cathegory_id: undefined,
});
const createProduct = async () => {
  console.clear();
  console.log(1);
  if (value.cathegory_id === undefined) return;
  console.log(2);
  if (file.value === undefined) return;
  console.log(3);
  await addProduct(
    {
      name: value.name,
      cost: value.cost,
      count: value.count,
      cathegory_id: value.cathegory_id,
    },
    file.value,
  );
};

const caths = computed(
  (): {
    display: string;
    select: number;
  }[] => {
    if (!categoriesRef.value) return [];
    return categoriesRef.value.map((v) => ({ display: v.name, select: v.id }));
  },
);

const selectedCathegory = (id: number) => {
  if (!categoriesRef.value) return null;
  const value = categoriesRef.value.filter((v) => v.id == id);
  if (value.length > 0) return value[0];
  return null;
};
</script>

<template>
  <div class="caths-wrapper">
    <main>
      <ProductForm
        v-model="value"
        v-model:file="file"
        @post="createProduct()"
      />

      <div class="products" v-for="p in productsRef">
        <div class="child-form">
          <h6>Обложка</h6>
          <UiFallbackImg
            style="aspect-ratio: 600/400; width: 100%; max-width: 200px"
            :src="coverUrl(p.id)"
          />
          <UiImageInput
            :width="200"
            :aspect="600 / 400"
            style="flex-shrink: 0"
            size="sm"
            variant="outline"
            @set="
              async (file) => {
                await updateCover(p.id, file);
                await refresh();
              }
            "
          />
          <h6>Название</h6>
          <UiInput v-model="p.name" class="input" size="sm" variant="outline" />
          <h6>Цена</h6>
          <UiInput v-model="p.cost" class="input" size="sm" variant="outline" />
          <h6>Количество</h6>
          <UiNumberInput
            v-model="p.count"
            class="input"
            size="sm"
            variant="outline"
          />
          <h6>{{ selectedCathegory(p.cathegory_id)?.name || "Категория" }}</h6>
          <UiSelectMenu
            size="sm"
            variant="outline"
            :entries="caths"
            @select="
              (id) => {
                p.cathegory_id = id;
              }
            "
          ></UiSelectMenu>
        </div>
      </div>
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
