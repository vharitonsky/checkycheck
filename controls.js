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
  var params = {product_id: image.getAttribute('data-product-id'),
                computer: image.getAttribute('data-computer'),
                moderator: true};
  const searchParams = Object.keys(params).map(function (key){
  return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
  }).join('&');

  fetch(window.location.href, {
    method: "POST",
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    },
    body: searchParams
  });
}

function deny(el) {
  var image = el.parentNode.previousSibling;
  var params = {product_id: image.getAttribute('data-product-id'),
                computer: image.getAttribute('data-computer')};
  const searchParams = Object.keys(params).map(function (key){
    return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
  }).join('&');

  fetch(window.location.href, {
    method: "POST",
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    },
    body: searchParams
  });
}