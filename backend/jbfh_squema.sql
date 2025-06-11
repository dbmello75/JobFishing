-- Estados
CREATE TABLE IF NOT EXISTS states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    active BOOLEAN NOT NULL DEFAULT 1
);

-- Regiões (com estado e flag para cobertura estadual)
CREATE TABLE IF NOT EXISTS regions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    state_id INTEGER NOT NULL,
    active BOOLEAN NOT NULL DEFAULT 1,
    is_statewide BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY(state_id) REFERENCES states(id)
);

-- Categorias de trabalho
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);


CREATE TABLE IF NOT EXISTS whatsapp_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    link_whatsapp TEXT NOT NULL,
    short_id TEXT UNIQUE NOT NULL,
    click_count INTEGER DEFAULT 0,
    members_count INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    active BOOLEAN DEFAULT 1
);


CREATE TABLE IF NOT EXISTS ads (
    id TEXT PRIMARY KEY,
    short_id TEXT UNIQUE,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    employer_phone TEXT NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    active INTEGER DEFAULT 1,
    click_count INTEGER DEFAULT 0
);


-- Estados iniciais
INSERT OR IGNORE INTO states (name, code) VALUES
  ('Massachusetts', 'MA'),
  ('Rhode Island', 'RI'),
  ('New Hampshire', 'NH');

-- Regiões por estado
INSERT OR IGNORE INTO regions (name, state_id, is_statewide) VALUES
  ('MetroWest', 1, 0),
  ('Worcester', 1, 0),
  ('SouthShore', 1, 0),
  ('NorthShore', 1, 0),
  ('Rhode Island (RI)', 2, 1),
  ('New Hampshire (NH)', 3, 1);

-- Categorias
INSERT OR IGNORE INTO categories (name) VALUES
  ('Geral'),
  ('Construção'),
  ('Limpeza'),
  ('Restaurante'),
  ('Jardinagem'),
  ('Serviços Gerais');

