// threadService.ts
const chatService = {
  sendChat: async (query: string, history: any) => {
	const data= {
      query: query,
      history: history,
      stream: true,
    };
	const response = await fetch(
	  `${import.meta.env.VITE_BASE_URL}/chat/chat`,
	  {
		method: "POST",
		headers: {
		  "Content-Type": "application/json",
		},
		body: JSON.stringify(data),
	  },
	);
	return response;
  },
};

export default chatService;
