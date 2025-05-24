import type { Product, ProductPost } from "~/types/orders";

export const useProduct = () => {
  const { token, logged } = useAuth();
  const config = useRuntimeConfig();

  const { data: products, refresh } = useAsyncData<Product[]>(
    "product",
    async () => {
      if (!logged) return [];
      return await $fetch("/api/admin/products", {
        baseURL: config.public.apiBase,
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      });
    },
  );

  const addProduct = async (form: ProductPost, file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("scheme", JSON.stringify(form));

    const { data } = await useFetch("/api/admin/product", {
      method: "POST",
      body: formData,
      baseURL: config.public.apiBase,
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
  };

  const updateCover = async (id: number, file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    const { data } = await useFetch(`/api/admin/product/${id}/cover`, {
      method: "PUT",
      body: formData,
      baseURL: config.public.apiBase,
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
  };

  const deleteProduct = async (id: number) => {
    const { data } = await useFetch(`/api/admin/product/${id}`, {
      method: "DELETE",
      baseURL: config.public.apiBase,
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
    refresh();
  };

  const coverUrl = (id: number): string => {
    return `${config.public.apiBase}/api/client/product/${id}/cover`;
  };

  return {
    products: products.value || [],
    productsRef: products,
    addProduct,
    updateCover,
    deleteProduct,
    refresh,
    coverUrl,
  };
};
