import type { Product, SearchParams, SearchResult } from "~/types/orders";

export const useCatalogStore = defineStore("catalog", () => {
  const config = useRuntimeConfig();
  const { categoriesRef } = useCathegory();

  const state = reactive({
    asideActive: false,
    selected_cathegory: 0,
    selected_search_filter: 0,
    reversed_search: false,
    index: 0,
    prompt: "",
    end: false,
  });

  const products = ref<Product[]>([]);

  const debounce = ref<ReturnType<typeof setTimeout> | null>(null);

  const search = async () => {
    const cathegory_id = state.selected_cathegory;
    const in_stock_only = false;
    const prompt = state.prompt;
    const reversed = state.reversed_search;
    const order_by = state.selected_search_filter == 0 ? "name" : "cost";

    const form: SearchParams = {
      cathegory_id: cathegory_id,
      in_stock_only: in_stock_only,
      prompt: prompt,
      reversed: reversed,
      order_by: order_by,
    };

    const { data, error } = await useFetch<SearchResult>(
      `/api/client/search/${state.index}`,
      {
        method: "POST",
        body: form,
        baseURL: config.public.apiBase,
      },
    );

    if (error.value) {
      debounce.value = setTimeout(async () => {
        state.index = 0;

        await search();
      }, 5000);
      return;
    }

    if (data.value) {
      state.end = data.value.end;
      if (state.index === 0) {
        products.value = data.value.products;
      } else {
        products.value = [...products.value, ...data.value.products];
      }
      state.index += 1;
      return;
    }
  };

  watch(
    () => [
      state.selected_cathegory,
      state.selected_search_filter,
      state.reversed_search,
      state.prompt,
    ],
    (newValues, oldValues) => {
      if (
        newValues[0] !== oldValues[0] ||
        newValues[1] !== oldValues[1] ||
        newValues[2] !== oldValues[2] ||
        newValues[3] !== oldValues[3]
      ) {
        if (debounce.value) clearTimeout(debounce.value);

        debounce.value = setTimeout(async () => {
          state.index = 0;

          await search();
        }, 100);
      }
    },
  );

  onMounted(() => {
    if (!categoriesRef.value) {
      state.selected_cathegory = 0;
    } else {
      state.selected_cathegory = categoriesRef.value[0].id;
    }

    debounce.value = setTimeout(async () => {
      state.index = 0;

      await search();
    }, 600);
  });

  return {
    state,
    products,
  };
});
