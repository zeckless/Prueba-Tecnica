import { useEffect, useMemo, useState } from "react";
import "./biblioteca.css";

const API_BASE = "http://127.0.0.1:8000/api";

const nivelLabels = {
  basica: "Básica",
  media: "Media",
  universitario: "Universitario",
  transversal: "Todos",
};

function adaptPrompt(item) {
  return {
    id: item.id,
    title: item.titulo,
    summary: item.descripcion,
    prompt: item.contenido,
    subject: item.asignatura,
    level: item.nivel,
    author: item.autor,
    status: item.estado,
    likes: item.likes,
    tags: item.tags_lista || [],
    categoria: item.categoria,
    categoriaNombre: item.categoria_nombre,
    totalComentarios: item.total_comentarios ?? 0,
    creadoEn: item.creado_en,
  };
}

function PromptCard({ item, onVote }) {
  const [voted, setVoted] = useState(false);
  const fecha = item.creadoEn ? new Date(item.creadoEn).toISOString().slice(0, 10) : "";
  return (
    <article className="prompt-card-row">
      <div className="card-row-top">
        <div className="chip-row">
          {item.categoriaNombre && <span className="chip">{item.categoriaNombre}</span>}
          <span className="chip">{nivelLabels[item.level] || item.level}</span>
          {item.status === "destacado" && <span className="chip">Destacado</span>}
        </div>
        <button
          type="button"
          className={`like-btn ${voted ? "voted" : ""}`}
          onClick={() => {
            if (voted) return;
            setVoted(true);
            onVote();
          }}
        >
          Votar ({item.likes})
        </button>
      </div>
      <h3>{item.title}</h3>
      <p>{item.summary}</p>
      <p className="card-meta">
        Por {item.author}{fecha ? ` · ${fecha}` : ""}
      </p>
      <details className="card-expand">
        <summary>Ver prompt completo</summary>
        <blockquote>{item.prompt}</blockquote>
        {item.tags.length > 0 && (
          <div className="tag-row">{item.tags.map((t) => <span key={t}>{t}</span>)}</div>
        )}
      </details>
      <details className="card-expand">
        <summary>Comentarios ({item.totalComentarios})</summary>
        <p className="card-meta">Sin comentarios todavía.</p>
      </details>
    </article>
  );
}

export default function Biblioteca() {
  const [prompts, setPrompts] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [query, setQuery] = useState("");
  const [categoriaFiltro, setCategoriaFiltro] = useState("");
  const [nivelFiltro, setNivelFiltro] = useState("");
  const [orden, setOrden] = useState("likes");
  const [notice, setNotice] = useState("");

  useEffect(() => {
    async function load() {
      const [pRes, cRes] = await Promise.all([
        fetch(`${API_BASE}/biblioteca/prompts/`),
        fetch(`${API_BASE}/biblioteca/categorias/`),
      ]);
      setPrompts((await pRes.json()).results.map(adaptPrompt));
      setCategorias(await cRes.json());
    }
    load().catch(() => setNotice("No se pudo conectar con la API."));
  }, []);

  const filtrados = useMemo(() => {
    const out = prompts.filter((item) => {
      const text = `${item.title} ${item.summary} ${item.subject} ${item.tags.join(" ")}`.toLowerCase();
      const matchesQuery = text.includes(query.toLowerCase());
      const matchesCategoria = categoriaFiltro ? String(item.categoria) === categoriaFiltro : true;
      const matchesNivel = nivelFiltro ? item.level === nivelFiltro : true;
      return matchesQuery && matchesCategoria && matchesNivel;
    });
    return out.sort((a, b) => {
      if (orden === "likes") return b.likes - a.likes;
      return new Date(b.creadoEn) - new Date(a.creadoEn);
    });
  }, [prompts, query, categoriaFiltro, nivelFiltro, orden]);

  async function votar(id) {
    const r = await fetch(`${API_BASE}/biblioteca/prompts/${id}/votar/`, { method: "POST" });
    if (!r.ok) return;
    const data = await r.json();
    setPrompts((curr) =>
      curr.map((p) => (p.id === id ? { ...p, likes: data.likes, status: data.estado } : p))
    );
  }

  async function submit(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const payload = {
      titulo: form.get("title"),
      autor: form.get("author"),
      asignatura: form.get("subject"),
      nivel: form.get("level"),
      descripcion: form.get("summary"),
      contenido: form.get("prompt"),
      tags: String(form.get("tags") || ""),
      categoria: Number(form.get("categoria")) || 1,
    };
    const r = await fetch(`${API_BASE}/biblioteca/prompts/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!r.ok) {
      setNotice("No se pudo enviar la propuesta.");
      return;
    }
    const created = await r.json();
    setPrompts((curr) => [adaptPrompt(created), ...curr]);
    setNotice("Prompt publicado.");
    event.currentTarget.reset();
  }

  return (
    <div className="biblioteca-layout">
      {notice ? <div className="biblioteca-notice">{notice}</div> : null}
      <section className="biblioteca-main">
        <div className="biblioteca-toolbar">
          <input
            className="biblioteca-input"
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Buscar prompts..."
            value={query}
          />
          <select onChange={(e) => setCategoriaFiltro(e.target.value)} value={categoriaFiltro}>
            <option value="">Todas las categorías</option>
            {categorias.map((c) => (
              <option key={c.id} value={c.id}>{c.nombre}</option>
            ))}
          </select>
          <select onChange={(e) => setNivelFiltro(e.target.value)} value={nivelFiltro}>
            <option value="">Todos los niveles</option>
            <option value="basica">Básica</option>
            <option value="media">Media</option>
            <option value="universitario">Universitario</option>
            <option value="transversal">Transversal</option>
          </select>
          <select onChange={(e) => setOrden(e.target.value)} value={orden}>
            <option value="likes">Más votados</option>
            <option value="recientes">Más recientes</option>
          </select>
        </div>

        <p className="biblioteca-count">{filtrados.length} prompts encontrados</p>

        <div className="prompt-list">
          {filtrados.map((item) => (
            <PromptCard key={item.id} item={item} onVote={() => votar(item.id)} />
          ))}
        </div>
      </section>

      <aside className="biblioteca-form">
        <h2>Proponer actividad</h2>
        <form onSubmit={submit}>
          <input name="title" placeholder="Título" required />
          <input name="author" placeholder="Autor/a" required />
          <div className="biblioteca-form-row">
            <input name="subject" placeholder="Asignatura" required />
            <select name="level" required defaultValue="transversal">
              <option value="basica">Básica</option>
              <option value="media">Media</option>
              <option value="universitario">Universitario</option>
              <option value="transversal">Transversal</option>
            </select>
          </div>
          <select name="categoria" required defaultValue="">
            <option value="" disabled>Categoría</option>
            {categorias.map((c) => (
              <option key={c.id} value={c.id}>{c.nombre}</option>
            ))}
          </select>
          <textarea name="summary" placeholder="Resumen pedagógico" required rows="3" />
          <textarea name="prompt" placeholder="Prompt o instrucción reutilizable" required rows="5" />
          <input name="tags" placeholder="Etiquetas separadas por coma" />
          <button type="submit">Publicar</button>
        </form>
      </aside>
    </div>
  );
}
