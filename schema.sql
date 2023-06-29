-- postgreSQL
CREATE TABLE account (
    account_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE TABLE post (
    post_id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    source VARCHAR(255),
    score INTEGER NOT NULL,
    fav_count INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    rating CHAR(1) NOT NULL DEFAULT 's',
    FOREIGN KEY (account_id) REFERENCES account(account_id)
);

CREATE TABLE image (
    image_id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    preview_url VARCHAR(255) NOT NULL,
    sample_url VARCHAR(255) NOT NULL,
    original_url VARCHAR(255) NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    FOREIGN KEY (post_id) REFERENCES post(post_id) ON DELETE CASCADE
);

CREATE TABLE tag (
    tag_id SERIAL PRIMARY KEY,
    type INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    count INTEGER NOT NULL
);

CREATE TABLE post_tag (
    post_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tag(tag_id) ON DELETE CASCADE
);

CREATE TABLE comment (
    comment_id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL,
    parent_id INTEGER,
    account_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    FOREIGN KEY (post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES comment(comment_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES account(account_id)
);

CREATE TABLE vote (
    post_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    value INTEGER NOT NULL,
    PRIMARY KEY (post_id, account_id),
    FOREIGN KEY (post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES account(account_id)
);

CREATE TABLE favorite (
    post_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    PRIMARY KEY (post_id, account_id),
    FOREIGN KEY (post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES account(account_id)
);