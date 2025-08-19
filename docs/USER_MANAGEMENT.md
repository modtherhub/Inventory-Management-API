# User Management & Item Ownership

## Features

1. **User Registration (CRUD)**
   - Register users with `username`, `email`, and `password`.
   - Validation:
     - `username` and `email` are required.
     - `username` and `email` must be unique.
     - Password must meet minimum requirements.

2. **Authentication**
   - Token-based authentication using DRF `TokenAuthentication`.
   - Only authenticated users can create, update, or delete inventory items.

3. **Item Ownership**
   - Each inventory item is linked to its creator (owner).
   - Users can only view, update, or delete their own items.
   - Ownership is enforced in all API endpoints.

## API Endpoints

- `POST /api/register/` → Register a new user
- `POST /api/login/` → Obtain authentication token
- `GET /api/items/` → List items (only own items)
- `POST /api/items/` → Create item
- `PUT /api/items/{id}/` → Update item
- `PATCH /api/items/{id}/` → Partial update
- `DELETE /api/items/{id}/` → Delete item

## Testing

Use `curl` or Postman to:
1. Register users
2. Obtain token
3. Test CRUD operations with ownership enforcement
