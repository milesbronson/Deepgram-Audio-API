CREATE TABLE audio(
    fileid INTEGER PRIMARY KEY AUTOINCREMENT,
    filename VARCHAR(64) NOT NULL,
    filepath VARCHAR(64) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    duration INTEGER NOT NULL
);