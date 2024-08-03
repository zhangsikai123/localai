<template>
  <Sidebar/>
  <div class="entry-container">
    <h1></h1>
    <div class="entry-input-box">
      <a-input type="text" v-model:value="userInput" placeholder="Tell AI what you want to do!" @keyup.enter="navigateToChat"/>
      <button @click="navigateToChat">➤</button>
    </div>
    <div class="entry-shortcut-tips">
    </div>
  </div>
</template>
<script lang="ts">
 import { ref } from 'vue';
 import Sidebar from './Sidebar.vue';
 import threadService from "@/backend/threadService";
 import { getUserOrRedirect } from '@/composables/user';
 import { useRouter } from "vue-router";
export default {
  components: {
    Sidebar,
  },
  setup() {
	const user = getUserOrRedirect();
	const router = useRouter();
	const userInput = ref(null);
	const navigateToChat = async () => {
	  if (userInput.value != null && userInput.value != "") {
		try{
		  const response = await threadService.createThread();
		  router.push({ name: 'ChatWindow', query: { id: response.data.id, input: userInput.value }});
		} catch (error) {
		  console.error(error)
		}
	  }
	}
	return {
	  user,
	  userInput,
	  navigateToChat,
	}
  }
};
</script>
