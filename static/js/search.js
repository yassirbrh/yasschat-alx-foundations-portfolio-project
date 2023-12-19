let searchQuery = "";
// Example data for search results
async function fetchSearchResults(query) {
	try {
		const response = await fetch(`/api/users?query=${query}`);
		const data = await response.json();
		return data;
	} catch (error) {
		console.error('Error fetching search results:', error);
		return [];
	}
}
async function fetchFriendshipResults() {
	try {
		const response = await fetch(`/api/friendships`);
		const data = await response.json();
		//console.log(data)
		return data;
	} catch (error) {
		console.error('Error fetching search results:', error);
		return [];
	}
}
async function getUsername() {
	try {
		const response = await fetch(`/api/get-username`);
		const data = await response.json();
		//console.log(data)
		return data;
	} catch (error) {
		console.error('Error fetching search results:', error);
		return [];
	}
}
//let myUsername = getUsername();
//console.log(myUsername);
// Function to display search results
function displaySearchResults(results) {
	const resultsContainer = document.getElementById('searchResultsContainer');
	const noResultsMessage = document.getElementById('noResultsMessage');

	// Clear previous results
	resultsContainer.innerHTML = '';

	// Check if there are results
	getUsername().then(myUsername => {
		if (results.includes(myUsername[0])) {
			results.splice(results.indexOf(myUsername[0]), 1);
		}

		if (results.length > 0) {
			// Loop through results and create HTML for each
			results.forEach(result => {
				const resultDiv = document.createElement('div');
				resultDiv.classList.add('result-container');

				// Create user details
				const userDetailsDiv = document.createElement('div');
				userDetailsDiv.classList.add('user-details');
				userDetailsDiv.innerHTML = `<p><strong>Username:</strong> ${result}</p>`;

				// Create action buttons
				const actionButtonsDiv = document.createElement('div');
				actionButtonsDiv.classList.add('action-buttons');

				// Fetch friendships and handle conditions
				fetchFriendshipResults().then(friendships => {
					let invitationSentHTML = '';
					let acceptDenyHTML = '';
					let alreadyFriendsHTML = '';
					let inviteButtonHTML = '';

					for (let i = 0; i < friendships.length; i++) {
						let friendship = friendships[i];

						if (friendship.ReceiverUsername === result && friendship.isAccepted === null) {
							invitationSentHTML = `
				<button class="sent-button">Invitation Sent</button>
				<button class="cancel-button" onclick="cancelFriend(${friendship.FriendshipID})">Cancel Invitation</button>`;
						} else if (friendship.SenderUsername === result && friendship.isAccepted === null) {
							acceptDenyHTML = `
				<button class="accept-button" onclick="acceptInvitation(${friendship.FriendshipID})">&#10003;  Accept</button>
				<button class="deny-button" onclick="cancelFriend(${friendship.FriendshipID})">&#10060;  Deny</button>`;
						} else if (friendship.SenderUsername === result || friendship.ReceiverUsername === result)
						{
							alreadyFriendsHTML = `<button class="friend-button">🤝 Friend</button>`;
						}
					}

					// Set inviteButtonHTML only if none of the conditions are met
					if (!invitationSentHTML && !acceptDenyHTML && !alreadyFriendsHTML) {
						inviteButtonHTML = `<button class="invite-button" onclick="inviteFriend('${result}')">+ Send Invitation</button>`;
					}

					// Concatenate the HTML content for all conditions
					actionButtonsDiv.innerHTML = invitationSentHTML + acceptDenyHTML + alreadyFriendsHTML + inviteButtonHTML;

					// Append user details and action buttons to the result div
					resultDiv.appendChild(userDetailsDiv);
					resultDiv.appendChild(actionButtonsDiv);

					// Append the result div to the results container
					resultsContainer.appendChild(resultDiv);

					// Hide the no results message
					noResultsMessage.style.display = 'none';
				});
			});
		} else {
			// Show the no results message
			noResultsMessage.style.display = 'block';
			noResultsMessage.textContent = `No results for ${searchQuery}`;
		}
	});
}
// Display the search results using the example data
async function simulateSearch() {
	// Simulate user input (replace this with your actual search input)
	const currentUrl = window.location.search;

	// Extract the query parameter value
	const urlParams = new URLSearchParams(currentUrl);
	const searchInput = urlParams.get('query');
	searchQuery = searchInput;
	// Fetch search results using the simulated input
	const results = await fetchSearchResults(searchQuery);

	// Display the search results
	displaySearchResults(results);
}

// Simulate a search when the script runs (you can trigger this based on user input)
simulateSearch();
function inviteFriend(friend) {
	//console.log(friend);
	window.location.href = `/api/invite-friend?friend=${friend}`;
};
function cancelFriend(friendshipID) {
	window.location.href = `/api/cancel-friend?query=${friendshipID}`;
}
function acceptInvitation(friendshipID) {
	window.location.href = `/api/accept-friend?query=${friendshipID}`;
}
