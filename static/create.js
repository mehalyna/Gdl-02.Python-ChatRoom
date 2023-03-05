document.querySelector("#roomName").focus();
document.querySelector("#roomName").onkeyup = function (e) {
  if (e.keyCode === 13) {
    // enter, return
    document.querySelector("#roomSubmit").click();
  }
};

document.querySelector("#roomSubmit").onclick = function (e) {
  var roomName = document.querySelector("#roomName").value;
  window.location.pathname = "chat/detail/" + roomName + "/";
};
