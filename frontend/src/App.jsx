import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [authMode, setAuthMode] = useState("login");
  const [form, setForm] = useState({ full_name: "", email: "", password: "" });
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    if (token) {
      loadHistory();
      loadStats();
      loadUsers();
    }
  }, [token]);

  const handleAuth = async (e) => {
    e.preventDefault();

    if (authMode === "login") {
      const body = new URLSearchParams({
        username: form.email,
        password: form.password,
      });

      const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body,
      });

      const data = await response.json();
      if (!response.ok) {
        alert(data.detail || "Login failed");
        return;
      }

      setToken(data.access_token);
      localStorage.setItem("token", data.access_token);
      return;
    }

    const response = await fetch(`${API_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        full_name: form.full_name,
        email: form.email,
        password: form.password,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      alert(data.detail || "Registration failed");
      return;
    }

    alert("Registration successful. Please login.");
    setAuthMode("login");
  };

  const loadHistory = async () => {
    const response = await fetch(`${API_URL}/api/history`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.ok) {
      const data = await response.json();
      setHistory(data);
    }
  };

  const loadStats = async () => {
    try {
      const response = await fetch(`${API_URL}/admin/stats`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (error) {
      console.error("Stats fetch failed", error);
    }
  };

  const loadUsers = async () => {
    try {
      const response = await fetch(`${API_URL}/admin/users`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.ok) {
        const data = await response.json();
        setUsers(data);
      }
    } catch (error) {
      console.error("Users fetch failed", error);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    const response = await fetch(`${API_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    if (!response.ok) {
      alert(data.detail || "Request failed");
      return;
    }

    setChat((prev) => [
      ...prev,
      {
        question: message,
        answer: data.response,
        city: data.city,
      },
    ]);

    setMessage("");
    loadHistory();
  };

  const logout = () => {
    setToken("");
    localStorage.removeItem("token");
    setHistory([]);
    setChat([]);
    setStats(null);
    setUsers([]);
  };

  if (!token) {
    return (
      <div className="auth-page">
        <div className="auth-card">
          <h1>Weather Chat Bot</h1>

          <div className="switch">
            <button
              className={authMode === "login" ? "active" : ""}
              onClick={() => setAuthMode("login")}
            >
              Login
            </button>
            <button
              className={authMode === "register" ? "active" : ""}
              onClick={() => setAuthMode("register")}
            >
              Register
            </button>
          </div>

          <form onSubmit={handleAuth}>
            {authMode === "register" && (
              <input
                type="text"
                placeholder="Full Name"
                value={form.full_name}
                onChange={(e) => setForm({ ...form, full_name: e.target.value })}
              />
            )}
            <input
              type="email"
              placeholder="Email"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
            <input
              type="password"
              placeholder="Password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />
            <button type="submit">
              {authMode === "login" ? "Login" : "Register"}
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <h2>Weather Assistant</h2>
        <button className="logout-btn" onClick={logout}>
          Logout
        </button>
      </header>

      <div className="stats-grid">
        <div className="stat-box">
          <label>Total Users</label>
          <strong>{stats?.total_users ?? 0}</strong>
        </div>
        <div className="stat-box">
          <label>Total Messages</label>
          <strong>{stats?.total_messages ?? 0}</strong>
        </div>
        <div className="stat-box">
          <label>Unique Cities</label>
          <strong>{stats?.cities_queried ?? 0}</strong>
        </div>
        <div className="stat-box">
          <label>Avg Temp</label>
          <strong>{stats?.avg_temperature?.toFixed(1) ?? "0.0"}°C</strong>
        </div>
      </div>

      <div className="admin-box">
        <h3>Admin Users</h3>
        <ul>
          {users.map((user) => (
            <li key={user.id}>
              {user.full_name} — {user.email} — {user.is_admin ? "Admin" : "User"}
            </li>
          ))}
        </ul>
      </div>

      <div className="chat-box">
        {[...chat, ...history].map((msg, index) => (
          <div key={index} className="message-pair">
            <div className="message user">
              <strong>You:</strong> {msg.question || "Weather Query"}
            </div>
            <div className="message bot">
              <strong>Bot:</strong> {msg.answer || "No answer"}
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={sendMessage} className="chat-form">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask like: Weather in Lahore"
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default App;
