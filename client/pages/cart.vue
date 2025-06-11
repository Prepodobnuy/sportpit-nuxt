<script setup lang="ts">
import { ProductRow, UButton } from "#components";

const { state, form, post, in_cart_count } = useCartStore();
const toast = useToast();

const total_price = computed(() => {
  return state.products.reduce((total, item) => {
    const productStore = useProductStore(item.id);
    const product = productStore.data;
    const cost = Number(product?.cost) || 0;
    return total + cost * item.count;
  }, 0);
});

const submitOrder = async () => {
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
    return;
  }

  try {
    await post();
    toast.add({
      title: "Заказ отправлен!",
      description: "Дождитесь звонка оператора для уточнения деталей.",
      color: "success",
    });
  } catch (err) {
    toast.add({
      title: "Ошибка =(",
      description: "Ошибка при отправке заказа.",
      color: "error",
    });
  }
};
</script>

<template>
  <div class="w-full flex justify-center p-4">
    <div
      v-if="in_cart_count > 0"
      class="w-full max-w-[1100px] flex flex-col gap-2"
    >
      <ProductRow v-for="s in state.products" :id="s.id" />

      <UForm :state="form" class="grid gap-4" @submit="submitOrder">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
          <UFormGroup label="ФИО" name="name" required>
            <UInput
              v-model="form.name"
              placeholder="Иванов Иван Иванович"
              size="xl"
              class="w-full"
            />
          </UFormGroup>

          <UFormGroup label="Телефон" name="phone" required>
            <UInput
              v-model="form.phone"
              type="tel"
              placeholder="+375 25 123-45-67"
              size="xl"
              class="w-full"
            />
          </UFormGroup>

          <UFormGroup label="Email" name="email">
            <UInput
              v-model="form.email"
              type="email"
              placeholder="example@mail.com"
              size="xl"
              class="w-full"
            />
          </UFormGroup>

          <UFormGroup label="Адрес доставки" name="adress" required>
            <UInput
              v-model="form.adress"
              placeholder="г. Москва, ул. Примерная, д. 1"
              size="xl"
              class="w-full"
            />
          </UFormGroup>
        </div>

        <div class="flex flex-col items-end gap-4 mt-4">
          <div class="text-xl font-bold">
            Итого: {{ total_price.toFixed(2) }} $
          </div>

          <UButton
            type="submit"
            label="Подтвердить заказ"
            size="xl"
            :disabled="state.products.length === 0"
          />
        </div>
      </UForm>
    </div>
    <div
      v-else
      class="flex flex-col gap-2 items-center min-h-[80vh] justify-center"
    >
      <h1 class="text-[2em]">Корзина пуста =(</h1>
      <UButton label="На главную" @click="navigateTo('/')" />
    </div>
  </div>
</template>
