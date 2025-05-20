export const useAuth = () => {
  const config = useRuntimeConfig();

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

      const { data, error } = await useFetch<{
        access_token: string;
        token_type: string;
      }>("/api/auth/login", {
        baseURL: config.public.apiBase,
        method: "POST",
        body: formData,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      if (error.value) throw error.value;

      if (data.value) {
        token.value = data.value.access_token;
      }

      return navigateTo("/");
    } catch (err) {
      throw err;
    }
  };

  const logout = () => {
    token.value = null;
    return navigateTo("/login");
  };

  const logged = computed(() => token.value !== null);

  return {
    token,
    login,
    logout,
    logged,
  };
};
