Dropzone.autoDiscover = false;

var myDropzone = new Dropzone(".dropzone", {
  url: "/file/post",
  paramName: "file",
  maxFilesize: 10, // MB
  maxFiles: 1,
  acceptedFiles: "image/*,application/pdf", // Accepts both images and PDF files
  dictDefaultMessage: "Drag files here or click to upload.",
  clickable: true,
  autoProcessQueue: false,
  init: function () {
    this.on("addedfile", function (file) {
      var deleteButton = Dropzone.createElement(
        "<button class='btn btn-danger btn-sm mt-2'>Remove file</button>"
      );

      var _this = this;

      deleteButton.addEventListener("click", function () {
        _this.removeFile(file);
      });

      file.previewElement.appendChild(deleteButton);
    });
  },
});
