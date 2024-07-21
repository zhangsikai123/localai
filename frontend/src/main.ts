// main.ts
import { createApp } from 'vue';
import App from './App.vue';
import { router } from './router'; // Import the router
import store from './store';
import './assets/style.css'; // Import the global stylesheet
import Antd from 'ant-design-vue';
import { Layout } from 'ant-design-vue';
const app = createApp(App);

app.component('a-header', Layout.header);
app.use(Antd);
app.use(router);
app.use(store)
app.mount('#app');
