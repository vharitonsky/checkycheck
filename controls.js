window.onload = function () {
  var controls = '<button onclick="approve(this)">PRAVILNO</button>' +
      '<button onclick="deny(this)">NE PRAVILNO</button>';

  var images = [].slice.call(document.querySelectorAll('img'));
  images.map(function (image) {
      var node = document.createElement('div');
      node.innerHTML = controls;
      document.body.insertBefore(node, image.nextSibling)
  })
};

function approve(el) {
  var image = el.parentNode.previousSibling;
  var product_id = image.getAttribute('data-product-id');
  var computer = image.getAttribute('data-computer');
  var formData = new FormData();
  formData.append('product_id', product_id);
  formData.append('computer', !!computer);
  formData.append('moderator', true);
  fetch(window.location.href, {
    method: "POST",
    body: formData
  });
}

function deny(el) {
  var image = el.parentNode.previousSibling;
  var product_id = image.getAttribute('data-product-id');
  var computer = image.getAttribute('data-computer');
  var formData = new FormData();
  formData.append('product_id', product_id);
  formData.append('computer', !!computer);
  formData.append('moderator', false);
  fetch(window.location.href, {
    method: "POST",
    body: formData
  });
}