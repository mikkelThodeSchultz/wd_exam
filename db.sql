CREATE TABLE users (
    user_pk             VARCHAR(255) NOT NULL,
    user_username        VARCHAR(255) NOT NULL,
    user_email          VARCHAR(255) UNIQUE NOT NULL,
    user_password       VARBINARY(255) NOT NULL,
    user_role           VARCHAR(50) NOT NULL,
    user_created_at     INT DEFAULT 0,
    user_updated_at     INT DEFAULT 0,
    user_deleted_at     INT DEFAULT 0,
    user_is_verified     TINYINT DEFAULT 0,
    user_is_blocked      TINYINT DEFAULT 0,
    user_verification_key VARCHAR(255),
    PRIMARY KEY (user_pk)
);

CREATE TABLE password_reset (
    user_pk             VARCHAR(255),
    reset_token         VARCHAR(255) UNIQUE NOT NULL,
    created_at          INT DEFAULT 0,
    FOREIGN KEY (user_pk) REFERENCES users(user_pk) ON DELETE CASCADE
);

CREATE TABLE houses (
    house_pk                VARCHAR(255) NOT NULL,
    house_name              VARCHAR(255) NOT NULL,
    house_description       TEXT,
    house_price_per_night   DECIMAL(10, 2),
    house_latitude          DECIMAL(10, 8),
    house_longitude         DECIMAL(11, 8),
    house_stars             DECIMAL(2, 1),
    house_created_at        INT DEFAULT 0,
    house_updated_at        INT DEFAULT 0,
    house_is_blocked        TINYINT DEFAULT 0,
    user_pk                 VARCHAR(255),
    PRIMARY KEY (house_pk),
    FOREIGN KEY (user_pk) REFERENCES users(user_pk)
);

CREATE TABLE house_images (
    house_pk                VARCHAR(255),
    image_url               VARCHAR(255),
    PRIMARY KEY (house_pk, image_url),
    FOREIGN KEY (house_pk) REFERENCES houses(house_pk)
);

-- Insert data
INSERT INTO users (user_pk, user_username, user_email, user_password, user_role, user_created_at, user_updated_at, user_deleted_at, user_is_verified, user_is_blocked, user_verification_key)
VALUES
("09648d2920c84cdaacc40ce232557291", "Admin", "admin@company.com", UNHEX('24326224313224775137576f436d676b6f32794861664a4f354a5734754a6847684b726e526478423163775166413351375162764d6c70596e503236'), "admin", 1690000000, 1690000000, 0, 1, 0, '123'),
("09648d2920c83edaadc40ce232557291", "Partner", "partner@company.com", UNHEX('24326224313224775137576f436d676b6f32794861664a4f354a5734754a6847684b726e526478423163775166413351375162764d6c70596e503236'), "partner", 1690000000, 1690000000, 0, 1, 0, '123'),
("09648d2920c83edabdc40ce232557291", "Customer", "customer@company.com", UNHEX('24326224313224775137576f436d676b6f32794861664a4f354a5734754a6847684b726e526478423163775166413351375162764d6c70596e503236'), "customer", 1690000000, 1690000000, 0, 1, 0, '123');

INSERT INTO houses (house_pk, house_name, house_description, house_price_per_night, house_latitude, house_longitude, house_stars, house_created_at, house_updated_at, house_is_blocked, user_pk)
VALUES
('6f187675-8b42-4bc3-bab4-394d584b07af', 'Nyhvan', "Nestled in the heart of a vibrant city, this cozy house offers a peaceful retreat from the bustling streets. With its charming architecture and inviting ambiance, you'll feel right at home the moment you step through the door. Enjoy the spacious living areas, modern amenities, and lush garden oasis, perfect for relaxing or entertaining guests. Whether you're exploring the nearby attractions or simply unwinding in your own private sanctuary, this house promises an unforgettable stay.", 250000.00, 55.6794, 12.5918, 4.5, 1690000000, 1690000000, 0, "09648d2920c83edaadc40ce232557291"),
('a0a597fc-bf7f-4fb4-bb90-8c192158cf4c', 'Tivoli', "Perched atop a picturesque hillside, this stunning house boasts panoramic views of rolling hills and sparkling waters. Step inside to discover elegant interiors adorned with luxurious furnishings and stylish decor. The spacious bedrooms offer plush bedding and breathtaking vistas, while the gourmet kitchen is a chef's dream come true. Outside, the expansive terrace is an ideal spot for al fresco dining or soaking up the sun. With its unbeatable location and unparalleled beauty, this house is truly a hidden gem.", 350000.00, 55.6736, 12.5681, 3.4, 1690000000, 1690000000, 0, "09648d2920c83edaadc40ce232557291"),
('f2d3d6fa-f168-44ed-8aef-61e187fdb2ec', 'Christiansborg', "Experience the ultimate beachfront getaway at this charming coastal retreat. Just steps away from the sandy shores and azure waters, this house offers the perfect blend of comfort and convenience. Spend your days lounging on the sun-kissed deck, swimming in the crystal-clear ocean, or exploring the nearby attractions. Inside, the airy interiors feature coastal-inspired decor and modern amenities, creating a tranquil haven for relaxation. Whether you're seeking adventure or serenity, this house has everything you need for an unforgettable beach vacation.", 180000.00, 55.6761, 12.5770, 5.0, 1690000000, 1690000000, 0, "09648d2920c83edaadc40ce232557291");

INSERT INTO house_images (house_pk, image_url)
VALUES
('6f187675-8b42-4bc3-bab4-394d584b07af', 'images/5dbce622fa2b4f22a6f6957d07ff4910.webp'),
('6f187675-8b42-4bc3-bab4-394d584b07af', 'images/5dbce622fa2b4f22a6f6957d07ff4951.webp'),
('a0a597fc-bf7f-4fb4-bb90-8c192158cf4c', 'images/5dbce622fa2b4f22a6f6957d07ff4952.webp'),
('f2d3d6fa-f168-44ed-8aef-61e187fdb2ec', 'images/5dbce622fa2b4f22a6f6957d07ff4953.webp'),
('f2d3d6fa-f168-44ed-8aef-61e187fdb2ec', 'images/5dbce622fa2b4f22a6f6957d07ff4954.webp');

-- Sample SELECT statements
SELECT * FROM users;
SELECT * FROM houses;
SELECT * FROM password_reset;

