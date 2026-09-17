import { StatusBadge } from "../components/StatusBadge";

export function ResearchPage() {
  return (
    <section className="workspace-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Research Lab</p>
          <h2>Compare processing engines with real evidence.</h2>
        </div>
        <StatusBadge label="PLANNED" />
      </div>
      <p>
        This area will compare Track A and Track B on Invoice and Contract using ground truth.
        It must not render invented metrics.
      </p>
      <div className="metric-list">
        {['Precision / Recall / F1', 'Latency', 'Robustness', 'Cost', 'Agreement / disagreement'].map((metric) => (
          <span key={metric}>{metric}</span>
        ))}
      </div>
    </section>
  );
}
