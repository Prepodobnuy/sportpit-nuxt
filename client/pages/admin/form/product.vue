<script setup lang="ts">
import * as v from "valibot";
import type { FormSubmitEvent } from "@nuxt/ui";
import { MdEditor } from "md-editor-v3";
import "md-editor-v3/lib/style.css";
import ImageInput from "~/components/ImageInput.vue";
import CathegorySelect from "~/components/cathegorySelect.vue";

const { form, schema, state, post } = useProductForm();
const toast = useToast();
const { categories, selected_cathegory, selected_cathegory_id } = storeToRefs(
  useCathegoriesStore(),
);

type Schema = v.InferOutput<typeof schema>;

async function onSubmit(event: FormSubmitEvent<Schema>) {}
</script>

<template>
  <div class="w-[100vw] p-[20px] inline-flex justify-center">
    <UForm
      class="flex flex-col h-max p-1 rounded-md items-center gap-2 max-w-[900px] w-[100%] bg-gray-800 light:bg-gray-200"
      :schema="schema"
      :state="form"
    >
      <UFormField label="Обложка" class="self-start w-full">
        <ImageInput v-model="form.cover" :aspect="295 / 221" />
      </UFormField>
      <UFormField label="Название" class="self-start w-[100%]" name="name">
        <UInput v-model="form.name" class="w-[100%]" variant="subtle" />
      </UFormField>

      <UFormField label="Цена" class="self-start w-[100%]" name="cost">
        <UInput v-model="form.cost" class="w-[100%]" variant="subtle" />
      </UFormField>

      <UFormField label="Количество" class="self-start w-[100%]" name="count">
        <UInputNumber v-model="form.count" class="w-[100%]" variant="subtle" />
      </UFormField>

      <UFormField label="Категория" class="self-start w-full">
        <CathegorySelect />
      </UFormField>

      <UFormField
        label="Описание"
        class="self-start w-[100%]"
        name="description"
      >
        <MdEditor class="rounded-md" v-model="form.description" />
      </UFormField>

      <UButton
        class="mt-3 self-end"
        label="Отправить"
        type="submit"
        :loading="state.loading"
        @click="post(selected_cathegory_id)"
      />
    </UForm>
  </div>
</template>
