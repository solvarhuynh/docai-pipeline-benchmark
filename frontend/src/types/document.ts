export type DocumentType = "invoice" | "receipt" | "contract" | "unknown";

export interface BoundingBox {
  xmin: number;
  ymin: number;
  xmax: number;
  ymax: number;
  normalized: boolean;
}

export interface ExtractedField {
  field_name: string;
  field_value: string;
  confidence: number;
  bounding_box?: BoundingBox | null;
  page_number: number;
  raw_text?: string | null;
}

export type SeverityLevel = "low" | "medium" | "high" | "critical";

export interface RiskFlag {
  rule_id: string;
  rule_name: string;
  severity: SeverityLevel;
  description: string;
  target_field?: string | null;
}

export interface UnifiedDocumentOutput {
  document_type: DocumentType;
  fields: ExtractedField[];
  overall_confidence: number;
  risk_flags: RiskFlag[];
  execution_time_ms?: number | null;
  pipeline_track?: string | null;
  metadata: Record<string, unknown>;
}
