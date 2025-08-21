const API_URL = "http://127.0.0.1:8000/api";

function getCSRFToken() {
  const name = "csrftoken";
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Utility
function getToken() { return localStorage.getItem("token"); }
function setToken(token) { localStorage.setItem("token", token); }
function clearToken() { localStorage.removeItem("token"); }

// ------------------ Register ------------------
const registerForm = document.getElementById("register-form");
if (registerForm) {
  registerForm.addEventListener("submit", async e => {
    e.preventDefault();
    const data = {
      username: document.getElementById("username").value,
      email: document.getElementById("email").value,
      password: document.getElementById("password").value
    };
    const res = await fetch(`${API_URL}/register/`, {
      method: "POST",
      headers: {"Content-Type":"application/json",
        "X-CSRFToken": getCSRFToken()
      },
      body: JSON.stringify(data)
    });
    const result = await res.json();
    document.getElementById("message").innerText = res.ok ? "Registered! Redirecting..." : JSON.stringify(result);
    if (res.ok) setTimeout(() => window.location.href = "/login", 1000);
  });
}

// ------------------ Login ------------------
const loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.addEventListener("submit", async e => {
    e.preventDefault();
    const data = {
      username: document.getElementById("username").value,
      password: document.getElementById("password").value
    };
    const res = await fetch(`${API_URL}/login/`, {
      method: "POST",
      headers: {"Content-Type":"application/json",
        "X-CSRFToken": getCSRFToken()
      },
      body: JSON.stringify(data)
    });
    const result = await res.json();
    if (res.ok) {
      setToken(result.token);
      window.location.href = "/dashboard/";
    } else {
      document.getElementById("message").innerText = result.error;
    }
  });
}

// ------------------ Logout ------------------
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", async () => {
    const res = await fetch(`${API_URL}/logout/`, {
      method: "POST",
      headers: { "Authorization": `Token ${getToken()}`,
        "X-CSRFToken": getCSRFToken()
      }
    });
    clearToken();
    window.location.href = "/login/";
  });
}

// ------------------ Dashboard ------------------
async function loadItems() {
  const tableBody = document.querySelector("#items-table tbody");
  if (!tableBody) return;

  const res = await fetch(`${API_URL}/items/`, {
    headers: { "Authorization": `Token ${getToken()}` }
  });
  const data = await res.json();
  console.log("Items from API:", data); // idat0ocz

  tableBody.innerHTML = "";

  const items = data.results || data;

  items.forEach(item => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${item.name}</td>
      <td>${item.description}</td>
      <td>${item.quantity}</td>
      <td>${item.price}</td>
      <td>${item.category}</td>
      <td>
        <button onclick="editItem(${item.id})">Edit</button>
        <button onclick="deleteItem(${item.id})">Delete</button>
        <button onclick="viewHistory(${item.id})">History</button>
      </td>
    `;
    tableBody.appendChild(row);
  });
}


// Load items on dashboard
if (document.querySelector("#items-table")) loadItems();

// ------------------ CRUD ------------------
const itemForm = document.getElementById("item-form");
if (itemForm) {
  itemForm.addEventListener("submit", async e => {
    e.preventDefault();
    const id = document.getElementById("item-id").value;
    const data = {
      name: document.getElementById("name").value,
      description: document.getElementById("description").value,
      quantity: parseInt(document.getElementById("quantity").value),
      price: parseFloat(document.getElementById("price").value),
      category: document.getElementById("category").value
    };
    const method = id ? "PUT" : "POST";
    const url = id ? `${API_URL}/items/${id}/` : `${API_URL}/items/`;
    const res = await fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Token ${getToken()}`,
        "X-CSRFToken": getCSRFToken()
      },
      body: JSON.stringify(data)
    });
    if (res.ok) {
      document.getElementById("item-id").value = "";
      itemForm.reset();
      loadItems();
    } else {
      alert("Error: " + JSON.stringify(await res.json()));
    }
  });
}

async function editItem(id) {
  const res = await fetch(`${API_URL}/items/${id}/`, {
    headers: { "Authorization": `Token ${getToken()}` }
  });
  const item = await res.json();
  document.getElementById("item-id").value = item.id;
  document.getElementById("name").value = item.name;
  document.getElementById("description").value = item.description;
  document.getElementById("quantity").value = item.quantity;
  document.getElementById("price").value = item.price;
  document.getElementById("category").value = item.category;
}

async function deleteItem(id) {
  if (!confirm("Are you sure?")) return;
  await fetch(`${API_URL}/items/${id}/`, {
    method: "DELETE",
    headers: { "Authorization": `Token ${getToken()}`,
        "X-CSRFToken": getCSRFToken()
      }
  });
  loadItems();
}

// ------------------ History ------------------
async function viewHistory(itemId) {
  const res = await fetch(`${API_URL}/changes/?item=${itemId}`, {
    headers: { "Authorization": `Token ${getToken()}` }
  });
  const data = await res.json();
  const historyDiv = document.getElementById("history");
  historyDiv.innerHTML = `<h3>History for item ${itemId}</h3>`;
  data.results.forEach(change => {
    historyDiv.innerHTML += `
      <p>${change.change_date}: ${change.change_type} | Old: ${change.old_quantity} | New: ${change.new_quantity}</p>
    `;
  });
}