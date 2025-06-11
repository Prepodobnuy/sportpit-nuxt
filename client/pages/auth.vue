<script setup lang="ts">
import * as v from "valibot";
import type { FormSubmitEvent } from "@nuxt/ui";

const { form, schema, state } = useLoginForm();
const auth = useAuth();

type Schema = v.InferOutput<typeof schema>;

async function onSubmit(event: FormSubmitEvent<Schema>) {
  auth.login({
    username: event.data.username,
    password: event.data.password,
  });
}
</script>

<template>
  <div class="w-[100vw] p-2 inline-flex justify-center">
    <UForm
      class="flex flex-col h-max p-1 rounded-md items-center gap-2 max-w-[700px] w-[100%] bg-gray-800 light:bg-gray-200"
      :schema="schema"
      :state="form"
      @submit="onSubmit"
    >
      <UFormField label="Юзернейм" class="self-start w-[100%]" name="username">
        <UInput v-model="form.username" class="w-[100%]" variant="subtle" />
      </UFormField>

      <UFormField label="Пароль" class="self-start w-[100%]" name="password">
        <UInput
          v-model="form.password"
          class="w-[100%]"
          variant="subtle"
          type="password"
        />
      </UFormField>

      <UButton
        class="mt-3 self-end"
        label="Отправить"
        type="submit"
        :loading="state.loading"
      />
    </UForm>
  </div>
</template>
