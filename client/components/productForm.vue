<script lang="ts" setup>
import { UiButton } from "#components";
import type { Product } from "~/types/orders";

const model = defineModel<Product>({ required: true });
const fileModel = defineModel<File | undefined>("file");
const count = ref("0");

watch(count, (v) => {
  const value = Number(v);
  if (isNaN(value)) return;
  model.value.count = value;
});

const { categoriesRef } = useCathegory();

const emit = defineEmits(["post"]);

const {
  size = "md",
  roundness = "standart",
  color = "neutral",
  variant = "solid",
} = defineProps<{
  size?: "xs" | "sm" | "md" | "lg" | "xl";
  roundness?: "standart" | "pill" | "none";
  color?: "neutral" | "primary" | "success" | "warning" | "error";
  variant?: "solid" | "outline" | "soft" | "softborder" | "ghost" | "link";
}>();

const caths = computed(
  (): {
    display: string;
    select: number;
  }[] => {
    if (!categoriesRef.value) return [];
    return categoriesRef.value.map((v) => ({ display: v.name, select: v.id }));
  },
);

const selectedCathegory = computed(() => {
  if (!categoriesRef.value) return null;
  const value = categoriesRef.value.filter(
    (v) => v.id == model.value.cathegory_id,
  );
  if (value.length > 0) return value[0];
  return null;
});
</script>

<template>
  <div class="form">
    <h6>Обложка</h6>
    <UiImageInput
      :width="200"
      :aspect="600 / 400"
      style="flex-shrink: 0"
      v-model="fileModel"
      :size="size"
      :roundness="roundness"
      :color="color"
      :variant="variant"
    />
    <h6>Название</h6>
    <UiInput
      v-model="model.name"
      class="input"
      :size="size"
      :roundness="roundness"
      :color="color"
      :variant="variant"
    />
    <h6>Цена</h6>
    <UiInput
      v-model="model.cost"
      class="input"
      :size="size"
      :roundness="roundness"
      :color="color"
      :variant="variant"
    />
    <h6>Количество</h6>
    <UiInput
      v-model="count"
      class="input"
      :size="size"
      :roundness="roundness"
      :color="color"
      :variant="variant"
    />
    <h6>{{ selectedCathegory?.name || "Категория" }}</h6>
    <UiSelectMenu
      :size="size"
      :roundness="roundness"
      :color="color"
      :variant="variant"
      :entries="caths"
      @select="
        (id) => {
          model.cathegory_id = id;
        }
      "
    ></UiSelectMenu>
    <div />
    <div class="bar">
      <UiButton
        trailing="hugeicons:add-square"
        label="Добавить"
        :fw="false"
        size="sm"
        @click="emit('post')"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: var(--gap);

  .bar {
    display: inline-flex;
    flex-direction: row-reverse;
  }
}
</style>
