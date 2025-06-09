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

-- Grupos de WhatsApp
CREATE TABLE IF NOT EXISTS whatsapp_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_id INTEGER,
    category_id INTEGER,
    nome TEXT,
    link_whatsapp TEXT NOT NULL,
    active BOOLEAN DEFAULT 1,
    FOREIGN KEY (region_id) REFERENCES regions(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Links encurtados dos grupos
CREATE TABLE IF NOT EXISTS group_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_id TEXT UNIQUE,
    group_id INTEGER,
    click_count INTEGER DEFAULT 0,
    created_at TEXT,
    FOREIGN KEY (group_id) REFERENCES whatsapp_groups(id)
);

-- Estados iniciais
INSERT INTO states (name, code) VALUES
  ('Massachusetts', 'MA'),
  ('Rhode Island', 'RI'),
  ('New Hampshire', 'NH');

-- Regiões por estado
INSERT INTO regions (name, state_id, is_statewide) VALUES
  ('MetroWest', 1, 0),
  ('Worcester', 1, 0),
  ('SouthShore', 1, 0),
  ('NorthShore', 1, 0),
  ('Rhode Island (RI)', 2, 1),
  ('New Hampshire (NH)', 3, 1);

-- Categorias
INSERT INTO categories (name) VALUES
  ('Geral'),
  ('Construção'),
  ('Limpeza'),
  ('Restaurante'),
  ('Jardinagem'),
  ('Serviços Gerais');

-- Grupos de WhatsApp
INSERT INTO whatsapp_groups (region_id, category_id, nome, link_whatsapp) VALUES
-- MetroWest
(1, 1, 'JobFishing_MetroWest_Geral', 'https://chat.whatsapp.com/metro-geral'),
(1, 2, 'JobFishing_MetroWest_Construcao', 'https://chat.whatsapp.com/metro-construcao'),
(1, 3, 'JobFishing_MetroWest_Limpeza', 'https://chat.whatsapp.com/metro-limpeza'),
(1, 4, 'JobFishing_MetroWest_Restaurante', 'https://chat.whatsapp.com/metro-restaurante'),
(1, 5, 'JobFishing_MetroWest_Jardinagem', 'https://chat.whatsapp.com/metro-jardinagem'),
(1, 6, 'JobFishing_MetroWest_ServGerais', 'https://chat.whatsapp.com/metro-servgerais'),

-- Worcester
(2, 1, 'JobFishing_Worcester_Geral', 'https://chat.whatsapp.com/worcester-geral'),
(2, 2, 'JobFishing_Worcester_Construcao', 'https://chat.whatsapp.com/worcester-construcao'),
(2, 3, 'JobFishing_Worcester_Limpeza', 'https://chat.whatsapp.com/worcester-limpeza'),
(2, 4, 'JobFishing_Worcester_Restaurante', 'https://chat.whatsapp.com/worcester-restaurante'),
(2, 5, 'JobFishing_Worcester_Jardinagem', 'https://chat.whatsapp.com/worcester-jardinagem'),
(2, 6, 'JobFishing_Worcester_ServGerais', 'https://chat.whatsapp.com/worcester-servgerais'),

-- SouthShore
(3, 1, 'JobFishing_SouthShore_Geral', 'https://chat.whatsapp.com/south-geral'),
(3, 2, 'JobFishing_SouthShore_Construcao', 'https://chat.whatsapp.com/south-construcao'),
(3, 3, 'JobFishing_SouthShore_Limpeza', 'https://chat.whatsapp.com/south-limpeza'),
(3, 4, 'JobFishing_SouthShore_Restaurante', 'https://chat.whatsapp.com/south-restaurante'),
(3, 5, 'JobFishing_SouthShore_Jardinagem', 'https://chat.whatsapp.com/south-jardinagem'),
(3, 6, 'JobFishing_SouthShore_ServGerais', 'https://chat.whatsapp.com/south-servgerais'),

-- NorthShore
(4, 1, 'JobFishing_NorthShore_Geral', 'https://chat.whatsapp.com/north-geral'),
(4, 2, 'JobFishing_NorthShore_Construcao', 'https://chat.whatsapp.com/north-construcao'),
(4, 3, 'JobFishing_NorthShore_Limpeza', 'https://chat.whatsapp.com/north-limpeza'),
(4, 4, 'JobFishing_NorthShore_Restaurante', 'https://chat.whatsapp.com/north-restaurante'),
(4, 5, 'JobFishing_NorthShore_Jardinagem', 'https://chat.whatsapp.com/north-jardinagem'),
(4, 6, 'JobFishing_NorthShore_ServGerais', 'https://chat.whatsapp.com/north-servgerais'),

-- Rhode Island
(5, 1, 'JobFishing_RI_Geral', 'https://chat.whatsapp.com/ri-geral'),
(5, 2, 'JobFishing_RI_Construcao', 'https://chat.whatsapp.com/ri-construcao'),
(5, 3, 'JobFishing_RI_Limpeza', 'https://chat.whatsapp.com/ri-limpeza'),
(5, 4, 'JobFishing_RI_Restaurante', 'https://chat.whatsapp.com/ri-restaurante'),
(5, 5, 'JobFishing_RI_Jardinagem', 'https://chat.whatsapp.com/ri-jardinagem'),
(5, 6, 'JobFishing_RI_ServGerais', 'https://chat.whatsapp.com/ri-servgerais'),

-- New Hampshire
(6, 1, 'JobFishing_NH_Geral', 'https://chat.whatsapp.com/nh-geral'),
(6, 2, 'JobFishing_NH_Construcao', 'https://chat.whatsapp.com/nh-construcao'),
(6, 3, 'JobFishing_NH_Limpeza', 'https://chat.whatsapp.com/nh-limpeza'),
(6, 4, 'JobFishing_NH_Restaurante', 'https://chat.whatsapp.com/nh-restaurante'),
(6, 5, 'JobFishing_NH_Jardinagem', 'https://chat.whatsapp.com/nh-jardinagem'),
(6, 6, 'JobFishing_NH_ServGerais', 'https://chat.whatsapp.com/nh-servgerais');
