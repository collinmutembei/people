-- upgrade --
ALTER TABLE "socialaccount" ALTER COLUMN "modified_at" SET NOT NULL;
ALTER TABLE "socialaccount" ALTER COLUMN "created_at" SET NOT NULL;
ALTER TABLE "socialnetwork" ALTER COLUMN "modified_at" SET NOT NULL;
ALTER TABLE "socialnetwork" ALTER COLUMN "created_at" SET NOT NULL;
-- downgrade --
ALTER TABLE "socialaccount" ALTER COLUMN "modified_at" DROP NOT NULL;
ALTER TABLE "socialaccount" ALTER COLUMN "created_at" DROP NOT NULL;
ALTER TABLE "socialnetwork" ALTER COLUMN "modified_at" DROP NOT NULL;
ALTER TABLE "socialnetwork" ALTER COLUMN "created_at" DROP NOT NULL;
