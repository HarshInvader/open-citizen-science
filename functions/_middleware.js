// Host routing for opencitizenscience.org.
// mind. and origins. serve the project sites that build.py copies into dist/mind/ and dist/origins/.
// The old /mind/ and /origins/ paths on the main domain, and www., redirect to the right place.
const APEX = "opencitizenscience.org";
const SUBS = { [`mind.${APEX}`]: "/mind", [`origins.${APEX}`]: "/origins" };

export async function onRequest({ request, next, env }) {
  const url = new URL(request.url);
  if (url.pathname.startsWith("/api/")) return next();
  const host = url.hostname;
  if (host === `www.${APEX}`) {
    url.hostname = APEX;
    return Response.redirect(url.toString(), 301);
  }
  if (host === APEX) {
    const m = url.pathname.match(/^\/(mind|origins)(\/.*)?$/);
    if (m) return Response.redirect(`https://${m[1]}.${APEX}${m[2] || "/"}${url.search}`, 301);
    return next();
  }
  const prefix = SUBS[host];
  if (!prefix) return next();
  url.pathname = prefix + url.pathname;
  const res = await env.ASSETS.fetch(new Request(url.toString(), request));
  const loc = res.headers.get("Location");
  if (loc && loc.startsWith(prefix + "/")) {  // Pages' own redirects (e.g. /x.html -> /x) carry the prefix; drop it
    const h = new Headers(res.headers);
    h.set("Location", loc.slice(prefix.length));
    return new Response(res.body, { status: res.status, headers: h });
  }
  return res;
}
