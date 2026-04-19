import { useState } from "react";
import api from "../../api/api";
import Spinner from "../common/Spinner";
import Alert from "../common/Alert";

export default function LoginPage({ onLogin }) {
  const [form, setForm]       = useState({ username: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await api.post("/token/", form);
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      const profile = await api.get("/users/profile/");
      onLogin(profile);
    } catch (e) {
      setError(e?.data?.detail || "Credenciales inválidas");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-logo">Task<span>Flow</span></div>
        <p className="login-sub">Gestor de tareas colaborativo</p>
        <div className="login-divider" />
        <Alert type="error" message={error} />
        <form onSubmit={submit}>
          <div className="field">
            <label className="label">Usuario</label>
            <input
              className="input"
              type="text"
              placeholder="tu_usuario"
              value={form.username}
              onChange={e => setForm(f => ({ ...f, username: e.target.value }))}
              required
            />
          </div>
          <div className="field">
            <label className="label">Contraseña</label>
            <input
              className="input"
              type="password"
              placeholder="••••••••"
              value={form.password}
              onChange={e => setForm(f => ({ ...f, password: e.target.value }))}
              required
            />
          </div>
          <button
            className="btn btn-primary"
            style={{ width: "100%", justifyContent: "center" }}
            disabled={loading}
          >
            {loading ? <Spinner /> : "Ingresar"}
          </button>
        </form>
      </div>
    </div>
  );
}