---

## Feature 4: Inventory Change History API

The **Inventory Change History API** allows authenticated users to track all modifications made to their inventory items. Every change is logged with timestamps, user info, and quantity details.

Each user can only access the change history for items they own.

---

### 🔹 Endpoints

* `GET /api/changes/` → Retrieves all change logs for the authenticated user.
* `GET /api/changes/?item=<item_id>` → Retrieves the change history for a specific inventory item.

---

### 🔹 Change Types

* **Restock** → Quantity added to an item.
* **Sale** → Quantity removed from an item.
* **Adjustment** → Manual change without affecting stock movement.

---

### 🔹 Example Requests

#### 1. Retrieve all changes

```bash
curl -X GET "http://127.0.0.1:8000/api/changes/" \
-H "Authorization: Token YOUR_AUTH_TOKEN"
```

#### 2. Retrieve changes for a specific item

```bash
curl -X GET "http://127.0.0.1:8000/api/changes/?item=14" \
-H "Authorization: Token YOUR_AUTH_TOKEN"
```

---

### 🔹 Example Response

```json
{
  "count": 3,
  "results": [
    {
      "id": 6,
      "item": 14,
      "changed_by": "moibhub",
      "old_quantity": 10,
      "new_quantity": 7,
      "change_type": "sale",
      "change_date": "2025-08-20T02:01:21Z"
    },
    {
      "id": 5,
      "item": 14,
      "changed_by": "moibhub",
      "old_quantity": 5,
      "new_quantity": 10,
      "change_type": "restock",
      "change_date": "2025-08-20T02:00:54Z"
    },
    {
      "id": 4,
      "item": 14,
      "changed_by": "moibhub",
      "old_quantity": 0,
      "new_quantity": 5,
      "change_type": "restock",
      "change_date": "2025-08-20T01:59:33Z"
    }
  ]
}
```

---

### 🔹 Notes

* All logs include the user who performed the change (`changed_by`), the old and new quantities, and the timestamp.
* Users cannot see changes for items they do not own.
* Useful for auditing, stock management, and tracking inventory movement over time.

---
