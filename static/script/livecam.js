const socket = io.connect(window.location.origin);

function startCamera() {
    var videoElement = document.createElement('img');
    videoElement.className = "video"
    videoElement.src = "/video_feed";
    videoElement.alt = "Video Feed";
    videoElement.id = "videoFeed";

    var container = document.getElementById('camera-area');
    container.appendChild(videoElement);
}
var buttons = document.getElementById('button-start-stop');
var audio_indicator = document.getElementById('audio-indicator');
if (buttons) {
    buttons.style.display = 'none';
}
if (audio_indicator) {
    audio_indicator.style.display = 'none';
}

var taskbarDict = document.getElementById("camera-toggle");
var camera_button_text_element = document.getElementById("camera_text_element");
var camera_is_on = false;
if (taskbarDict) {
    taskbarDict.addEventListener("click", function (e) {
        if (camera_is_on) {
            camera_is_on = false;
            camera_button_text_element.textContent = "TURN ON CAMERA";
            var container = document.getElementById('camera-area');
            var lastVideoElement = container.lastChild;
            if (lastVideoElement) {
                lastVideoElement.src = "";
                container.removeChild(lastVideoElement);
            }
            if (buttons) {
                buttons.style.display = 'none';
            }
            if (audio_indicator) {
                audio_indicator.style.display = 'none';
            }
        } else {
            camera_is_on = true;
            camera_button_text_element.textContent = "TURN OFF CAMERA";
            startCamera();
            if (buttons) {
                buttons.style.display = 'block';
            }
            if (audio_indicator) {
                audio_indicator.style.display = 'block';
            }
        }
    });
}

var start_stop_button = document.getElementById("start_stop");
var start_stop_text = document.getElementById("start_stop_text");
if(start_stop_button){
    start_stop_button.addEventListener("click", function(e){
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/start-stop-clicked', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({clicked: true}));
        if (start_stop_text.textContent == "STOP"){
            start_stop_text.textContent = "START";
        }else{
            start_stop_text.textContent = "STOP";
        }
    });
}

var audio_button = document.getElementById("audio-button");
if(audio_button){
    audio_button.addEventListener("click", function (e){
        var translated_text = document.getElementById("translated_words");
        var message = new SpeechSynthesisUtterance();
        message.text = translated_text.textContent;
        message.lang = "en-US";
        window.speechSynthesis.speak(message);

    })
}

socket.on('update_data', function (data) {
    var translated_text = document.getElementById("translated_words");
    translated_text.textContent = data.words;
    console.log(data.predicted_class);
    console.log(data.probability);
    console.log(data.words);
});

