# Manual Testing Plan

This document outlines manual test steps and expected outcomes for each page and feature of the Django eCommerce site.

---

## 1. Registration Page

### Accessing the Registration Page

**Step 1:** Open the website in a browser.

- **Action:** Enter the site URL and press Enter.
- **Expectation:** Homepage loads without errors.

**Step 2:** Locate and click the "Register" or "Sign Up" link/button.

- **Action:** Click the registration link/button in the navigation or login page.
- **Expectation:** Registration form page loads, displaying all required fields: username, email, password, confirm password, address, phone.

**Step 3:** Inspect the registration form for UI and accessibility.

- **Action:** Check that all fields are labeled, required fields are marked, and tab order is logical.
- **Expectation:** Form is clear, accessible, and ready for input.

### Successful Registration

**Step 1:** Enter valid user details in all required fields.

- **Action:** Fill in username, email, password, confirm password, address, and phone with valid, unique values.
- **Expectation:** All fields accept input, no client-side validation errors.

**Step 2:** Submit the registration form.

- **Action:** Click the "Register" or "Sign Up" button.
- **Expectation:** Form submits, loading indicator or feedback appears.

**Step 3:** Observe the result after submission.

- **Action:** Wait for server response.
- **Expectation:**
  - Account is created in the database.
  - User is redirected to login page.
  - A confirmation message is displayed: "Registration successful. You can now log in."
  - User is not automatically logged in.

### Registration Validation

**Step 1:** Attempt to submit the form with missing required fields.

- **Action:** Leave one or more required fields blank and click submit.
- **Expectation:** Validation errors are shown, indicating which fields are missing.

**Step 2:** Enter invalid data (e.g., invalid email format, weak password, mismatched passwords).

- **Action:** Fill in fields with invalid data and submit.
- **Expectation:** Specific validation error messages are displayed for each issue (e.g., "Invalid email address", "Passwords do not match").

**Step 3:** Try to register with a username or email that already exists.

- **Action:** Use credentials of an existing user and submit.
- **Expectation:** Error message appears (e.g., "Username/email already taken"), account is not created.

**Step 4:** Check for security and feedback.

- **Action:** Inspect error messages for clarity and security (no sensitive info leaked).
- **Expectation:** Errors are clear, do not reveal sensitive details, and form remains ready for correction and resubmission.

## 2. Login/Logout

### Accessing the Login Page

**Step 1:** Open the website and locate the "Login" link/button.

- **Action:** Click the login link/button in the navigation or homepage.
- **Expectation:** Login form page loads, displaying username and password fields.

### Successful Login

**Step 1:** Enter valid credentials (existing username and password).

- **Action:** Fill in username and password fields with correct values.
- **Expectation:** All fields accept input, no client-side validation errors.

**Step 2:** Submit the login form.

- **Action:** Click the "Login" button.
- **Expectation:** Form submits, loading indicator or feedback appears.

**Step 3:** Observe the result after submission.

- **Action:** Wait for server response.
- **Expectation:**
  - User is logged in.
  - User is redirected to homepage.
  - A welcome message is displayed: "Login successful."

### Login Validation

**Step 1:** Enter invalid credentials (wrong username or password).

- **Action:** Fill in incorrect values and submit.
- **Expectation:** Error message displayed: "Invalid username or password."

### Logout

**Step 1:** Click the "Logout" link/button.

- **Action:** Click logout in the navigation or user menu.
- **Expectation:**
  - User is logged out.
  - User is redirected to homepage.
  - A message is displayed: "You have been logged out."

## 3. Product Catalogue & Pagination

### Browsing the Catalogue

**Step 1:** Open the homepage or catalogue page.

- **Action:** Navigate to the main product listing page.
- **Expectation:** Products are listed with name, brand, category, price, and image.

**Step 2:** Inspect pagination controls.

- **Action:** Look for pagination controls (e.g., next/previous links or page numbers).
- **Expectation:** Pagination controls are visible if there are more products than fit on one page.

### Using Pagination

**Step 1:** Click pagination controls (next/previous/page number).

- **Action:** Click to navigate to another page of products.
- **Expectation:** Next/previous page of products loads, product list updates accordingly.

## 4. Product Detail Page

### Viewing Product Details

**Step 1:** Click on a product from the catalogue or search results.

- **Action:** Select a product to view its details.
- **Expectation:** Product detail page loads, showing product name, brand, category, description, price, stock, and image.

**Step 2:** Inspect available actions and button conditions.

- **Action:** Check for the following buttons:
  - **Add to Cart**: Visible only if the user is authenticated.
  - **Add to Wishlist**: Visible only if the user is authenticated and there are wishlists available.
  - **Back to Shop**: Always visible.
- **Expectation:** Each button is present and functional under the correct conditions:
  - Authenticated users can add to cart and wishlist (if wishlists exist).
  - All users can use "Back to Shop".

**Note:** All actions (add to cart, add to wishlist) require authentication. Unauthenticated users are redirected to login or shown an error. There is no ratings section on the product detail page. Only reviews may be present if implemented.

## 5. Search/Filter

### Using Search and Filter

**Step 1:** Locate search and filter controls on the catalogue or homepage.

- **Action:** Find the search input, category dropdown, and brand dropdown.
- **Expectation:** Controls are visible and usable.

**Step 2:** Enter a search term or select a category/brand.

- **Action:** Type a product name/keyword, or select a category/brand from the dropdowns.
- **Expectation:** Product list updates to show only matching products.

**Step 3:** Clear or change search/filter criteria.

