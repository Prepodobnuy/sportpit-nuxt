<script setup lang="ts">
import type { DropdownMenuItem } from "@nuxt/ui";
import { function_ } from "valibot";

const auth = useAuth();
const items = computed((): DropdownMenuItem[][] => {
  let res: DropdownMenuItem[][] = [];

  if (!auth.token.value) {
    res.push([
      {
        label: "Войти",
        type: "link",
        to: "/auth",
      },
    ]);
  } else {
    res.push([
      {
        label: "Панель администратора",
        type: "label",
      },
      {
        label: "Товары",
        type: "link",
        to: "/admin/product",
      },
      {
        label: "Категории",
        type: "link",
        to: "/admin/cath",
      },
    ]);
    res.push([
      {
        label: "Выйти",
        type: "link",
        onSelect() {
          logout();
        },
      },
    ]);
  }

  return res;
});

function logout() {
  console.clear();
  console.log(auth.token.value);
  auth.logout();
}
</script>

<template>
  <UDropdownMenu :items="items">
    <UButton icon="i-lucide-menu" size="xl" color="neutral" variant="ghost" />
  </UDropdownMenu>
</template>
