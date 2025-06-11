<script setup lang="ts">
import { MdEditor } from "md-editor-v3";
import ImageInput from "~/components/ImageInput.vue";
import "md-editor-v3/lib/style.css";

const route = useRoute();
const id = Number(route.params.id);
const productStore = useProductStore(id);

onMounted(async () => {
  await productStore.refresh();
});

const handleNameChange = async (e: Event) => {
  if (productStore.data) {
    productStore.data.name = (e.target as HTMLInputElement).value;
    await productStore.put();
  }
};

const handleCostChange = async (e: Event) => {
  if (productStore.data) {
    productStore.data.cost = (e.target as HTMLInputElement).value;
    await productStore.put();
  }
};

const handleCountChange = async (e: Event) => {
  if (productStore.data) {
    productStore.data.count = Number((e.target as HTMLInputElement).value);
    await productStore.put();
  }
};

const handleDescriptionChange = async (value: string) => {
  if (productStore.data) {
    productStore.data.description = value;
    await productStore.put();
  }
};

const handleCoverChange = async (file: File) => {
  await productStore.put_cover(file);
};

const handleCategoryChange = async (catId: number) => {
  if (productStore.data) {
    productStore.data.cathegory_id = catId;
    await productStore.put();
  }
};
</script>

<template>
  <div class="w-[100vw] p-[20px] inline-flex justify-center">
    <div
      class="flex flex-col h-max p-1 rounded-md items-center gap-2 max-w-[900px] w-[100%] bg-gray-800 light:bg-gray-200"
    >
      <UFormField label="Обложка" class="self-start w-full">
        <ImageInput @select="handleCoverChange" :aspect="295 / 221" />
      </UFormField>

      <UFormField label="Название" class="self-start w-[100%]">
        <UInput
          :value="productStore.data?.name"
          @input="handleNameChange"
          class="w-[100%]"
          variant="subtle"
        />
      </UFormField>

      <UFormField label="Цена" class="self-start w-[100%]">
        <UInput
          :value="productStore.data?.cost"
          @input="handleCostChange"
          type="number"
          class="w-[100%]"
          variant="subtle"
        />
      </UFormField>

      <UFormField label="Количество" class="self-start w-[100%]">
        <UInputNumber
          :value="productStore.data?.count"
          @input="handleCountChange"
          class="w-[100%]"
          variant="subtle"
        />
      </UFormField>

      <UFormField label="Категория" class="self-start w-full">
        <CathegorySelect
          @change="handleCategoryChange"
          :idd="productStore.data?.cathegory_id"
        />
      </UFormField>

      <UFormField label="Описание" class="self-start w-[100%]">
        <MdEditor
          :model-value="productStore.data?.description || ''"
          @update:model-value="handleDescriptionChange"
          class="rounded-md"
        />
      </UFormField>

      <UButton
        class="mt-3 self-end"
        label="Удалить продукт"
        color="error"
        @click="productStore.deletee()"
      />
    </div>
  </div>
</template>
