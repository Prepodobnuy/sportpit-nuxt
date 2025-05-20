<script setup lang="ts">
const colorMode = useColorMode();

const isDark = computed({
  get() {
    return colorMode.value === "dark";
  },
  set(_isDark) {
    colorMode.preference = _isDark ? "dark" : "light";
  },
});

const icon = computed(() =>
  isDark.value ? "hugeicons:moon-02" : "hugeicons:sun-03",
);

const cycle = () => {
  isDark.value = !isDark.value;
};
</script>

<template>
  <UiButton :leading="icon" variant="ghost" icon @click="cycle" />
</template>
