window.onload = function () {
  var controls = '<button value="PRAVILNO" onclick="approve(this)" />' +
      '<button value="NE PRAVILNO" onclick="deny(this)" />';

  var images = [].slice.call(document.querySelectorAll('img'));
  images.map(function (image) {
      var node = document.createElement('div');
      node.innerHTML = controls;
      image.parentNode.appendChild(node)
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