export const useGridColumns = () => {
  const { breakpoint, isLessOrEquals } = useViewport();

  const cols = ref(4);

  watch(breakpoint, () => {
    cols.value = 4;
    if (isLessOrEquals("tablet")) cols.value = 3;
    if (isLessOrEquals("mobileWide")) cols.value = 2;
    if (isLessOrEquals("mobileMedium")) cols.value = 1;
  });

  return {
    cols,
  };
};
