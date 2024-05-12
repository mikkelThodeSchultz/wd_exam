DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS password_reset;

CREATE TABLE users(
    user_pk                 TEXT,
    user_username           TEXT,
    user_email              TEXT UNIQUE,
    user_password           TEXT,
    user_role               TEXT,
    user_created_at         INTEGER,
    user_updated_at         INTEGER,
    user_deleted_at         INTEGER,
    user_is_verified        INTEGER,
    user_verification_key   TEXT,
    PRIMARY KEY(user_pk)
) WITHOUT ROWID;

CREATE TABLE password_reset (
    user_pk             INTEGER,
    reset_token         TEXT UNIQUE,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_pk) REFERENCES users(id) ON DELETE CASCADE
);


INSERT INTO users VALUES("09648d2920c84cdaacc40ce232557291", "Admin", "admin@company.com", X'24326224313224775137576f436d676b6f32794861664a4f354a5734754a6847684b726e526478423163775166413351375162764d6c70596e503236', "admin", 1712648346, 0, 0, 1, 123); 
INSERT INTO users VALUES("09648d2920c83edaadc40ce232557291", "Partner", "partner@company.com", X'24326224313224775137576f436d676b6f32794861664a4f354a5734754a6847684b726e526478423163775166413351375162764d6c70596e503236', "partner", 1712648346, 0, 0, 1, 123); 
INSERT INTO users VALUES("09648d2920c83edabdc40ce232557291", "Customer", "customer@company.com", X'24326224313224775137576f436d676b6f32794861664a4f354a5734754a6847684b726e526478423163775166413351375162764d6c70596e503236', "customer", 1712648346, 0, 0, 1, 123); 

SELECT * FROM users;

SELECT * FROM password_reset;