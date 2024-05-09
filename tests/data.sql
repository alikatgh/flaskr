INSERT INTO user (username, password)
VALUES ('test', 'pbkdf2:sha256:150000$3Z3Z3Z3Z$'),
       ('other', 'pbkdf2:sha256:150000$3Z3Z3Z3Z$');

INSERT INTO post(title, body, author_id, created)
VALUES 
    ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');