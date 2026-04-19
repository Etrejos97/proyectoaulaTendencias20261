export default function Sidebar({ user, activePage, onNav, onLogout }) {
  const items = [
    { id: "projects", icon: "📂", label: "Proyectos" },
    { id: "profile",  icon: "👤", label: "Mi perfil" },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">Gestor<span>.</span></div>
      <div className="sidebar-section">Menú</div>
      {items.map(it => (
        <div
          key={it.id}
          className={`sidebar-item ${activePage === it.id ? "active" : ""}`}
          onClick={() => onNav(it.id)}
        >
          <span className="icon">{it.icon}</span>
          <span>{it.label}</span>
        </div>
      ))}
      <div className="sidebar-bottom">
        <div className="user-chip">
          <div className="avatar">{(user.username || "?")[0].toUpperCase()}</div>
          <div style={{ overflow: "hidden" }}>
            <div className="user-name">{user.username}</div>
            <div className="user-role">{user.role || "member"}</div>
          </div>
        </div>
        <button className="btn btn-ghost" onClick={onLogout}>
          Cerrar sesión
        </button>
      </div>
    </aside>
  );
}