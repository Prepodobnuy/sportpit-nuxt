<script setup lang="ts">
import { useLoginForm } from "~/forms/useLoginForm";

const { form, post } = useLoginForm();
</script>

<template>
  <div class="login-wrapper">
    <main>
      <h6>Логин</h6>
      <UiInput
        v-model="form.username"
        style="width: 100%"
        variant="outline"
        size="sm"
      />
      <div />
      <h6>Пароль</h6>
      <UiInput
        v-model="form.password"
        style="width: 100%"
        type="password"
        variant="outline"
        size="sm"
      />
      <div />
      <div class="button-box">
        <UiButton
          leading="hugeicons:account-setting-03"
          label="Вход"
          size="sm"
          color="success"
          :fw="false"
          @click="post()"
        />
      </div>
    </main>
  </div>
</template>

<style lang="scss" scoped>
.login-wrapper {
  width: 100%;
  height: calc(85vh - var(--margin-top));

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  main {
    width: 100%;
    max-width: 600px;
    display: flex;
    flex-direction: column;
    gap: var(--gap);
    padding: var(--pd);

    .button-box {
      display: inline-flex;
      flex-direction: row-reverse;
    }
  }
}
</style>
