/**
 * CodebaseGPT Frontend API Client
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Citation {
  file_path: string;
  line_number: number;
  snippet: string;
}

export interface QueryResponse {
  answer: string;
  citations: Citation[];
  thinking?: string;
}

export interface SearchResult {
  file_path: string;
  line_start: number;
  line_end: number;
  language: string;
  preview: string;
}

export interface IndexResponse {
  status: string;
  chunks_indexed: number;
  files_processed: number;
}

export interface StatsResponse {
  total_chunks: number;
  files: number;
  languages: string[];
}

class CodebaseGPTApi {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE) {
    this.baseUrl = baseUrl;
  }

  async health(): Promise<{ status: string }> {
    const res = await fetch(`${this.baseUrl}/health`);
    return res.json();
  }

  async indexLocal(path: string): Promise<IndexResponse> {
    const res = await fetch(`${this.baseUrl}/index/local?path=${encodeURIComponent(path)}`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  }

  async query(question: string, includeThinking: boolean = false): Promise<QueryResponse> {
    const res = await fetch(`${this.baseUrl}/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, include_thinking: includeThinking }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  }

  async search(q: string, limit: number = 10): Promise<SearchResult[]> {
    const res = await fetch(`${this.baseUrl}/search?q=${encodeURIComponent(q)}&limit=${limit}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  }

  async stats(): Promise<StatsResponse> {
    const res = await fetch(`${this.baseUrl}/stats`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  }
}

export const api = new CodebaseGPTApi();
