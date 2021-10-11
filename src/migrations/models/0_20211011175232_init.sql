-- upgrade --
CREATE TABLE IF NOT EXISTS "user" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(255) NOT NULL,
    "is_active" INT NOT NULL  DEFAULT 1,
    "is_superuser" INT NOT NULL  DEFAULT 0,
    "is_verified" INT NOT NULL  DEFAULT 0,
    "name" VARCHAR(50) NOT NULL,
    "birthdate" DATE
);
CREATE INDEX IF NOT EXISTS "idx_user_email_1b4f1c" ON "user" ("email");
CREATE TABLE IF NOT EXISTS "socialnetwork" (
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(20) NOT NULL UNIQUE,
    "domain" VARCHAR(50),
    "account_prefix" VARCHAR(30)
);
CREATE TABLE IF NOT EXISTS "socialaccount" (
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" VARCHAR(20) NOT NULL UNIQUE,
    "network_id" INT NOT NULL REFERENCES "socialnetwork" ("id") ON DELETE CASCADE,
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_socialaccou_usernam_c7b09a" UNIQUE ("username", "network_id")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSON NOT NULL
);
