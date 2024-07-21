import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

import ChatWindow from '../components/ChatWindow.vue';
import EntryPage from '../components/EntryPage.vue';
import WelcomePage from '../components/WelcomePage.vue';
import MailActivation from '../components/MailActivation.vue';

import { hasLoggedin } from "@/composables/user";
const routes: Array<RouteRecordRaw> =  [
  {
      path: '/',
      name: 'WelcomePage',
      component: WelcomePage
    },
  {
	  path: '/entry',
	  name: 'EntryPage',
	  component: EntryPage,
	  beforeEnter: (to, from, next) => {
	    if (!hasLoggedin()) next({ name: 'WelcomePage' })
	    else next()
	  }
	},
  {
      path: '/chat',
      name: 'ChatWindow',
	  component: ChatWindow,
	  props: true,
	  beforeEnter: (to, from, next) => {
	    if (!hasLoggedin()) next({ name: 'WelcomePage' })
	    else next()
	  }
  },
  {
	path: '/activation',
	name: 'MailActivation',
	component: MailActivation,
  },
];

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || "/"),
  routes
});
