<template>
  <a-layout class="activation-layout">
    <a-spin :spinning="loading">
      <div v-if="message" class="activation-message">{{ message }}</div>
    </a-spin>
  </a-layout>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { Layout, Spin, message as antMessage } from 'ant-design-vue';
import userService from '@/backend/userService'; // Assume you have a service for user operations

export default defineComponent({
  components: {
    'a-layout': Layout,
    'a-spin': Spin,
  },
  setup() {
    const router = useRouter();
    const loading = ref(true);
    const message = ref('');

    onMounted(async () => {
      try {
        // Assume the token is passed as a query parameter
        const activatecode = router.currentRoute.value.query.activation_code;
        if (!activatecode) {
          throw new Error('No activation token provided.');
        }

        // Replace this with the actual activation call to your userService
        await userService.activateAccount(activatecode);

        antMessage.success('Account activated successfully!');
        message.value = 'Your account has been activated successfully. Redirecting to login...';

        // Redirect to the login page after a short delay
        setTimeout(() => {
          router.push('/');
        }, 3000);

      } catch (err) {
        antMessage.error('Failed to activate account.' + err);
        message.value = 'Failed to activate your account. Please try again or contact support.';
        loading.value = false;
      }
    });

    return {
      loading,
      message,
    };
  },
});
</script>

<style scoped>
.activation-layout {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.activation-message {
  text-align: center;
}
</style>
