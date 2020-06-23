const swup = new Swup();

const init = () => {
  if (document.getElementById("scanner")) {
    var width = "100%";
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
          //spinner.setAttribute("hidden", true);
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
          }
        },
        false
      );

      button.addEventListener(
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
      /* photo.setAttribute("src", data); */
      formPhoto.setAttribute("value", data);
    }

    loadCamera();
  }
};

init();
swup.on("contentReplaced", init);
