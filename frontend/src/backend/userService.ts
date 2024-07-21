// userService.ts
import apiClient from "./apiClient";
import qs from "qs";

const userService = {
  async activateAccount(activatecode: string) {
		const response = await apiClient.get("/activate?activate_code=" + activatecode);
		return response;
  },
  async login(username: string, password: string) {
    const response = await apiClient.post(
      "/token",
      qs.stringify({
        grant_type: "password",
        username: username,
        password: password,
      }),
      {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      },
    );
    return response;
  },

  async signup(email: string, password: string) {
    const response = await apiClient.post("/signup",{
      email: email,
      password: password,
    }
    );
    return response;
  },
  async logout() {
    await apiClient.post("/logout");
  },
  async getUser(token: string) {
    const response = await apiClient.get("/me", {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response;
  },
};

export default userService;
