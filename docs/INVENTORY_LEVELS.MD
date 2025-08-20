
---

## Feature 3: Inventory Levels API

The **Inventory Levels API** provides authenticated users with an endpoint to monitor and filter their inventory items efficiently. Each user only has access to their own items.

---

### 🔹 Endpoint

* `GET /api/inventory-levels/` → Returns the authenticated user’s inventory with quantities and details.

---

### 🔹 Filtering Options

#### 1. **Category Filter**

Retrieve items belonging to a specific category.

```bash
GET /api/inventory-levels/?category=electronics
```

#### 2. **Price Range Filter**

Filter items within a price range using `min_price` and `max_price`.

```bash
GET /api/inventory-levels/?min_price=100&max_price=500
```

#### 3. **Low Stock Filter**

Identify items with low stock using `low_stock`.

* Default threshold: `5` (if no value is provided).
* Custom threshold: pass a number (e.g., `?low_stock=10`).

```bash
# Default low stock (≤ 5)
GET /api/inventory-levels/?low_stock=true  

# Custom threshold (≤ 10)
GET /api/inventory-levels/?low_stock=10
```

---

### 🔹 Search Functionality

Search items by `name`, `description`, or `category`.

```bash
GET /api/inventory-levels/?search=laptop
```

---

### 🔹 Ordering

Sort results by specific fields:

* By price:

  * Ascending → `?ordering=price`
  * Descending → `?ordering=-price`
* By quantity: `?ordering=quantity`
* By last updated: `?ordering=-last_updated`

```bash
# Most recent items first
GET /api/inventory-levels/?ordering=-last_updated
```

---

### 🔹 Example Combined Query

```bash
# Get low-stock electronics under $500, ordered by quantity
curl -X GET "http://127.0.0.1:8000/api/inventory-levels/?category=electronics&max_price=500&low_stock=5&ordering=quantity" \
-H "Authorization: Token YOUR_AUTH_TOKEN"
```

---
