<script setup lang="ts">
import { UiDropdown } from "#components";

const { state } = useCatalogStore();
const { breakpoint, isLessOrEquals } = useViewport();

const cols = ref(4);
const { categoriesRef } = useCathegory();
const store = useCatalogStore();

watch(breakpoint, () => {
  cols.value = 4;
  if (isLessOrEquals("tablet")) cols.value = 3;
  if (isLessOrEquals("mobileWide")) cols.value = 2;
  if (isLessOrEquals("mobileMedium")) cols.value = 1;
});
</script>

<template>
  <div class="catalog-wrapper">
    <div class="aside-wrapper">
      <UiButton
        class="close-button"
        :class="state.asideActive ? 'active' : ''"
        :trailing="
          state.asideActive
            ? 'hugeicons:arrow-left-03'
            : 'hugeicons:arrow-right-03'
        "
        :label="state.asideActive ? '' : 'Параметры'"
        size="sm"
        :icon="state.asideActive"
        :fw="false"
        variant="outline"
        :color="state.asideActive ? 'neutral' : 'success'"
        @click="state.asideActive = !state.asideActive"
      />
      <Transition name="slide">
        <aside v-if="state.asideActive">
          <UiButton
            v-for="c in categoriesRef"
            :toggle="c.id == store.state.selected_cathegory"
            @click="store.state.selected_cathegory = c.id"
            :key="c.id"
            :label="c.name"
            variant="ghost"
            start
          />
        </aside>
      </Transition>
    </div>

    <div class="main-wrapper">
      <main>
        <div class="search-bar">
          <UiInput
            v-model="store.state.prompt"
            style="width: 100%; flex-shrink: 1"
            variant="outline"
          />
          <UiDropdown align="right">
            <template #head>
              <UiButton
                style="flex-shrink: 0"
                leading="hugeicons:menu-01"
                icon
                variant="outline"
              />
            </template>
            <p style="margin: calc(var(--pd) * 2); font-size: 0.9em">
              Сортировать по
            </p>
            <UiButton
              :toggle="store.state.selected_search_filter === 0"
              @click="store.state.selected_search_filter = 0"
              label="названию"
              variant="ghost"
              start
              size="sm"
              roundness="none"
            />
            <UiButton
              :toggle="store.state.selected_search_filter === 1"
              @click="store.state.selected_search_filter = 1"
              label="цене"
              variant="ghost"
              start
              size="sm"
              roundness="none"
            />
            <UiButton
              :toggle="!store.state.reversed_search"
              @click="store.state.reversed_search = false"
              label="возрастанию"
              variant="ghost"
              start
              size="sm"
              roundness="none"
            />
            <UiButton
              :toggle="store.state.reversed_search"
              @click="store.state.reversed_search = true"
              label="убыванию"
              variant="ghost"
              start
              size="sm"
              roundness="none"
            />
          </UiDropdown>
        </div>
        <UiResponsiveGrid :cols="cols" :gap="12">
          <Card v-for="p in store.products" :key="p.id" :product="p" />
        </UiResponsiveGrid>
      </main>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.catalog-wrapper {
  display: inline-flex;
  width: 100%;
}

.aside-wrapper {
  cursor: pointer;
  pointer-events: none;
  position: fixed;
  left: 0;
  top: var(--margin-top);
  height: calc(100vh - var(--margin-top));
  max-width: 400px;
  width: calc(100vw - 50px);
  flex-shrink: 0;
  z-index: 3001;

  .close-button {
    z-index: 4000;
    pointer-events: all;
    position: absolute;
    bottom: var(--gap);
    left: var(--gap);
    transition:
      transform 500ms ease,
      background-color 200ms ease;
  }

  aside {
    padding: var(--gap);
    pointer-events: all;
    width: 100%;
    height: 100%;
    background-color: var(--window-bg);
    overflow-y: auto;
    box-shadow:
      0px 6px 6px 0 var(--shadow-color),
      0px 9999px 0px 9999px color-mix(in srgb, black 100%, transparent 100%);
  }
}

.main-wrapper {
  display: flex;
  width: 100%;
  flex-shrink: 1;
  justify-content: center;
  margin: var(--gap);

  main {
    max-width: 1100px;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: var(--gap);

    .search-bar {
      display: inline-flex;
      width: 100%;
      gap: var(--gap);
    }
  }
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}
</style>
