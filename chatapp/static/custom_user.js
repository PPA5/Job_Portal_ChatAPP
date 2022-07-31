console.log("Sanity check from room.js.");

const userName = JSON.parse(document.getElementById('userName').textContent);
const userID = JSON.parse(document.getElementById('userID').textContent);

let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let timestamp = document.querySelector("#timestamp");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");

// add input event of typing ...
document.getElementById("chatMessageInput").oninput = function () { myFunction() };

function myFunction() {
    chatSocket.send(JSON.stringify({
        "type": 'oninput',
        "message": 'Typing',
    }));
}

// add a new paragraph element into div
function chatmessage(value, al_value, ts, edited, deleted) {
    const para = document.createElement("p");
    para.setAttribute('id', ts);

    const msg_span = document.createElement("span");
    msg_span.setAttribute('id', 'msg_' + ts);
    msg_span.classList.add('msg');

    const edit_span = document.createElement("span");
    edit_span.setAttribute('id', 'edit_' + ts);
    edit_span.classList.add('edit');

    const time_span = document.createElement("span");
    time_span.setAttribute('id', 'time_' + ts);
    time_span.classList.add('time');

    //const t = document.createElement("span");
    //const status = document.createElement("span");

    //edit_span.setAttribute('id', ts + "_" + userName);
    edit_span.textContent = ' edited';
    if (edited != true) {
        edit_span.classList.add('sp_dis');
    }

    var date = new Date(ts);
    var AmOrPm = date.getHours() >= 12 ? 'PM' : 'AM';
    time_span.textContent = "  " + date.getHours() % 12 + ":" + date.getMinutes() + " " + AmOrPm;

    para.classList.add(al_value);
    if (al_value == 'right') {
        para.setAttribute('align', 'right');
    }
    else {
        para.setAttribute('align', 'left');
    }
    const node = document.createTextNode(value);
    msg_span.appendChild(node);

    //para.appendChild(status);
    //para.setAttribute('id', ts);
    if (para.getAttribute('align') == 'right') {
        para.setAttribute("onmouseup", "mouseUp(this.id)");
    }
    const element = document.getElementById("chatmsg");
    //para.appendChild(t);
    if (deleted == true) {
        return
    }
    element.appendChild(para);
    para.appendChild(msg_span);
    para.appendChild(edit_span);
    para.appendChild(time_span);
    element.scrollTop = element.scrollHeight;
}

function mouseUp(p_id) {
    chatMessageInput.value = document.getElementById('msg_' + p_id).textContent;
    timestamp.value = p_id;
}

// adds a new option to 'onlineUsersSelector'
function onlineUsersSelectorAdd(value) {
    if (document.querySelector("option[value='" + value + "']")) return;
    let newOption = document.createElement("option");
    newOption.value = value;
    newOption.innerHTML = value;
    onlineUsersSelector.appendChild(newOption);
}

// removes an option from 'onlineUsersSelector'
function onlineUsersSelectorRemove(value) {
    let oldOption = document.querySelector("option[value='" + value + "']");
    if (oldOption !== null) oldOption.remove();
}

// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function () {
    if (chatMessageInput.value.length === 0) {
        const text = 'Are you sure to delete?';
        if (confirm(text) == true) {
            chatSocket.send(JSON.stringify({
                "type": 'delete_message',
                "message": 'delete',
                "timestamp": timestamp.value,
            }));
        }
    }
    else {
        if (timestamp.value.length === 0) {
            var ts = new Date().getTime();
            chatSocket.send(JSON.stringify({
                "type": 'newmessage',
                "message": chatMessageInput.value,
                "timestamp": ts,
            }));
        }
        else {
            chatSocket.send(JSON.stringify({
                "type": 'updatemessage',
                "message": chatMessageInput.value,
                "timestamp": timestamp.value,
            }));
        }
        chatMessageInput.value = "";
    }
};

let chatSocket = null;

function connect() {
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + userName + "/");

    chatSocket.onopen = function (e) {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = function (e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function () {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(data);

        switch (data.type) {
            case "chat_message":
                chatLog.value += data.user + ": " + data.message + "\n";  // new
                break;
            case "user_list":
                for (let i = 0; i < data.users.length; i++) {
                    onlineUsersSelectorAdd(data.users[i]);
                }
                break;
            case "user_join":
                chatLog.value += data.user + " joined the room.\n";
                onlineUsersSelectorAdd(data.user);
                break;
            case "user_leave":
                chatLog.value += data.user + " left the room.\n";
                onlineUsersSelectorRemove(data.user);
                break;
            case "private_message":
                al_value = 'left'
                chatmessage(data.message, al_value, data.timestamp);
                break;

            case "private_message_delivered":
                al_value = 'right';
                chatmessage(data.message, al_value, data.timestamp);
                break;

            case "update_message":
                let um_e = document.getElementById('edit_' + data.timestamp);
                let um_m = document.getElementById('msg_' + data.timestamp);
                um_m.textContent = data.message;
                um_e.classList.remove('sp_dis');
                break

            case "update_message_delivered":
                let umd_e = document.getElementById('edit_' + data.timestamp);
                let umd_m = document.getElementById('msg_' + data.timestamp);
                umd_m.textContent = data.message;
                umd_e.classList.remove('sp_dis');
                break

            case "delete_message":
                let dm_p = document.getElementById(data.timestamp);
                dm_p.remove();
                break;

            case "delete_message_delivered":
                let dmd_p = document.getElementById(data.timestamp);
                dmd_p.remove();
                break;
            case "history_msg":
                data_message = JSON.parse(data.message);
                for (i = 0; i < data_message.length; i++) {
                    if (data_message[i].fields.user == userID) {
                        al_value = 'left';
                        chatmessage(data_message[i].fields.content, al_value, data_message[i].fields.timestamp, data_message[i].fields.edited);
                    }
                    else {
                        al_value = 'right';
                        chatmessage(data_message[i].fields.content, al_value, data_message[i].fields.timestamp, data_message[i].fields.edited, data_message[i].fields.deleted);
                    }
                }
                break
            case "typing_message":
                document.getElementById("typing").removeAttribute('hidden');
                setTimeout(() => document.getElementById("typing").setAttribute('hidden', 'false'), 5000);
                break
            default:
                console.error("Unknown message type!");
                break;
        }

        // scroll 'chatLog' to the bottom
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onerror = function (err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}
connect();

onlineUsersSelector.onchange = function () {
    window.location.pathname = "chat/" + onlineUsersSelector.value + "/";
    chatMessageInput.focus();
};