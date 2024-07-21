// apiClient.ts
import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL,
});

apiClient.interceptors.request.use(
  (config) => {
		const token = localStorage.getItem("token");
		if (token) {
			config.headers["Authorization"] = `Bearer ${token}`;
		}
		return config;
	},
	(error) => {
		return Promise.reject(error);
	},
)

apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (
      error.response != null &&
      error.response.data != null &&
      error.response.data.detail != null
    ) {
      if (typeof error.response.data.detail != "string") {
        throw Error(error.message);
      } else {
        throw Error(error.response.data.detail);
      }
    } else {
      throw Error(error.message);
    }
  },
);
export default apiClient;
