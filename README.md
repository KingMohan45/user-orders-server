### User Orders Management Platform APIs
- `make seed-users` Validates and adds users to the database
  - Removed few users and updated emails in users.csv which are duplicates and few with invalid/missing emails
  - Here users's email is unique but not phone number
- `make seed-orders` Validates and adds orders to the database
  - Removed few orders, orders.csv with missing products
    - john.doe@example.com,P011,2024-02-28
    - lily.parker@example.com,P019,2023-12-25
    - olivia.perez@example.com,P050,2024-01-25

### To Start
- Requires python3.10
- `make install` Installs the dependencies
- `make start` Starts the server
