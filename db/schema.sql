CREATE TABLE IF NOT EXISTS subscribers (
  email TEXT PRIMARY KEY,
  projects TEXT NOT NULL,          -- comma list: mind,origins,indus
  source TEXT,                     -- page the form was on
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  unsub_token TEXT NOT NULL,       -- for the one-click unsubscribe link in every issue
  status TEXT NOT NULL DEFAULT 'active'  -- active | unsubscribed
);
