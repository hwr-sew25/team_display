PRAGMA foreign_keys = ON;

-- Table: points
CREATE TABLE IF NOT EXISTS points (
    point_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    x REAL NOT NULL,
    y REAL NOT NULL,
    z REAL NOT NULL
);

-- Table: POI (Points of Interest)
CREATE TABLE IF NOT EXISTS poi (
    poi_id INTEGER PRIMARY KEY AUTOINCREMENT,
    descriptionGER TEXT,
    descriptionENG TEXT,
    FOREIGN KEY (poi_id) REFERENCES points(point_id)
);

-- Table: wing
CREATE TABLE IF NOT EXISTS wing (
    wing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    wing TEXT NOT NULL,
    point_id INTEGER NOT NULL,
    FOREIGN KEY (point_id) REFERENCES points(point_id)
);

-- Table: room
CREATE TABLE IF NOT EXISTS room (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building TEXT NOT NULL,
    room_id TEXT NOT NULL UNIQUE,
    room_name TEXT NOT NULL,
    floor TEXT NOT NULL,
    wing_id INTEGER NOT NULL,
    side TEXT,
    category TEXT NOT NULL,
    gender TEXT,
    accessible INTEGER,
    notes TEXT,
    FOREIGN KEY (wing_id) REFERENCES wing(wing_id)
);
