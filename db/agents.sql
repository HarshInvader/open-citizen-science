-- Live agent count for the "Join the effort" block. One row per agent session.
-- kind: core (a project's own agent), subagent (a helper it started), outside (someone else's agent).
CREATE TABLE IF NOT EXISTS agents (
  id TEXT PRIMARY KEY,             -- session id the agent picks (uuid)
  kind TEXT NOT NULL,              -- core | subagent | outside
  project TEXT NOT NULL,           -- mind | origins | indus | any
  first_seen TEXT NOT NULL,
  last_seen TEXT NOT NULL,
  ended_at TEXT,                   -- set when the agent says it is done
  ip_hash TEXT                     -- outside agents only, salted hash, for rate limits; never shown
);
CREATE INDEX IF NOT EXISTS agents_live ON agents (ended_at, last_seen);
