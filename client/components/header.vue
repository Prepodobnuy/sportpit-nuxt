<script setup lang="ts">
const { logged, logout } = useAuth();

const handleExit = () => {
  logout();
};
</script>

<template>
  <header>
    <div class="header__content">
      <div class="left">
        <UiButton
          leading="hugeicons:align-box-middle-left"
          variant="ghost"
          label="Каталог"
          :fw="false"
          @click="navigateTo('/')"
        />
        <CartHeaderButton />
      </div>

      <div class="right">
        <ThemeButton />
        <UiDropdown align="right">
          <template #head>
            <UiButton
              leading="hugeicons:menu-01"
              variant="ghost"
              icon
              :fw="false"
            />
          </template>
          <UiButton
            v-if="!logged"
            leading="hugeicons:account-setting-02"
            label="Войти"
            variant="ghost"
            roundness="none"
            size="sm"
            start
            @click="navigateTo('/login')"
          />
          <UiButton
            v-if="logged"
            leading="hugeicons:apple-pie"
            label="Товары"
            variant="ghost"
            roundness="none"
            size="sm"
            start
            @click="navigateTo('/admin/product')"
          />
          <UiButton
            v-if="logged"
            leading="hugeicons:product-loading"
            label="Заказы"
            variant="ghost"
            roundness="none"
            size="sm"
            start
            @click="navigateTo('/admin/orders')"
          />
          <UiButton
            v-if="logged"
            leading="hugeicons:tag-02"
            label="Категории"
            variant="ghost"
            roundness="none"
            size="sm"
            start
            @click="navigateTo('/admin/cathegories')"
          />
          <UiButton
            v-if="logged"
            label="Выйти"
            variant="ghost"
            roundness="none"
            size="sm"
            color="error"
            start
            @click="handleExit()"
          />
        </UiDropdown>
      </div>
    </div>
  </header>
</template>

<style lang="scss" scoped>
header {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  background-color: var(--window-bg);
  box-shadow: var(--header-shadow);

  .header__content {
    display: inline-flex;
    height: 100%;
    max-width: calc(1600px * var(--root-scale));
    width: 100%;
    justify-content: space-between;

    .left,
    .right {
      display: inline-flex;
      gap: var(--gap);
      align-items: center;
      margin: 0 var(--gap);

      * {
        flex-shrink: 0;
      }
    }
  }
}
</style>
