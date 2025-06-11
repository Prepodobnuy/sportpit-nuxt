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
  isDark.value ? "heroicons:moon-16-solid" : "heroicons:sun-16-solid",
);

const cycle = () => {
  isDark.value = !isDark.value;
};
</script>

<template>
  <UButton
    :leading-icon="icon"
    variant="ghost"
    color="neutral"
    size="xl"
    @click="cycle"
  />
</template>
