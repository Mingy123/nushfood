/* Use the following code to obtain b64 data

const video = document.querySelector('video');
var canvas = document.createElement('canvas');
canvas.width = video.videoWidth;
canvas.height = video.videoHeight;

var ctx = canvas.getContext('2d');
ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
var dataURL = canvas.toDataURL('image/png');
*/



export async function api_drink(b64img) {
  console.log("sending to api for drink classification")
  var data = new URLSearchParams()
  data.append("b64img", b64img.substring(b64img.indexOf(',') + 1).trim())
  var response = await fetch("/api/ai_orz", {
    method: "POST",
    body: data
  })
  let text = await response.text()
  return text
}

export async function api_segment(b64img) {
  console.log("sending to api for image segmentation")
  var data = new URLSearchParams()
  data.append("b64img", b64img.substring(b64img.indexOf(',') + 1).trim())
  var response = await fetch("/api/segment", {
    method: "POST",
    body: data
  })
  let text = await response.text()
  return text
}