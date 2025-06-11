<script setup lang="ts">
import { UDropdownMenu } from "#components";
import type { DropdownMenuItem } from "@nuxt/ui";

const categoriesStore = useCathegoriesStore();
const { categories, selected_cathegory, selected_cathegory_id } =
  storeToRefs(categoriesStore);

const emit = defineEmits(["change"]);

const selectCategory = (id: number) => {
  emit("change", id);
  categoriesStore.select_cathegory(id);
};

const { idd = undefined } = defineProps<{
  idd?: number;
}>();

onMounted(async () => {
  await categoriesStore.refresh();
  if (typeof idd !== "undefined") {
    categoriesStore.select_cathegory(idd);
  }
});

const dropdownItems = (): DropdownMenuItem[][] => {
  return [
    categories.value?.map((c) => {
      return {
        label: c.name,
        icon:
          selected_cathegory_id.value === c.id
            ? "i-heroicons-check-20-solid"
            : "i-heroicons-folder-20-solid",
        onSelect() {
          selectCategory(c.id);
        },
        class:
          selected_cathegory_id.value === c.id
            ? "bg-gray-100 dark:bg-gray-800"
            : "",
      };
    }) || [],
  ];
};
</script>

<template>
  <div class="w-full">
    <UDropdownMenu
      :items="dropdownItems()[0]"
      :popper="{ placement: 'bottom-start', strategy: 'absolute' }"
      mode="hover"
      :content="{
        align: 'end',
        side: 'bottom',
      }"
      :ui="{
        content: 'w-100',
      }"
      class="w-full"
    >
      <UButton
        color="neutral"
        class="w-full justify-between"
        variant="subtle"
        size="xl"
        trailing-icon="i-heroicons-chevron-down-20-solid"
        :label="selected_cathegory?.name || 'Выберите категорию'"
        @click="console.log(dropdownItems())"
      />
    </UDropdownMenu>

    <USkeleton v-if="!categories" class="w-full h-10 mt-2" />

    <UAlert
      v-else-if="categories.length === 0"
      icon="i-heroicons-exclamation-circle"
      color="warning"
      variant="soft"
      title="Категории не найдены"
      class="mt-4"
    />
  </div>
</template>
