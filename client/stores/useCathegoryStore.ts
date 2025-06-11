import type { Cathegory } from "~/types/cathegory";

export const useCathegoryStore = (id: number) => {
  const config = useRuntimeConfig();

  const store = defineStore(`cathegory-${id}`, () => {
    const { data, refresh } = useAsyncData<Cathegory>(
      `cathegory-data-${id}`,
      async () => {
        const response = await $fetch<Cathegory>(`/api/client/product/${id}`, {
          baseURL: config.public.apiBase,
        });
        return response;
      },
    );

    return { data, refresh };
  });

  return store();
};

export const useCathegoriesStore = defineStore("cathegories", () => {
  const config = useRuntimeConfig();
  const { token, logged } = useAuth();
  const prompt = ref("");

  const post = async () => {
    await $fetch("/api/admin/cathegory", {
      method: "POST",
      body: { name: prompt.value },
      baseURL: config.public.apiBase,
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
    await refresh();
  };

  const deletee = async (id: number) => {
    await $fetch(`/api/admin/cathegory/${id}`, {
      method: "DELETE",
      body: { name: prompt.value },
      baseURL: config.public.apiBase,
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
    await refresh();
  };

  const { data, refresh } = useAsyncData<Cathegory[]>(
    "all-cathegories",
    async () => {
      try {
        const response = await $fetch<Cathegory[]>("/api/client/cathegories", {
          baseURL: config.public.apiBase,
        });
        return response;
      } catch (error) {
        console.error("Error fetching categories:", error);
        return [];
      }
    },
    {
      watch: [],
    },
  );

  const selected_cathegory_id = ref<number | null>(null);

  watch(
    data,
    (newCategories) => {
      if (newCategories && newCategories.length > 0) {
        if (
          !selected_cathegory_id.value ||
          !newCategories.some((c) => c.id === selected_cathegory_id.value)
        ) {
          selected_cathegory_id.value = newCategories[0].id;
        }
      } else {
        selected_cathegory_id.value = null;
      }
    },
    { immediate: true },
  );

  const selected_cathegory = computed(() => {
    return data.value?.find((v) => v.id === selected_cathegory_id.value);
  });

  const categoryStores = computed(() => {
    return data.value?.map((category) => useCathegoryStore(category.id)) || [];
  });

  const select_cathegory = (id: number) => {
    if (data.value?.some((c) => c.id === id)) {
      selected_cathegory_id.value = id;
    }
  };

  return {
    selected_cathegory_id,
    selected_cathegory,
    select_cathegory,
    categories: data,
    stores: categoryStores,
    refresh,
    prompt,
    post,
    deletee,
  };
});
