--
-- PostgreSQL database dump
--

-- Dumped from database version 14.18 (Homebrew)
-- Dumped by pg_dump version 14.18 (Homebrew)

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
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: newimmi_user
--

INSERT INTO public.users (id, username, email, password_hash, is_member, membership_expires, created_at) VALUES (1, 'aaa', 'zealot820514@gmail.com', 'pbkdf2:sha256:600000$w91Ia10qu9Eep87f$8686cc82712f3c515dbf52374e637fb13a28adc0a2262e307e110716641d8b01', false, NULL, '2025-07-07 20:37:36.454724');
INSERT INTO public.users (id, username, email, password_hash, is_member, membership_expires, created_at) VALUES (2, 'testuser', 'test@example.com', 'pbkdf2:sha256:600000$UsPiwbF6v96IMSCl$5945efbbc553f04b59ede852a7b9958ce67541bce30e2842576a3561178722bb', false, NULL, '2025-07-07 20:57:07.464006');
INSERT INTO public.users (id, username, email, password_hash, is_member, membership_expires, created_at) VALUES (3, 'testuser2', 'test2@example.com', 'pbkdf2:sha256:600000$H8Lf1GZFBpgWTQb1$e1056d5dcff7f3017df40da5c578b5c5baf82fc81cdd5622a095d0fc91134a59', false, NULL, '2025-07-07 21:01:42.282088');
INSERT INTO public.users (id, username, email, password_hash, is_member, membership_expires, created_at) VALUES (4, 'testuser4', 'test4@example.com', 'pbkdf2:sha256:600000$iJy5HjP1H8cVwqB1$a5bc92f248f566104298630377c490ac67fba96b488ce2214ae041d9d07d642d', false, NULL, '2025-07-07 21:03:45.575651');
INSERT INTO public.users (id, username, email, password_hash, is_member, membership_expires, created_at) VALUES (5, 'aaa2132312', 'dfaf@fdfaf.com', 'pbkdf2:sha256:600000$9oqDrAv7tdNRqoGC$880395ca64cf21d51e17333307085598220a4728773a142bf1433ecbf2ac14e3', false, NULL, '2025-07-07 21:09:27.424029');
INSERT INTO public.users (id, username, email, password_hash, is_member, membership_expires, created_at) VALUES (6, 'gagas', 'fdfgfda@fdas.com', 'pbkdf2:sha256:600000$SlaJn0pBlkquN3FI$f7e10c107bc491017f99253a8f9eb48653dcd2161ff77cd8497edc73eac26cd9', false, NULL, '2025-07-07 21:10:08.530722');
INSERT INTO public.users (id, username, email, password_hash, is_member, membership_expires, created_at) VALUES (7, 'qw', 'qw@afd.com', 'pbkdf2:sha256:600000$0KOeZhrrlfluyZr1$a71f684e5e0c9a296ab05ab705719d336aac4e894d012db92a8d2aa741d89203', false, NULL, '2025-07-08 16:10:40.374822');
INSERT INTO public.users (id, username, email, password_hash, is_member, membership_expires, created_at) VALUES (8, 'zx', 'zx@fdaf', 'pbkdf2:sha256:600000$0uQ9CHUveMrMhvht$1cf3db23f349142c326d9ba3b225163029dd796dde3f7eb2e08b07d5944916b0', false, NULL, '2025-07-08 17:07:06.342164');
INSERT INTO public.users (id, username, email, password_hash, is_member, membership_expires, created_at) VALUES (9, 'admin', 'admin@example.com', 'pbkdf2:sha256:600000$RLZypFBHzHfuMRJM$cc30e4d07866ca63edaeef660a377053c032f37ca9b6ddf146610193c830c00d', true, '2026-07-09 15:49:33.125569', '2025-07-09 19:49:33.126336');
INSERT INTO public.users (id, username, email, password_hash, is_member, membership_expires, created_at) VALUES (10, 'testuser1', 'user1@example.com', 'pbkdf2:sha256:600000$VR4s5PiwycKzP67c$c407abd614d353b7a0cc8d437e17e994d177a8d90f1e914d7b6d1917f3c1c731', true, '2026-07-09 15:49:33.176748', '2025-07-09 19:49:33.177097');
INSERT INTO public.users (id, username, email, password_hash, is_member, membership_expires, created_at) VALUES (11, 'vipuser', 'vip@example.com', 'pbkdf2:sha256:600000$0RAFweJxwAUhGA1A$813f016c6a956ebf5126eb0f99c04b83b77b5242f555aacc1e43d621e8b64e31', true, '2026-07-09 15:49:33.223012', '2025-07-09 19:49:33.223208');


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: newimmi_user
--



--
-- Data for Name: rent_info; Type: TABLE DATA; Schema: public; Owner: newimmi_user
--

