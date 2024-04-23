# Playwright in Python, practice project

As part of my employment requirements, this project showcases the skills
I have acquired from our Playwright training course.

This project focuses on testing a simple web application, namely [Sauce Demo](https://www.saucedemo.com/) by Swag Labs, with the following functionalities:

1. Login page with fields for username and password
2. Product page with a list of products available
3. Shopping cart page where users can view the added items in cart
4. Shipping information form page with fields for First name, Last name and Zip code
5. Checkout page

My task is to create the following test cases:

1. Test Case 1: Login Page
    * Open the web application
    * Verigy that the lign page is displayed
    * Enter valid credentials and click the login button
    * Verify that the Home/Products page is displayed after successful login
2. Test Case 2: Adding Products
    * After loggin-in, in the Products Page:
        * Add one specific product (Sauce Labs Fleece Jacket) to the shopping cart
        * Add any one random product to the shopping cart, sleection should be dynamic
    * Navigate to the shopping cart
    * Verify that there are 2 products successfully added to the cart
3. Test Case 3: Checkout Page
    * In the Shopping cart page, proceed to the checkout page
    * On the Shopping information form page, fill out the shipping information form by entering you First Name, Last Name and Zip Code
    * Verify that the changes are reflected on the shipping information form page
    * Complete the purchases process and verify that the order is successful

To run this project:

1. First install the dependencies
    > pip install -r requirements.txt
2. Install the playwright dependencies
    > playwright install
3. Then you may run pytest with this simple command
    > pytest
4. If you want to run in headed mode, or in all or some browser you may run this code
    > pytest --headed --browser chromium --browser firefox --browser webkit
