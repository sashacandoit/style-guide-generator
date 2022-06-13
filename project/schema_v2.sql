CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
)

CREATE TABLE color_schemes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users,
    primary_color TEXT NOT NULL DEFAULT '000000',
    secondary_color TEXT NOT NULL DEFAULT 'ffffff',
    accent_1 TEXT DEFAULT 'None',
    accent_2 TEXT DEFAULT 'None',
    accent_3 TEXT DEFAULT 'None'
    timestamp TIMESTAMP DEFAULT (now())
)

CREATE TABLE font_styles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    style_name TEXT NOT NULL DEFAULT 'sans-serif', 
    font_weight INTEGER NOT NULL DEFAULT 400,
    font_style TEXT NOT NULL DEFAULT 'Normal',
    font_size INTEGER NOT NULL DEFAULT 16,
    font_color TEXT NOT NULL DEFAULT 'primary_color'
    -- Should font_color reference the color_schemes table?
    timestamp TIMESTAMP DEFAULT (now())
)

CREATE TABLE style_guides (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    user_id INTEGER REFERENCES users,
    color_scheme_id INTEGER REFERENCES color_schemes,
    p INTEGER REFERENCES font_styles,
    h1 INTEGER REFERENCES font_styles,
    h2 INTEGER REFERENCES font_styles,
    h3 INTEGER REFERENCES font_styles,
    h4 INTEGER REFERENCES font_styles,
    h5 INTEGER REFERENCES font_styles,
    h6 INTEGER REFERENCES font_styles,
    timestamp TIMESTAMP DEFAULT (now())
)