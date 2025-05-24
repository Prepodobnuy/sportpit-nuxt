<script setup lang="ts">
import OrderEntry from "~/components/orderEntry.vue";

const { pendingOrders, workingOrders, completedOrders } = useOrder();
const current_tab = ref(0);
const tabs = [
  { label: "Актуальные" },
  { label: "В процессе" },
  { label: "Завершенные" },
];

console.clear();
console.log(pendingOrders.value);
console.log(workingOrders.value);
console.log(completedOrders.value);
</script>

<template>
  <div class="orders-wrapper">
    <main>
      <UiTabs
        style="border-radius: var(--br); overflow: hidden"
        :tabs="tabs"
        full-width
        v-model="current_tab"
      />
      <section v-if="current_tab === 0">
        <OrderEntry v-for="o in pendingOrders" :order="o" />
      </section>
      <section v-if="current_tab === 1">
        <OrderEntry v-for="o in workingOrders" :order="o" />
      </section>
      <section v-if="current_tab === 2">
        <OrderEntry v-for="o in completedOrders" :order="o" />
      </section>
    </main>
  </div>
</template>

<style lang="scss" scoped>
.orders-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;

  align-items: center;
}

main {
  padding: var(--pd);
  width: 100%;
  max-width: 1100px;
}

section {
  padding: var(--gap);
  display: flex;
  flex-direction: column;
  gap: var(--gap);
}
</style>
