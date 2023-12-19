import * as timeFunctions from './timeFunctions.js';

document.querySelector(".logo").onclick = function() {
	window.location.href = "/";
};

import { io } from "https://cdn.socket.io/4.4.1/socket.io.esm.min.js";

const socket = io.connect('http://' + document.domain + '/');

socket.on('connect', function (event) {
	console.log('Connected to the WebSocket server!');
});



// Step 1: Fetch username from /api/get-username
fetch('/api/get-username')
	.then(response => response.json())
	.then(data => {
		const username = data[0]; // Assuming the username is the first item in the array
		if (username) {
			// Step 2: Fetch friendships from /api/friendships based on the username
			fetch('/api/friendships')
				.then(response => response.json())
				.then(friendships => {
					// Filter friendships based on ReceiverUsername
					const filteredFriendships = friendships.filter(friendship => 
						friendship.ReceiverUsername === username && friendship.isAccepted === null
					);

					// Create an array with SenderUsername and FriendshipID
					const friendshipDetailsArray = filteredFriendships.map(friendship => {
						return {
							'SenderUsername': friendship.SenderUsername,
							'FriendshipID': friendship.FriendshipID
						};
					});

					// Update the HTML content based on the fetched data
					updateInvitationsContainer(friendshipDetailsArray);
				})
				.catch(error => console.error('Error fetching friendships:', error));
		} else {
			console.error('Error fetching username:', data.error);
		}
	})
	.catch(error => console.error('Error fetching username:', error));

// Function to update the HTML content of the invitations container
function updateInvitationsContainer(friendshipDetailsArray) {
	// Clear previous content
	const invitationsContainer = document.querySelector('.invitations-list');
	invitationsContainer.innerHTML = '';

	// Check if there are any invitations
	if (friendshipDetailsArray.length === 0) {
		// No invitations
		invitationsContainer.innerHTML = '<p class="no-invitation">No Invitations</p>';
	} else {
		// Display invitations
		friendshipDetailsArray.forEach(friendship => {
			const invitationHTML = `
	<div class="invitation">
	  <p>Invitation from ${friendship.SenderUsername}</p>
	  <button class="accept-button" onclick="acceptInvitation(${friendship.FriendshipID})">Accept</button>
	  <button class="deny-button" onclick="denyInvitation(${friendship.FriendshipID})">Deny</button>
	</div>
      `;
			invitationsContainer.insertAdjacentHTML('beforeend', invitationHTML);
		});
	}
}
function sendMessage() {
	// Get the input element and destination username element
	const inputElement = document.querySelector('.chat-input input');
	const destinationUsernameElement = document.querySelector('.centered-header');

	// Get the content of the input and destination username
	const messageContent = inputElement.value.trim();
	const destinationUsername = destinationUsernameElement.textContent;

	// Check if the message content is not empty
	if (messageContent !== '') {
		// Emit the 'sendMessage' event with the message content and destination username
		const data = {
			to: destinationUsername,
			message: messageContent
		};

		const requestOptions = {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
				// You may need to include additional headers if required by your server
			},
			body: JSON.stringify(data)
		};
		// Use the fetch API to send the message to the server
		fetch('/api/send-message', requestOptions)

		// Clear the input content
		inputElement.value = '';
		fetchAndDisplayFriendConversation(destinationUsername);
	}
}

// Function to fetch the username
async function getUsername() {
	try {
		const response = await fetch('/api/get-username');
		const data = await response.json();

		if (Array.isArray(data) && data.length > 0) {
			return data[0]; // Assuming the username is the first (and only) element in the array
		} else {
			console.error('Error: Username not found in session');
			return null; // Handle the case where the username is not found
		}
	} catch (error) {
		console.error('Error fetching username:', error);
		return null; // Handle any other errors that may occur during the fetch
	}
}

// Function to fetch friendships
async function fetchFriendships() {
	const username = await getUsername();

	const response = await fetch('/api/friendships');
	const data = await response.json();

	const onlineFriendsList = document.querySelector('.online-friends-list');

	// Clear existing friend elements
	onlineFriendsList.innerHTML = '';
	if (data.length === 0)
		onlineFriendsList.innerHTML = '<p class="no-invitation">No Friends</p>';

	data.forEach(friendship => {
		if (friendship.isAccepted && friendship.ReceiverUsername !== username) {
			createFriendElement(friendship.ReceiverUsername, friendship.isOnline, friendship.Last_Active);
		} else if (friendship.isAccepted && friendship.SenderUsername !== username) {
			createFriendElement(friendship.SenderUsername, friendship.isOnline, friendship.Last_Active);
		}
	});
}

