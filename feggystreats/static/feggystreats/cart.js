var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var itemId = this.dataset.item
        var action = this.dataset.action
        

        console.log('itemId:', itemId, 'action:', action)

        console.log('User;', user)
        if(user == 'AnonymousUser'){
            updateGuestOrder(itemId, action)
        }else{
            updateUserOrder(itemId, action)
        }
    })
}

function updateGuestOrder(itemId, action){
    console.log('User is not authenticated')

    if(document.getElementById('q' + itemId)){
        var q = document.getElementById('q' + itemId).value
    }else{
        var q = '1'
    }

    q = Number(q)

    if(action == 'add'){
        if(cart[itemId] == undefined){
            cart[itemId] = {'quantity': q}
        }else{
            cart[itemId]['quantity'] = cart[itemId]['quantity'] + q
        }
    }

    if(action == 'add2'){
        cart[itemId]['quantity'] += q
    }

    if(action == 'remove'){
        cart[itemId]['quantity'] -= q

        if(cart[itemId]['quantity'] <= 0){
            console.log('Item should be deleted')
            delete cart[itemId]
        }
    }

    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}

function updateUserOrder(itemId, action){
    console.log('User is logged in, sending data...')

    if(document.getElementById('q' + itemId)){
        var quantity = document.getElementById('q' + itemId).value
    }else{
        var quantity = '1'
    }

    console.log(quantity)

    fetch('/add_item/', {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'itemId':itemId, 'action':action, 'quantity':quantity})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}
