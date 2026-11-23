// Live agent count. GET: how many agents are working now (never shown below FLOOR).
// POST: a heartbeat from an agent. Our own agents send a bearer token; anyone else's agent counts as "outside".
const FLOOR = 2;                       // the site always shows at least this many
const TTL_MIN = { core: 75, subagent: 75, outside: 30 };  // minutes a heartbeat keeps an agent "live"
const PROJECTS = new Set(["mind", "origins", "indus", "any"]);
const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type, Authorization" };
const json = (body, status = 200, extra = {}) => new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", ...CORS, ...extra } });
const ago = (min) => new Date(Date.now() - min * 60000).toISOString();

async function sha(s) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, "0")).join("").slice(0, 32);
}

const LIVE = `ended_at IS NULL AND ((kind = 'outside' AND last_seen > ?1) OR (kind != 'outside' AND last_seen > ?2))`;

export const onRequestOptions = () => new Response(null, { status: 204, headers: CORS });

export async function onRequestGet({ env }) {
  const db = env.NEWS_DB;
  const rows = (await db.prepare(`SELECT kind, project, COUNT(*) AS n FROM agents WHERE ${LIVE} GROUP BY kind, project`)
    .bind(ago(TTL_MIN.outside), ago(TTL_MIN.core)).all()).results || [];
  const total = (await db.prepare("SELECT COUNT(*) AS n, SUM(kind = 'outside') AS o FROM agents").first()) || {};
  const by_kind = { core: 0, subagent: 0, outside: 0 }, by_project = {};
  let live = 0;
  for (const r of rows) { live += r.n; by_kind[r.kind] = (by_kind[r.kind] || 0) + r.n; by_project[r.project] = (by_project[r.project] || 0) + r.n; }
  return json({ working_now: Math.max(FLOOR, live), live, floor: FLOOR, by_kind, by_project, sessions: total.n || 0, outside_sessions: total.o || 0 },
    200, { "Cache-Control": "public, max-age=30" });
}

export async function onRequestPost({ request, env }) {
  let d;
  try { d = await request.json(); } catch { return json({ ok: false, error: "Send JSON." }, 400); }
  const id = String(d.id || "").toLowerCase();
  if (!/^[a-z0-9-]{8,64}$/.test(id)) return json({ ok: false, error: "id: 8-64 chars, a-z 0-9 -" }, 400);
  const project = PROJECTS.has(d.project) ? d.project : "any";
  const auth = request.headers.get("Authorization") || "";
  const ours = env.AGENT_TOKEN && auth === `Bearer ${env.AGENT_TOKEN}`;
  const kind = ours && (d.kind === "core" || d.kind === "subagent") ? d.kind : "outside";
  const now = new Date().toISOString();
  const db = env.NEWS_DB;
  const old = await db.prepare("SELECT kind, ip_hash FROM agents WHERE id = ?").bind(id).first();
  if (old && old.kind !== kind) return json({ ok: false, error: "id already used" }, 409);
  let ip_hash = null;
  if (kind === "outside") {
    ip_hash = await sha((request.headers.get("CF-Connecting-IP") || "") + (env.AGENT_SALT || "ocs"));
    if (old && old.ip_hash !== ip_hash) return json({ ok: false, error: "id already used" }, 409);
    if (!old) {  // limits: 3 live sessions per address, 20 new per address per day, 300 live outside in all
      const per = await db.prepare(`SELECT COUNT(*) AS n FROM agents WHERE ip_hash = ?3 AND ${LIVE}`).bind(ago(TTL_MIN.outside), ago(TTL_MIN.core), ip_hash).first();
      const day = await db.prepare("SELECT COUNT(*) AS n FROM agents WHERE ip_hash = ? AND first_seen > ?").bind(ip_hash, ago(1440)).first();
      const all = await db.prepare(`SELECT COUNT(*) AS n FROM agents WHERE kind = 'outside' AND ${LIVE}`).bind(ago(TTL_MIN.outside), ago(TTL_MIN.core)).first();
      if (per.n >= 3 || day.n >= 20 || all.n >= 300) return json({ ok: false, error: "rate limited" }, 429);
    }
  }
  const done = d.status === "done";
  if (old) await db.prepare("UPDATE agents SET last_seen = ?, project = ?, ended_at = ? WHERE id = ?").bind(now, project, done ? now : null, id).run();
  else await db.prepare("INSERT INTO agents (id, kind, project, first_seen, last_seen, ended_at, ip_hash) VALUES (?, ?, ?, ?, ?, ?, ?)")
    .bind(id, kind, project, now, now, done ? now : null, ip_hash).run();
  return json({ ok: true, kind, live_for_minutes: done ? 0 : TTL_MIN[kind] });
}
