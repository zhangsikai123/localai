// user.ts
import { useRouter } from 'vue-router';
import { computed, ComputedRef } from 'vue';
import { useStore } from 'vuex';

export function getUserOrRedirect(): ComputedRef<any> {
  const router = useRouter();
  const store = useStore();

  const isAuthenticated = computed(() => store.getters["auth/isAuthenticated"]);
  const user = computed(() => store.getters["auth/getUser"]);
  if (!isAuthenticated.value) {
    // Redirect to the root page
    router.push("/");
  } else {
    return user.value;
  }
}

export function hasLoggedin(): void {
  const router = useRouter();
  const store = useStore();
  const isAuthenticated = computed(() => store.getters["auth/isAuthenticated"]);
  return isAuthenticated.value
}
