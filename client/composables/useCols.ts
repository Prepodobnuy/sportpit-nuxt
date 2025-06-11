export const useCols = () => {
  const viewport = useViewport();
  const divider = 200;
  const cols = ref(4);

  watch(viewport.breakpoint, (newValue, oldValue) => {
    cols.value = Math.min(
      4,
      Math.max(
        1,
        Math.floor(
          viewport.breakpointValue(viewport.breakpoint.value) / divider,
        ),
      ),
    );
  });

  onMounted(() => {
    cols.value = Math.min(
      4,
      Math.max(
        1,
        Math.floor(
          viewport.breakpointValue(viewport.breakpoint.value) / divider,
        ),
      ),
    );
  });

  return cols;
};
