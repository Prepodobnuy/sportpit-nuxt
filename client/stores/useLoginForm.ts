import * as v from "valibot";

export const useLoginForm = defineStore("auth", () => {
  const auth = useAuth();

  const state = reactive({
    loading: false,
  });

  const form = reactive<{
    username?: string;
    password?: string;
  }>({
    username: undefined,
    password: undefined,
  });

  const schema = v.object({
    username: v.pipe(
      v.string("Обязательное поле"),
      v.minLength(4, "Минимум 4 символа"),
      v.maxLength(30, "Максимум 30 символов"),
    ),
    password: v.pipe(
      v.string("Обязательное поле"),
      v.minLength(8, "Минимум 8 символов"),
      v.maxLength(30, "Максимум 30 символов"),
    ),
  });

  const login = async () => {
    if (
      typeof form.username === "undefined" ||
      typeof form.password === "undefined"
    )
      return;
    state.loading = true;
    try {
      await auth.login({
        username: form.username,
        password: form.password,
      });
    } catch (err) {
    } finally {
      state.loading = false;
    }
  };

  return { state, form, schema, login };
});
