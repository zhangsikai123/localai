<template>
<Sidebar/>
<section class="chat-container">
  <!-- Messages list -->
  <div class="messages-list" ref="messagesList" @scroll="checkScrollPosition">
    <chat-message
      v-for="(message, index) in messages"
      :key="index"
      :text="messageText(message)"
      :sender="message.sender"
	  :is-typing="message.isTyping"
      ></chat-message>
  </div>
  <a-button v-show="!isScrolledToBottom" @click="scrollToBottomButton" class="scroll-to-bottom-button" shape="circle">
	<template #icon>
      <DownOutlined />
    </template>
  </a-button>
  <!-- User input container -->
  <div class="user-input-container">
	<a-textarea  class="user-input-area" type="text" v-model:value="inputText" placeholder="Send another message or file..." @pressEnter="handleInputAreaEnter"/>
	<Button v-if="isGenerating" size="middle" type="primary" shape="circle" @click="stopGeneration" class="stop-button">stop</Button>
	<Button v-else size="middle" type="primary" shape="circle" @click="handleSendMessage" class="send-button">send</Button>
  </div>
</section>
</template>
<script lang="ts">
 import {
  h,
  defineComponent,
  ref,
  nextTick,
  onMounted,
  watch,
  computed,
 } from "vue";
 import { DownOutlined } from '@ant-design/icons-vue';
 import { getUserOrRedirect } from "@/composables/user";
 import { useRouter, useRoute } from "vue-router";
 import { Button } from "ant-design-vue";
 import ChatMessage from "./ChatMessage.vue";
 import UserInput from "./UserInput.vue";
 import Sidebar from "./Sidebar.vue";
 import threadService from "@/backend/threadService";
 import chatService from "@/backend/chatService";
import { parseHistory } from "@/composables/chat";
 export default defineComponent({
   components: {
	 DownOutlined,
     Sidebar,
     ChatMessage,
     UserInput,
	 Button,
  },
   setup(props) {
	 const inputText = ref(""); // Add this line to declare the ref
     const router = useRouter();
     const messages = ref([]);
	 const messagesList = ref(null); // Reference to the messages list DOM element
	 const isGenerating = ref(false);
     const route = useRoute();
     const threadId = ref(route.query.id);
     const user = getUserOrRedirect();
	 const stopGeneratingSignal = ref(false);
	 const isScrolledToBottom = ref(true);
	 const checkScrollPosition = () => {
      if (messagesList.value) {
        isScrolledToBottom.value = messagesList.value.scrollHeight - messagesList.value.clientHeight <= messagesList.value.scrollTop + 1;
      }
    };

    const scrollToBottomButton = () => {
      if (!isScrolledToBottom.value) {
        messagesList.value.scrollTop = messagesList.value.scrollHeight;
      }
    };
	 const stopGeneration = () => {
       // Set isGenerating to false to stop the generation
       isGenerating.value = false;
	   stopGeneratingSignal.value = true;
	 };

	const scrollToBottom = () => {
      nextTick(() => {
        if (messagesList.value) {
          messagesList.value.scrollTop = messagesList.value.scrollHeight;
        }
      });
    };
     const messageText = (message) => {
       return computed(() => {
         // Join the words into a single string and append a cursor
		 let result = ""
		 if (message == null || message.content == null ){
		   return result;
		 }
		 const content = message.content

         if (typeof content == "string") {
           result = content;
         } else {
           result = content.join("");
         }
		 if (message.isTyping){
		   result += " ▌"
		 }
		 return result;
       }).value;
     };
     async function loadMessages(id) {
       try {
         const response = await threadService.getThreadMessages(id);
         if (response.data.length > 0) {
           messages.value = response.data;
		   scrollToBottom();
         } else {}
       } catch (error) {
         alert(error);
      }
     }

	 // Initial load when the component is mounted
     onMounted(() => {
	   if (threadId.value != null) {
         loadMessages(threadId.value);
	   }
     });
     watch(
       () => route.query.id,
       (newThreadId, oldThreadId) => {
         if (newThreadId !== oldThreadId) {
           loadMessages(newThreadId);
         }
       }
     );
	 const handleInputAreaEnter = (event) => {
	   event.preventDefault();
	   const text = inputText.value.trim();
	   if (event.shiftKey) {
		 inputText.value += "\n"
		 return
	   }
	   if (text === "") { return }
	   handleSendMessage();
	 }

     const handleSendMessage = async () => {
	   const history_window = 5;
       const history = parseHistory(messages.value, history_window);
	   const text = inputText.value.trim();
	   inputText.value = "";
	   if (text === "") { return }
       const sender = "user";
	   const userMessage = { content: text, sender: sender, isTyping: false };
       messages.value.push(userMessage);
	   console.log(messages.value);
	   console.log(history);
	   scrollToBottom();

       try {
         // Send the message to the AI backend using Fetch API
         const response = await chatService.sendChat(userMessage.content, history);
        // Handle stream response
         if (response.body) {
           // Handle the stream response
		   isGenerating.value = true;
           const reader = response.body.getReader();
           let chunks = ""; // This will accumulate chunks of text
           const content = [""];
           const aiMessage = ref({
             content: content,
             sender: "ai",
             isTyping: true,
           });
		   scrollToBottom();
           messages.value.push(aiMessage.value);
           // Read the stream
           reader.read().then(function processText({ done, value }) {
             if (done || stopGeneratingSignal.value) {
               // Stream is complete
			   if (stopGeneratingSignal.value){
				 stopGeneratingSignal.value = false;
			   }
               console.log("Stream complete");
			   scrollToBottom();
			   isGenerating.value = false;
               aiMessage.value.isTyping = false;
			   aiMessage.value.content = messageText(aiMessage.value);
			   threadService.addMessageToThread(
				 threadId.value,
				 [{content: messageText(userMessage), sender: userMessage.sender},
				  {content:messageText(aiMessage.value), sender: aiMessage.value.sender}]
			   );
               return;
             }
             // Decode the stream chunk to text
             const chunkText = new TextDecoder().decode(value);
             chunks += chunkText;
             aiMessage.value.content.push(chunkText);
			 // if line break, add to messages
			 if (chunkText.includes("\n")){
			   scrollToBottom();
			 }

             // Read the next chunk
             reader.read().then(processText);
           });
         }
       } catch (error) {
         console.error("Error sending message:", error);
       }
     };

	 if (route.query.input != null) {
	   inputText.value = route.query.input
	   handleSendMessage();
	   route.query.input = null;
	}

     return {
	   handleInputAreaEnter,
	   inputText,
	   isGenerating,
       stopGeneration,
       messageText,
       messages,
       messagesList,
       handleSendMessage,
	   isScrolledToBottom,
       scrollToBottomButton,
       checkScrollPosition,
     };
  },
});
</script>
<style scoped>

