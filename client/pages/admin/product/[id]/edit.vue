<script setup lang="ts">
import {
  UiFallbackImg,
  UiImageInput,
  UiInput,
  UiNumberInput,
} from "#components";
import type { Product } from "~/types/orders";

const route = useRoute();
const id = route.params.id;
const config = useRuntimeConfig();
const { categoriesRef } = useCathegory();
const debounce = ref<ReturnType<typeof setTimeout> | null>(null);

const data = ref<Product | null>(null);

const update = async () => {
  const { token, logged } = useAuth();
  if (!logged) navigateTo("/admin/product");
  await useFetch("/api/admin/product", {
    method: "PUT",
    baseURL: config.public.apiBase,
    body: data.value,
    headers: {
      Authorization: `Bearer ${token.value}`,
    },
  });
};

const updateCover = async (file: File) => {
  const { token, logged } = useAuth();
  if (!logged) navigateTo("/admin/product");

  const formData = new FormData();
  formData.append("file", file);

  await useFetch(`/api/admin/product/${id}/cover`, {
    method: "PUT",
    baseURL: config.public.apiBase,
    body: formData,
    headers: {
      Authorization: `Bearer ${token.value}`,
    },
  });
};

onMounted(async () => {
  const { data: prData } = await useFetch<Product>(
    `/api/client/product/${id}`,
    {
      baseURL: config.public.apiBase,
    },
  );
  if (prData.value) {
    data.value = prData.value;
    watch(data.value, (value) => {
      if (debounce.value) clearTimeout(debounce.value);
      debounce.value = setTimeout(update, 3000);
    });
  } else {
    navigateTo("/admin/product");
  }
});

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
    (v) => v.id == data.value.cathegory_id,
  );
  if (value.length > 0) return value[0];
  return null;
});
</script>

<template>
  <div class="caths-wrapper">
    <main v-if="data">
      <div class="image-row">
        <UiImageInput
          :preview="`${config.public.apiBase}/api/client/product/${id}/cover`"
          :aspect="600 / 400"
          :width="300"
          @set="
            (file) => {
              updateCover(file);
            }
          "
        />
      </div>
      <UiInput v-model="data.name" />
      <UiInput v-model="data.cost" />
      <UiNumberInput v-model="data.count" />

      <h6>{{ selectedCathegory?.name || "Категория" }}</h6>
      <UiSelectMenu
        v-if="data.cathegory_id"
        :entries="caths"
        @select="
          (id) => {
            data.cathegory_id = id;
          }
        "
      />
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

    .image-row {
      display: flex;
      flex-direction: column;
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
