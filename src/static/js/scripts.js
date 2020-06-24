const swup = new Swup();

const init = () => {
  if (document.getElementById("scanner")) {
    // initiate Socket
    let socket = io("http://localhost:5000");
    socket.on("connect", function () {
      console.log("connected...!", socket.connected);
    });

    const box = document.getElementById("box");
    var width = box.offsetWidth;
    var height = 0;
    var streaming = false;
    var video = null;
    var canvas = null;
    // var photo = null;
    var button = null;

    function loadCamera() {
      video = document.getElementById("video");
      canvas = document.getElementById("canvas");
      // photo = document.getElementById("photo");
      formPhoto = document.getElementById("formPhoto");
      submitDiv = document.getElementById("submitDiv");
      button = document.getElementById("button");
      spinner = document.getElementById("spinner");

      navigator.mediaDevices
        .getUserMedia({ video: true, audio: false })
        .then(function (stream) {
          video.srcObject = stream;
          video.play();
          spinner.setAttribute("hidden", true);
        })
        .catch(function (err) {
          console.log(err);
        });

      video.addEventListener(
        "canplay",
        function (ev) {
          if (!streaming) {
            height = video.videoHeight / (video.videoWidth / width);

            if (isNaN(height)) {
              height = width / (4 / 3);
            }

            video.setAttribute("width", width);
            video.setAttribute("height", height);
            canvas.setAttribute("width", width);
            canvas.setAttribute("height", height);
            streaming = true;

            let src = new cv.Mat(height, width, cv.CV_8UC4);
            let dst = new cv.Mat(height, width, cv.CV_8UC1);
            let cap = new cv.VideoCapture(video);

            const FPS = 60;

            id = setInterval(() => {
              cap.read(src);
              var context = canvas.getContext("2d");
              canvas.width = width;
              canvas.height = height;
              context.drawImage(video, 0, 0, width, height);

              var type = "image/png";
              data = canvas.toDataURL("image/png");
              //data = data.replace("data:" + type + ";base64,", "");

              socket.emit("videostream", data);
            }, 10000 / FPS);

            socket.on("response_back", function (image) {
              const image_id = document.getElementById("photo");
              const barcode_input = document.getElementById("barcode");
              const newItem_button = document.getElementById("newItem-btn");
              const notification = document.getElementById("notification");
              if (typeof image["message"] !== "undefined") {
                notification.innerText = image["message"];
                notification.removeAttribute("hidden");
              }

              video.setAttribute("hidden", true);
              image_id.setAttribute("width", width);
              image_id.setAttribute("height", height);
              image_id.src = image["image"];
              formPhoto.value = image["image"];
              barcode_input.value = image["code"];
              newItem_button.innerText = "Use this barcode: " + image["code"];
            });
          }
        },
        false
      );

      /*   button.addEventListener(
        "click",
        function (ev) {
          takepicture();
        },
        false
      );
    }

    function takepicture() {
      var context = canvas.getContext("2d");
      canvas.width = width;
      canvas.height = height;
      context.drawImage(video, 0, 0, width, height);

      var data = canvas.toDataURL("image/png");
      console.log(data);
      formPhoto.setAttribute("value", data);
      box.classList.add("loading");
    } */
      cv["onRuntimeInitialized"] = () => {};
    }

    loadCamera();
  } else {
    try {
      clearInterval(id);
    } catch (error) {
      console.log("ERR");
    }
  }

  logoutButton = document.getElementById("logout");
  logoutButton.addEventListener("click", () => {
    swup.destroy();
  });
};

init();
swup.on("contentReplaced", init);
