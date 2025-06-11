import type { ProductPost } from "~/types/product";
import * as v from "valibot";

export const useProductForm = defineStore("product-form", () => {
  const auth = useAuth();
  const config = useRuntimeConfig();

  const state = reactive({
    loading: false,
  });

  const form = reactive<{
    cover?: File;
    name?: string;
    cost?: string;
    count?: number;
    cathegory_id?: number;
    description?: string;
  }>({
    cover: undefined,
    name: undefined,
    cost: undefined,
    count: undefined,
    cathegory_id: undefined,
    description: undefined,
  });

  const schema = v.object({
    name: v.string("Должно быть строкой"),
    cost: v.string("Должно быть числом"),
    count: v.number("Должно быть числом"),
    cathegory_id: v.number("Должно быть числом"),
    cover: v.pipe(v.file("Выберите Обложку")),
    description: v.string("Должно быть строкой"),
  });

  const post = async (cid: number) => {
    if (!auth.logged) return;

    state.loading = true;
    try {
      const formData = new FormData();

      const body: ProductPost = {
        name: form.name,
        cost: form.cost,
        count: form.count,
        description: form.description || null,
        cathegory_id: cid,
      };

      formData.append("file", form.cover);
      formData.append("scheme", JSON.stringify(body));

      const response = await $fetch("/api/admin/product", {
        method: "POST",
        body: formData,
        baseURL: config.public.apiBase,
        headers: {
          Authorization: `Bearer ${auth.token.value}`,
        },
      });
    } finally {
      state.loading = false;
    }
  };

  return {
    state,
    form,
    schema,
    post,
  };
});
