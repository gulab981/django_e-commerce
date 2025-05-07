var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log(user)
        if (user === 'AnonymousUser') {
            // console.log('unknown user')
            addCookieItem(productId, action)
        }
        else {
            updateUserOrder(productId, action)
        }
    })
}

function getCookie(name) {
    var cookieArr = document.cookie.split(';')
    for (var i = 0; i < cookieArr.length; i++) {
      var cookiePair = cookieArr[i].split('=')
      if (name == cookiePair[0].trim()) {
        return decodeURIComponent(cookiePair[1])
      }
    }
    //return null if the cookie not found
    return null
  }

var cart = JSON.parse(getCookie('cart'));

function addCookieItem(productId, action) {
    console.log('user is not authenticated')

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1;
        }
    }
    if(action == 'remove'){
        cart[productId]['quantity'] -= 1;
        if(cart[productId]['quantity'] <= 0){
            console.log('Remove Item')
            delete cart[productId]
        }
    }
    console.log('cart is :',cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload()
}

function updateUserOrder(productId, action) {
    console.log('user logged in sending data...')

    var url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action
        })

    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log(data)
            location.reload()
        })
}