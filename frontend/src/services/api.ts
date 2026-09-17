import type { DocumentType, UnifiedDocumentOutput } from "../types/document";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "/api";

export async function healthCheck(): Promise<{ status: string }> {
  const response = await fetch(`${apiBaseUrl}/health`);
  if (!response.ok) throw new Error(`Health check failed: ${response.status}`);
  return response.json() as Promise<{ status: string }>;
}

export async function parseDocument(
  file: File,
  documentType: DocumentType,
  engine: "classic" | "vlm"
): Promise<UnifiedDocumentOutput> {
  const form = new FormData();
  form.append("file", file);
  form.append("document_type", documentType);

  const response = await fetch(`${apiBaseUrl}/parse/${engine}`, {
    method: "POST",
    body: form
  });
  if (!response.ok) throw new Error(`Document processing failed: ${response.status}`);
  return response.json() as Promise<UnifiedDocumentOutput>;
}
