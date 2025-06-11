<script setup lang="ts">
import { useCartStore } from "~/stores/useCartStore";

const mobile = isMobile();
const { in_cart_count } = storeToRefs(useCartStore());
</script>

<template>
  <header class="w-[100vw] gap-1 p-1 inline-flex justify-center items-center">
    <div class="w-[1220px] gap-1 p-1 inline-flex justify-between items-center">
      <div class="gap-1 inline-flex justify-start items-center">
        <UButton
          leading-icon="hugeicons:product-loading"
          to="/"
          :label="mobile ? undefined : 'Каталог'"
          color="neutral"
          variant="ghost"
          :size="mobile ? 'xl' : 'lg'"
        />
        <div class="relative w-fit h-fit">
          <UButton
            leading-icon="hugeicons:shopping-basket-01"
            to="/cart"
            :label="mobile ? undefined : 'Корзина'"
            color="neutral"
            variant="ghost"
            :size="mobile ? 'xl' : 'lg'"
          />
          <div
            v-if="in_cart_count > 0"
            class="absolute bg-red-500 text-gray-100 p-[2px] text-[0.8em] rounded-md min-w-[20px] max-w-[40px] overflow-hidden flex items-center justify-center top-[-5px] right-[-5px]"
            style="pointer-events: none"
          >
            {{ in_cart_count }}
          </div>
        </div>
      </div>

      <div class="gap-1 inline-flex justify-start items-center">
        <HeaderThemeButton />
        <HeaderDropDown />
      </div>
    </div>
  </header>
</template>
