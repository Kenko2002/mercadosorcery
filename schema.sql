BEGIN;

--
-- 1. Create model ContentType (CORRIGIDO: Removido campo 'name')
--
CREATE TABLE "django_content_type" ("id" SERIAL PRIMARY KEY, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");

--
-- 2. Create model Group and Permission
--
CREATE TABLE "auth_group" ("id" SERIAL PRIMARY KEY, "name" varchar(80) NOT NULL UNIQUE);
CREATE TABLE "auth_permission" ("id" SERIAL PRIMARY KEY, "name" varchar(50) NOT NULL, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL);
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "django_content_type" ("id");

--
-- 3. Create model SocialEntity (User) - ID IS UUID
--
CREATE TABLE "socialentities_socialentity" ("password" varchar(128) NOT NULL, "last_login" TIMESTAMP WITH TIME ZONE NULL, "is_superuser" boolean NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "is_staff" boolean NOT NULL, "is_active" boolean NOT NULL, "date_joined" TIMESTAMP WITH TIME ZONE NOT NULL, "email" varchar(254) NOT NULL UNIQUE, "id" UUID NOT NULL PRIMARY KEY);

--
-- 4. Create M2M table for Group and Permission
--
CREATE TABLE "auth_group_permissions" ("id" SERIAL PRIMARY KEY, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");

--
-- 5. Create M2M tables for SocialEntity
--
CREATE TABLE "socialentities_socialentity_groups" ("id" SERIAL PRIMARY KEY, "socialentity_id" UUID NOT NULL REFERENCES "socialentities_socialentity" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "socialentities_socialentity_user_permissions" ("id" SERIAL PRIMARY KEY, "socialentity_id" UUID NOT NULL REFERENCES "socialentities_socialentity" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "socialentities_socialentity_groups_socialentity_id_group_id_df0a8e8d_uniq" ON "socialentities_socialentity_groups" ("socialentity_id", "group_id");
CREATE INDEX "socialentities_socialentity_groups_socialentity_id_f3918721" ON "socialentities_socialentity_groups" ("socialentity_id");
CREATE INDEX "socialentities_socialentity_groups_group_id_97cf9d73" ON "socialentities_socialentity_groups" ("group_id");
CREATE UNIQUE INDEX "socialentities_socialentity_user_permissions_socialentity_id_permission_id_78b6ed86_uniq" ON "socialentities_socialentity_user_permissions" ("socialentity_id", "permission_id");
CREATE INDEX "socialentities_socialentity_user_permissions_socialentity_id_ef4d6a51" ON "socialentities_socialentity_user_permissions" ("socialentity_id");
CREATE INDEX "socialentities_socialentity_user_permissions_permission_id_92e62932" ON "socialentities_socialentity_user_permissions" ("permission_id");

--
-- 6. Create model LogEntry
--
CREATE TABLE "django_admin_log" ("id" SERIAL PRIMARY KEY, "action_time" TIMESTAMP WITH TIME ZONE NOT NULL, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint NOT NULL CHECK (action_flag >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" UUID NOT NULL REFERENCES "socialentities_socialentity" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");

--
-- 7. Create models from mercadosorcery app (TUDO UUID)
--

CREATE TABLE "mercadosorcery_carta" ("id" SERIAL PRIMARY KEY, "nome" varchar(255) NOT NULL, "printing" varchar(10) NOT NULL, "imagem" varchar(512) NULL, "mana_cost" varchar(50) NOT NULL, "cmc" double precision NOT NULL, "type_line" varchar(255) NOT NULL, "oracle_text" text NOT NULL, "power" varchar(10) NOT NULL, "toughness" varchar(10) NOT NULL, "rarity" varchar(50) NOT NULL);

CREATE TABLE "mercadosorcery_colecao" ("id" SERIAL PRIMARY KEY, "usuario_id" UUID NOT NULL UNIQUE REFERENCES "socialentities_socialentity" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "mercadosorcery_lista" ("id" SERIAL PRIMARY KEY, "nome" varchar(100) NOT NULL, "usuario_id" UUID NOT NULL REFERENCES "socialentities_socialentity" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "mercadosorcery_posse" ("id" SERIAL PRIMARY KEY, "estado_carta" varchar(2) NOT NULL, "status" varchar(20) NOT NULL, "preco_usd" NUMERIC NULL, "carta_id" bigint NOT NULL REFERENCES "mercadosorcery_carta" ("id") DEFERRABLE INITIALLY DEFERRED, "colecao_id" bigint NOT NULL REFERENCES "mercadosorcery_colecao" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "mercadosorcery_lista_cartas" ("id" SERIAL PRIMARY KEY, "lista_id" bigint NOT NULL REFERENCES "mercadosorcery_lista" ("id") DEFERRABLE INITIALLY DEFERRED, "posse_id" bigint NOT NULL REFERENCES "mercadosorcery_posse" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "mercadosorcery_usuario" ("user_id" UUID NOT NULL PRIMARY KEY REFERENCES "socialentities_socialentity" ("id") DEFERRABLE INITIALLY DEFERRED, "cpf" varchar(11) NULL UNIQUE, "imagem" varchar(100) NULL, "role" varchar(50) NULL);

--
-- 8. Create model Session
--
CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" TIMESTAMP WITH TIME ZONE NOT NULL);
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");

COMMIT;