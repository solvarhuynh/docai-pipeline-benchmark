import { WorkspacePlaceholder } from "../components/WorkspacePlaceholder";

export function InvoicePage() {
  return (
    <WorkspacePlaceholder
      title="Invoice Intelligence"
      description="A workspace for invoice and receipt upload, field extraction, confidence, risk flags, evidence and structured JSON."
      steps={["Upload an invoice or receipt", "Choose Track A or Track B", "View fields, confidence and evidence", "Review Invoice Risk and structured JSON"]}
    />
  );
}