- **Action:** Remove search term or change dropdown selection.
- **Expectation:** Product list updates accordingly, showing all or newly filtered products.

## 6. Shopping Cart

### Managing the Shopping Cart

**Step 1:** Add a product to the cart.

- **Action:** On the product detail page, click "Add to Cart" (only available if authenticated).
- **Expectation:** Product is added to the cart, confirmation message is shown.

**Step 2:** View the cart.

- **Action:** Navigate to the cart page from navigation or after adding a product.
- **Expectation:** Cart page lists all added products, quantities, and total price.

**Step 3:** Increment, decrement, or remove items.

- **Action:** Use provided controls (buttons/links) to change quantity or remove items.
- **Expectation:** Cart updates accordingly, reflecting new quantities or removed items, and updates total price.

**Step 4:** Cart access conditions.

- **Action:** Try to access the cart when not authenticated.
- **Expectation:** Redirected to login or shown an appropriate message.

## 7. Shipping Information

- **Step:** Proceed to checkout
- **Action:** Enter shipping details
- **Expectation:** Details saved, proceed to payment

## 8. Stripe Payment

**Authentication Required:** We redirect to the Stripe checkout page using the SDK, it's not possible for the user to manually get to the checkout page by manipulating the url. The SDK initializes the process.

### Stripe Payment Process

For test card scenarios and more, see the official Stripe testing documentation: [Stripe Testing Guide](https://docs.stripe.com/testing)

**Step 1:** Initiate checkout from the cart page.

- **Action:** Click the "Checkout" button (only available if cart is not empty and user is authenticated).
- **Expectation:** Redirected to Stripe payment page.

**Step 2:** Enter payment details on Stripe.

- **Action:** Fill in valid card/payment details and submit.
- **Expectation:** Payment is processed by Stripe.

**Step 3:** On successful payment, redirected to success page.

- **Action:** Complete payment and follow redirect.
- **Expectation:**
  - Success page loads, showing order reference, items, and total paid.
  - Cart is cleared.
  - Thank you message and order details shown.

**Step 4:** On payment failure or cancellation.

- **Action:** Cancel payment or enter invalid/declined card details (e.g., insufficient funds, Stripe test card errors).
- **Expectation:**
  - For cancellation, redirected to cart
  - For payment failures (e.g., declined card, insufficient funds), user remains on the Stripe payment page and Stripe displays the error message directly.

## 9. Order History & Management

**Authentication Required:** Only authenticated users can view their order history and order details. Unauthenticated users are redirected to login.

### Viewing Order History

**Step 1:** Access the order history page.

- **Action:** Navigate to "Order History" from the navigation or user menu.
- **Expectation:** List of past orders is displayed, showing order number, status, date, and total.

**Step 2:** View order details.

- **Action:** Click on an order to view its details.
- **Expectation:** Order detail page loads, showing all items, quantities, prices, total, and status.

**Step 3:** Review order actions.

- **Action:** If the order is not reviewed, click "Leave Review for Order". If reviewed, see review and star rating.
- **Expectation:**
  - If not reviewed, user can leave a review.
  - If reviewed, review and star rating are displayed.

**Note:** Deleting orders is not available; users cannot delete their order history in this eCommerce implementation.

## 10. Wishlist

**Authentication Required:** Only authenticated users can create, view, update, or manage wishlists and wishlist items. Unauthenticated users are redirected to login.

### Managing Wishlists

**Step 1:** Create a wishlist.

- **Action:** Navigate to "Wishlists" and enter a name.
- **Expectation:** Wishlist is created and confirmation message is shown.

**Step 2:** View all wishlists.

- **Action:** Go to "Wishlists" page.
- **Expectation:** List of all user wishlists is displayed.

**Step 3:** Rename or delete a wishlist.

- **Action:** Use provided controls to rename or delete a wishlist.
- **Expectation:** Wishlist name updates or wishlist is deleted, with confirmation message.

**Step 4:** Add items to wishlist from product detail

- **Action:** On product detail page, select a wishlist and add product.
- **Expectation:** Product is added to wishlist, confirmation or info message shown.

**Step 5:** Remove items from wishlist detail

- **Action:** Use provided controls to remove an item from a wishlist.
- **Expectation:** Item is removed, wishlist updates, confirmation message shown.

**Step 6:** Add wishlist item to cart.

- **Action:** Use provided controls to add a wishlist item to the shopping cart.
- **Expectation:** Item is added to cart and removed from the list, confirmation message shown.

## 11. Product Reviews & Ratings

**Authentication Required:** Only authenticated users who have placed an order can leave a review for that order. Unauthenticated users are redirected to login.

### Leaving Reviews and Ratings

**Step 1:** Leave a review for an order.

- **Action:** On the order detail page, click "Leave Review for Order" (only available if not already reviewed).
- **Expectation:** Review form loads, allowing entry of a star rating (1-5) and comment.

**Step 2:** Submit a valid review.

- **Action:** Enter a rating and comment, then submit the form.
- **Expectation:** Review is saved, confirmation message shown, and review appears on the order detail page with star rating and comment.

**Step 3:** Submit an invalid review (e.g., missing rating or comment, rating out of range).

- **Action:** Submit the form with invalid or missing data.
- **Expectation:** Validation error is shown, review is not saved.

**Step 4:** Attempt to leave a second review for the same order.

- **Action:** Try to submit another review for an already reviewed order.
- **Expectation:** Info message shown: "You have already reviewed this order." and no duplicate review is created.

---

Repeat steps for different user roles and edge cases as needed.
