// Newsletter signup: stores an email and the projects it wants. Sends nothing.
const PROJECTS = new Set(["mind", "origins", "indus"]);
const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type" };
const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", ...CORS } });

export const onRequestOptions = () => new Response(null, { status: 204, headers: CORS });

export async function onRequestPost({ request, env }) {
  let data;
  try {
    const type = request.headers.get("Content-Type") || "";
    data = type.includes("application/json") ? await request.json() : Object.fromEntries((await request.formData()).entries());
  } catch { return json({ ok: false, error: "Could not read the form." }, 400); }
  if (data.website) return json({ ok: true });  // honeypot: bots fill every field
  const email = String(data.email || "").trim().toLowerCase();
  if (email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return json({ ok: false, error: "That email address doesn’t look right." }, 400);
  let wanted = Array.isArray(data.projects) ? data.projects : String(data.projects || "").split(",");
  wanted = [...new Set(wanted.map((p) => String(p).trim()).filter((p) => PROJECTS.has(p)))];
  if (!wanted.length) wanted = ["mind", "origins", "indus"];
  const source = String(data.source || "").slice(0, 120);
  const now = new Date().toISOString();
  const old = await env.NEWS_DB.prepare("SELECT projects FROM subscribers WHERE email = ?").bind(email).first();
  if (old) {
    const merged = [...new Set([...old.projects.split(","), ...wanted])].filter(Boolean).join(",");
    await env.NEWS_DB.prepare("UPDATE subscribers SET projects = ?, status = 'active', updated_at = ? WHERE email = ?").bind(merged, now, email).run();
  } else {
    const token = crypto.randomUUID().replace(/-/g, "");
    await env.NEWS_DB.prepare("INSERT INTO subscribers (email, projects, source, created_at, updated_at, unsub_token) VALUES (?, ?, ?, ?, ?, ?)")
      .bind(email, wanted.join(","), source, now, now, token).run();
  }
  return json({ ok: true });
}
