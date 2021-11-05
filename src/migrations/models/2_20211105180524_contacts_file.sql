-- upgrade --
CREATE TABLE IF NOT EXISTS "contactsfile" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "uploaded_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "contactsfile";
