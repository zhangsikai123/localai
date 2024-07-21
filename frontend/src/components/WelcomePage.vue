<template>
  <a-layout>
    <a-header class="welcome-header">
	  <a-button type="link" @click="showLoginModal" v-if="!loggedin">LOG IN</a-button>
	  <a-button type="link" @click="logout">LOG OUT</a-button>
	  <a-button type="link" @click="showSignupModal" v-if="!loggedin">SIGN UP</a-button>
    </a-header>
	<a-modal
	  title="Signup"
	  :open="signupModalVisible"
	  @cancel="handleCancel"
	  footer=""
	  class="signup-modal"
    >
	  <div class="signup-content">
          <p>Sign Up to chat with Baozi.</p>
          <a-form @submit.prevent="handleSignup">
			<a-form-item>
              <a-input v-model:value="signupForm.email" placeholder="Email address" />
			</a-form-item>
			<a-form-item>
              <a-input-password v-model:value="signupForm.password" placeholder="Password" />
			</a-form-item>
          <a-form-item>
            <a-button
			  type="primary"
			  html-type="submit"
			  block
			  :loading="signupLoading"
			>Continue</a-button>
          </a-form-item>
          </a-form>
          <p>Already have an account? <a @click="showLoginModal">Log in</a></p>
		</div>
    </a-modal>
	<a-modal
	  title="Log In"
	  :open="loginModalVisible"
	  @cancel="handleLoginCancel"
	  footer=""
	  class="login-modal"
	>
	  <div class="login-content">
		<p>Log in to continue to Baozi.</p>
		<a-form @submit.prevent="handleLogin">
		  <a-form-item>
			<a-input v-model:value="loginForm.email" placeholder="Email address" />
		  </a-form-item>
		  <a-form-item>
			<a-input-password v-model:value="loginForm.password" placeholder="Password" />
		  </a-form-item>
		  <a-form-item>
			<a-button
			  type="primary"
				html-type="submit"
					block
			  :loading="loginLoading">Continue</a-button>
		  </a-form-item>
		</a-form>
		<p>Don't have an account? <a @click="showSignupModal">Sign up</a></p>
	  </div>
	</a-modal>
    <a-layout-content>
      <section class="hero">
        <h1>Baozi</h1>
        <p>Your personal chatbot</p>
        <div class="cta-buttons">
          <a-button type="primary" @click="startChat" style="margin: 0 10px">Start a chat</a-button>
        </div>
      </section>
    </a-layout-content>
    </a-layout>
</template>

<script lang="ts">
 import { defineComponent, ref, computed } from 'vue';
 import { useRouter } from 'vue-router';
 import { useStore } from 'vuex';
 import { Layout, Modal, Form, Input, Button, Menu, message as antMessage } from 'ant-design-vue';
 import { hasLoggedin } from "@/composables/user";
 import userService from "@/backend/userService";

 export default defineComponent({
   components:{
	 'a-header': Layout.Header,
   },
   setup() {
	 const loginForm = ref({
       email: '',
       password: '',
     });
	 const signupForm = ref({
       email: '',
       password: '',
     });
     const store = useStore();
     const router = useRouter();
	 const signupModalVisible = ref(false);
	 const loginModalVisible = ref(false);
	 const signupLoading = ref(false);
	 const loginLoading = ref(false);
	 const loggedin = computed(()=>hasLoggedin());
     const showLoginModal = () => {
       loginModalVisible.value = true;
	   signupModalVisible.value = false;
     };

     const handleLoginCancel = () => {
      loginModalVisible.value = false;
     };


	 const showSignupModal = () => {
       signupModalVisible.value = true;
	   loginModalVisible.value = false;
     };

     const handleCancel = () => {
       signupModalVisible.value = false;
     };

     const handleSignup = async () => {
	   signupLoading.value = true; // Start loading
	   try {
		 await userService.signup(
		   signupForm.value.email,
		   signupForm.value.password
		 )
		 signupLoading.value = false; // Stop loading
		 antMessage.success('signup succeeded, wait for the activation email and activate your account');
		 showLoginModal();

	   } catch (error) {
		 alert(error);
		 signupLoading.value = false; // Stop loading
	   }
     };

     const handleGoogleLogin = () => {
       // Implement Google login logic here
    };

     const handleAppleLogin = () => {
       // Implement Apple login logic here
     };

     const logout = () => {
       store.dispatch('auth/logout').then(() => {
         antMessage.success('logout succeeded');
      });
     };

     const download = (platform) => {
       // Logic to handle download based on platform (iOS or Android)
     };

     const startChat = () => {
      if (store.getters['auth/isAuthenticated']) {
        router.push('/entry');
      } else {
        // show login modal
		antMessage.info('Please login to start a chat');
		showLoginModal();
      }
     };
	 const handleLogin = async() => {
       loginLoading.value = true; // Start loading
	   try {
         await store.dispatch('auth/login', {
		   username: loginForm.value.email,
		   password: loginForm.value.password });
         antMessage.success('login succeeded');
		 loginLoading.value = false; // Stop loading
		 startChat();
       } catch (error) {
         alert(error);
		 loginLoading.value = false; // Stop loading
       }
     };

     return {
       logout,
	   loggedin,
       startChat,
       download,
	   signupLoading,
	   signupModalVisible,
       signupForm,
       showSignupModal,
       handleCancel,
       handleSignup,
       handleGoogleLogin,
       handleAppleLogin,
	   loginModalVisible,
       loginForm,
	   loginLoading,
       showLoginModal,
       handleLoginCancel,
       handleLogin,
     };
   },
 });
</script>
<style scoped>
/* General styles */
 .welcome-header {
	background-color: #ffffff;
	padding: 0 20px;
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
	z-index: 1;
 }

/* Hero section styles */
.hero {
  text-align: center;
  padding: 50px 20px;
}

.hero h1 {
  font-size: 2.5em;
  margin-bottom: 0.5em;
}

.hero p {
  font-size: 1.2em;
  color: #555555;
}

/* Call-to-action buttons */
.cta-buttons {
  margin-top: 30px;
  display: flex;
  justify-content: center;
 }

 .signup-modal .signup-content {
  text-align: center;
}

.social-login {
  margin-top: 16px;
}

.social-login .google-login {
  margin-bottom: 8px;
  background-color: #fff;
  color: rgba(0, 0, 0, 0.65);
  border-color: rgba(0, 0, 0, 0.15);
}

.social-login .apple-login {
  background-color: #000;
  color: #fff;
}
</style>
