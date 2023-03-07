document.querySelector("#roomSelect").onchange = function () {
  let roomName = document.querySelector("#roomSelect").value.split(" (")[0];
  window.location.pathname = "chat/" + "detail/" + roomName + "/";
};

function viewChat() {
  let roomName = document.querySelector("#roomSelect").value.split(" (")[0];
  window.location.pathname = "chat/" + "detail/" + roomName + "/";
}
