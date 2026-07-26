--
-- PostgreSQL database dump
--

\restrict yBMdFGj7VWgBtQKfw9gttX1YP9QXkO1SSCb70j2ro7s8dRq8BkOaENtTdknoHhr

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, created_at, username, google_id) FROM stdin;
5	g.anirudh.reddy@gmail.com	2026-07-24 17:13:47.821935+05:30	Anirudh	112856064850992017988
\.


--
-- Data for Name: Group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Group" (id, name, description, created_at, updated_at, owners_id) FROM stdin;
\.


--
-- Data for Name: Tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Tasks" (id, title, content, completed, created_at, users_id, updated_at) FROM stdin;
6	SQL	Relationships	f	2026-07-22 20:50:49.898126+05:30	5	2026-07-22 21:05:48.28847+05:30
7	SQL	Relationships	f	2026-07-22 20:52:46.715188+05:30	5	2026-07-22 21:05:48.28847+05:30
8	SQL Relationships	Relationships	f	2026-07-22 20:52:56.655844+05:30	5	2026-07-22 21:05:48.28847+05:30
9	Google Auth	Add google auth to my projects	f	2026-07-24 17:21:04.591074+05:30	5	2026-07-24 17:21:04.591074+05:30
10	Add group feature	Add groups project feature	f	2026-07-24 17:30:06.041972+05:30	5	2026-07-24 17:30:06.041972+05:30
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
3bfa19e08a16
\.


--
-- Name: Group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Group_id_seq"', 1, false);


--
-- Name: Tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Tasks_id_seq"', 10, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 5, true);


--
-- PostgreSQL database dump complete
--

\unrestrict yBMdFGj7VWgBtQKfw9gttX1YP9QXkO1SSCb70j2ro7s8dRq8BkOaENtTdknoHhr

