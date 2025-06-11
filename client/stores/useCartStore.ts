interface CartState {
  products: { id: number; count: number }[];
}

interface OrderProductPostScheme {
  products: { product_id: number; count: number }[];
}

export const useCartStore = defineStore("cart", () => {
  const config = useRuntimeConfig();
  const cookie = useCookie<CartState>("cart", {
    maxAge: 3600 * 24 * 7,
    default: () => ({ products: [] }),
  });

  const state = ref<CartState>(cookie.value);
  const form = reactive<{
    name: string;
    phone: string;
    email: string;
    adress: string;
    products: OrderProductPostScheme[];
  }>({
    name: "",
    phone: "",
    email: "",
    adress: "",
    products: [],
  });

  const add_product = (id: number) => {
    const existingProduct = state.value.products.find((p) => p.id === id);
    if (existingProduct) {
      existingProduct.count += 1;
    } else {
      state.value.products.push({ id, count: 1 });
    }
  };

  const set_product = (id: number, count: number) => {
    if (count <= 0) {
      remove_product(id);
      return;
    }

    const existingProduct = state.value.products.find((p) => p.id === id);
    if (existingProduct) {
      existingProduct.count = count;
    } else {
      state.value.products.push({ id, count });
    }
  };

  const remove_product = (id: number) => {
    const index = state.value.products.findIndex((p) => p.id === id);
    if (index !== -1) {
      if (state.value.products[index].count > 1) {
        state.value.products[index].count -= 1;
      } else {
        state.value.products.splice(index, 1);
      }
    }
  };

  const clear_product = (id: number) => {
    state.value.products = state.value.products.filter((p) => p.id !== id);
  };

  const clear_products = () => {
    state.value.products = [];
  };

  const in_cart_count = computed(() => {
    return state.value.products.reduce(
      (total, product) => total + product.count,
      0,
    );
  });

  const product_in_cart_count = (id: number) =>
    computed(() => {
      const pr = state.value.products.filter((v) => v.id === id);
      if (pr.length !== 1) return 0;
      return pr[0].count;
    });
  onMounted(() => {
    if (cookie.value) {
      state.value = cookie.value;
    }
  });

  const toast = useToast();

  const post = async (): Promise<{ error: null | any }> => {
    if (
      form.name.length < 4 ||
      form.phone.length < 7 ||
      form.email.length < 6 ||
      form.adress.length < 5
    ) {
      toast.add({
        title: "Ошибка",
        description: "Заполните форму",
        color: "error",
      });
      throw { error: { message: "form requiered" } };
      return { error: "asd" };
    }

    const config = useRuntimeConfig();

    const productsPost = state.value.products.map((v) => {
      return { product_id: v.id, count: v.count };
    });

    const scheme = {
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
      form.name = "";
      form.adress = "";
      form.email = "";
      form.phone = "";

      state.value.products = [];
    }

    return { error };
  };

  watch(
    () => state.value.products,
    (newProducts) => {
      cookie.value = { products: newProducts };
    },
    { deep: true },
  );

  return {
    state,
    form,
    add_product,
    set_product,
    remove_product,
    clear_product,
    clear_products,
    in_cart_count,
    product_in_cart_count,
    post,
  };
});
