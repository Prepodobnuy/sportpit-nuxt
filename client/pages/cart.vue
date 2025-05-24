<script setup lang="ts">
const { form, products, post } = useCartStore();
const { total, formValid } = storeToRefs(useCartStore());

const viewConfirmPopup = ref(false);
const viewNotifyPopup = ref(false);
const isNotifyError = ref(false);

const empty = computed(() => {
  return Object.keys(products).length === 0;
});

const buttonHandle = () => {
  if (!formValid.value) return;
  viewConfirmPopup.value = true;
};

const closePopup = () => {
  viewConfirmPopup.value = false;
};

const closeNotifyPopup = () => {
  if (!isNotifyError.value) {
    navigateTo("/");
  }
};

const confirmOrder = async () => {
  closePopup();
  const { error } = await post();
  if (error.value) {
    viewNotifyPopup.value = true;
    isNotifyError.value = true;
    return;
  }
};
</script>

<template>
  <div v-if="viewConfirmPopup" class="popup" @click.self="closePopup()">
    <div class="body">
      <h1>
        Нажимая на кнопку "Продолжить" вы подтверждаете правильность введенных
        данных
      </h1>
      <div class="buttons">
        <UiButton
          color="error"
          label="Отмена"
          variant="outline"
          size="sm"
          @click="closePopup()"
        />
        <UiButton
          color="success"
          label="Продолжить"
          variant="outline"
          size="sm"
          @click="confirmOrder()"
        />
      </div>
    </div>
  </div>

  <div v-if="viewNotifyPopup" class="popup" @click="closeNotifyPopup()">
    <div class="body">
      <h1>
        {{
          isNotifyError
            ? "Ошибка при отправке заказа. Попробуйте позже"
            : "Заказ успешно отправлен! в течении 30-ти минут с вами свяжется оператор для уточнения деталей."
        }}
      </h1>
      <div class="buttons">
        <UiButton
          color="success"
          label="Ок"
          variant="outline"
          size="sm"
          @click="closeNotifyPopup()"
        />
      </div>
    </div>
  </div>

  <div v-if="empty" class="empty-wrapper">
    <div class="empty">
      <h1>Корзина пуста =(</h1>
      <UiButton
        leading="hugeicons:align-box-middle-left"
        variant="outline"
        label="Каталог"
        size="sm"
        :fw="false"
        @click="navigateTo('/')"
      />
    </div>
  </div>

  <div v-else class="cart-wrapper">
    <main>
      <h6>Товары в корзине</h6>
      <div class="products">
        <ProductCartEntry
          v-for="p in Object.keys(products)"
          :product_id="Number(p)"
          :count="products[Number(p)].count"
        />
      </div>

      <div class="order-wrapper">
        <div class="order">
          <h6>Имя</h6>
          <UiInput
            style="width: 100%; flex-shrink: 1"
            variant="outline"
            size="sm"
            v-model="form.name"
          />
          <h6>Номер телефона</h6>
          <UiInput
            style="width: 100%; flex-shrink: 1"
            variant="outline"
            size="sm"
            v-model="form.phone"
          />
          <h6>Почта</h6>
          <UiInput
            style="width: 100%; flex-shrink: 1"
            variant="outline"
            size="sm"
            v-model="form.email"
          />
          <h6>Адресс</h6>
          <UiInput
            style="width: 100%; flex-shrink: 1"
            variant="outline"
            size="sm"
            v-model="form.adress"
          />
        </div>
        <div class="bottom-line">
          <UiButton
            label="Продолжить"
            variant="outline"
            :color="formValid ? `success` : 'neutral'"
            size="sm"
            :fw="false"
            @click="buttonHandle()"
          />
        </div>
      </div>
    </main>
  </div>
</template>

<style lang="scss" scoped>
.popup {
  background-color: #00000055;
  display: flex;
  position: fixed;
  z-index: 5000;
  width: 100vw;
  height: 100vh;
  top: 0;
  left: 0;
  justify-content: center;
  align-items: center;

  .body {
    display: flex;
    flex-direction: column;
    gap: var(--gap);
    width: 100%;
    max-width: 600px;
    padding: var(--pd);
    background-color: var(--window-bg);
    border-radius: var(--br);

    h1 {
      text-align: center;
    }

    .buttons {
      display: inline-flex;
      gap: var(--gap);
    }
  }
}

.empty-wrapper {
  width: 100%;
  min-height: 70vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  .empty {
    align-items: center;
    width: 100%;
    max-width: 1100px;
    height: 100%;
    display: flex;
    flex-direction: column;

    gap: calc(var(--gap) * 3);

    h1 {
      font-size: 1.5em;
      font-weight: 900;
    }
  }
}

.cart-wrapper {
  display: inline-flex;
  width: 100%;
  justify-content: center;

  main {
    width: 100%;
    max-width: 1200px;
    display: flex;
    flex-direction: column;
    gap: var(--gap);
    padding: var(--pd);

    .products {
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: var(--gap);
      overflow-y: auto;
      max-height: 480px;
    }

    .products-empty {
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 10px;
      align-items: center;

      h1 {
        font-weight: 800;
        font-size: 1.1em;
      }
    }

    .order-wrapper {
      display: flex;
      flex-direction: column;
      gap: calc(var(--gap) * 2.5);
      width: 100%;
      align-items: center;

      .order {
        display: flex;
        flex-direction: column;
        width: 100%;
        gap: var(--gap);
      }

      .bottom-line {
        width: 100%;
        display: inline-flex;
        flex-direction: row-reverse;
      }
    }
  }
}
</style>