// Function to create friend element and append it to the online friends list
function createFriendElement(friendUsername, isOnline, Last_Active) {
	const onlineFriendsList = document.querySelector('.online-friends-list');
	const offlineFriendsList = document.querySelector('.offline-friends-list');

	const friendElement = document.createElement('div');
	friendElement.classList.add('friend');
	friendElement.onclick = () => fetchAndDisplayFriendConversation(friendUsername);

	const friendInfoElement = document.createElement('div');
	friendInfoElement.classList.add('friend-info');

	const usernameElement = document.createElement('span');
	usernameElement.classList.add('username');
	usernameElement.textContent = friendUsername;

	friendInfoElement.appendChild(usernameElement);

	const statusElement = document.createElement('div');
	statusElement.classList.add('status');

	const statusCircleElement = document.createElement('div');
	statusCircleElement.classList.add('status-circle');

	const statusTextElement = document.createElement('span');
	if (isOnline)
	{
		statusTextElement.textContent = 'Online';
	}
	else
	{
		const timeDifference = timeFunctions.calculateTimeDifference(Last_Active);
		if (timeDifference.days > 1)
			statusTextElement.textContent = 'Last Active ' + timeDifference.targetDay + ' ' + timeDifference.targetMonth;
		else if (timeDifference.hours > 24 && timeDifference.hours < 48)
			statusTextElement.textContent = 'Last Active Yesterday';
		else if (timeDifference.hours < 24 && timeDifference.hours > 1)
			statusTextElement.textContent = 'Active ' + timeDifference.hours + 'h ago';
		else if (timeDifference.minutes < 60 && timeDifference.minutes > 1)
			statusTextElement.textContent = 'Active ' + timeDifference.minutes + ' min ago';
		else if (timeDifference.seconds < 60 && timeDifference.seconds > 1)
			statusTextElement.textContent = 'Active ' + timeDifference.seconds + ' seconds ago';
	}

	statusElement.appendChild(statusCircleElement);
	statusElement.appendChild(statusTextElement);

	friendElement.appendChild(friendInfoElement);
	friendElement.appendChild(statusElement);
	if (isOnline)
	{
		onlineFriendsList.appendChild(friendElement);
	}
	else
	{
		offlineFriendsList.appendChild(friendElement);
	}
}

function limitString(inputString, maxLength) {
	if (inputString.length > maxLength) {
		return inputString.substring(0, maxLength) + '...';
	} else {
		return inputString;
	}
}

const mainContent = document.getElementById('mainContent');
//const conversationsContainer = document.getElementById('conversationsContainer');

