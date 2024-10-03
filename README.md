# Django-Project
alex - seller , 
christen-admin,
admin access rights to entire web page he can just make modifications in product and cart update & delete not allowed to add products to cart list but can view cart list added by buyer
seller access rights to entire product list page to add,update or delete and can just view cart list added by buyer but cant make changes in cart page.
buyer access rights to entire cart page to add,update or delete but can just view product list page cant modify items in product list page
add to cart can be done only by buyer not ny admin or seller
 dennis-admin, 
 jack-buyer,
  Alice-buyer, 
  David-seller
  as admin i can make changes to product list to add,update or delete and can add product to cart list and remove any existing product and also decrease or increase quantity of product but cant do checkout process.
  as seller can make changes to product list to add,update or delete and no access to cart list and checkout process.
  as buyer can just view product list and make changes to cart list like add product, update quantity, remove product and do checkout product list.

Step 1: Running the Server
When the server starts, Django loads all the installed apps and configurations.
You access the web application by navigating to the homepage (e.g., localhost:8000).
Step 2: Authentication and Authorization
URL Access:

If the user is not logged in, they are redirected to the login page (/login).
If the user doesn’t have an account, they can visit the signup page (/signup), where they select a role (Admin, Seller, or Buyer) during the signup process.
Signup Workflow:

A user signs up by providing credentials (username, password) and choosing a role.
The backend saves the user in the database and assigns them to a specific group (Admin, Seller, or Buyer) based on the selected role.
Login Workflow:

After signing up, the user logs in with their credentials.
If login is successful, a JWT token is created, and the role of the user is embedded in the token.
This token is stored as an HttpOnly cookie to be used for subsequent requests to authenticate the user.
Step 3: Role-Based Permissions
Once the user is authenticated, the app checks their role using JWT token-based authentication:

Admin:

Can create, update, delete products.
Cannot access the checkout page.
Seller:

Can create, update, and view products.
Cannot view the cart page or perform checkout operations.
Buyer:

Can view products.
Can add products to the cart, view the cart, and proceed to checkout.
Step 4: Product Management
For Admin and Seller:
Product List Page: Lists all products in the system.
Admin/Seller can add a new product using the create product form, which includes uploading images, providing product details (name, price, description, stock, etc.), and saving the product.
Admin/Seller can edit existing products or delete them from the database.
Product Creation Workflow:
The Admin/Seller submits a product creation form.
The product data (including images) is saved in the database.
The user is redirected to the product list page, and a success message is displayed.
Step 5: Viewing Products
For Buyers:

On the product list page (/products), a buyer can view a list of available products.
There is also a search functionality that allows the buyer to search for products by name.
Product Viewing Workflow:

The buyer browses or searches for products.
A paginated list of products is displayed with their images, names, and prices.
Step 6: Cart Management
For Buyers:

Buyers can add products to their shopping cart.
They can view their cart by going to the cart page (/cart).
On the cart page, buyers can see the list of products added to the cart, with quantities, prices, and the total amount.
Cart Functionality Workflow:

The buyer clicks the "Add to Cart" button for a product.
The product is added to the user's cart (a CartItem entry is created in the database for that user).
The cart is displayed with options to increase or decrease product quantities using + and - buttons.
The total price is calculated based on the products in the cart.
Step 7: Checkout
For Buyers:
Once the buyer is ready to purchase, they click on the Checkout button on the cart page.
This action redirects the buyer to the Stripe payment gateway.
Checkout Workflow:
The total amount for the cart is calculated.
A Stripe Checkout Session is created with the total amount, currency (INR), and payment details.
The buyer is redirected to Stripe's payment page, where they complete the payment.
After payment success, the buyer is redirected back to the e-commerce site, where their cart is emptied, and the order is confirmed.
Step 8: Managing Cart and Checkout Access (Authorization)
Admin is restricted from performing checkout by checking their group membership in the checkout_view. If an admin tries to access the checkout page, they receive an error message.

Seller is restricted from viewing the cart. If a seller tries to view the cart page, they are redirected to the product list with an error message.

Detailed Flow of the Code Implementation
Signup View (signup_view):

Users choose their role during signup, and the role is stored in the Django groups (Admin, Seller, or Buyer).
Login View (login_view):

JWT tokens are generated upon successful login, embedding user roles in the token for subsequent role-based authentication.
Product Management Views (create_product, update_product, delete_product):

These views are restricted to Admin and Seller roles.
Cart Management Views (cart_view, checkout_view):

Buyers can view the cart, update quantities, and proceed to checkout.
Sellers are restricted from accessing the cart and checkout.
Admins are restricted from performing checkout operations.
Checkout Integration:

The checkout process is integrated with Stripe. The total amount is calculated, and the buyer is redirected to Stripe's hosted payment page. After successful payment, the cart is emptied.
Step 9: Static and Media Files Management
Your project includes static files (CSS, JS, images) that are organized in a way to style the pages (such as product list, cart, checkout page).
Images for products are uploaded via forms and stored in the media folder. These images are then displayed on the product list page and other related views.
Summary of Roles and Permissions
Admin:

Can create, update, delete products.
Cannot view or access the checkout process.
Seller:

Can create, update, and view products.
Cannot view the cart or perform checkout.
Buyer:

Can view products.
Can add products to the cart, view the cart, and proceed to checkout.