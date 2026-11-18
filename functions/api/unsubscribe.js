// One-click unsubscribe: /api/unsubscribe?t=<token>
export async function onRequest({ request, env }) {
  const t = new URL(request.url).searchParams.get("t") || "";
  if (/^[a-f0-9]{32}$/.test(t)) {
    await env.NEWS_DB.prepare("UPDATE subscribers SET status = 'unsubscribed', updated_at = ? WHERE unsub_token = ?").bind(new Date().toISOString(), t).run();
  }
  return new Response('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta name="robots" content="noindex"><title>Unsubscribed</title><body style="font:18px/1.5 system-ui;max-width:32em;margin:15vh auto;padding:0 16px"><h1>You’re unsubscribed</h1><p>You won’t get any more newsletters from Open Citizen Science. <a href="/">Back to the site</a></p>', { headers: { "Content-Type": "text/html; charset=utf-8" } });
}
