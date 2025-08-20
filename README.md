

---

# Inventory Management API

A **RESTful API** for managing inventory items, tracking changes, and monitoring stock levels. This API is built with Django REST Framework and follows an **API-First approach** (no frontend in v1). Each user manages their own inventory securely.

---

## 🔹 Features

### 1. User Management (CRUD)

* Register, authenticate, and manage users.
* Only authenticated users can manage inventory items.
* Admins can view and manage all users.

**Endpoints:**

| Endpoint         | Method                | Description                  |
| ---------------- | --------------------- | -----------------------------|
| `/api/register/` | POST                  | Create a new user            |
| `/api/login/`    | POST                  | Authenticate and get token   |
| `/api/logout/`   | POST                  | Authenticated users can delete their token to log out |
| `/api/users/`    | GET/POST/PATCH/DELETE | Admin-only user management   |

**Example: Register**

```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
-H "Content-Type: application/json" \
-d '{"username": "userA", "email": "userA@example.com", "password": "password123"}'
```

---

### 2. Inventory Item Management (CRUD)

* Users can create, read, update, and delete **their own inventory items**.
* Only the owner can access or modify their items.

**Endpoints:**

| Endpoint           | Method           | Description                   |
| ------------------ | ---------------- | ----------------------------- |
| `/api/items/`      | GET/POST         | List or create items          |
| `/api/items/<id>/` | GET/PATCH/DELETE | Retrieve, update, delete item |

**Example: Create Item**

```bash
curl -X POST http://127.0.0.1:8000/api/items/ \
-H "Content-Type: application/json" \
-H "Authorization: Token <TOKEN>" \
-d '{"name": "Mouse", "description": "Wireless Mouse", "quantity": 10, "price": "25.00"}'
```

---

### 3. Inventory Levels API

* Retrieve items with **quantities and details**.
* Supports **filtering**, **search**, and **ordering**.
* Only authenticated users can access their own items.

**Endpoints:**

| Endpoint                 | Method | Description                |
| ------------------------ | ------ | -------------------------- |
| `/api/inventory-levels/` | GET    | List items with quantities |

**Filters:**

* **Category:** `?category=electronics`
* **Price Range:** `?min_price=100&max_price=500`
* **Low Stock:** `?low_stock=5` (default ≤5)
* **Search:** `?search=laptop`
* **Ordering:** `?ordering=-price` or `?ordering=quantity`

**Example: Combined Query**

```bash
curl -X GET "http://127.0.0.1:8000/api/inventory-levels/?category=electronics&max_price=500&low_stock=5&ordering=quantity" \
-H "Authorization: Token <TOKEN>"
```

---

### 4. Track Changes / Item History

* Every change to an inventory item is **logged**: Restock, Sale, Adjustment.
* Shows **old quantity**, **new quantity**, **timestamp**, and **user** who made the change.

**Endpoints:**

| Endpoint                  | Method | Description                                 |
| ------------------------- | ------ | ------------------------------------------- |
| `/api/changes/`           | GET    | List all changes for the authenticated user |
| `/api/changes/?item=<id>` | GET    | List changes for a specific item            |

**Example: Get Item History**

```bash
curl -X GET "http://127.0.0.1:8000/api/changes/?item=14" \
-H "Authorization: Token <TOKEN>"
```

**Sample Response:**

```json
{
  "count": 3,
  "results": [
    {"id": 6, "item": 14, "changed_by": "userA", "old_quantity": 10, "new_quantity": 7, "change_type": "sale", "change_date": "2025-08-20T02:01:21Z"},
    {"id": 5, "item": 14, "changed_by": "userA", "old_quantity": 5, "new_quantity": 10, "change_type": "restock", "change_date": "2025-08-20T02:00:54Z"}
  ]
}
```

---

### 5. API-First Approach

* All features are accessible via **RESTful JSON endpoints**.
* No frontend/UI is included in v1.
* Authentication is **token-based** for all user-specific operations.
* Supports easy integration with **frontend frameworks** or mobile apps in the future.

---

### 🔹 Setup Instructions


```bash
# 1. Clone repository:

git clone <repo-url>
cd inventory-management-capstone


# 2. Create virtual environment:

python -m venv .venv
source .venv/bin/activate


# 3. Install dependencies:

pip install -r requirements.txt


# 4. Run migrations:

python manage.py migrate


# 5. Create superuser (optional, for admin):

python manage.py createsuperuser


# 6. Run the server:

python manage.py runserver
```

Test endpoints using curl, Postman, or any API client.

---

### 🔹 Notes

* Users can only manage **their own inventory items**.
* Low stock default threshold is **5**, but can be customized.
* All inventory changes are **auditable** via the `InventoryChangeLog` API.
* All endpoints require Authorization: Token **`<YOUR_AUTH_TOKEN>`** except **`/register/`** and **`/login/`**.

---