<script setup lang="ts">
import { UiButton, UiInput } from "#components";

const { categoriesRef, addCategory, updateCategory, deleteCategory, refresh } =
  useCathegory();

const value = ref("");

const createCathegory = async () => {
  await addCategory(value.value);
  await refresh();
  value.value = "";
};

const deleteCath = async (id: number) => {
  await deleteCategory((id = id));
  await refresh();
};

const timeOut = ref(null);

const handleInput = (id: number, name: string) => {
  if (timeOut) clearTimeout(timeOut.value);

  timeOut.value = setTimeout(async () => {
    updateCategory(id, name);
  }, 260);
};
</script>

<template>
  <div class="caths-wrapper">
    <main>
      <div class="top-bar">
        <UiInput
          style="width: 100%; flex-shrink: 1"
          v-model="value"
          size="sm"
        />
        <UiButton
          trailing="hugeicons:add-square"
          label="Добавить"
          :fw="false"
          size="sm"
          @click="createCathegory()"
        />
      </div>
      <div v-for="c in categoriesRef" class="cathegory" :key="c.id">
        <UiInput
          style="width: 100%; flex-shrink: 1"
          v-model="c.name"
          size="sm"
          variant="outline"
          @input="handleInput(c.id, c.name)"
        />
        <UiButton
          leading="hugeicons:delete-02"
          icon
          :fw="false"
          size="sm"
          variant="outline"
          @click="deleteCath(c.id)"
        />
      </div>
    </main>
  </div>
</template>

<style lang="scss" scoped>
.caths-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;

  main {
    width: 100%;
    max-width: 1100px;
    padding: var(--pd);
    display: flex;
    flex-direction: column;
    gap: var(--gap);

    .top-bar {
      display: inline-flex;
      gap: var(--gap);
    }
  }
}

.cathegory {
  display: inline-flex;
  gap: var(--gap);
}
</style>
