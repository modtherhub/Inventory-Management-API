
---

# Inventory Management Frontend

A **vanilla JavaScript frontend** that interacts with the **Inventory Management API** built using Django REST Framework.
This frontend handles **user authentication, inventory CRUD operations, and stock history visualization**, all via API calls.

---

## 🔹 Features

### 1. Authentication (Register, Login, Logout)

* **Register:** Create a new account with `username`, `email`, and `password`.
* **Login:** Authenticate and store token in `localStorage`.
* **Logout:** Remove token and redirect to login page.
* CSRF protection is handled automatically using cookies.

**Key Functions:**

```javascript
function getToken() { return localStorage.getItem("token"); }
function setToken(token) { localStorage.setItem("token", token); }
function clearToken() { localStorage.removeItem("token"); }
function getCSRFToken() { /* extracts csrftoken from cookies */ }
```

---

### 2. User Registration

* Submits `username`, `email`, `password` to `/api/register/`.
* Displays a success or error message on the page.
* Redirects to login page on success.

**Example (Frontend Form Submission):**

```javascript
fetch(`${API_URL}/register/`, {
  method: "POST",
  headers: {"Content-Type":"application/json", "X-CSRFToken": getCSRFToken()},
  body: JSON.stringify({username, email, password})
});
```

---

### 3. User Login

* Submits `username` and `password` to `/api/login/`.
* If successful, stores the `token` in `localStorage` and redirects to `/dashboard/`.
* If failed, displays error message in the UI.

**Example (Frontend):**

```javascript
fetch(`${API_URL}/login/`, {
  method: "POST",
  headers: {"Content-Type":"application/json", "X-CSRFToken": getCSRFToken()},
  body: JSON.stringify({username, password})
});
```

---

### 4. User Logout

* Calls `/api/logout/` with `Authorization` header.
* Clears local token and redirects to `/login/`.

**Example:**

```javascript
fetch(`${API_URL}/logout/`, {
  method: "POST",
  headers: { "Authorization": `Token ${getToken()}`, "X-CSRFToken": getCSRFToken() }
});
```

---

### 5. Dashboard: Load Items

* Fetches items from `/api/items/` and renders them in an HTML table.
* Shows **name, description, quantity, price, category**, with action buttons:

  * **Edit**
  * **Delete**
  * **History**

**Example:**

```javascript
const res = await fetch(`${API_URL}/items/`, {
  headers: { "Authorization": `Token ${getToken()}` }
});
const items = data.results || data;
```

---

### 6. CRUD Operations (Items)

* **Create Item:** Submit form without ID → POST `/api/items/`.
* **Update Item:** Submit form with ID → PUT `/api/items/<id>/`.
* **Delete Item:** Confirmation prompt → DELETE `/api/items/<id>/`.

**Example (Create/Update):**

```javascript
fetch(url, {
  method: id ? "PUT" : "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Token ${getToken()}`,
    "X-CSRFToken": getCSRFToken()
  },
  body: JSON.stringify(data)
});
```

---

### 7. View Change History

* Fetches changes for a specific item from `/api/changes/?item=<id>`.
* Displays old vs new quantity, change type, and date in the dashboard.

**Example:**

```javascript
fetch(`${API_URL}/changes/?item=${itemId}`, {
  headers: { "Authorization": `Token ${getToken()}` }
});
```

**Rendered Result in Dashboard:**

```
2025-08-20T02:01:21Z: sale | Old: 10 | New: 7
2025-08-20T02:00:54Z: restock | Old: 5 | New: 10
```
---

## 🔹 Notes

* Authentication uses **DRF TokenAuth** (stored in `localStorage`).
* CSRF token required for POST/PUT/DELETE (handled via `getCSRFToken()`).
* Users can only manage **their own items**.
* Change history is fully auditable per item.

---