async function fetchAndDisplayFriendConversation(friendUsername) {
	try {
		const response = await fetch('/api/conversations');
		const data = await response.json();
		const secondResponse = await fetch('/api/friendships');
		const friendshipData = await secondResponse.json();
		const friendship = friendshipData.find(friendship => {
			return (
				(friendship.SenderUsername === friendUsername || friendship.ReceiverUsername === friendUsername) &&
				friendship.isAccepted
			);
		});
		const conversationsHeader = document.createElement('div');
		conversationsHeader.classList.add('containers-header');

		const backButton = document.createElement('button');
		backButton.id = 'backToConversations';
		backButton.textContent = '<- Conversations';
		backButton.onclick = fetchAndDisplayConversations;

		const centeredHeaderConversations = document.createElement('span');
		centeredHeaderConversations.classList.add('centered-header');
		centeredHeaderConversations.textContent = friendUsername;

		const statusDiv = document.createElement('div');
		statusDiv.classList.add('status-div-online');
		const accountStatus = document.createElement('div');
		accountStatus.id = 'chathead-accountStatus';
		accountStatus.classList.add('chathead-account-status');

		const statusText = document.createElement('span');
		statusText.classList.add('chathead-status-text');

		if (friendship && friendship.isOnline) {
			// Friend is online
			statusText.textContent = 'Online';
		} else {
			// Friend is not online, calculate last active time
			const timeDifference = timeFunctions.calculateTimeDifference(friendship.Last_Active);

			if (timeDifference.days > 1) {
				statusText.textContent = 'Last Active ' + timeDifference.targetDay + ' ' + timeDifference.targetMonth;
			} else if (timeDifference.hours > 24 && timeDifference.hours < 48) {
				statusText.textContent = 'Last Active Yesterday';
			} else if (timeDifference.hours < 24 && timeDifference.hours > 1) {
				statusText.textContent = 'Active ' + timeDifference.hours + 'h ago';
			} else if (timeDifference.minutes < 60 && timeDifference.minutes > 1) {
				statusText.textContent = 'Active ' + timeDifference.minutes + ' min ago';
			} else if (timeDifference.seconds < 60 && timeDifference.seconds > 1) {
				statusText.textContent = 'Active ' + timeDifference.seconds + ' seconds ago';
			}

			statusDiv.classList.remove('status-div-online');
			statusDiv.classList.add('status-div-offline');
		}

		statusDiv.appendChild(accountStatus);
		statusDiv.appendChild(statusText);

		conversationsHeader.appendChild(backButton);
		conversationsHeader.appendChild(centeredHeaderConversations);
		conversationsHeader.appendChild(statusDiv);

		mainContent.innerHTML = '';

		const chatContainer = document.createElement('div');
		chatContainer.classList.add('chat-container');
		chatContainer.id = 'chatContainer';

		const chatMessages = document.createElement('div');
		chatMessages.classList.add('chat-messages');
		chatMessages.scrollTop = chatMessages.scrollHeight;
		const chatInput = document.createElement('div');
		chatInput.classList.add('chat-input');
		const inputElement = document.createElement('input')
		inputElement.type = "text";
		inputElement.placeholder = 'Type a message...';
		const sendButton = document.createElement('button');
		sendButton.textContent = 'Send';
		sendButton.onclick = sendMessage;
		chatInput.appendChild(inputElement);
		chatInput.appendChild(sendButton);
		chatContainer.appendChild(conversationsHeader)
		chatContainer.appendChild(chatMessages);
		chatContainer.appendChild(chatInput);
		mainContent.appendChild(chatContainer);
		for (let i = 0; i < data.conversations.length; i++)
		{
			if (data.conversations[i].other_username === friendUsername)
			{
				const selectedConversation = data.conversations[i];
				const messagesArray = selectedConversation.messages;
				const filteredMessages = messagesArray.filter(message => message.type === 'received' && !message.isRead);
				const messageIDs = filteredMessages.map(message => message.messageID);
				fetch('/api/read-message', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({ messageIDs }),
				});
				selectedConversation.messages.forEach(message => {
					const messageDiv = document.createElement('div');
					messageDiv.classList.add('message', message.type);

					const contentSpan = document.createElement('span');
					contentSpan.textContent = message.message;

					const timestampSpan = document.createElement('span');
					const messageTime = document.createElement('div');
					messageTime.classList.add('message-time');
					timestampSpan.textContent = message.timestamp;

					messageTime.appendChild(timestampSpan);
					messageDiv.appendChild(contentSpan);
					messageDiv.appendChild(messageTime);

					chatMessages.appendChild(messageDiv);
				});
				break;
			}
		}
		const chatMessagesContainer = document.querySelector('.chat-messages');

		// Scroll to the bottom of the chat-messages container
		chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
	} catch (error) {
		console.error('Error fetching messages:', error);
	}
}


async function fetchForRefreshChat(friendUsername) {
	try {
		const chatMessagesContainer = document.querySelector('.chat-messages');
		const response = await fetch('/api/conversations');
		const data = await response.json();

		// Scroll to the bottom of the chat-messages container
		chatMessagesContainer.innerHTML = '';
		for (let i = 0; i < data.conversations.length; i++)
		{
			if (data.conversations[i].other_username === friendUsername)
			{
				const selectedConversation = data.conversations[i];
				const messagesArray = selectedConversation.messages;
				const filteredMessages = messagesArray.filter(message => message.type === 'received' && !message.isRead);
				const messageIDs = filteredMessages.map(message => message.messageID);
				fetch('/api/read-message', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({ messageIDs }),
				});
				selectedConversation.messages.forEach(message => {
					const messageDiv = document.createElement('div');
					messageDiv.classList.add('message', message.type);

					const contentSpan = document.createElement('span');
					contentSpan.textContent = message.message;

					const timestampSpan = document.createElement('span');
					const messageTime = document.createElement('div');
					messageTime.classList.add('message-time');
					timestampSpan.textContent = message.timestamp;

					messageTime.appendChild(timestampSpan);
					messageDiv.appendChild(contentSpan);
					messageDiv.appendChild(messageTime);

					chatMessagesContainer.appendChild(messageDiv);
				});
				break;
			}
		}
		chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
	} catch(error) {
		console.log('Error fetching messages: ', error)
	}
}

