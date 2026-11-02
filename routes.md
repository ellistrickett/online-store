# Initial Route Ideas (Draft)

## Store Views (Jinja2)
- GET / -> Home / featured products
- GET /products -> Full catalog
- GET /products/<id> -> Product detail + reviews
- GET /cart -> Cart view
- GET /checkout -> Checkout form

## Auth
- GET, POST /login
- GET, POST /register
- GET /logout

## APIs
- GET /api/products -> return JSON list (MongoDB)
- POST /api/orders -> create order (SQL)