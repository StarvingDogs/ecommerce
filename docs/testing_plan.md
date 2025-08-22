# Manual Testing Plan

This document outlines manual test steps and expected outcomes for each page and feature of the Django eCommerce site.

---

## 1. Registration Page

- **Step:** Navigate to registration page
- **Action:** Fill in valid user details and submit
- **Expectation:** User account is created, redirected to login or homepage, confirmation message shown
- **Action:** Submit with missing/invalid data
- **Expectation:** Validation errors displayed, account not created

## 2. Login/Logout

- **Step:** Navigate to login page
- **Action:** Enter valid credentials and submit
- **Expectation:** User is logged in, redirected to homepage, welcome message shown
- **Action:** Enter invalid credentials
- **Expectation:** Error message displayed
- **Step:** Click logout
- **Expectation:** User is logged out, redirected to login/homepage

## 3. Product Catalogue & Pagination

- **Step:** Browse catalogue
- **Expectation:** Products are listed, pagination controls visible
- **Action:** Click pagination controls
- **Expectation:** Next/previous page of products loads

## 4. Product Detail Page

- **Step:** Click on a product
- **Expectation:** Product details, reviews, and rating are displayed

## 5. Search/Filter

- **Step:** Use search/filter controls
- **Expectation:** Product list updates to match criteria

## 6. Shopping Cart

- **Step:** Add product to cart
- **Expectation:** Product appears in cart, confirmation message shown
- **Action:** Increment/decrement/remove item
- **Expectation:** Cart updates accordingly

## 7. Shipping Information

- **Step:** Proceed to checkout
- **Action:** Enter shipping details
- **Expectation:** Details saved, proceed to payment

## 8. Stripe Payment

- **Step:** Enter payment details and submit
- **Expectation:** Payment is processed, success message shown, order created
- **Action:** Enter invalid payment details
- **Expectation:** Error message displayed, payment not processed

## 9. Order History & Management

- **Step:** View order history
- **Expectation:** List of past orders displayed
- **Action:** View/delete order
- **Expectation:** Order details shown or order deleted

## 10. Wishlist

- **Step:** Create wishlist
- **Expectation:** Wishlist created, confirmation shown
- **Action:** Add/remove items, rename/delete wishlist, add to cart from wishlist
- **Expectation:** Wishlist updates accordingly

## 11. Product Reviews & Ratings

- **Step:** Leave a review and star rating
- **Expectation:** Review is saved, appears on product page
- **Action:** Submit invalid review
- **Expectation:** Validation error shown

---

Repeat steps for different user roles and edge cases as needed.
