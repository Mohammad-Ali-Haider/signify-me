var signifyMeLogoCopy1 = document.getElementById("signifyMeLogoCopy1");
if (signifyMeLogoCopy1) {
    signifyMeLogoCopy1.addEventListener("click", function (e) {
        window.location.href = "./index.html";
    });
}

var signifyMeLogoCopy2 = document.getElementById("signifyMeLogoCopy2");
if (signifyMeLogoCopy2) {
    signifyMeLogoCopy2.addEventListener("click", function (e) {
        window.location.href = "./index.html";
    });
}

var liveCamTranslator1 = document.getElementById("liveCamTranslator1");
if (liveCamTranslator1) {
    liveCamTranslator1.addEventListener("click", function (e) {
        window.location.href = "./livecam.html";
    });
}

var videoTranslatorText1 = document.getElementById("videoTranslatorText1");
if (videoTranslatorText1) {
    videoTranslatorText1.addEventListener("click", function (e) {
        window.location.href = "./video.html";
    });
}

var phraseDictionaryText1 = document.getElementById("phraseDictionaryText1");
if (phraseDictionaryText1) {
    phraseDictionaryText1.addEventListener("click", function (e) {
        window.location.href = "./dictionary.html";
    });
}

var homeText = document.getElementById("homeText");
if (homeText) {
    homeText.addEventListener("click", function (e) {
        window.location.href = "./index.html";
    });
}

var aboutText = document.getElementById("aboutText");
if (aboutText) {
    aboutText.addEventListener("click", function (e) {
        window.location.href = "./about-us1.html";
    });
}

var supportText = document.getElementById("supportText");
if (supportText) {
    supportText.addEventListener("click", function (e) {
        window.location.href = "./support.html";
    });
}

var liveCamConvertorText = document.getElementById("liveCamConvertorText");
if (liveCamConvertorText) {
    liveCamConvertorText.addEventListener("click", function (e) {
        window.location.href = "./livecam.html";
    });
}

var videoConvertorText = document.getElementById("videoConvertorText");
if (videoConvertorText) {
    videoConvertorText.addEventListener("click", function (e) {
        window.location.href = "./video.html";
    });
}

var taskbarHome = document.getElementById("taskbar-home");
if (taskbarHome) {
    taskbarHome.addEventListener("click", function (e) {
        window.location.href = "./index.html";
    });
}

var taskbarVideo = document.getElementById("taskbar-video");
if (taskbarVideo) {
    taskbarVideo.addEventListener("click", function (e) {
        window.location.href = "./video.html";
    });
}

var taskbarLiveCam = document.getElementById("taskbar-livecam");
if (taskbarLiveCam) {
    taskbarLiveCam.addEventListener("click", function (e) {
        window.location.href = "./livecam.html";
    });
}

var taskbarAboutUs = document.getElementById("taskbar-aboutus");
if (taskbarAboutUs) {
    taskbarAboutUs.addEventListener("click", function (e) {
        window.location.href = "./about-us1.html";
    });
}

var taskbarDict = document.getElementById("taskbar-dict");
if (taskbarDict) {
    taskbarDict.addEventListener("click", function (e) {
        window.location.href = "./dictionary.html";
    });
}

var taskbarDict = document.getElementById("camera-toggle");
var camera_is_on = false;
if (taskbarDict) {
    taskbarDict.addEventListener("click", function (e) {
        if(camera_is_on) camera_is_on = false;
        else camera_is_on = true;

        if(camera_is_on){

        }
    });
}