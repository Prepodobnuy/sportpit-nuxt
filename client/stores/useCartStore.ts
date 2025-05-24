import type {
  OrderPost,
  OrderProduct,
  OrderProductPost,
  Product,
} from "~/types/orders";

export const useCartStore = defineStore("cart", () => {
  const productsCookie = useCookie<Record<number, { count: number }>>("cart", {
    maxAge: 60 * 60 * 24,
    watch: true,
  });
  const products = reactive<Record<number, { count: number }>>(
    productsCookie.value || {},
  );

  const form = reactive<{
    name?: string;
    phone?: string;
    email?: string;
    adress?: string;
  }>({
    name: undefined,
    phone: undefined,
    email: undefined,
    adress: undefined,
  });

  const saveToCookie = () => {
    productsCookie.value = { ...products };
  };

  watch(
    products,
    () => {
      saveToCookie();
    },
    { deep: true },
  );

  const post = async (): Promise<{ error: null | any }> => {
    if (
      typeof form.name === "undefined" ||
      typeof form.phone === "undefined" ||
      typeof form.email === "undefined" ||
      typeof form.adress === "undefined"
    )
      return { error: { message: "form requiered" } };

    const config = useRuntimeConfig();

    let productsPost: OrderProductPost[] = [];

    Object.keys(products).forEach((k) => {
      const id = Number(k);
      if (products[id]) {
        productsPost.push({ count: products[id].count, product_id: id });
      }
    });

    const scheme: OrderPost = {
      name: form.name,
      email: form.email,
      phone: form.phone,
      adress: form.adress,
      products: productsPost,
    };

    const { data, error } = await useFetch("/api/client/order", {
      method: "POST",
      body: scheme,
      baseURL: config.public.apiBase,
    });

    if (!error.value) {
      form.name = undefined;
      form.adress = undefined;
      form.email = undefined;
      form.phone = undefined;

      Object.keys(products).forEach((key) => {
        delete products[Number(key)];
      });
    }

    return { error };
  };

  const addProduct = (id: number) => {
    if (!products[id]) {
      products[id] = { count: 1 };
    } else {
      products[id].count++;
    }
  };

  const removeProduct = (id: number) => {
    if (!products[id]) return;

    if (products[id].count === 1) {
      delete products[id];
    } else {
      products[id].count--;
    }
  };

  const inCart = (id: number) => id in products;
  const inCartCount = (id: number) => products[id]?.count || 0;

  const total = computed(() => {
    return Object.values(products).reduce((sum, item) => sum + item.count, 0);
  });

  const formValid = computed(() => {
    if (
      typeof form.name === "undefined" ||
      typeof form.phone === "undefined" ||
      typeof form.email === "undefined" ||
      typeof form.adress === "undefined"
    )
      return false;
    return true;
  });

  onMounted(() => {
    if (productsCookie.value) {
    }
  });

  return {
    form,
    formValid,
    products,
    post,
    inCart,
    inCartCount,
    addProduct,
    removeProduct,
    total,
  };
});
