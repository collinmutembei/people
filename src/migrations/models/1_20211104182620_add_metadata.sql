-- upgrade --
ALTER TABLE "user" ADD "metadata" JSONB NOT NULL;
-- downgrade --
ALTER TABLE "user" DROP COLUMN "metadata";