INSERT INTO public.rent_info (id, zipcode, address, content) VALUES (2, '77072', '10910 Sharpview Dr, Houston, TX 77072', '房东姓刘，名gui zhou 。这里的居住条件太差，房间小，车库和后院都是搭建的。最重要一点，房子里面到处都是虫，各种蟑螂、蜘蛛、爬虫，后院还有马蜂。就是这样所以房子不好租，房东想法设法让你长租，然后你住了一段时间发现受不了了，不想租了。这个时候他就利用之前强迫的长租想法设法扣你押金。');
INSERT INTO public.rent_info (id, zipcode, address, content) VALUES (4, '91732', '11622 Hemlock St, El Monte, CA 91732', '房东是一群广东人，女房东姓Tan。这个房子比较老，设施设备都很旧。所在的地方也是老墨区，治安不太好。房东会让你最好拿现金租房。然后会想方设法让你长租，如果你住了一段时间受不了了不想住了，就想方设法扣你押金。');
INSERT INTO public.rent_info (id, zipcode, address, content) VALUES (5, '90660', '9073 Catherine St, Pico Rivera, CA 90660', '房东是两个上海人，女的叫Cui Xia，典型的老上海人，精明刻薄。这是一个联排别墅townhouse, 房东住在三层，一、二层出租，如果住在这里，你就准备遭罪吧。二层的灶是不让用的，要用使用完就要清理得一尘不染。卫生要搞得非常干净，搞不干净就要扣你押金。然后也是想方设法要你长租，你一旦受不了了不租了，就想方设法扣你押金。此外房东还会进你的房间偷东西，然后他把房子全部装上监控，防止你偷他东西，哈哈哈。');
INSERT INTO public.rent_info (id, zipcode, address, content) VALUES (6, '91103', '2001 Linda Vista Ave, Pasadena, CA 91103', '房东韩国人，名字是 Song geon Hyung。房子面对高速，非常吵。房东歧视中国人，如果你住在这里，就准备接受高丽棒子的吹毛求疵吧。而且这一家韩国人作息时间都不规律，晚上经常开party到深夜，那酸爽。。。');
INSERT INTO public.rent_info (id, zipcode, address, content) VALUES (7, '91780', '5832 Golden West Ave, Temple City, CA 91780', '房东是一对夫妻。这套房子住了4、5个房东的亲戚，两个七八十岁老人早上7点就开始嚎叫。老头在外面捡破烂，堆在院子里，厨房地上堆满烂咸菜。房子有蟑螂。押金找各种理由不退，地上有根头发都要扣钱。');
INSERT INTO public.rent_info (id, zipcode, address, content) VALUES (8, '91733', '2600 Marybeth Ave, South El Monte, CA 91733', '房东是60多岁夫妻。退房时找各种理由恶意克扣押金。说什么多用了电，还有给房间刷漆，还污蔑租客抽大麻，无所不用其极，想方设法克扣押金。');
INSERT INTO public.rent_info (id, zipcode, address, content) VALUES (9, '91745', '15417 Los Robles Ave, Hacienda Heights, CA 91745', '房东叫 Benjamin Chen和Catherine Yu。这对房东经常在家开party, 吵的人无法休息。而且变态房东还会性骚扰租客！在你退房的时候想法设法克扣你的押金，比如说要粉刷，要修地板，要换马桶。');
INSERT INTO public.rent_info (id, zipcode, address, content) VALUES (10, '92704', '1130 S Douglas St, Santa Ana, CA 92704', '房东真实姓ING, 自称annie。三房一厅两卫。房东租房前不说不能在家洗衣服，租进去以后不让洗衣服，百般刁难租客。不管多热不能开空调。几乎和每一个租客吵架，不签合同，一不高兴就赶人而且以各种理由不退押金。');


--
-- Data for Name: work_info; Type: TABLE DATA; Schema: public; Owner: newimmi_user
--

INSERT INTO public.work_info (id, name, zipcode, address, content) VALUES (1, '中国餐馆golden wall', NULL, '914 Canal St New Orleans, LA 70112', '这个餐馆老板是福州人，叫一个老员工管理。管理的人对下面干活的人总是催你“快一点，快一点”，和催命鬼一样，看到你在休息就跟要了他的命一样。');
INSERT INTO public.work_info (id, name, zipcode, address, content) VALUES (2, '中国餐馆火锅店香天下x-pot', NULL, '18558 Gale Ave, Suite 122-128,  Rowland Heights, CA 91748', '这个火锅店虽然做的很大，金玉其外败絮其中。洛杉矶店的老板是个年轻的男的，姓杨，牛的不得了，骂起手下来一口一个“弱智”。火锅的调料都是中国进口的垃圾食品，少部分油还是过期的。店里的海鲜不新鲜了就打折处理卖给顾客。花了大钱在营销上，抖音、tiktok等等到处做广告，给自己员工吃的伙食像猪食一样。');
INSERT INTO public.work_info (id, name, zipcode, address, content) VALUES (3, 'blue sail logistics LLC', NULL, NULL, '公司老板自称 Charlie。整个公司其实只有他一个人，其它资料都是虚假的。你给他工作，一开始他会每周给你付款，过了几周以后，就可以找借口什么资金周转困难，家中有事等等，反正就是不会再付你钱了。');
INSERT INTO public.work_info (id, name, zipcode, address, content) VALUES (4, '卡车公司BUFU Investment INC.', NULL, NULL, '老板开了两家卡车公司，拖欠仓库租金，拖欠员工工资，拖欠修车公司的修车费。');
INSERT INTO public.work_info (id, name, zipcode, address, content) VALUES (5, '卡车公司CangShan INC.', NULL, NULL, '老板开了两家卡车公司，拖欠仓库租金，拖欠员工工资，拖欠修车公司的修车费。');
INSERT INTO public.work_info (id, name, zipcode, address, content) VALUES (6, '私家侦探猎狐者FoxHunter', NULL, NULL, '通过google找到这个网站，是个诈骗公司，拿了钱不做事。');


--
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: newimmi_user
--

SELECT pg_catalog.setval('public.payments_id_seq', 2, true);


--
-- Name: rent_info_id_seq; Type: SEQUENCE SET; Schema: public; Owner: newimmi_user
--

SELECT pg_catalog.setval('public.rent_info_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: newimmi_user
--

SELECT pg_catalog.setval('public.users_id_seq', 11, true);


--
-- Name: work_info_id_seq; Type: SEQUENCE SET; Schema: public; Owner: newimmi_user
--

SELECT pg_catalog.setval('public.work_info_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

