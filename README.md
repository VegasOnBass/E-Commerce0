# Feggy's Treats 
#### Video Demo:  https://youtu.be/yLBOZ2TdWWE
#### Description:

My project is a simple e-commerce site for baked goods. It allows both users and guest to put products into a cart, process the order, and take payments. Currently it is set up only to take dummy payments for test purposes. The following will break down the components to help understand the process taken.

###### Templates
In *layout.html* you find you'll find a basic navbar with a dropdown feature for the store pages. On this page is where you will also find the the javascript to set the cookie information. *Index.html* is the home page welcoming customers to the site. The store pages are named for each current category of treat we have and have the items in rows of 3 at max screen width. The rows are responsive. clicking the cart image in the navbar sends you to *cart.html* where you will find all the information about you cart including items in it, quantity per item, price, total amount of items and total price. If your cart is populated with items a bottom will appear at the bottom of the cart page to send you to the *checkout.html*. You are able to change the quantity amount of each item in you cart on this page. *Checkout.html* is where the order is finalized. It gives you a review of your cart, takes all th necessary info needed to complete the order and processes payments. On this page you find some javascript for the payment process thru PAYPAL. There is also the javascript to send all the customer and shipping info to the backend to be processed and stored.

###### Views.py

In our *views.py* file we find most of the backend functionality to present our site. It mainly renders out the templates with a few JSON responses added in. A lot of the coding was cleaned up and move to *utils.py* to give *views.py* a more presentable look. Each current item category has its on view rendering, i.e. *cookies* and *brownies*.  *AddItem* only adds/removes items for a user cart. *ProcessOrder* handles the finalization of the order getting all the necessary info for shipping.

###### Utils.py

Utils.py is where you find the repeated bulk code. There are three functions. *Cookie_cart* is where the guest cart information is processed. *CartData* neatly acquires the cart information for users and guest so that cart information can be presented across all pages. *GuestOrder* processes the guest information to complete the order without a user login.

###### Models.py

In *models.py* you'll find th framework for our a database. There are 5 models , not including *User*, that are used to store the data needed for our site. 
    -*Item* has all the basic information about each individual item. It also includes a property to access the item image easily on the html pages.
    -*Customer* has the basic information about the customer like there username if applicable, name and email.
    -*Order* is where the transaction status is stored. It connects the items to the customer. There are two properties found with this model. One to get the total amount of items in the cart and another to get the total price of the items in the cart.
    -*OrderItem* connects an item to an order and get adjusts the quantity of that item for the order. There is a property to help get the total price of the item multiplying the price by quantity.
    -*ShippingAddress* is where you find the customers shipping info.

###### Media/Uploads

The media/uploads file contains all the images for each item.

###### Urls.py

*Urls.py* has a urls for our view functions. To access the item images in our *media/uploads* we simply add *+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)* to the end.


##### Static
###### Styles.css

*Styles.css* is where a majority of the sites styling will be found with the exception of some in-line styling and bootstrap classes.

###### Cart.js

Cart.js is where our javascript is found to add items to our cart. It first gets the item id and action that the function wants to perform. Once a user is verified it proceeds to either *updateGuestOrder* or *updateUserOrder* from which it will transfer the information to either *cookie_cart* in *utils.py for guest or *addItem* in *views.py* for users.

###### Images
*Images* is where all the images used on the site are stored for access. You find the main site background, cart and arrows to add/remove items.