// src/store/index.ts
import { createStore } from 'vuex';
import { authModule } from './auth';
const store = createStore({
  modules: {
    auth: authModule,
  },
});
export default store
