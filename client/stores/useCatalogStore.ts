interface ProductScheme {
  id: number;
  name: string;
  cost: string;
  count: number;
  cathegory_id: number;
  description: string | null;
}

export const useCatalogStore = defineStore("catalog", () => {
  const config = useRuntimeConfig();
  const { selected_cathegory_id } = useCathegoriesStore();
  const categoriesStore = useCathegoriesStore();

  const state = reactive<{
    loading: boolean;
    prompt: string;
    products: number[];
    sort_index: number;
    descending: boolean;
    index: number;
    end: boolean;
    cathegory_id: number;
  }>({
    loading: false,
    prompt: "",
    products: [],
    sort_index: 0, // 0 - name 1 - cost
    descending: false,
    index: 0,
    end: false,
    cathegory_id: selected_cathegory_id || 0,
  });

  const search_debounce = ref<ReturnType<typeof setTimeout> | null>(null);

  const search = () => {
    if (state.loading) return;
    if (state.end) return;
    if (search_debounce.value) clearTimeout(search_debounce.value);

    search_debounce.value = setTimeout(async () => {
      state.loading = true;
      try {
        const body = {
          cathegory_id: state.cathegory_id,
          in_stock_only: true,
          prompt: state.prompt,
          reversed: state.descending,
          order_by: state.sort_index === 0 ? "name" : "cost",
        };

        const response = await $fetch<{
          end: boolean;
          products: ProductScheme[];
        }>(`/api/client/search/${state.index}`, {
          method: "POST",
          baseURL: config.public.apiBase,
          body: body,
        });

        state.index += 1;
        state.end = response.end;
        state.products = response.products.map((v) => v.id);
      } finally {
        state.loading = false;
      }
    }, 1000);
  };

  const reset_search = () => {
    if (search_debounce.value) clearTimeout(search_debounce.value);
    state.loading = false;
    state.end = false;
    state.index = 0;

    search();
  };

  onMounted(() => {
    reset_search();
  });

  watch(
    () => [
      state.cathegory_id,
      state.prompt,
      state.descending,
      state.sort_index,
    ],
    (value) => {
      reset_search();
    },
  );

  watch(
    () => categoriesStore.selected_cathegory_id,
    (newId) => {
      if (newId !== undefined && newId !== null) {
        state.cathegory_id = newId;
        reset_search();
      }
    },
  );

  watch(
    [
      () => state.cathegory_id,
      () => state.prompt,
      () => state.descending,
      () => state.sort_index,
    ],
    () => {
      reset_search();
    },
    { deep: true },
  );

  return {
    state,
  };
});
