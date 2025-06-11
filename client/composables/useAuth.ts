import type { User } from "~/types/user";

export const useAuth = () => {
  const config = useRuntimeConfig();
  const toast = useToast();

  const token = useCookie<string | null>("token", {
    default: () => null,
    maxAge: 60 * 60 * 24 * 7,
    watch: true,
    sameSite: "strict",
  });

  const login = async (credentials: { username: string; password: string }) => {
    try {
      const formData = new URLSearchParams();
      formData.append("username", credentials.username);
      formData.append("password", credentials.password);

      const { access_token } = await $fetch<{ access_token: string }>(
        "/api/auth/login",
        {
          baseURL: config.public.apiBase,
          method: "POST",
          body: formData,
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        },
      );

      token.value = access_token;
      toast.add({
        description: "Вы успешно вошли!",
        color: "success",
      });
      return navigateTo("/");
    } catch (err) {
      toast.add({
        description: "Ошибка при входе",
        color: "error",
      });
      throw err;
    }
  };

  const signup = async (credentials: {
    username: string;
    email: string;
    password: string;
  }) => {
    try {
      await $fetch("/api/auth/signup", {
        baseURL: config.public.apiBase,
        method: "POST",
        body: credentials,
        headers: {
          "Content-Type": "application/json",
        },
      });

      return await login({
        username: credentials.username,
        password: credentials.password,
      });
    } catch (err) {
      console.error("Signup error:", err);
      throw err;
    }
  };

  const logout = () => {
    token.value = null;
    toast.add({
      description: "Вы вышли из аккаунта",
      color: "success",
    });
  };

  const logged = computed(() => !!token.value);

  return {
    token: readonly(token),
    login,
    signup,
    logout,
    logged,
  };
};
