console.log("worked");

// const msgReceiver = document.getElementById('msg-receiver').textContent.trim().toLowerCase();
const submitBtn = document.getElementById('submit-btn');
// const user = document.getElementById('user').textContent;
const dataInput = document.getElementById('data-input');
const reciepient = document.getElementById('recipient').textContent.trim().toLowerCase();

const socket = new WebSocket(`ws://${window.location.host}/ws/message/inbox/${recipient}`);
console.log(socket);

socket.onmessage = function (e) {
    console.log('Server ' + e.data);
    const { sender, message } = JSON.parse(e.data);
    console.log(message);
    console.log(sender);
}

submitBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const dataValue = dataInput.value;
    // console.log("Logged in user: ", user);
    console.log("message: ", dataValue);
    console.log("Receiver: ", reciepient);

    socket.send(JSON.stringify({
        // 'user': user,
        'message': dataValue,
        'reciepient': reciepient
    }))
});

// socket.onopen = function (e) {
//     socket.send(JSON.stringify({
//         'message': 'Hello from client',
//         'sender': 'test sender',
//         'reciepient_id': reciepient_id
//     }));
// };
