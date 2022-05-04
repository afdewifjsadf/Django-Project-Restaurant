var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        updateUserOrder(productId, action)
    })
}

function updateUserOrder(productId, action) {
    console.log('User is Authenticated, sending data...')
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        // the below 'body' is being sent as a JSON string to 'updateItem' view in views.py
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('Data:', data)
            //below line is written, to refresh the page to increment the cart total in red on top right corner
            location.reload()
        })
}