import { StatusBadge } from "./StatusBadge";

interface WorkspacePlaceholderProps {
  title: string;
  description: string;
  steps: string[];
}

export function WorkspacePlaceholder({ title, description, steps }: WorkspacePlaceholderProps) {
  return (
    <section className="workspace-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Product workspace</p>
          <h2>{title}</h2>
        </div>
        <StatusBadge label="SCAFFOLD" />
      </div>
      <p>{description}</p>
      <ol className="workflow-list">
        {steps.map((step) => <li key={step}>{step}</li>)}
      </ol>
      <p className="notice">This UI is a scaffold. It does not display fake extraction results.</p>
    </section>
  );
}
