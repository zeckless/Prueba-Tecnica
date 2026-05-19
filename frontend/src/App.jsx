import { useEffect, useMemo, useState } from "react";
import Biblioteca from "./Biblioteca";
import {
  BookOpenCheck,
  ClipboardList,
  ExternalLink,
  Filter,
  LibraryBig,
  MessageSquareText,
  Plus,
  Search,
  Sparkles,
  UsersRound,
} from "lucide-react";

const API_BASE = "http://127.0.0.1:8000/api";

const tabs = [
  { id: "dashboard", label: "Inicio", icon: ClipboardList },
  { id: "prompts", label: "Biblioteca", icon: Sparkles },
  { id: "resources", label: "Recursos", icon: LibraryBig },
  { id: "community", label: "Espacio comunitario", icon: UsersRound },
];

const statusLabels = {
  curated: "Curado",
  review: "En revisión",
  draft: "Borrador",
};

function App() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [prompts, setPrompts] = useState([]);
  const [resources, setResources] = useState([]);
  const [discussions, setDiscussions] = useState([]);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState("");

  async function loadData() {
    setLoading(true);
    const [promptRes, resourceRes, discussionRes] = await Promise.all([
      fetch(`${API_BASE}/prompts/`),
      fetch(`${API_BASE}/resources/`),
      fetch(`${API_BASE}/discussions/`),
    ]);

    setPrompts((await promptRes.json()).results);
    setResources((await resourceRes.json()).results);
    setDiscussions((await discussionRes.json()).results);
    setLoading(false);
  }

  useEffect(() => {
    loadData().catch(() => {
      setNotice("No se pudo conectar con la API local.");
      setLoading(false);
    });
  }, []);

  const filteredPrompts = useMemo(() => {
    return prompts.filter((item) => {
      const text = `${item.title} ${item.summary} ${item.subject} ${item.tags.join(" ")}`.toLowerCase();
      const matchesQuery = text.includes(query.toLowerCase());
      const matchesStatus = status ? item.status === status : true;
      return matchesQuery && matchesStatus;
    });
  }, [prompts, query, status]);

  async function submitPrompt(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const payload = {
      title: form.get("title"),
      author: form.get("author"),
      subject: form.get("subject"),
      level: form.get("level"),
      summary: form.get("summary"),
      prompt: form.get("prompt"),
      tags: String(form.get("tags") || "")
        .split(",")
        .map((tag) => tag.trim())
        .filter(Boolean),
    };

    const response = await fetch(`${API_BASE}/prompts/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const created = await response.json();
    setPrompts((current) => [created, ...current]);
    setNotice("Propuesta enviada a curación.");
    event.currentTarget.reset();
  }

  const ActiveIcon = tabs.find((tab) => tab.id === activeTab)?.icon ?? ClipboardList;

  return (
    <main className="app-shell">
      <header className="app-header">
        <button className="brand home-brand" onClick={() => setActiveTab("dashboard")} type="button">
          <span className="brand-mark">
            <BookOpenCheck size={22} />
          </span>
          <div>
            <strong>Comunidad Docente IA</strong>
            <small>Prototipo navegable</small>
          </div>
        </button>

        <nav className="top-nav" aria-label="Navegación principal">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                className={activeTab === tab.id ? "tab active" : "tab"}
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                title={tab.label}
                type="button"
              >
                <Icon size={18} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </header>

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Oficina de Inteligencia Artificial</p>
            <h1>
              <ActiveIcon size={28} />
              {tabs.find((tab) => tab.id === activeTab)?.label}
            </h1>
          </div>
        </header>

        {notice ? <div className="notice">{notice}</div> : null}
        {loading ? <div className="loading">Cargando datos del prototipo...</div> : null}

        {!loading && activeTab === "dashboard" && (
          <Dashboard setActiveTab={setActiveTab} />
        )}
        {!loading && activeTab === "prompts" && <Biblioteca />}
        {!loading && activeTab === "resources" && <Resources resources={resources} />}
        {!loading && activeTab === "community" && <Community discussions={discussions} />}
      </section>
    </main>
  );
}

function Dashboard({ setActiveTab }) {
  const landingCards = [
    {
      id: "prompts",
      title: "Biblioteca",
      description: "Prompts y actividades de aula compartidas por docentes, con estado de curación y etiquetas.",
      icon: Sparkles,
    },
    {
      id: "resources",
      title: "Recursos",
      description: "Afiches de cursos, programas, guías y materiales relevantes para profundizar el trabajo con IA.",
      icon: LibraryBig,
    },
    {
      id: "community",
      title: "Espacio comunitario",
      description: "Conversaciones para resolver dudas, mejorar actividades existentes y levantar acuerdos docentes.",
      icon: UsersRound,
    },
  ];

  return (
    <div className="landing-stack">
      <section className="landing-hero">
        <div>
          <p className="eyebrow">Comunidad docente IA</p>
          <h2>Un punto de entrada para aprender, compartir y mejorar prácticas pedagógicas con IA generativa.</h2>
        </div>
      </section>

      <section className="landing-card-grid" aria-label="Secciones principales">
        {landingCards.map((card) => {
          const Icon = card.icon;
          return (
            <button
              className="landing-card"
              key={card.id}
              onClick={() => setActiveTab(card.id)}
              type="button"
            >
              <span className="landing-card-icon">
                <Icon size={24} />
              </span>
              <span className="landing-card-content">
                <strong>{card.title}</strong>
                <span>{card.description}</span>
              </span>
            </button>
          );
        })}
      </section>
    </div>
  );
}

function Prompts({ prompts, query, setQuery, status, setStatus, submitPrompt }) {
  return (
    <div className="prompt-layout">
      <section className="content-column">
        <div className="toolbar">
          <label className="search-box">
            <Search size={18} />
            <input
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Buscar por tema, etiqueta o asignatura"
              value={query}
            />
          </label>
          <label className="filter-box">
            <Filter size={18} />
            <select onChange={(event) => setStatus(event.target.value)} value={status}>
              <option value="">Todos</option>
              <option value="curated">Curados</option>
              <option value="review">En revisión</option>
            </select>
          </label>
        </div>

        <div className="card-grid">
          {prompts.map((item) => (
            <article className="prompt-card" key={item.id}>
              <div className="card-header">
                <span className={`badge ${item.status}`}>{statusLabels[item.status]}</span>
                <span>{item.likes} votos</span>
              </div>
              <h2>{item.title}</h2>
              <p>{item.summary}</p>
              <blockquote>{item.prompt}</blockquote>
              <div className="tag-row">
                {item.tags.map((tag) => (
                  <span key={tag}>{tag}</span>
                ))}
              </div>
              <footer>
                <strong>{item.author}</strong>
                <span>{item.subject} · {item.level}</span>
              </footer>
            </article>
          ))}
        </div>
      </section>

      <aside className="submit-panel">
        <div className="section-heading">
          <h2>Proponer actividad</h2>
        </div>
        <form onSubmit={submitPrompt}>
          <input name="title" placeholder="Título" required />
          <input name="author" placeholder="Autor/a" required />
          <div className="form-row">
            <input name="subject" placeholder="Área" required />
            <input name="level" placeholder="Nivel" required />
          </div>
          <textarea name="summary" placeholder="Resumen pedagógico" required rows="3" />
          <textarea name="prompt" placeholder="Prompt o instrucción reutilizable" required rows="5" />
          <input name="tags" placeholder="Etiquetas separadas por coma" />
          <button type="submit">
            <Plus size={18} />
            Enviar a curación
          </button>
        </form>
      </aside>
    </div>
  );
}

function Resources({ resources }) {
  return (
    <div className="resource-section">
      <div className="resource-section-header">
        <div>
          <p className="eyebrow">Repositorio curado</p>
          <h2>Materiales para llevar IA al aula</h2>
        </div>
      </div>

      <section className="resource-grid">
        {resources.map((resource) => (
          <article className="resource-card" key={resource.id}>
            <div className="poster-image">
              <img alt="" src={resource.imageUrl} />
              <span className="resource-type">{resource.type}</span>
            </div>
            <div className="poster-body">
              <span className="poster-source">{resource.source}</span>
              <h2>{resource.title}</h2>
              <p>{resource.description}</p>
            </div>
            <footer>
              {resource.featured ? <strong>Destacado</strong> : <span>Recurso</span>}
              {resource.url ? (
                <a href={resource.url} rel="noreferrer" target="_blank">
                  <ExternalLink size={17} />
                  Abrir
                </a>
              ) : (
                <span>Interno</span>
              )}
            </footer>
          </article>
        ))}
      </section>
    </div>
  );
}

function Community({ discussions }) {
  return (
    <div className="community-list">
      {discussions.map((discussion) => (
        <article className="discussion-card" key={discussion.id}>
          <div className="discussion-icon">
            <MessageSquareText size={22} />
          </div>
          <div>
            <span className="resource-type">{discussion.topic}</span>
            <h2>{discussion.title}</h2>
            <p>{discussion.body}</p>
            <footer>
              <strong>{discussion.author}</strong>
              <span>{discussion.replies} respuestas</span>
            </footer>
          </div>
        </article>
      ))}
    </div>
  );
}

export default App;
