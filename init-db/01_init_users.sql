--
-- PostgreSQL database dump
--

-- Dumped from database version 15.14 (Debian 15.14-1.pgdg13+1)
-- Dumped by pg_dump version 15.14 (Debian 15.14-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

-- Garante que a sequência está no valor correto
SELECT setval('usuarios_id_seq', (SELECT COALESCE(MAX(id), 0) FROM usuarios));

-- Insere o usuário apenas se ele não existir
INSERT INTO usuarios (id, nome, email, senha_hash, is_admin, data_criacao, foto)
VALUES (1, 'gui', 'guilhermef512435@gmail.com', 
        'pbkdf2:sha256:600000$4ugh0Diku0lguKnz$e497d896611ac2aa43761265f8b6251b8ae6828462e71269a644279a0fa91368',
        true, '2025-10-28 04:25:08.887097', 'user_1.jpg')
ON CONFLICT (id) DO NOTHING;