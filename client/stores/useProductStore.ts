import type { Product, ProductPost } from "~/types/product";

export const useProductStore = (id: number) => {
  const config = useRuntimeConfig();
  const { token, logged } = useAuth();

  const store = defineStore(`product-${id}`, () => {
    const { data, refresh } = useAsyncData<Product>(
      `product-data-${id}`,
      async () => {
        const responce = await $fetch<Product>(`/api/client/product/${id}`, {
          baseURL: config.public.apiBase,
        });
        return responce;
      },
    );

    const cover = `${config.public.apiBase}/api/client/product/${id}/cover`;

    const put = async () => {
      if (!data.value) return;
      try {
        const form = {
          id: data.value.id,
          name: data.value.name,
          cost: data.value.cost,
          count: data.value.count,
          cathegory_id: data.value.cathegory_id,
          description: data.value.description,
        };
        const response = await $fetch(`/api/admin/product`, {
          method: "PUT",
          body: form,
          baseURL: config.public.apiBase,
          headers: {
            Authorization: `Bearer ${token.value}`,
          },
        });
        if (response) {
          await refresh();
        }
      } finally {
      }
    };

    const put_cover = async (cover: File) => {
      if (!data.value) return;
      const formData = new FormData();
      formData.append("file", cover);
      try {
        const response = await $fetch(
          `/api/admin/product/${data.value.id}/cover`,
          {
            method: "PUT",
            body: formData,
            baseURL: config.public.apiBase,
            headers: {
              Authorization: `Bearer ${token.value}`,
            },
          },
        );
        if (response) {
          await refresh();
        }
      } finally {
      }
    };

    const deletee = async () => {
      await $fetch(`/api/admin/product/${id}`, {
        method: "DELETE",
        baseURL: config.public.apiBase,
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      });

      await refresh();
    };

    return {
      data,
      refresh,
      cover,
      put,
      put_cover,
      deletee,
    };
  });

  return store();
};
