const API_BASE = '/api';

export async function compileCode(code) {
  const res = await fetch(`${API_BASE}/compile`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, include_ast: true, include_tokens: true })
  });
  return res.json();
}

export async function tokenizeCode(code) {
  const res = await fetch(`${API_BASE}/tokenize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code })
  });
  return res.json();
}

export async function parseCode(code) {
  const res = await fetch(`${API_BASE}/parse`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code })
  });
  return res.json();
}

export async function getExamples() {
  const res = await fetch(`${API_BASE}/examples`);
  return res.json();
}

export async function getExample(name) {
  const res = await fetch(`${API_BASE}/examples/${name}`);
  return res.json();
}
