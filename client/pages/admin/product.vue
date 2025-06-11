<script setup lang="ts">
import type { DropdownMenuItem } from "@nuxt/ui";
import { useCatalogStore } from "~/stores/useCatalogStore";

const cols = useCols();
const catalog = useCatalogStore();
const { state: catalogState } = storeToRefs(useCatalogStore());
const items = (): DropdownMenuItem[][] => [
  [
    {
      label: "По названию",
      icon: "i-heroicons-bars-arrow-down-20-solid",
      disabled: catalogState.value.sort_index === 0,
      onSelect() {
        catalog.state.sort_index = 0;
      },
    },
    {
      label: "По цене",
      icon: "i-heroicons-currency-dollar-20-solid",
      disabled: catalogState.value.sort_index === 1,
      onSelect() {
        catalog.state.sort_index = 1;
      },
    },
  ],
  [
    {
      label: "По возрастанию",
      icon: "i-heroicons-arrow-up-20-solid",
      disabled: !catalogState.value.descending,
      onSelect() {
        catalog.state.descending = false;
      },
    },
    {
      label: "По убыванию",
      icon: "i-heroicons-arrow-down-20-solid",
      disabled: catalogState.value.descending,
      onSelect() {
        catalog.state.descending = true;
      },
    },
  ],
];
</script>

<template>
  <div class="w-[100vw] p-2 inline-flex justify-center">
    <div class="max-w-[1220px] w-[100%] flex flex-col gap-2">
      <div class="w-[100%] inline-flex gap-2">
        <UInput
          v-model="catalog.state.prompt"
          class="w-[100%]"
          placeholder="Поиск"
          color="neutral"
          variant="subtle"
          size="xl"
          icon="hugeicons:search-02"
        />
        <UDropdownMenu :items="items()">
          <UButton
            leading-icon="hugeicons:filter"
            color="neutral"
            variant="subtle"
            size="xl"
            class="aspect-[1/1] flex items-center justify-center"
          />
        </UDropdownMenu>
        <UButton
          size="xl"
          leading-icon="hugeicons:plus-sign-square"
          color="success"
          class="aspect-[1/1] h-10 flex align-center justify-center"
          @click="navigateTo('/admin/form/product')"
        />
      </div>

      <CathegorySelect />

      <ResponsiveGrid :cols="cols">
        <ProductCard
          v-for="id in catalog.state.products"
          :key="id"
          :id="id"
          mod
        />
      </ResponsiveGrid>
    </div>
  </div>
</template>
