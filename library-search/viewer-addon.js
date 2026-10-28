// Library Chat addition to the PDF.js viewer: a floating "Download this PDF" button for the file being viewed.
(function () {
  var file = new URLSearchParams(location.search).get("file") || "";
  if (file.indexOf("/pdf/") !== 0) return;                 // only our own library PDFs
  var a = document.createElement("a");
  a.id = "lcDownload";
  a.href = file.split(/[?#]/)[0] + "?dl=1";
  a.setAttribute("download", decodeURIComponent(file.split("/").pop().split(/[?#]/)[0]));
  a.textContent = "\u2B07 Download this PDF";
  a.title = "Save the whole guide to this device";
  document.body.appendChild(a);
})();
