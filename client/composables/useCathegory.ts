import type { Cathegory } from "~/types/orders";

export const useCathegory = () => {
  const { token, logged } = useAuth();
  const config = useRuntimeConfig();

  const { data: categories, refresh } = useAsyncData<Cathegory[]>(
    "categories",
    async () => {
      return await $fetch("/api/client/cathegories", {
        baseURL: config.public.apiBase,
      });
    },
  );

  const addCategory = async (name: string) => {
    const { data } = await useFetch("/api/admin/cathegory", {
      method: "POST",
      body: { name: name },
      baseURL: config.public.apiBase,
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
  };

  const updateCategory = async (id: number, name: string) => {
    const { data } = await useFetch("/api/admin/cathegory", {
      method: "PUT",
      body: { id: id, name: name },
      baseURL: config.public.apiBase,
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
  };

  const deleteCategory = async (id: number) => {
    const { data } = await useFetch(`/api/admin/cathegory/${id}`, {
      method: "DELETE",
      baseURL: config.public.apiBase,
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
  };

  return {
    categories: categories.value || [],
    categoriesRef: categories,
    addCategory,
    updateCategory,
    deleteCategory,
    refresh,
  };
};
