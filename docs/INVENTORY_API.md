
---

### Inventory API Documentation

#### 1. Overview

This feature implements the **Inventory Item Management** API with full CRUD functionality and ownership controls.

#### 2. Endpoints

| HTTP Method | Endpoint           | Description                                        | Auth Required |
| ----------- | ------------------ | -------------------------------------------------- | ------------- |
| GET         | `/api/items/`      | List all inventory items of the authenticated user | Yes (Token)   |
| GET         | `/api/items/<id>/` | Retrieve a single inventory item                   | Yes (Token)   |
| POST        | `/api/items/`      | Create a new inventory item                        | Yes (Token)   |
| PUT         | `/api/items/<id>/` | Update an existing inventory item completely       | Yes (Token)   |
| PATCH       | `/api/items/<id>/` | Partially update an existing inventory item        | Yes (Token)   |
| DELETE      | `/api/items/<id>/` | Delete an inventory item                           | Yes (Token)   |

#### 3. Request & Response Example

**Create Item (POST /api/items/):**

```json
{
  "name": "Laptop",
  "description": "Dell XPS 13",
  "quantity": 10,
  "price": 1500.50,
  "category": "Electronics"
}
```

**Response:**

```json
{
  "id": 1,
  "name": "Laptop",
  "description": "Dell XPS 13",
  "quantity": 10,
  "price": "1500.50",
  "category": "Electronics",
  "date_added": "2025-08-19T01:45:06.997710Z",
  "last_updated": "2025-08-19T01:45:06.997766Z",
  "owner": "moibhub"
}
```

#### 4. Validations

* `name` cannot be empty.
* `quantity` must be >= 0.
* `price` must be >= 0.

#### 5. Ownership

* Each user can **only manage their own items**.
* `owner` field is automatically set to the authenticated user.

#### 6. Authentication

* Token-based authentication (DRF `TokenAuthentication`) is required for all endpoints.

#### 7. Notes

* CRUD operations tested with `curl` and DRF web interface.
* Superuser can view all items in the Django admin panel.

---

