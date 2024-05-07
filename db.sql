DROP TABLE IF EXISTS users;

CREATE TABLE users(
    user_pk             TEXT,
    user_username       TEXT,
    user_name           TEXT,
    user_email          TEXT UNIQUE,
    user_password       TEXT,
    user_role           TEXT,
    user_created_at     INTEGER,
    user_updated_at     INTEGER,
    user_deleted_at     INTEGER,
    user_is_active      INTEGER,
    user_is_verified    INTEGER,
    PRIMARY KEY(user_pk)
) WITHOUT ROWID;

INSERT INTO users VALUES("09648d2920c84cdaacc40ce232557291", "Admin", "admin name", "admin@company.com", "$2b$12$aiHKkHuEZggs9IQsbqMJA.9WmPszw0CBby/VAOKFQuBgzRH/81/6u", "admin", 1712648346, 0, 0, 1, 1); 

SELECT * FROM users;