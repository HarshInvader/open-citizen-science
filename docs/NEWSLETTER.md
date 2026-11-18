# Newsletter

## What exists

- Signup form on the home page and on each project's News page posts to `/api/subscribe` (Pages Function, `functions/api/subscribe.js`).
- Subscribers are stored in Cloudflare D1 `ocs-newsletter` (binding `NEWS_DB`, table `subscribers`: email, projects, source, created_at, updated_at, unsub_token, status). Picking more projects later merges them.
- Unsubscribe link: `/api/unsubscribe?t=<unsub_token>`.
- Drafts collect in `docs/newsletter/next-<project>.md`, written by the paper watch (`PAPER_WATCH.md`).

## What does not exist yet

Nothing sends email. Sending needs a provider the user picks (for example Resend, Postmark, Buttondown or Cloudflare Email Routing with a worker), a verified sending domain, and a send step that only mails people subscribed to that project, with the unsubscribe link in every email.

Until then: no email is sent to subscribers.

## Reading the list

`npx wrangler d1 execute ocs-newsletter --remote --command "select projects, count(*) from subscribers where status='active' group by projects"`
