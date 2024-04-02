function startCamera() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert('getUserMedia is not supported in your browser');
        return;
    }

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            var videoElement = document.createElement('video');
            videoElement.autoplay = true;
            videoElement.srcObject = stream;

            var container = document.getElementById('camera-area');
            container.appendChild(videoElement);
        })
        .catch(function(error) {
            console.error('Error accessing camera:', error);
            alert('Error accessing camera: ' + error.name);
        });
}

var buttons = document.getElementById('button-start-stop');
var audio_indicator = document.getElementById('audio-indicator');
if(buttons){
    buttons.style.display = 'none';
}
if(audio_indicator){
    audio_indicator.style.display = 'none';
}

var taskbarDict = document.getElementById("camera-toggle");
var camera_button_text_element = document.getElementById("camera_text_element");
var camera_is_on = false;
if (taskbarDict) {
    taskbarDict.addEventListener("click", function (e) {
        if(camera_is_on){
            camera_is_on = false;
            camera_text_element.textContent = "TURN ON CAMERA";
            // var container = document.getElementById('camera-area');
            // var lastVideoElement = container.lastChild;
            // if (lastVideoElement) {
            //     var tracks = lastVideoElement.srcObject.getTracks();
            //     tracks.forEach(function(track) {
            //         track.stop();
            //     });
            //     container.removeChild(lastVideoElement);
            // }
            if(buttons){
                buttons.style.display = 'none';
            }
            if(audio_indicator){
                audio_indicator.style.display = 'none';
            }
        }else{
            camera_is_on = true;
            camera_text_element.textContent = "TURN OFF CAMERA";
            // startCamera()
            if(buttons){
                buttons.style.display = 'block';
            }
            if(audio_indicator){
                audio_indicator.style.display = 'block';
            }
            const socket = io.connect(window.location.origin);

            socket.on('update_data', function(data) {
                console.log(data.predicted_class);
                console.log(data.probability);
            });
        }
    });
}