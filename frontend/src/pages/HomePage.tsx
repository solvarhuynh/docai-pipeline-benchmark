import { StatusBadge } from "../components/StatusBadge";

export function HomePage() {
  return (
    <section className="hero-grid">
      <div>
        <p className="eyebrow">Document Intelligence platform</p>
        <h1>Understand invoices and contracts with evidence.</h1>
        <p className="lead">
          DocAI turns document-processing outputs into structured data and review signals.
          FastAPI remains the only business backend; this React application is the web UI.
        </p>
      </div>
      <aside className="status-card">
        <p className="eyebrow">Current delivery status</p>
        <StatusBadge label="SCAFFOLD" />
        <p>Frontend structure is ready. Backend inference and end-to-end processing are not enabled yet.</p>
      </aside>
    </section>
  );
}
