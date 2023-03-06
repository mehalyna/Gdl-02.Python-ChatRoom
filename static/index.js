console.log("Sanity check from index.js.");
console.log("Hi");
// document.querySelector("#roomInput").focus();

// document.querySelector("#roomInput").onkeyup = function (e) {
//   if (e.keyCode === 13) {
//     document.querySelector("#roomConnect").click();
//   }
// };

// document.querySelector("#roomConnect").onclick = function () {
//   let roomName = document.querySelector("#roomInput").value;
//   window.location.pathname = "chat/" + roomName + "/";
// };

document.querySelector("#roomSelect").onchange = function () {
  let roomName = document.querySelector("#roomSelect").value.split(" (")[0];
  window.location.pathname = "chat/" + "detail/" + roomName + "/";
};

function viewChat() {
  console.log("Get in");
  let roomName = document.querySelector("#roomSelect").value.split(" (")[0];
  console.log("Get room", roomName);
  window.location.pathname = "chat/" + "detail/" + roomName + "/";
}
