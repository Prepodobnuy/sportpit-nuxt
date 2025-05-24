import type { Order } from "~/types/orders";

export const useOrder = () => {
  const { token, logged } = useAuth();
  const config = useRuntimeConfig();

  const { data: pendingOrders, refresh: pendingRefresh } = useAsyncData<
    Order[]
  >("pending_orders", async () => {
    return await $fetch("/api/admin/orders/pending", {
      method: "GET",
      baseURL: config.public.apiBase,
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
  });

  const { data: completedOrders, refresh: completedRefresh } = useAsyncData<
    Order[]
  >("completed_orders", async () => {
    return await $fetch("/api/admin/orders/completed", {
      method: "GET",
      baseURL: config.public.apiBase,
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
  });

  const { data: workingOrders, refresh: workingRefresh } = useAsyncData<
    Order[]
  >("working_orders", async () => {
    return await $fetch("/api/admin/orders/working", {
      method: "GET",
      baseURL: config.public.apiBase,
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
  });

  const approveOrder = async (id: number) => {
    await useFetch(`/api/admin/order/${id}/approve`, {
      method: "PUT",
      baseURL: config.public.apiBase,
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
  };

  const declineOrder = async (id: number) => {
    await useFetch(`/api/admin/order/${id}/decline`, {
      method: "DELETE",
      baseURL: config.public.apiBase,
      headers: {
        Authorization: `Bearer ${token.value}`,
      },
    });
  };

  const refresh = () => {
    pendingRefresh();
    completedRefresh();
    workingRefresh();
  };

  return {
    pendingOrders,
    workingOrders,
    completedOrders,
    pendingRefresh,
    completedRefresh,
    approveOrder,
    declineOrder,
    refresh,
  };
};
