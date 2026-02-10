BEGIN;

-- 1. Cria o Usuário na tabela de autenticação (SocialEntity)
INSERT INTO socialentities_socialentity (
    id, 
    password, 
    last_login, 
    is_superuser, 
    username, 
    first_name, 
    last_name, 
    is_staff, 
    is_active, 
    date_joined, 
    email
) 
VALUES (
    '3184d1b0-e883-4b9b-a84c-d92701bbbfaf', 
    -- Se você souber a senha desse hash abaixo, mantenha.
    -- Se não souber, troque por este hash (senha = admin): 
    -- 'pbkdf2_sha256$260000$123456$jIq... (gerar localmente é mais seguro)'
    'pbkdf2_sha256$1000000$7pIVx5e1cuz6ZeRqLsiw61$uvY1xqryTqv6R5OxY+llYCvT05lnqIS/K+HHWIuWL1c=', 
    NULL, 
    true, 
    'Renzo Fraga', 
    'Renzo', 
    'Fraga', 
    true, 
    true, 
    NOW(), 
    'kenkomarinho@gmail.com'
);

-- 2. Cria o perfil na sua tabela customizada (MercadoSorcery)
INSERT INTO mercadosorcery_usuario (user_id, cpf, imagem, role)
VALUES (
    '3184d1b0-e883-4b9b-a84c-d92701bbbfaf', -- Tem que ser o mesmo UUID de cima
    NULL,
    NULL,
    'admin'
);

COMMIT;