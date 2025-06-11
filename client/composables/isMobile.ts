export const isMobile = () => {
  const viewport = useViewport();
  const breakpoint = "mobileWide";
  const mobile = ref(false);

  watch(viewport.breakpoint, (newValue, oldValue) => {
    mobile.value = viewport.isLessOrEquals(breakpoint);
  });

  onMounted(() => {
    mobile.value = viewport.isLessOrEquals(breakpoint);
  });

  return mobile;
};
