<template>
  <a-layout-sider width="250" class="sidebar">
	<div v-if="!collapsed">
    <div class="profile">
      <img
        src="../assets/baozi.png"
        alt="Profile Image"
        class="profile-image"
      />
    </div>
    <a-button
      type="primary"
      block
      class="new-chat"
      @click="navigateToNewChat"
    >
      New Chat
    </a-button>
	<a-menu mode="inline" defaultOpenKeys="['sub1']" class="chat-menu" style="border: none">
      <a-sub-menu key="sub1">
		<template #title>
          Chats ({{ chatThreads.length }})
		</template>
		<div class="scrollable-menu">
		  <a-dropdown-button
			v-for="(thread, index) in chatThreads"
			:key="thread.id"
			class="menu-title-content"
		  >
			<div class="menu-item-content" @click="navigateToThread(thread.id)" v-if="!thread.editing || editingIndex !== index">
			  {{ thread.name || 'new chat' }}
			</div>
			<a-input v-else v-model:value="newName" @blur="endEditing" @keypress.enter="endEditing" />
			<template #icon><MoreOutlined /></template>
			<template #overlay>
				<a-menu>
				  <a-menu-item key="rename" @click="startEditing(index)">Rename</a-menu-item>
				  <a-menu-item key="delete" @click="deleteThread(thread.id)">Delete</a-menu-item>
				</a-menu>
			</template>
		  </a-dropdown-button>
		</div>
      </a-sub-menu>
	</a-menu>
	<div class="user-profile" @click="toggleUserMenu">
      <a-avatar :src="user.avatar" class="user-avatar" v-if="user" />
      <span class="user-name" v-if="user">{{ user.nickname }}</span>
	</div>
	<a-menu
      v-if="userMenuVisible"
      class="user-menu"
      selectable="false"
	>
      <a-menu-item @click="logOut">
	  <LogoutOutlined />
      Log out
      </a-menu-item>
	</a-menu>
	</div>
  </a-layout-sider>
</template>
<script lang="ts">
 import { defineComponent, ref, onMounted } from "vue";
 import { router } from "@/router"; // Import your Vue router instance
 import { useStore } from 'vuex';
 import { getUserOrRedirect } from '@/composables/user';
 import { message as antMessage, Dropdown } from 'ant-design-vue';
 import { MoreOutlined, SettingOutlined, LogoutOutlined, CheckSquareOutlined, DownOutlined } from '@ant-design/icons-vue';

 import threadService from "@/backend/threadService";

 export default defineComponent({
   components: {
	 MoreOutlined,
     SettingOutlined,
	 LogoutOutlined,
	 CheckSquareOutlined,
	 DownOutlined,
	 'a-dropdown-button': Dropdown.Button,
  },
   setup() {
	 let collapsed = ref(false);
	 const store = useStore();
	 const user = getUserOrRedirect();
	 let newName = ref(""); // Track the new name being edited
     let editingIndex = ref(null); // Track the index of the currently edited thread
	 let chatThreads = ref([]);
	 let userMenuVisible = ref(false);
	 const isChatsCollapsed = ref(false);
	 const startEditing = (index) => {
       editingIndex.value = index; // Set the index of the thread being edited
       newName.value = chatThreads.value[index].name || "";
       chatThreads.value[index].editing = true;
     };

     const endEditing = () => {
      const threadId = chatThreads.value[editingIndex.value].id;
      renameThread(threadId, newName.value);
      chatThreads.value[editingIndex.value].editing = false;
      editingIndex.value = null; // Reset editing index after editing is complete
     };

     const renameThread = (threadId, new_name) => {
	  threadService.renameThread(threadId, new_name).then(() => {
		antMessage.success('Thread renamed');
		loadThreads();
	  });
     };
	 const logOut = () => {
       store.dispatch('auth/logout').then(() => {
         antMessage.success('logout succeeded');
       });
	  router.push('/');
     };
     const navigateToSettings = () => {};
	 const navigateToNewChat = () => {
	   router.push({ path: "/entry" });
	 };
	 const toggleUserMenu = () => {
	   userMenuVisible.value = !userMenuVisible.value;
	 };
	 const loadThreads = async () => {
	   chatThreads.value = [];
	   try {
		 const response = await threadService.getThreads();
		 if (response.data.length > 0) {
		   chatThreads.value.push(...response.data);
		   chatThreads.value.forEach((thread) => {
			 if (thread.name == "") {
			   thread.name = thread.last_message;
			 }
		   });
		 }
		 else{
		   chatThreads.value.push(...[{ id: 1, name: "Welcome to chat with Baozi!" }]);
		 }
	   }
	   catch (error) {
		 console.error(error);
	   }
	 };
	 onMounted(async () => {
	   await loadThreads();
	 });

    // Function to handle chat thread click
     const navigateToThread = (threadId) => {
      router.push({ path: "/chat", query: { id: threadId } });
    };

     const deleteThread = (threadId) => {
	   threadService.deleteThread(threadId).then(() => {
		 antMessage.success('Thread deleted');
	   	 loadThreads();
	   })
     };

     return {
	   user,
	   chatThreads,
	   userMenuVisible,
	   toggleUserMenu,
	   navigateToSettings,
	   navigateToNewChat,
       isChatsCollapsed,
       navigateToThread,
	   logOut,
	   deleteThread,
	   newName,
       editingIndex,
       startEditing,
       endEditing,
	   collapsed,
    };
  },
});
</script>
<style>
 .menu-title-content .ant-btn {
   background-color: #f5f5f5;
   margin-bottom: 20px;
   border: none;
   box-shadow: none;
 }