async function fetchAndDisplayMessages(conversationIndex) {
	try {
		const response = await fetch('/api/conversations');
		const data = await response.json();
		const secondResponse = await fetch('/api/friendships');
		const friendshipData = await secondResponse.json();
		const selectedConversation = data.conversations[conversationIndex];
		const friendUsername = selectedConversation.other_username;
		const messagesArray = selectedConversation.messages;
		const filteredMessages = messagesArray.filter(message => message.type === 'received' && !message.isRead);
		const messageIDs = filteredMessages.map(message => message.messageID);
		const friendship = friendshipData.find(friendship => {
			return (
				(friendship.SenderUsername === friendUsername || friendship.ReceiverUsername === friendUsername) &&
				friendship.isAccepted
			);
		});

		fetch('/api/read-message', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ messageIDs }),
		});
		const conversationsHeader = document.createElement('div');
		conversationsHeader.classList.add('containers-header');

		const backButton = document.createElement('button');
		backButton.id = 'backToConversations';
		backButton.textContent = '<- Conversations';
		backButton.onclick = fetchAndDisplayConversations;

		const centeredHeaderConversations = document.createElement('span');
		centeredHeaderConversations.classList.add('centered-header');
		centeredHeaderConversations.textContent = 'Real-Time Chat';

		const statusDiv = document.createElement('div');
		statusDiv.classList.add('status-div-online');
		const accountStatus = document.createElement('div');
		accountStatus.id = 'chathead-accountStatus';
		accountStatus.classList.add('chathead-account-status');

		const statusText = document.createElement('span');
		statusText.classList.add('chathead-status-text');

		if (friendship && friendship.isOnline) {
			// Friend is online
			statusText.textContent = 'Online';
		} else {
			// Friend is not online, calculate last active time
			const timeDifference = timeFunctions.calculateTimeDifference(friendship.Last_Active);

			if (timeDifference.days > 1) {
				statusText.textContent = 'Last Active ' + timeDifference.targetDay + ' ' + timeDifference.targetMonth;
			} else if (timeDifference.hours > 24 && timeDifference.hours < 48) {
				statusText.textContent = 'Last Active Yesterday';
			} else if (timeDifference.hours < 24 && timeDifference.hours > 1) {
				statusText.textContent = 'Active ' + timeDifference.hours + 'h ago';
			} else if (timeDifference.minutes < 60 && timeDifference.minutes > 1) {
				statusText.textContent = 'Active ' + timeDifference.minutes + ' min ago';
			} else if (timeDifference.seconds < 60 && timeDifference.seconds > 1) {
				statusText.textContent = 'Active ' + timeDifference.seconds + ' seconds ago';
			}

			statusDiv.classList.remove('status-div-online');
			statusDiv.classList.add('status-div-offline');
		}

		statusDiv.appendChild(accountStatus);
		statusDiv.appendChild(statusText);

		conversationsHeader.appendChild(backButton);
		conversationsHeader.appendChild(centeredHeaderConversations);
		conversationsHeader.appendChild(statusDiv);

		mainContent.innerHTML = '';


		const chatContainer = document.createElement('div');
		chatContainer.classList.add('chat-container');
		chatContainer.id = 'chatContainer';

		const chatMessages = document.createElement('div');
		chatMessages.classList.add('chat-messages');
		const chatInput = document.createElement('div');
		chatInput.classList.add('chat-input');
		const inputElement = document.createElement('input')
		inputElement.type = "text";
		inputElement.placeholder = 'Type a message...';
		const sendButton = document.createElement('button');
		sendButton.textContent = 'Send';
		sendButton.onclick = sendMessage;
		chatInput.appendChild(inputElement);
		chatInput.appendChild(sendButton);
		chatContainer.appendChild(conversationsHeader)
		chatContainer.appendChild(chatMessages);
		chatContainer.appendChild(chatInput);
		mainContent.appendChild(chatContainer);
		const chatHeader = document.querySelector('.containers-header .centered-header');
		chatHeader.textContent = selectedConversation.other_username;

		selectedConversation.messages.forEach(message => {
			const messageDiv = document.createElement('div');
			messageDiv.classList.add('message', message.type);

			const contentSpan = document.createElement('span');
			contentSpan.textContent = message.message;


			const timestampSpan = document.createElement('span');
			const messageTime = document.createElement('div');
			messageTime.classList.add('message-time');
			timestampSpan.textContent = message.timestamp;

			messageTime.appendChild(timestampSpan);
			messageDiv.appendChild(contentSpan);
			messageDiv.appendChild(messageTime);

			chatMessages.appendChild(messageDiv);
		});
		const chatMessagesContainer = document.querySelector('.chat-messages');

		// Scroll to the bottom of the chat-messages container
		chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
	} catch (error) {
		console.error('Error fetching messages:', error);
	}
}

