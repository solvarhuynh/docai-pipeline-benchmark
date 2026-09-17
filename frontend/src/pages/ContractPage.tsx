import { WorkspacePlaceholder } from "../components/WorkspacePlaceholder";

export function ContractPage() {
  return (
    <WorkspacePlaceholder
      title="Contract Intelligence"
      description="A workspace for contract metadata, clause spans, supporting text and Contract Risk review."
      steps={["Upload a contract", "Choose Track A or Track B", "View metadata and important clauses", "Review supporting text and Contract Risk"]}
    />
  );
}