.scroll-to-bottom-button {
  position: absolute;
  z-index: 999; /* Ensure it appears above other content */
}

.messages-container {
  display: flex;
  flex-direction: column;
 }


 /* chat window */
.chat-container {
  flex-grow: 1; /* Take remaining space */
  display: flex;
  flex-direction: column; /* Stack children vertically */
  position: relative;
  padding: 20px; /* Space around the chat container */
  padding-bottom: 120px; /* Space for the user input container */
  overflow: hidden; /* Prevents child elements from overflowing */
  align-items: center; /* Center items horizontally */
}

.messages-list {
  overflow-y: auto;
  padding: 10px 20px; /* Adjust padding as needed */
  width: 66.66%;
  scrollbar-width: none; /* For Firefox */
  -ms-overflow-style: none; /* For Internet Explorer and Edge */
  scroll-behavior: smooth;
 }

.messages-list::-webkit-scrollbar {
  display: none; /* For Chrome, Safari, and Opera */
}

/* user input */
.user-input {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 10px; /* Adjust the padding as needed */
  background-color: white; /* Or any other color that fits your design */
}


.user-input-container {
  position: absolute;
  bottom: 50px;
  left: 50%;
  transform: translateX(-50%);
  width: 66.66%;
  max-width: none;
  height: 60px; /* Adjust the height as needed to fit the input */
  z-index: 20;
  background-color: white;
  border-radius: 30px; /* Rounded corners for the container */
  border: 1px solid #ccc; /* Gray border for the container */
  box-shadow: 0 2px 5px rgba(0,0,0,0.2); /* Subtle shadow for depth */
  padding: 0; /* Padding removed to allow the input to fill the container */
  box-sizing: border-box; /* Include padding and border in the element's width and height */
  display: flex; /* Flexbox to align the input field */
  align-items: center; /* Center items vertically */
  overflow: hidden; /* Prevents child elements from overflowing */
}

.user-input-area {
  width: 100%; /* Full width of the container */
  height: 100%; /* Full height of the container */
  border: none; /* Remove individual input border */
  border-radius: 30px; /* Rounded corners for the input field, should match the container */
  outline: none; /* Remove focus outline */
  padding: 10px 20px; /* Padding inside the input field for text */
  box-sizing: border-box; /* Padding doesn't add to width/height */
 }

.stop-button {
  background-color: white; /* Set the background color */
  color: black; /* Set the text color */
  border: 2px solid black; /* Set the border */
  font-size: 10px; /* Set the font size */
  margin: 10px; /* Remove the margin */
  cursor: pointer; /* Change mouse cursor on hover */
  outline: none; /* Remove the outline */
  transition: all 0.3s; /* Smooth transition for hover effects */
}

.stop-button:hover {
  background-color: #f8f8f8; /* Slightly change color on hover */
 }

 .send-button {
   font-size: 10px; /* Set the font size */
   margin: 10px; /* Remove the margin */
   cursor: pointer; /* Change mouse cursor on hover */
   outline: none; /* Remove the outline */
   transition: all 0.3s; /* Smooth transition for hover effects */
}

.send-button:hover {
  background-color: #f8f8f8; /* Slightly change color on hover */
}
</style>