async function fetchAndDisplayConversations() {
	try {
		const response = await fetch('/api/conversations');
		const data = await response.json();

		mainContent.innerHTML = '';
		const conversationsContainer = document.createElement('div');
		conversationsContainer.classList.add('conversations-container');
		const conversationsHeader = document.createElement('div');
		conversationsHeader.classList.add('containers-header');

		const centeredHeaderConversations = document.createElement('span');
		centeredHeaderConversations.classList.add('centered-header');
		centeredHeaderConversations.textContent = 'Conversations';

		conversationsHeader.appendChild(centeredHeaderConversations);
		conversationsContainer.appendChild(conversationsHeader);
		mainContent.appendChild(conversationsContainer);

		if (!data.conversations || data.conversations.length === 0) {
			const conversationContainer = document.createElement('div');
			conversationContainer.innerHTML = '<p class="no-invitation">No Conversations</p>';
			conversationsContainer.appendChild(conversationContainer);
		} else {
			const conversationList = document.createElement('div');

			for (let i = 0; i < data.conversations.length; i++) {
				let conversation = data.conversations[i];
				const conversationContainer = document.createElement('div');
				conversationContainer.classList.add('conversation-container');
				conversationContainer.onclick = () => fetchAndDisplayMessages(i);

				const userDetails = document.createElement('div');
				userDetails.classList.add('conv-user-details');

				const username = document.createElement('div');
				username.classList.add('conv-username');
				username.textContent = conversation.other_username;

				const messageCount = document.createElement('div');
				const receivedUnreadMessagesCount = conversation.messages.filter(message => message.type === 'received' && !message.isRead).length;
				messageCount.classList.add('conv-message-count');
				messageCount.textContent = receivedUnreadMessagesCount;

				userDetails.appendChild(username);
				if (receivedUnreadMessagesCount !== 0)
					userDetails.appendChild(messageCount);

				const messageDetails = document.createElement('div');
				messageDetails.classList.add('conv-message-details');

				const message = document.createElement('div');
				message.classList.add('conv-message');
				const maxLength = 20;
				const lastMessageInfo = conversation.messages[conversation.messages.length - 1];
				const limitedString = limitString(lastMessageInfo.message, maxLength);
				if (lastMessageInfo.type === 'sent')
					message.textContent = 'You: ' + limitedString;
				else
					message.textContent = conversation.other_username + ': ' + limitedString;

				const lastMessageTimestamp = new Date(lastMessageInfo.timestamp);
				const now = new Date();
				const timestamp = document.createElement('div');
				timestamp.classList.add('conv-timestamp');

				if (timeFunctions.isSameDay(lastMessageTimestamp, now)) {
					// If the message is from the same day, display only the hour and minute
					const formattedTime = timeFunctions.formatTime(lastMessageTimestamp);
					timestamp.textContent = formattedTime;
				} else if (timeFunctions.isYesterday(lastMessageTimestamp, now)) {
					// If the message is from yesterday, display "Yesterday"
					timestamp.textContent = 'Yesterday';
				} else {
					// Otherwise, display the date
					timestamp.textContent = timeFunctions.formatDate(lastMessageTimestamp);
				}

				messageDetails.appendChild(message);
				messageDetails.appendChild(timestamp);

				conversationContainer.appendChild(userDetails);
				conversationContainer.appendChild(messageDetails);

				conversationList.appendChild(conversationContainer);
			}

			conversationsContainer.appendChild(conversationList);
		}
	} catch (error) {
		console.error('Error fetching conversations:', error);
	}
}

// Example functions for accepting and denying invitations (replace with actual logic)

function getMessages() {

	const conversations = document.querySelector('.conversations-container');
	const chat = document.querySelector('.chat-container');

	if (conversations !== null) {
		fetchAndDisplayConversations();
	} else if (chat !== null) {
		const friendUsername = document.querySelector('.containers-header .centered-header');
		fetchForRefreshChat(friendUsername.textContent);
	}
}

function listenForMessages() {
	// Make a fetch request to '/api/refresh-chat'
	fetch('/api/refresh-chat')
		.then(response => {
			if (response.ok) {
				return response.json();
			} else {
				throw new Error('Failed to refresh chat');
			}
		})
		.then(data => {
			if (data.refresh) {
				getMessages();
			}
		})
		.catch(error => {
			console.error('Error refreshing chat:', error);
		});
}


fetchAndDisplayConversations();

fetchFriendships();
// Call the function to start listening
listenForMessages();

// Set up a repeating interval (e.g., every 1 second)
setInterval(listenForMessages, 1000);

