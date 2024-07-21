// src/store/auth.ts
import { Module } from "vuex";
import axios from "axios";
import qs from "qs";
import { RootState } from "index"; // Import your RootState type if you have one
import { router } from "@/router"; // Import your Vue router instance
import userService from "@/backend/userService";

interface User {
  id: string;
  name: string;
  // Add other user properties here
}

interface AuthState {
  user: User | null;
}

export const authModule: Module<AuthState, RootState> = {
  namespaced: true,
  state: {
    user: JSON.parse(sessionStorage.getItem("user") || "null"),
	token: localStorage.getItem("token") || "",
  },
  getters: {
    isAuthenticated: (state): boolean => !!state.user,
    getUser: (state): User | null => state.user,
	getToken: (state): string => state.token,
  },
  mutations: {
	SET_TOKEN(state, token: token) {
      state.token = token;
	  localStorage.setItem("token", token);
    },
    SET_USER(state, user: User) {
      state.user = user;
      sessionStorage.setItem("user", JSON.stringify(user));
    },
    CLEAR_USER(state) {
      state.user = null;
      sessionStorage.removeItem("user");
	  localStorage.removeItem("token");
    },
  },
  actions: {
    async login(
      { commit, getters },
      { username, password }: { username: string; password: string },
    ) {
      // check if already logged in
      if (getters.isAuthenticated) {
        return;
      } else {
        const formData = new FormData();
        try {
          const response = await userService.login(username, password);
          const userResponse = await userService.getUser(
            response.data.access_token,
          );
          if (userResponse.data == null) {
            throw new Error("response from userService.getUser is null");
          }
		  commit("SET_TOKEN", response.data.access_token);
          commit("SET_USER", userResponse.data);
        } catch (error) {
          throw error;
        }
      }
    },
    logout({ commit }) {
      commit("CLEAR_USER");
      // Optionally, redirect to the login page after logout
      router.push("/");
    },
  },
};
