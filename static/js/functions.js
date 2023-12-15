function acceptInvitation(friendshipID) {
	window.location.href = `/api/accept-friend?query=${friendshipID}`;
}

function denyInvitation(friendshipID) {
	window.location.href = `/api/cancel-friend?query=${friendshipID}`;
}
