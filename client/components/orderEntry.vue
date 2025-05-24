<script setup lang="ts">
import { ProductAdminEntry } from "#components";
import { useOrder } from "#imports";
import type { Order } from "~/types/orders";

const { approveOrder, declineOrder, refresh } = useOrder();
const { order } = defineProps<{
  order: Order;
}>();

const active = ref(false);

const approve = async () => {
  await approveOrder(order.id);
  refresh();
};
const decline = async () => {
  await declineOrder(order.id);
  refresh();
};
</script>

<template>
  <div class="order-wrapper">
    <div>Заказ номер: {{ order.id }}</div>
    <div class="actions">
      <UiButton
        :label="active ? 'Свернуть' : 'Развернуть'"
        @click="active = !active"
        size="sm"
        :fw="false"
      />
      <UiButton
        label="Отменить"
        :fw="false"
        size="sm"
        color="error"
        @click="decline()"
      />
      <UiButton
        v-if="!order.completed"
        label="Подтвердить"
        :fw="false"
        size="sm"
        color="success"
        @click="approve()"
      />
    </div>
  </div>
  <menu v-if="active" class="active">
    <p class="title">Номер телефона</p>
    <p>{{ order.phone }}</p>
    <p class="title">Имя</p>
    <p>{{ order.name }}</p>
    <p class="title">Адрес</p>
    <p>{{ order.adress }}</p>
    <p class="title">Товары</p>
    <ProductAdminEntry v-for="p in order.products" :product="p.product" />
  </menu>
</template>

<style lang="scss" scoped>
.order-wrapper {
  display: inline-flex;
  gap: var(--gap);
  justify-content: space-between;
}

.actions {
  display: inline-flex;
  gap: var(--gap);
}

menu {
  display: flex;
  flex-direction: column;
  gap: var(--gap);
}

.title {
  opacity: 0.85;
  font-size: 0.85em;
}
</style>
