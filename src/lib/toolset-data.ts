import yaml from 'js-yaml';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const repoRoot = fileURLToPath(new URL('../../', import.meta.url));

function loadYaml<T>(rel: string): T {
  return yaml.load(readFileSync(`${repoRoot}${rel}`, 'utf-8')) as T;
}

export interface AiAgent {
  title: string;
  url?: string;
  licence: string;
  cost_self?: string;
  cost_cloud?: string;
  mcp?: boolean | string;
  open_weights?: boolean | string;
  cpp_verdict: string;
  best_when?: string;
  skip_if?: string;
}

export interface LocalLlmTier {
  vram: string;
  pick: string;
  score: string;
  notes: string;
}

export interface LocalLlmRuntime {
  name: string;
  best_for: string;
  licence: string;
}

export interface LocalLlmData {
  tiers: LocalLlmTier[];
  runtimes: LocalLlmRuntime[];
}

export const aiAgents = loadYaml<Record<string, AiAgent>>('src/data/ai-agents-for-cpp.yml');
export const localLlm = loadYaml<LocalLlmData>('src/data/local-llm-tiers.yml');
