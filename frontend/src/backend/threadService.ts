// threadService.ts
import apiClient from "./apiClient";

const threadService = {
  async renameThread(threadId: string, name: string) {
	const response = await apiClient.put(
	  '/threads/' + threadId + '/name', name
	);
	return response.data;
  },
  async deleteThread(threadId: string) {
	const response = await apiClient.delete('/threads/' + threadId);
	return response.data;
  },
  async createThread() {
    const response = await apiClient.post('/threads');
    return response.data;
  },
  async getThreads() {
    const response = await apiClient.get('/threads');
    return response.data;
  },
  async getThreadMessages(threadId: string) {
		const response = await apiClient.get('/threads/messages/' + threadId);
		return response.data;
  },
  async addMessageToThread(threadId: int, messages: Array) {
    const response = await apiClient.post('/threads/messages/' + threadId, messages);
    return response.data;
  },
};

export default threadService;
