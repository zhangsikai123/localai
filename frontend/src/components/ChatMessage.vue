<template>
  <div class="chat-message" :class="{ 'user-message': isUser, 'ai-message': !isUser }">
	<div class="profile">
	  <img :src="avatarSource" alt="Avatar" class="avatar" />
	  <div class="profile-name">{{ profileName }}</div>
	</div>
	<div class="message-container">
	  <div class="message-content">
		<div class="message-body" v-html="parsedText"></div>
	  </div>
	</div>
  </div>
</template>
<script lang="ts">
 import Clipboard from "clipboard";
 import { defineComponent, ref, computed } from 'vue';
 import { marked } from 'marked'
 import hljs from 'highlight.js';
 import { markedHighlight } from "marked-highlight";
 import 'highlight.js/styles/github-dark.min.css';
export default defineComponent({
  props: {
	text: String,
	sender: String,
	isTyping: Boolean
  },
   setup(
	 props,
   ) {
	 const renderer = {
	   code(code, language, escaped) {
		 if (props.sender == "user") {
		   return code;
		 }
		 const codeIndex = "codeblock-" + parseInt(Date.now() + "") + Math.floor(Math.random() * 10000000);
		 const highlightedCode = hljs.highlightAuto(code).value;
		 return `<pre class="marked-code-block">
		<div class="code-header">
			<span>${language}</span>
			<button id='copy-btn' data-clipboard-action="copy" data-clipboard-target="#${codeIndex}" class="codeblock-copy-button">copy code</button>
		</div>
		<code id=${codeIndex} class="hljs ${language}">${highlightedCode}</code></pre>`
	   }
	 };
	 marked.use({renderer})
	 const isUser = computed(() => props.sender == "user");
	 const parsedText = computed(() => {
	   let text = props.text;
	   if (props.sender == "user") {
		 text = text.replaceAll("\n", "<br>")
		 text = text.replaceAll("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
		 text = text.replaceAll(" ", "&nbsp;")
		 return text
	   }
	   return marked.parse(text)
	 });
	 const profileName = computed(() => {
	   return props.sender == "user"
        ? "You"
       : "Baozi";
	 });
	 const avatarSource = computed(() => {
	   return props.sender == "user"
        ? "src/assets/user.png"
       : "src/assets/baozi.png";
	 });
	 const clipboard = new Clipboard("#copy-btn");
    // 复制成功失败的提示
     clipboard.on("success", (e) => {
	   e.trigger.innerHTML = "copied";
	   setTimeout(() => {
		 e.trigger.innerHTML = "copy code";
		 e.clearSelection();
       }, 1000); // Change back after 2 seconds
	   console.log("copied")
    });
    clipboard.on("error", (e) => {
	  console.error("copy failed:" + e)
    });

     return {
	   clipboard,
	   profileName,
	   avatarSource,
	   isUser,
	   parsedText,
	 };
   }
 });
</script>

<style>
 .profile-name {
   display: flex;
   margin-left: 10px;
   font-weight: bold;
   align-self: flex-start;
   height: 40px;
   width: 40px;
   align-items: center;
   padding-top: 10px
 }

 .profile {
   display: flex;
   align-items: center;
   padding-top: 10px;
 }

 .avatar {
   width: 40px;
   height: 40px;
   border-radius: 50%;
 }

 .message-container {
 }

 .message-content {
   border-radius: 15px;
   margin-left: 10px;
   font-size: .875rem;
   line-height: 1.625;
 }

 .message-body code {
   font-weight: bold; /* Make inline code text bold */
   font-family: ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace;
 }
 /* Reset styles for code blocks within <pre> to avoid the bold effect */
 .message-body pre code {
   background-color: #00000069;
   font-weight: normal;
   font-family: 12px/normal 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', 'Source Code Pro', 'source-code-pro', monospace;
   /* Reset other styles as needed to match your design for code blocks */
 }

 .marked-code-block {
   background-color: #333;
   color: white;
   padding: 0.5em;
   border-radius: 5px;
   margin: 0.5em 0;
   display: flex;
   flex-direction: column;
 }

 .code-header {
   display: flex;
   justify-content: space-between;
   align-items: center;
   background-color: #333;
   color: white;
   font-size: .75rem;
 }

 .codeblock-copy-button {
   background-color: #333;
   color: white;
   border: none;
   cursor: pointer;
   padding: 0.5em;
   border-radius: 5px;
   display: flex;
   flex-direction: column;
 }
</style>
