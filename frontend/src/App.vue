// Purpose: Main component for the application
<link
  rel="stylesheet"
  href="https://unpkg.com/highlightjs-copy/dist/highlightjs-copy.min.css"
/>
<template>
  <div class="app-container">
    <router-view></router-view>
  </div>
</template>

<script lang="ts">
import WelcomePage from './components/WelcomePage.vue';
export default {
   name: 'Chatchat',
   components: {
     WelcomePage,
   }
 }
</script>
