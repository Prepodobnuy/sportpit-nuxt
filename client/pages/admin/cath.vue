<script setup lang="ts">
const store = useCathegoriesStore();
</script>

<template>
  <div class="w-full flex justify-center">
    <div class="max-w-[1100px] w-full p-[20px] flex flex-col gap-2">
      <div v-for="c in store.categories" class="inline-flex gap-2 align-center">
        <div
          class="w-full h-10 flex align-center p-2 rounded-md light:bg-gray-200 bg-gray-700"
        >
          {{ c.name }}
        </div>
        <UButton
          size="xl"
          leading-icon="hugeicons:delete-02"
          color="error"
          class="aspect-[1/1] h-10 flex align-center justify-center"
          @click="store.deletee(c.id)"
        />
      </div>
      <div class="inline-flex gap-2 align-center">
        <UInput
          v-model="store.prompt"
          variant="subtle"
          size="xl"
          class="w-full"
        />

        <UButton
          size="xl"
          leading-icon="hugeicons:plus-sign-square"
          color="success"
          class="aspect-[1/1] h-10 flex align-center justify-center"
          @click="store.post()"
        />
      </div>
    </div>
  </div>
</template>
