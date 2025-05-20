import type { OrderProduct } from "~/types/orders";

export const useCartStore = defineStore("cart", () => {
  const products = ref<OrderProduct[]>([]);

  return {
    products,
  };
});
