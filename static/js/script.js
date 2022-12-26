// Geting the chat messags to automatically scroll down when a user opens a
// chat in jQuery

$(document).ready(function () {
    $(".chat-messages").scrollTop($(".chat-messages")[0].scrollHeight);
});

// Geting the chat messags to automatically scroll down when a user opens a
// chat in javascript
// let targetDiv = document.querySelector('.chat-messages');
// targetDiv.scrollTop = targetDiv.scrollHeight;

// console.log("It's working");