import { useState, useEffect } from "react";
import api from "../../api/api";
import { STATUS_COLS, PRIORITY_MAP } from "../../constants/taskConstants";
import TagInput from "../common/TagInput";
import Spinner from "../common/Spinner";
import Alert from "../common/Alert";
import {
  getComments,
  createComment,
  updateComment,
  deleteComment,
} from "../../api/api";

export default function KanbanBoard({ project, user, onBack }) {
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [taskModal, setTaskModal] = useState(null);
  const [membersOpen, setMembersOpen] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [error, setError] = useState("");
  const [form, setForm] = useState({});
  const [saving, setSaving] = useState(false);
  const [formError, setFormError] = useState("");

  // ── Estados comentarios ──
  const [comments, setComments] = useState([]);
  const [commentsLoading, setCommentsLoading] = useState(false);
  const [newComment, setNewComment] = useState("");
  const [commentSubmitting, setCommentSubmitting] = useState(false);
  const [editingCommentId, setEditingCommentId] = useState(null);
  const [editCommentContent, setEditCommentContent] = useState("");
  const [commentError, setCommentError] = useState("");

  useEffect(() => {
    let cancelled = false;
    const fetchData = async () => {
      setLoading(true);
      setError("");
      try {
        const usersEndpoint = user?.is_admin ? "/users/" : "/users/profile/";
        const [t, u] = await Promise.allSettled([
          api.get(`/tasks/?project=${project.id}`),
          api.get(usersEndpoint),
        ]);
        if (cancelled) return;
        const tareas = t.status === "fulfilled"
          ? Array.isArray(t.value) ? t.value : (t.value?.results ?? [])
          : [];
        const miembros = u.status === "fulfilled"
          ? Array.isArray(u.value)
            ? u.value
            : u.value?.results
              ? u.value.results
              : u.value?.id
                ? [u.value]
                : []
          : [];
        setTasks(tareas);
        setUsers(miembros);
      } catch (e) {
        if (!cancelled) setError(e?.data?.detail || "Error al cargar tareas");
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    fetchData();
    return () => { cancelled = true; };
  }, [project.id, user?.is_admin]);

  const buildForm = (task, defaultStatus) =>
    task
      ? {
          title: task.title,
          description: task.description || "",
          priority: task.priority,
          status: task.status,
          due_date: task.due_date ? task.due_date.slice(0, 16) : "",
          assigned_to: task.assigned_to || "",
          tags: task.tags || [],
        }
      : {
          title: "",
          description: "",
          priority: "medium",
          status: defaultStatus || "pending",
          due_date: "",
          assigned_to: "",
          tags: [],
        };

  const openTaskModal = (task, defaultStatus) => {
    setForm(buildForm(task, defaultStatus));
    setFormError("");
    setTaskModal({ task, defaultStatus });
    // reset comentarios
    setComments([]);
    setNewComment("");
    setEditingCommentId(null);
    setEditCommentContent("");
    setCommentError("");
    if (task) loadComments(task.id);
  };

  const saveTask = async (e) => {
    e.preventDefault();
    if (!form.title?.trim()) return setFormError("El título es obligatorio.");
    setSaving(true);
    setFormError("");
    const payload = {
      ...form,
      project: project.id,
      due_date: form.due_date || null,
      assigned_to: form.assigned_to || null,
      tags: (form.tags || []).map(t => typeof t === "string" ? t : t.name),
    };
    try {
      if (taskModal.task) {
        const updated = await api.patch(`/tasks/${taskModal.task.id}/`, payload);
        setTasks(t => t.map(x => x.id === updated.id ? updated : x));
      } else {
        const created = await api.post("/tasks/", payload);
        setTasks(t => [...t, created]);
      }
      setTaskModal(null);
    } catch (e) {
      setFormError(
        e?.data?.detail ||
        e?.data?.title?.[0] ||
        e?.data?.status?.[0] ||
        "Error al guardar la tarea."
      );
    }
    setSaving(false);
  };

  const deleteTask = async (id) => {
    try {
      await api.delete(`/tasks/${id}/`);
      setTasks(t => t.filter(x => x.id !== id));
      setDeleteConfirm(null);
    } catch (e) {
      setError(e?.data?.detail || "Error al eliminar la tarea");
      setDeleteConfirm(null);
    }
  };

  const moveTask = async (task, newStatus) => {
    try {
      await api.patch(`/tasks/${task.id}/`, { status: newStatus });
      setTasks(t => t.map(x => x.id === task.id ? { ...x, status: newStatus } : x));
    } catch (e) {
      setError(e?.data?.detail || "Error al mover la tarea");
    }
  };

  const getUserName = (id) => users.find(u => u.id === id)?.username || "";

  // ── Funciones comentarios ──
  const loadComments = async (taskId) => {
    setCommentsLoading(true);
    setCommentError("");
    try {
      const data = await getComments(taskId);
      setComments(Array.isArray(data) ? data : data?.results ?? []);
    } catch {
      setCommentError("No se pudieron cargar los comentarios.");
    } finally {
      setCommentsLoading(false);
    }
  };

  const handleAddComment = async () => {
    const trimmed = newComment.trim();
    if (!trimmed || !taskModal?.task) return;
    setCommentSubmitting(true);
    setCommentError("");
    try {
      const created = await createComment(taskModal.task.id, trimmed);
      setComments(prev => [...prev, created]);
      setNewComment("");
    } catch {
      setCommentError("No se pudo agregar el comentario.");
    } finally {
      setCommentSubmitting(false);
    }
  };

  const handleUpdateComment = async (commentId) => {
    const trimmed = editCommentContent.trim();
    if (!trimmed) return;
    setCommentError("");
    try {
      const updated = await updateComment(commentId, trimmed);
      setComments(prev => prev.map(c => c.id === commentId ? updated : c));
      setEditingCommentId(null);
    } catch {
      setCommentError("No se pudo editar el comentario.");
    }
  };

  const handleDeleteComment = async (commentId) => {
    if (!window.confirm("¿Eliminar este comentario?")) return;
    setCommentError("");
    try {
      await deleteComment(commentId);
      setComments(prev => prev.filter(c => c.id !== commentId));
    } catch {
      setCommentError("No se pudo eliminar el comentario.");
    }
  };

  return (
    <div>
      {/* Header */}
      <div className="page-header">
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <button className="btn btn-ghost btn-sm" onClick={onBack}>← Volver</button>
          <h1 className="page-title">{project.name}</h1>
        </div>
        <div style={{ display: "flex", gap: "8px" }}>
          <button className="btn btn-ghost" onClick={() => setMembersOpen(true)}>
            👥 Miembros
          </button>
          <button className="btn btn-primary" onClick={() => openTaskModal(null, "pending")}>
            + Nueva tarea
          </button>
        </div>
      </div>

      {/* Board */}
      <div className="page-body">
        {error && <Alert>{error}</Alert>}
        {loading ? (
          <div style={{ textAlign: "center", padding: "48px" }}><Spinner /></div>
        ) : (
          <div className="kanban-board">
            {STATUS_COLS.map((col) => {
              const colTasks = tasks.filter(t => t.status === col.value);
              return (
                <div key={col.value} className="kanban-col">
                  <div className="kanban-col-header">
                    <span className="kanban-col-title">{col.label}</span>
                    <span className="kanban-col-count">{colTasks.length}</span>
                  </div>
                  <div className="kanban-col-body">
                    {colTasks.length === 0 ? (
                      <div className="kanban-empty">Sin tareas</div>
                    ) : (
                      colTasks.map(task => (
                        <div key={task.id} className="task-card">
                          <div className="task-title">{task.title}</div>
                          {task.description && (
                            <div className="task-desc">{task.description}</div>
                          )}
                          <div className="task-meta">
                            <span
                              className="badge"
                              style={{
                                color: PRIORITY_MAP[task.priority]?.color,
                                background: `${PRIORITY_MAP[task.priority]?.color}22`,
                              }}
                            >
                              {PRIORITY_MAP[task.priority]?.label || task.priority}
                            </span>
                            {task.assigned_to && (
                              <span className="task-assignee">
                                👤 {getUserName(task.assigned_to)}
                              </span>
                            )}
                          </div>
                          {task.tags?.length > 0 && (
                            <div className="task-tags">
                              {task.tags.map((tag, i) => {
                                const label = typeof tag === "string" ? tag : tag.name;
                                const key = typeof tag === "string" ? tag : (tag.id ?? i);
                                return <span key={key} className="tag">{label}</span>;
                              })}
                            </div>
                          )}
                          <div className="task-actions">
                            <button
                              className="btn btn-ghost btn-xs"
                              onClick={() => openTaskModal(task, task.status)}
                            >
                              Editar
                            </button>
                            <button
                              className="btn btn-danger btn-xs"
                              onClick={() => setDeleteConfirm(task)}
                            >
                              Eliminar
                            </button>
                            {STATUS_COLS.filter(s => s.value !== task.status).map(s => (
                              <button
                                key={`${task.id}-move-${s.value}`}
                                className="btn btn-ghost btn-xs"
                                onClick={() => moveTask(task, s.value)}
                              >
                                → {s.label}
                              </button>
                            ))}
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Modal crear / editar tarea */}
      {taskModal && (
        <div className="overlay" onClick={e => e.target === e.currentTarget && setTaskModal(null)}>
          <div className="modal">
            <h2 className="modal-title">
              {taskModal.task ? "Editar tarea" : "Nueva tarea"}
            </h2>
            {formError && <Alert>{formError}</Alert>}
            <form onSubmit={saveTask}>
              <div className="field">
                <label className="label">Título</label>
                <input
                  className="input"
                  value={form.title || ""}
                  onChange={e => setForm({ ...form, title: e.target.value })}
                  autoFocus
                />
              </div>
              <div className="field">
                <label className="label">Descripción</label>
                <textarea
                  className="textarea"
                  value={form.description || ""}
                  onChange={e => setForm({ ...form, description: e.target.value })}
                />
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
                <div className="field">
                  <label className="label">Prioridad</label>
                  <select
                    className="select"
                    value={form.priority || "medium"}
                    onChange={e => setForm({ ...form, priority: e.target.value })}
                  >
                    {Object.entries(PRIORITY_MAP).map(([val, { label }]) => (
                      <option key={val} value={val}>{label}</option>
                    ))}
                  </select>
                </div>
                <div className="field">
                  <label className="label">Estado</label>
                  <select
                    className="select"
                    value={form.status || "pending"}
                    onChange={e => setForm({ ...form, status: e.target.value })}
                  >
                    {STATUS_COLS.map(s => (
                      <option key={s.value} value={s.value}>{s.label}</option>
                    ))}
                  </select>
                </div>
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
                <div className="field">
                  <label className="label">Fecha límite</label>
                  <input
                    className="input"
                    type="datetime-local"
                    value={form.due_date || ""}
                    onChange={e => setForm({ ...form, due_date: e.target.value })}
                  />
                </div>
                <div className="field">
                  <label className="label">Asignar a</label>
                  <select
                    className="select"
                    value={form.assigned_to || ""}
                    onChange={e => setForm({ ...form, assigned_to: e.target.value })}
                  >
                    <option value="">Sin asignar</option>
                    {users.map(u => (
                      <option key={u.id} value={u.id}>{u.username}</option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="field">
                <label className="label">Etiquetas</label>
                <TagInput
                  value={form.tags || []}
                  onChange={tags => setForm({ ...form, tags })}
                />
              </div>

              {/* ── Sección comentarios: solo al editar tarea existente ── */}
              {taskModal.task && (
                <div className="field" style={{ borderTop: "1px solid #e2e8f0", paddingTop: "12px", marginTop: "4px" }}>
                  <label className="label">Comentarios ({comments.length})</label>
                  {commentError && (
                    <p style={{ color: "#e53e3e", fontSize: "12px", marginBottom: "6px" }}>
                      {commentError}
                    </p>
                  )}
                  {commentsLoading ? (
                    <Spinner />
                  ) : comments.length === 0 ? (
                    <p style={{ fontSize: "12px", color: "gray", marginBottom: "8px" }}>
                      No hay comentarios aún.
                    </p>
                  ) : (
                    <ul style={{ listStyle: "none", padding: 0, margin: "0 0 12px 0", display: "flex", flexDirection: "column", gap: "8px" }}>
                      {comments.map(c => {
                        const isOwner = c.author === user?.id;
                        return (
                          <li key={c.id} style={{ background: "#f7fafc", border: "1px solid #e2e8f0", borderRadius: "6px", padding: "8px 10px" }}>
                            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                              <span style={{ fontWeight: 600, fontSize: "12px" }}>{c.author_username}</span>
                              <span style={{ fontSize: "11px", color: "gray" }}>
                                {new Date(c.created_at).toLocaleString("es-CO")}
                                {c.updated_at !== c.created_at && <em> · editado</em>}
                              </span>
                            </div>
                            {editingCommentId === c.id ? (
                              <div>
                                <textarea
                                  className="textarea"
                                  rows={2}
                                  value={editCommentContent}
                                  onChange={e => setEditCommentContent(e.target.value)}
                                  style={{ marginBottom: "6px" }}
                                />
                                <div style={{ display: "flex", gap: "6px" }}>
                                  <button type="button" className="btn btn-primary btn-xs" onClick={() => handleUpdateComment(c.id)}>Guardar</button>
                                  <button type="button" className="btn btn-ghost btn-xs" onClick={() => setEditingCommentId(null)}>Cancelar</button>
                                </div>
                              </div>
                            ) : (
                              <p style={{ fontSize: "13px", margin: "0 0 4px 0", whiteSpace: "pre-wrap" }}>{c.content}</p>
                            )}
                            {isOwner && editingCommentId !== c.id && (
                              <div style={{ display: "flex", gap: "6px", marginTop: "4px" }}>
                                <button type="button" className="btn btn-ghost btn-xs" onClick={() => { setEditingCommentId(c.id); setEditCommentContent(c.content); }}>Editar</button>
                                <button type="button" className="btn btn-danger btn-xs" onClick={() => handleDeleteComment(c.id)}>Eliminar</button>
                              </div>
                            )}
                          </li>
                        );
                      })}
                    </ul>
                  )}
                  <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
                    <textarea
                      className="textarea"
                      rows={2}
                      placeholder="Escribe un comentario…"
                      value={newComment}
                      onChange={e => setNewComment(e.target.value)}
                      disabled={commentSubmitting}
                    />
                    <button
                      type="button"
                      className="btn btn-primary btn-sm"
                      onClick={handleAddComment}
                      disabled={commentSubmitting || !newComment.trim()}
                      style={{ alignSelf: "flex-end" }}
                    >
                      {commentSubmitting ? <Spinner /> : "Comentar"}
                    </button>
                  </div>
                </div>
              )}
              {/* ── fin comentarios ── */}

              <div className="modal-footer">
                <button type="button" className="btn btn-ghost" onClick={() => setTaskModal(null)}>Cancelar</button>
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
            <h2 className="modal-title">¿Eliminar tarea?</h2>
            <p style={{ fontSize: "13px", color: "var(--muted)", marginBottom: "20px" }}>
              Esta acción no se puede deshacer. Tarea:{" "}
              <strong style={{ color: "var(--text)" }}>{deleteConfirm.title}</strong>
            </p>
            <div className="modal-footer">
              <button className="btn btn-ghost" onClick={() => setDeleteConfirm(null)}>Cancelar</button>
              <button className="btn btn-danger" onClick={() => deleteTask(deleteConfirm.id)}>Eliminar</button>
            </div>
          </div>
        </div>
      )}

      {/* Modal miembros */}
      {membersOpen && (
        <div className="overlay" onClick={e => e.target === e.currentTarget && setMembersOpen(false)}>
          <div className="modal" style={{ maxWidth: "400px" }}>
            <h2 className="modal-title">Miembros del proyecto</h2>
            {users.length === 0 ? (
              <p style={{ fontSize: "13px", color: "var(--muted)" }}>No hay miembros registrados.</p>
            ) : (
              <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: "8px" }}>
                {users.map(u => (
                  <li key={u.id} style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                    <div className="avatar-sm">{u.username[0].toUpperCase()}</div>
                    <div>
                      <div style={{ fontWeight: 500, fontSize: "13px" }}>{u.username}</div>
                      <div style={{ fontSize: "12px", color: "var(--muted)" }}>{u.role || u.email || ""}</div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
            <div className="modal-footer">
              <button className="btn btn-ghost" onClick={() => setMembersOpen(false)}>Cerrar</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}