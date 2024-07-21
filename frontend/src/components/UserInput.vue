<template>
	<div class="user-input">
		<a-textarea type="text" v-model="inputText" placeholder="Send another message or file..." @pressEnter="send" />
	</div>
</template>
<script lang="ts">
import { ref } from 'vue';

export default {
  setup(props, { emit }) {
    const inputText = ref('');

    function send() {
      if (inputText.value.trim()) {
        emit('sendMessage', inputText.value);
        inputText.value = ''; // Clear input after sending
      }
    }
	return {
      inputText,
      send,
    };
  },
};

</script>