.scrollable-menu {
  max-height: 450px; /* Adjust this value to fit your design */
  overflow-y: auto; /* Enable vertical scrolling */
  background-color: #f5f5f5; /* Light grey background */
}

/* sidebar */
.sidebar {
  position: relative;
  width: 250px; /* Sidebar width */
  background-color: #f5f5f5; /* Light grey background */
  padding: 20px;
}

.profile {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding-top: 20px;
}

.profile-image {
  width: 50px; /* Profile image size */
  height: 50px;
  border-radius: 50%; /* Circular image */
  margin-bottom: 10px;
}

 .chat-menu {
   overflow: hidden;  /* Ensures the child elements adhere to the menu's border radius */
   background-color: #f5f5f5; /* Light grey background */
}

.submenu-arrow {
  float: right;
  transition: transform 0.3s;
}

/* Rotate arrow when submenu is collapsed */
.a-menu-item-group-collapsed .submenu-arrow {
  transform: rotate(-90deg);
}

/* Style the menu item to look like the screenshot */
.menu-item-content {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 180px;
}

/* Adjust the appearance when the item is selected/active */
.a-menu-item-selected::before {
  border-color: #1890ff; /* Highlight color when selected */
  background-color: #e6f7ff; /* Background color for the square */
}

/* Styles for the new chat button */
.new-chat {
   margin-top: 16px;
   margin-bottom: 24px;
   display: block;
   border: 1px solid #ccc; /* Border color similar to the screenshot */
}

.new-chat:hover {
  background-color: #e9e9e9; /* Slightly darker background on hover */
}

/* Styles for chat threads */
.menu-title {
  cursor: pointer;
  /* other styles... */
}

.profile-menu {
  display: flex;
  align-items: center;
  width: 60%;
}

.arrow {
  display: inline-block;
  transition: transform 0.3s ease;
}

.arrow-collapsed {
  transform: rotate(-90deg);
}

.chat-name {
  font-weight: bold; /* Bold font for chat names */
}

/* Styles for user menu */
/* User menu styles */
/* User profile styles */
.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
  position: absolute;
  bottom: 0;
  left: 10px;
  width: 100%;
  padding: 10px;
  box-sizing: border-box; /* Include padding in the width */
}

.user-avatar {
  width: 40px; /* Adjust to match the image */
  height: 40px; /* Adjust to match the image */
  border-radius: 50%;
  margin-right: 10px; /* Space between avatar and name */
}

.user-name {
  flex-grow: 1; /* Ensure the name takes up remaining space */
}

/* User menu styles */
.user-menu {
  position: absolute;
  bottom: 55px; /* Height of the user profile */
  width: 60%;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.user-actions {
  list-style: none;
  margin: 0;
  padding: 0;
}

.user-actions li {
  padding: 10px 20px;
  display: flex;
  align-items: center;
}

.user-actions li:not(:last-child) {
  border-bottom: 1px solid #eee;
}

.settings-icon,
.logout-icon {
  /* Icons are represented by classes for custom icons */
  margin-right: 10px;
}

/* Hover effect for menu items */
.user-actions li:hover {
  background-color: #f5f5f5;
}

/* Icons (if you are using fonts like FontAwesome) */
.settings-icon:before {
  content: "\f013"; /* FontAwesome icon unicode */
}

.logout-icon:before {
  content: "\f08b"; /* FontAwesome icon unicode */
}
</style>
