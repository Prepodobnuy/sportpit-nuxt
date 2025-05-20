export const useLoginForm = defineStore("login", () => {
  const { login } = useAuth();

  const form = reactive({
    username: "",
    password: "",
  });

  const post = async () => {
    await login({
      username: form.username,
      password: form.password,
    });
  };

  return {
    form,
    post,
  };
});
