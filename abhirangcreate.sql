CREATE TABLE  Commission (
    commission_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL, -- buyer
    artist_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    agreed_price REAL CHECK(agreed_price >= 0),
    status TEXT NOT NULL, -- pending, in progress, completed
    deadline DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (artist_id) REFERENCES user(user_id)
);