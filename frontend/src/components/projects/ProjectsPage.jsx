import { useState, useEffect } from "react";
import api from "../../api/api";
import Spinner from "../common/Spinner";
import Alert from "../common/Alert";

export default function ProjectsPage({ user, onSelectProject }) {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modal, setModal] = useState(null);
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [form, setForm] = useState({ name: "", description: "", status: "active" });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    try {
      const data = await api.get("/projects/");
      setProjects(Array.isArray(data) ? data : (data?.results || []));
    } catch (e) {
      setError(e?.data?.detail || "Error al cargar proyectos");
    }
    setLoading(false);
  };

  useEffect(() => { load(); }, []);

  const openNew = () => {
    setForm({ name: "", description: "", status: "active" });
    setError("");
    setModal("new");
  };

  const openEdit = (project) => {
    setForm({ name: project.name, description: project.description || "", status: project.status });
    setError("");
    setModal(project);
  };

  const saveProject = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    try {
      if (modal === "new") {
        const created = await api.post("/projects/", form);
        setProjects(p => [created, ...p]);
      } else {
        const updated = await api.patch(`/projects/${modal.id}/`, form);
        setProjects(p => p.map(x => x.id === modal.id ? updated : x));
      }
      setModal(null);
    } catch (e) {
      setError(e?.data?.name?.[0] || e?.data?.detail || "Error al guardar el proyecto");
    }
    setSaving(false);
  };

  const deleteProject = async (id) => {
    try {
      await api.delete(`/projects/${id}/`);
      setProjects(p => p.filter(x => x.id !== id));
      setDeleteConfirm(null);
    } catch (e) {
      setError(e?.data?.detail || "Error al eliminar el proyecto");
      setDeleteConfirm(null);
    }
  };

  const STATUS_LABEL = { active: "Activo", archived: "Archivado", inactive: "Inactivo" };
  const STATUS_COLOR = { active: "#22c55e", archived: "#f59e0b", inactive: "#6b7280" };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Proyectos</h1>
        <button className="btn btn-primary" onClick={openNew}>+ Nuevo proyecto</button>
      </div>

      <div className="page-body">
        {error && <Alert>{error}</Alert>}

        {loading ? (
          <div style={{ textAlign: "center", padding: "48px" }}><Spinner /></div>
        ) : projects.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📁</div>
            <p className="empty-text">No tienes proyectos aún. ¡Crea el primero!</p>
          </div>
        ) : (
          <div className="projects-grid">
            {projects.map(p => (
              <div key={p.id} className="card project-card">
                <div className="project-name">{p.name}</div>
                <p className="project-desc">{p.description || "Sin descripción"}</p>
                <div className="project-meta">
                  <span
                    className="badge"
                    style={{ color: STATUS_COLOR[p.status], background: `${STATUS_COLOR[p.status]}22` }}
                  >
                    {STATUS_LABEL[p.status] || p.status}
                  </span>
                </div>
                <div style={{ display: "flex", gap: "8px", marginTop: "14px" }}>
                  <button className="btn btn-primary btn-sm" onClick={() => onSelectProject(p)}>Abrir</button>
                  <button className="btn btn-ghost btn-sm" onClick={() => openEdit(p)}>Editor</button>
                  <button className="btn btn-danger btn-sm" onClick={() => setDeleteConfirm(p)}>Eliminar</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modal crear / editar */}
      {modal && (
        <div className="overlay" onClick={e => e.target === e.currentTarget && setModal(null)}>
          <div className="modal">
            <h2 className="modal-title">{modal === "new" ? "Nuevo proyecto" : "Editar proyecto"}</h2>
            {error && <Alert>{error}</Alert>}
            <form onSubmit={saveProject}>
              <div className="field">
                <label className="label">Nombre</label>
                <input
                  className="input"
                  value={form.name}
                  onChange={e => setForm({ ...form, name: e.target.value })}
                  autoFocus
                />
              </div>
              <div className="field">
                <label className="label">Descripción</label>
                <textarea
                  className="textarea"
                  value={form.description}
                  onChange={e => setForm({ ...form, description: e.target.value })}
                />
              </div>
              <div className="field">
                <label className="label">Estado</label>
                <select
                  className="select"
                  value={form.status}
                  onChange={e => setForm({ ...form, status: e.target.value })}
                >
                  <option value="active">Activo</option>
                  <option value="archived">Archivado</option>
                  <option value="inactive">Inactivo</option>
                </select>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-ghost" onClick={() => setModal(null)}>Cancelar</button>
                <button type="submit" className="btn btn-primary" disabled={saving}>
                  {saving ? <Spinner /> : "Guardar"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal confirmar eliminación */}
      {deleteConfirm && (
        <div className="overlay" onClick={e => e.target === e.currentTarget && setDeleteConfirm(null)}>
          <div className="modal" style={{ maxWidth: "400px" }}>
            <h2 className="modal-title">¿Eliminar proyecto?</h2>
            <p style={{ fontSize: "13px", color: "var(--muted)", marginBottom: "20px" }}>
              Se eliminará <strong style={{ color: "var(--text)" }}>{deleteConfirm.name}</strong> y todas sus tareas. Esta acción no se puede deshacer.
            </p>
            <div className="modal-footer">
              <button className="btn btn-ghost" onClick={() => setDeleteConfirm(null)}>Cancelar</button>
              <button className="btn btn-danger" onClick={() => deleteProject(deleteConfirm.id)}>Eliminar</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}