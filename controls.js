window.onload = function () {
  var controls = '<div>' +
      '<button value="Правильно" onclick="approve(this)" />' +
      '<button value="Не правильно" onclick="deny(this)" />' +
  '</div>';
  var images = [].slice.call(document.querySelectorAll('img'));
  images.map(function (image) {
      image.parentNode.appendChild(controls)
  })
};

function approve(el) {
  var image = el.parentNode.previousNode();
  var product_id = image.getAttribute('data-product-id');
  var computer = image.getAttribute('data-computer');
  var formData = new FormData();
  formData.append('product_id', product_id);
  formData.append('computer', !!computer);
  formData.append('moderator', true);
  fetch("/check", {
    method: "POST",
    body: formData
  });
}

function deny(el) {
  var image = el.parentNode.previousNode();
  var product_id = image.getAttribute('data-product-id');
  var computer = image.getAttribute('data-computer');
  var formData = new FormData();
  formData.append('product_id', product_id);
  formData.append('computer', !!computer);
  formData.append('moderator', false);
  fetch("/check", {
    method: "POST",
    body: formData
  });
}