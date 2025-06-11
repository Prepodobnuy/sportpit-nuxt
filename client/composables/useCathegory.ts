import type { cathegory } from "~/types/cathegory";

export const useCathegory = async () => {
  const config = useRuntimeConfig();

  const { data: cathegories, refresh } = useAsyncData<cathegory[]>(
    "cathegories",
    async (): Promise<cathegory[]> => {
      const response = await $fetch<cathegory[]>("/api/client/cathegories", {
        baseURL: config.public.apiBase,
      });
      return response;
    },
  );
};
