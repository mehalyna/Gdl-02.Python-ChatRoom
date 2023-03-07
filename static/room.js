console.log("Sanity check from room.js.");

const roomId = JSON.parse(document.getElementById("roomId").textContent);

let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");
let currentUser = document.querySelector("#currentUser");

function onlineUsersSelectorAdd(value) {
  if (document.querySelector("option[value='" + value + "']")) return;
  let newOption = document.createElement("option");
  newOption.value = value;
  newOption.innerHTML = value;
  onlineUsersSelector.appendChild(newOption);
}

function onlineUsersSelectorRemove(value) {
  let oldOption = document.querySelector("option[value='" + value + "']");
  if (oldOption !== null) oldOption.remove();
}

chatMessageInput.focus();

chatMessageInput.onkeyup = function (e) {
  if (e.keyCode === 13) {
    chatMessageSend.click();
  }
};

chatMessageSend.onclick = function () {
  if (chatMessageInput.value.length === 0) return;
  chatSocket.send(
    JSON.stringify({
      message: chatMessageInput.value,
    }),
  );
  chatMessageInput.value = "";
};

let chatSocket = null;

function connect() {
  chatSocket = new WebSocket(
    "ws://" + window.location.host + "/ws/chat/" + roomId + "/",
  );

  chatSocket.onopen = function (e) {
    console.log("Successfully connected to the WebSocket.");
  };

  chatSocket.onclose = function (e) {
    console.log(
      "WebSocket connection closed unexpectedly. Trying to reconnect in 2s...",
    );
    setTimeout(function () {
      console.log("Reconnecting...");
      connect();
    }, 2000);
  };

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(
      typeof data.user,
      typeof currentUser.textContent,
      data.user,
      currentUser.textContent.replace(/"/g, ""),
    );
    const options = {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "numeric",
      minute: "numeric",
    };
    console.log(data);
    const timeNow = new Date().toLocaleDateString("en-MX", options);
    switch (data.type) {
      case "chat_message":
        console.log("adding div");
        if (data.user === currentUser.textContent.replace(/"/g, "")) {
          var newDiv = document.createElement("div");
          newDiv.innerHTML += `
                            <div class="media w-100 ml-auto mb-3 d-flex flex-row-reverse">
                            <div class="media-body text-end">
                            <div class="bg-dark rounded py-2 px-3 mb-2">
                                <p class="text-small mb-0 text-white">${data.message}</p>
                            </div>
                            <p class="small text-muted">${timeNow}</p>
                            </div>
                        </div>
                                    `;
          chatLog.appendChild(newDiv);
        } else {
          var newDiv = document.createElement("div");
          newDiv.innerHTML += `
                    <div class="media w-100 mb-3 d-flex flex-row">
                    <img src="https://freesvg.org/storage/img/thumb/abstract-user-flat-3.png" class="m-1" alt="user" style="width:32px; height:32px;" class="rounded-circle" />
                    <div class="media-body ml-3 text-start">
                      <div class="bg-light rounded py-2 px-3 mb-2">
                        <p class="text-small fw-bold text-black">${data.user}</p>
                        <p class="text-small fw-bold text-black">${data.message}</p>
                      </div>
                      <p class="small text-muted">${timeNow}</p>
                    </div>
                  </div>
                    `;

          chatLog.appendChild(newDiv);
        }

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
        chatLog.value += "PM from " + data.user + ": " + data.message + "\n";
        break;
      case "private_message_delivered":
        chatLog.value += "PM to " + data.target + ": " + data.message + "\n";
        break;

      case "tagged_message":
        if (data.user === currentUser.textContent.replace(/"/g, "")) {
          var newDiv = document.createElement("div");
          newDiv.innerHTML += `
                            <div class="media w-100 ml-auto mb-3 d-flex flex-row-reverse">
                            <div class="media-body text-end">
                            <div class="bg-dark rounded py-2 px-3 mb-2">
                                <p class="text-small mb-0 text-danger">${data.message}</p>
                            </div>
                            <p class="small text-muted">${timeNow}</p>
                            </div>
                        </div>
                                    `;
          chatLog.appendChild(newDiv);
        } else {
          var newDiv = document.createElement("div");
          newDiv.innerHTML += `
                    <div class="media w-100 mb-3 d-flex flex-row">
                    <img src="https://freesvg.org/storage/img/thumb/abstract-user-flat-3.png" class="m-1" alt="user" style="width:32px; height:32px;" class="rounded-circle" />
                    <div class="media-body ml-3 text-start">
                      <div class="bg-light rounded py-2 px-3 mb-2">
                        <p class="text-small fw-bold text-black">${data.user}</p>
                        <p class="text-small mb-0 text-danger">${data.message}</p>
                      </div>
                      <p class="small text-muted">${timeNow}</p>
                    </div>
                  </div>
                    `;

          chatLog.appendChild(newDiv);
        }
        break;

      default:
        console.error("Unknown message type!");
        break;
    }

    chatLog.scrollTop = chatLog.scrollHeight;
  };

  chatSocket.onerror = function (err) {
    console.log("WebSocket encountered an error: " + err.message);
    console.log("Closing the socket.");
    chatSocket.close();
  };
}
connect();

onlineUsersSelector.onchange = function () {
  chatMessageInput.value = "/pm " + onlineUsersSelector.value + " ";
  onlineUsersSelector.value = null;
  chatMessageInput.focus();
};
