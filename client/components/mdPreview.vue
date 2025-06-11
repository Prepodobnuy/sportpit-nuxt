<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import markdownIt from "markdown-it";
import DOMPurify from "dompurify";

const model = defineModel<string | undefined>(undefined);

const md = markdownIt({
  html: true,
  linkify: true,
  typographer: true,
});

const isClient = ref(false);

onMounted(() => {
  isClient.value = true;
});

const htmlContent = computed(() => {
  if (!model.value) return "";

  const rawHtml = md.render(model.value);
  return isClient.value ? DOMPurify.sanitize(rawHtml) : rawHtml;
});
</script>

<template>
  <div class="flex flex-col md:flex-row w-full min-h-[300px] gap-2">
    <div class="flex-1 w-[50%] rounded-lg overflow-hidden">
      <UTextarea
        v-model="model"
        class="w-full h-full font-mono text-sm"
        :ui="{ base: 'h-full resize-none' }"
        placeholder="..."
      />
    </div>

    <div class="flex-1 w-[50%]">
      <ClientOnly>
        <div
          class="markdown-preview h-full rounded-lg pt-1 pl-2 overflow-auto bg-white"
          v-html="htmlContent"
        />
        <template #fallback>
          <div class="h-full flex items-center justify-center text-gray-500">
            Загрузка предпросмотра...
          </div>
        </template>
      </ClientOnly>
    </div>
  </div>
</template>
