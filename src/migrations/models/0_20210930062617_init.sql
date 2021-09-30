-- upgrade --
CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(255) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_superuser" BOOL NOT NULL  DEFAULT False,
    "is_verified" BOOL NOT NULL  DEFAULT False,
    "birthdate" DATE
);
CREATE INDEX IF NOT EXISTS "idx_user_email_1b4f1c" ON "user" ("email");
CREATE TABLE IF NOT EXISTS "socialaccountservice" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "domain" VARCHAR(50),
    "provider" VARCHAR(9) NOT NULL
);
COMMENT ON COLUMN "socialaccountservice"."provider" IS 'FACEBOOK: facebook\nTWITTER: twitter\nINSTAGRAM: instagram\nTIKTOK: tiktok\nYOUTUBE: youtube';
CREATE TABLE IF NOT EXISTS "socialaccount" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "address" VARCHAR(20) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "service_id" INT NOT NULL REFERENCES "socialaccountservice" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
