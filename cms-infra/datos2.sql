--
-- PostgreSQL database dump
--

-- Dumped from database version 13.16
-- Dumped by pg_dump version 16.2

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
-- Name: cms_24; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE cms_24 WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Spain.1252';


ALTER DATABASE cms_24 OWNER TO postgres;

\connect cms_24

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
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.django_content_type VALUES (1, 'admin', 'logentry');
INSERT INTO public.django_content_type VALUES (2, 'auth', 'permission');
INSERT INTO public.django_content_type VALUES (3, 'auth', 'group');
INSERT INTO public.django_content_type VALUES (4, 'auth', 'user');
INSERT INTO public.django_content_type VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO public.django_content_type VALUES (6, 'sessions', 'session');
INSERT INTO public.django_content_type VALUES (7, 'cms_backend', 'parametro');
INSERT INTO public.django_content_type VALUES (8, 'cms_backend', 'categoria');
INSERT INTO public.django_content_type VALUES (9, 'cms_backend', 'contenido');
INSERT INTO public.django_content_type VALUES (10, 'cms_backend', 'subcategoria');
INSERT INTO public.django_content_type VALUES (11, 'cms_backend', 'permiso');
INSERT INTO public.django_content_type VALUES (12, 'cms_backend', 'rol');
INSERT INTO public.django_content_type VALUES (13, 'cms_backend', 'usuario');
INSERT INTO public.django_content_type VALUES (14, 'cms_backend', 'comentario');
INSERT INTO public.django_content_type VALUES (15, 'cms_backend', 'like');
INSERT INTO public.django_content_type VALUES (16, 'cms_backend', 'historial');
INSERT INTO public.django_content_type VALUES (17, 'cms_backend', 'articulo');
INSERT INTO public.django_content_type VALUES (18, 'cms_backend', 'vista');


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.auth_permission VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO public.auth_permission VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO public.auth_permission VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO public.auth_permission VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO public.auth_permission VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO public.auth_permission VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO public.auth_permission VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO public.auth_permission VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO public.auth_permission VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO public.auth_permission VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO public.auth_permission VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO public.auth_permission VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO public.auth_permission VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO public.auth_permission VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO public.auth_permission VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO public.auth_permission VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO public.auth_permission VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO public.auth_permission VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO public.auth_permission VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO public.auth_permission VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO public.auth_permission VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO public.auth_permission VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO public.auth_permission VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO public.auth_permission VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO public.auth_permission VALUES (25, 'Can add parametro', 7, 'add_parametro');
INSERT INTO public.auth_permission VALUES (26, 'Can change parametro', 7, 'change_parametro');
INSERT INTO public.auth_permission VALUES (27, 'Can delete parametro', 7, 'delete_parametro');
INSERT INTO public.auth_permission VALUES (28, 'Can view parametro', 7, 'view_parametro');
INSERT INTO public.auth_permission VALUES (29, 'Can add categoria', 8, 'add_categoria');
INSERT INTO public.auth_permission VALUES (30, 'Can change categoria', 8, 'change_categoria');
INSERT INTO public.auth_permission VALUES (31, 'Can delete categoria', 8, 'delete_categoria');
INSERT INTO public.auth_permission VALUES (32, 'Can view categoria', 8, 'view_categoria');
INSERT INTO public.auth_permission VALUES (33, 'Can add contenido', 9, 'add_contenido');
INSERT INTO public.auth_permission VALUES (34, 'Can change contenido', 9, 'change_contenido');
INSERT INTO public.auth_permission VALUES (35, 'Can delete contenido', 9, 'delete_contenido');
INSERT INTO public.auth_permission VALUES (36, 'Can view contenido', 9, 'view_contenido');
INSERT INTO public.auth_permission VALUES (37, 'Can add subcategoria', 10, 'add_subcategoria');
INSERT INTO public.auth_permission VALUES (38, 'Can change subcategoria', 10, 'change_subcategoria');
INSERT INTO public.auth_permission VALUES (39, 'Can delete subcategoria', 10, 'delete_subcategoria');
INSERT INTO public.auth_permission VALUES (40, 'Can view subcategoria', 10, 'view_subcategoria');
INSERT INTO public.auth_permission VALUES (41, 'Can add permiso', 11, 'add_permiso');
INSERT INTO public.auth_permission VALUES (42, 'Can change permiso', 11, 'change_permiso');
INSERT INTO public.auth_permission VALUES (43, 'Can delete permiso', 11, 'delete_permiso');
INSERT INTO public.auth_permission VALUES (44, 'Can view permiso', 11, 'view_permiso');
INSERT INTO public.auth_permission VALUES (45, 'Can add rol', 12, 'add_rol');
INSERT INTO public.auth_permission VALUES (46, 'Can change rol', 12, 'change_rol');
INSERT INTO public.auth_permission VALUES (47, 'Can delete rol', 12, 'delete_rol');
INSERT INTO public.auth_permission VALUES (48, 'Can view rol', 12, 'view_rol');
INSERT INTO public.auth_permission VALUES (49, 'Can add usuario', 13, 'add_usuario');
INSERT INTO public.auth_permission VALUES (50, 'Can change usuario', 13, 'change_usuario');
INSERT INTO public.auth_permission VALUES (51, 'Can delete usuario', 13, 'delete_usuario');
INSERT INTO public.auth_permission VALUES (52, 'Can view usuario', 13, 'view_usuario');
INSERT INTO public.auth_permission VALUES (53, 'Can add comentario', 14, 'add_comentario');
INSERT INTO public.auth_permission VALUES (54, 'Can change comentario', 14, 'change_comentario');
INSERT INTO public.auth_permission VALUES (55, 'Can delete comentario', 14, 'delete_comentario');
INSERT INTO public.auth_permission VALUES (56, 'Can view comentario', 14, 'view_comentario');
INSERT INTO public.auth_permission VALUES (57, 'Can add like', 15, 'add_like');
INSERT INTO public.auth_permission VALUES (58, 'Can change like', 15, 'change_like');
INSERT INTO public.auth_permission VALUES (59, 'Can delete like', 15, 'delete_like');
INSERT INTO public.auth_permission VALUES (60, 'Can view like', 15, 'view_like');
INSERT INTO public.auth_permission VALUES (61, 'Can add historial', 16, 'add_historial');
INSERT INTO public.auth_permission VALUES (62, 'Can change historial', 16, 'change_historial');
INSERT INTO public.auth_permission VALUES (63, 'Can delete historial', 16, 'delete_historial');
INSERT INTO public.auth_permission VALUES (64, 'Can view historial', 16, 'view_historial');
INSERT INTO public.auth_permission VALUES (65, 'Can add articulo', 17, 'add_articulo');
INSERT INTO public.auth_permission VALUES (66, 'Can change articulo', 17, 'change_articulo');
INSERT INTO public.auth_permission VALUES (67, 'Can delete articulo', 17, 'delete_articulo');
INSERT INTO public.auth_permission VALUES (68, 'Can view articulo', 17, 'view_articulo');
INSERT INTO public.auth_permission VALUES (69, 'Can add vista', 18, 'add_vista');
INSERT INTO public.auth_permission VALUES (70, 'Can change vista', 18, 'change_vista');
INSERT INTO public.auth_permission VALUES (71, 'Can delete vista', 18, 'delete_vista');
INSERT INTO public.auth_permission VALUES (72, 'Can view vista', 18, 'view_vista');


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: cms_backend_categoria; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cms_backend_categoria VALUES (1, 'MUS', 'Música');
INSERT INTO public.cms_backend_categoria VALUES (2, 'not', 'Noticias');
INSERT INTO public.cms_backend_categoria VALUES (3, 'MOD', 'Moda');
INSERT INTO public.cms_backend_categoria VALUES (5, 'SAL', 'Salud');


--
-- Data for Name: cms_backend_subcategoria; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cms_backend_subcategoria VALUES (1, 'Internacionales', 'Noticias internacionales', 2);
INSERT INTO public.cms_backend_subcategoria VALUES (2, 'Nacionales', 'Noticias nacionales', 2);
INSERT INTO public.cms_backend_subcategoria VALUES (3, 'Pop', 'Estilo pop', 1);
INSERT INTO public.cms_backend_subcategoria VALUES (4, 'Trap', 'Estilo trap', 1);
INSERT INTO public.cms_backend_subcategoria VALUES (5, 'Rock', 'Estilo rock', 1);
INSERT INTO public.cms_backend_subcategoria VALUES (6, 'Clean look', 'Estilo de make up y cabello', 3);
INSERT INTO public.cms_backend_subcategoria VALUES (7, 'Lencería', 'ropa de lenceria', 3);
INSERT INTO public.cms_backend_subcategoria VALUES (9, 'Nutrició', 'Todo sobre buena alimentación', 5);


--
-- Data for Name: cms_backend_usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cms_backend_usuario VALUES (1, 'CEO', 'cmsa154@gmail.com');
INSERT INTO public.cms_backend_usuario VALUES (2, 'Paula', 'cmsautor@gmail.com');
INSERT INTO public.cms_backend_usuario VALUES (3, 'Enrique', 'cmseditor214@gmail.com');
INSERT INTO public.cms_backend_usuario VALUES (5, 'Ma. Luján', 'alejandralezcanosalinas@gmail.com');
INSERT INTO public.cms_backend_usuario VALUES (6, 'Jorge', 'publicadorcms@gmail.com');
INSERT INTO public.cms_backend_usuario VALUES (7, 'Alejandra', 'ma.alexa2000@fpuna.edu.py');


--
-- Data for Name: cms_backend_contenido; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cms_backend_contenido VALUES (10, 'prueba tit', 'aa', '<p>as</p>', '', 'aprobado', 'no es coherente', 4, '2024-10-31', 1);
INSERT INTO public.cms_backend_contenido VALUES (9, 'Prueba para sprint', 'una publicacion (resumen)', '<p>Publicacion de sprint 4</p>', '', 'aprobado', '', 2, '2024-10-25', 2);
INSERT INTO public.cms_backend_contenido VALUES (11, 'contenido', 'rres', '<p>contenido de prueba</p>', '', 'inactivo', '', 1, '2024-11-07', 1);
INSERT INTO public.cms_backend_contenido VALUES (7, 'El glorioso retorno del Victoria’s Secret Fashion Show', 'todo sobre la noche!', '<p>Uno de los eventos más esperados del año en el ámbito de la moda finalmente aconteció y dejó impactado a todo el mundo. Tras seis años de ausencia, el Victoria’s Secret Fashion Show retornó con sus “ángeles” con todo el brillo acostumbrado de una de las pasarelas más sensuales, cautivantes y de mayor audiencia en el globo.</p><p class="ql-align-center"><br></p><p>Entre las figuras más solicitadas del momento, como las hermanas Gigi y Bella Hadid, Bárbara Palvin o Lila Mossse, se sumaron con glamour y estilo emblemáticas modelos como Kate Moss, Eva Herzigova, Adriana Lima, Alessandra Ambrosio, Tyra Banks y Carla Bruni, que lucieron diseños más sofisticados y cómodos, sin alejarse de la sensualidad que desparrama la marca en cada fashion show.</p><p>En el Duggal Greenhouse del Brooklyn Navy Yard, donde tuvo lugar el espectáculo, desfilaron exángeles de Victoria’s Secret junto a modelos cuyos tipos de cuerpo, edad y talla no estaban representados por la marca hace una década, pero que hoy toman protagonismo con la idea de proyectar una imagen de inclusión. Esto, tras años de lidiar con fuertes críticas por fomentar un estándar de belleza poco saludable y mostrarse ajena a la diversidad. Pero el regreso fue glorioso, con un impactante show de belleza, brillo y mucho poder femenino.</p><p><em>Ashley Graham, modelo de tallas grandes y defensora de la positividad corporal</em></p><p><img src="https://www.lanacion.com.py/resizer/v2/TK6JLSRUCRADLJMGQ2LT5ASGG4.jpg?auth=7017bf9fc1ab57036035fe2e4b98f9e0eb66120b68e00b7e1b9f8cae8f821d2b&amp;width=900&amp;smart=true"></p><p><em>La supermodelo húngara Barbara Palvin, una de las más aclamadas de la noche</em></p><p><img src="https://www.lanacion.com.py/resizer/v2/Q6V6NETLCRHVBHTQ5E7LK7PCGE.jpg?auth=ed9e7cdbe6064384bf0f227ac7b24cbf9b1e140d0356d7ce3851524c7d5ca2fc&amp;width=900&amp;smart=true"></p><p><em>Gigi Hadid abrió el desfile de punta en rosa con las características alas de la marca, confeccionadas en plumas sintéticas aprobadas por PETA</em></p><p><img src="https://www.lanacion.com.py/resizer/v2/HPYMDRMIUFE73K5I2KPSSTSVUU.jpg?auth=58f4d6e815fcb5fa0071bf6bf019ad9bf13274a4638a5567ad1fc9f06220f496&amp;width=900&amp;smart=true"></p><p><em>La mítica Cher, quien a sus 78 años derrochó fuerza y carisma interpretando sus potentes canciones “Believe” y “Strong enough”</em></p><p><img src="https://www.lanacion.com.py/resizer/v2/3U5VFM3W5FCRPNS3FRJOPXFLD4.jpg?auth=e7e99242ee65eea3ede236827ffeed21d18b83d3f8e0989f028de86ea115deeb&amp;width=900&amp;smart=true"></p><p><em>Adriana Lima es una de las ángeles originales de Victoria’s Secret</em></p><p><br></p>', '', 'inactivo', '', 7, '2024-10-24', 2);
INSERT INTO public.cms_backend_contenido VALUES (8, '¡Desde G. 180.000! Atendé cómo podés comprar las entradas para el show de Chayanne ¡ya!', 'Chayanne confirmó su regreso a Paraguay después de 10 años con su gira mundial: “Bailemos Otra Vez Tour” y emocionó a los miles de fanáticos.', '<p>Mejor que nunca, regresará Chayanne a los escenarios de Latinoamérica con “Bailemos Otra Vez Tour”, después de agotar las entradas para sus shows en Estados Unidos y Canadá y de agotar en 24 horas la primera fase de ventas de su show en Costa Rica, Chayanne llevará su tan esperada gira por diversas ciudades de Latinoamérica, donde sus fans están ansiosos de disfrutar un show sin precedentes, incluyendo también a Paraguay en la misma.</p><p>Una exitosa gira global se llevo a cabo entre el 2018 y comienzos del 2020, y el intérprete de “Un Siglo sin Ti” ahora está de vuelta con una imagen fresca y absolutamente renovada y en consecuencia ha provocado cientos de miles de reacciones en redes sociales, donde se destaca su inagotable energía y entrega.</p><p>Acumula en su haber más de 50 millones de álbumes vendidos y es uno de los creadores e intérpretes con más canciones en el primer lugar de la lista Billboard Hot Latin Songs en más de 40 años de exitosa carrera. Se ha consagrado, así como uno de los mayores artistas latinos a nivel mundial y ha sido sin duda el pionero en combinar el arte del canto con el baile.</p><p>Chayanne se presentará en nuestro país el 26 de julio del próximo año en el Jockey Club e incluirá en su repertorio clásicos como “Torero” y “Dejaría Todo”, junto a nuevos éxitos como “Bailando Bachata”, “Como Tú y Yo” y “Te Amo y Punto”, con la intención de guiar a su público por un recorrido emocional a través de su música.</p><p><strong>Sobre las entradas:</strong></p><p>Se habilitará PREVENTA EXCLUSIVA para clientes de tarjetas de crédito ueno el lunes 28 desde las 10:00 h. hasta las 23:59 h. del martes 29 de octubre. en todos los puntos de TICKETEA y a través de&nbsp;<a href="https://ticketea.com.py/" rel="noopener noreferrer" target="_blank" style="color: var(--color-link-text);">www.ticketea.com.py</a>. con costos desde G. 180.000. En lo que respecta a la venta general, esta iniciará el miércoles 30 de octubre a partir de las 10:00 h. con costos desde G. 210.000. Cabe destacar que clientes de tarjetas de crédito ueno podrán acceder a beneficios también durante la venta general.</p><p>El concierto de Chayanne “Bailemos Otra Vez Tour” es apto para todo público. Menores de hasta 8 años cumplidos no abonan ingreso en los sectores no numerados: Campo Vip, Campo General y Plateas, acompañados de su adulto responsable con entrada.</p><p>Esta es un producción de G5PRO y CMN.</p>', '', 'aprobado', '[{''userId'': 1, ''comId'': 8, ''fullName'': ''CEO'', ''userProfile'': ''https://link-to-profile/cmsa154@gmail.com'', ''text'': ''quiero verle a chayanne'', ''avatarUrl'': ''https://lh3.googleusercontent.com/a/ACg8ocL06SHyqJ1glWQshwKcg2k5buY_udvo0_a8Rx4e93opc9NfUw=s96-c'', ''replies'': []}, {''userId'': 2, ''comId'': 9, ''fullName'': ''Paula'', ''userProfile'': ''https://link-to-profile/cmsautor@gmail.com'', ''text'': ''quiero ir con mi Mamaaa'', ''avatarUrl'': ''https://lh3.googleusercontent.com/a/ACg8ocKcm1ZzAc8r3INbTV0xtKaNHCa_120ZvEjWlCz6G-PuXKYrig=s96-c'', ''replies'': []}]', 3, '2024-10-25', 2);
INSERT INTO public.cms_backend_contenido VALUES (5, 'Murió Liam Payne, de One Direction: qué reveló la autopsia?', 'El músico británico, de 31 años, cayó desde un tercer piso en un hotel boutique de la calle Costa Rica al 6000.
Según un llamado del jefe de recepción al 911, el artista estaba "sobrepasado de droga y alcohol".', '<p><strong style="color: rgb(0, 0, 0);">Liam Payne</strong><span style="color: rgb(0, 0, 0);">, ex integrante de la banda británica&nbsp;</span><strong style="color: rgb(0, 0, 0);">One Direction</strong><span style="color: rgb(0, 0, 0);">, sufrió una muerte instantánea. El músico cayó del tercer piso de un hotel boutique de&nbsp;</span><strong style="color: rgb(0, 0, 0);">Palermo&nbsp;</strong><span style="color: rgb(0, 0, 0);">y, según el resultado preliminar de la autopsia, al que accedió&nbsp;</span><strong style="color: rgb(0, 0, 0);">Clarín</strong><span style="color: rgb(0, 0, 0);">, el fallecimiento fue a causa de "</span><strong style="color: rgb(0, 0, 0);">politraumatismos</strong><span style="color: rgb(0, 0, 0);">" y debido a "</span><strong style="color: rgb(0, 0, 0);">hemorragia interna y externa</strong><span style="color: rgb(0, 0, 0);">".</span></p><p><span style="color: rgb(0, 0, 0);"><img src="https://www.clarin.com/img/2024/10/16/s_SKeAUgr_600x600__1.jpg"></span></p><p><span style="color: rgb(0, 0, 0);">La pericia fue realizada a última hora del miércoles (entre las 21.45 y 23.05) en la morgue de la Corte Suprema de Justicia, que funciona desde 1908 en el predio ubicado entre las calles Viamonte y Junín.</span></p><p><span style="color: rgb(0, 0, 0);">El protocolo de autopsia, remitido a la fiscalía y firmado por los forenses&nbsp;</span><strong style="color: rgb(0, 0, 0);">Santiago Maffia Bizzozero y Roberto Víctor Cohen,&nbsp;</strong><span style="color: rgb(0, 0, 0);">concluyó que ''</span><em style="color: rgb(0, 0, 0);">la causa de muerte de Liam James Payne determinada macroscópicamente, ha sido politraumatismo, hemorragia interna y externa</em><span style="color: rgb(0, 0, 0);">", informó el Ministerio Público Fiscal.</span></p><p><br></p><p><span style="color: rgb(0, 0, 0);">"</span><em style="color: rgb(0, 0, 0);">Las lesiones craneoencefálicas tuvieron la idoneidad suficiente como para producir la muerte, mientras que las hemorragias internas y externas en cráneo, tórax, abdomen y miembros contribuyeron con el mecanismo de muerte</em><span style="color: rgb(0, 0, 0);">", agregó.</span></p><p><br></p><p><span style="color: rgb(0, 0, 0);">La muerte de Liam Payne ¿Hubo responsabilidad del hotel?</span></p><p><span style="color: rgb(0, 0, 0);">Payne, de 31 años, estaba alojado en una habitación del tercer piso del hotel&nbsp;</span><strong style="color: rgb(0, 0, 0);">Casa Sur</strong><span style="color: rgb(0, 0, 0);">, en Costa Rica al 6000. Según el llamado del jefe de recepción al 911, el artista estaba "</span><strong style="color: rgb(0, 0, 0);"><em>sobrepasado de droga y alcohol</em></strong><span style="color: rgb(0, 0, 0);">", por lo que requerían la presencia "</span><em style="color: rgb(0, 0, 0);">urgente</em><span style="color: rgb(0, 0, 0);">" en el lugar.</span></p><p><span style="color: rgb(0, 0, 0);">"</span><em style="color: rgb(0, 0, 0);">Necesitamos que nos envíen a alguien urgente porque no se si corre riesgo la vida del huésped. La habitación tiene balcón y tenemos temor a que pueda hacer algo</em><span style="color: rgb(0, 0, 0);">", expresó.</span></p><p><span style="color: rgb(0, 0, 0);">Este temor se hizo realidad, ya que Payne cayó del balcón hacia un patio interno, desde unos 14 metros, y murió.</span></p><p><span style="color: rgb(0, 0, 0);"><img src="https://www.clarin.com/img/2024/10/16/X2W0Xn1uI_720x0__1.jpg" height="480">Destrucción y drogas en la habitación que ocupó Liam Payne antes de morir.</span></p><p><span style="color: rgb(0, 0, 0);">En un comunicado, el&nbsp;</span><a href="https://www.fiscales.gob.ar/fiscalias/la-muerte-de-liam-james-payne-el-musico-fallecio-producto-de-politraumatismos-y-hemorragia-interna-y-externa/" rel="noopener noreferrer" target="_blank" style="color: rgb(0, 0, 0);">Ministerio Público Fiscal</a><span style="color: rgb(0, 0, 0);">&nbsp;señaló que se investiga una “</span><em style="color: rgb(0, 0, 0);">muerte dudosa</em><span style="color: rgb(0, 0, 0);">” y que todo parece indicar que Payne estaba solo en su habitación, "</span><strong style="color: rgb(0, 0, 0);"><em>atravesando algún tipo de brote producto del abuso de sustancias</em></strong><span style="color: rgb(0, 0, 0);">".</span></p><p><span style="color: rgb(0, 0, 0);">La Fiscalía Nacional en lo Criminal y Correccional N° 14, interinamente a cargo de Marcelo Roma, investiga el caso.</span></p><p><span style="color: rgb(0, 0, 0);">Según reconstruyeron los investigadores, todo ocurrió alrededor de las 17.07 de este miércoles.</span></p><p><span style="color: rgb(0, 0, 0);">"</span><em style="color: rgb(0, 0, 0);">La fiscalía adelantó que, más allá de reconstruir las circunstancias de la muerte del músico, la investigación también está orientada en&nbsp;</em><strong style="color: rgb(0, 0, 0);"><em>determinar la eventual intervención de terceras personas</em></strong><em style="color: rgb(0, 0, 0);">&nbsp;en los sucesos previos al deceso de la víctima</em><span style="color: rgb(0, 0, 0);">", aseguraron.</span></p><p><span style="color: rgb(0, 0, 0);">Todas las miradas apuntan por estas horas contra la persona que le podría haber proporcionado las drogas al músico para evaluar si tuvo algún grado de responsabilidad en el fatal desenlace.</span></p><p><span style="color: rgb(0, 0, 0);">El jefe del SAME, Alberto Crescenti, precisó que "presentaba lesiones gravísimas, incompatibles con la vida, producto de su caída".</span></p><p><span style="color: rgb(0, 0, 0);">"O sea, tuvimos que constatar fallecimiento, no hubo posibilidad de reanimación ni nada", explicó. Esto fue a las 17.11 del miércoles.</span></p><p><span style="color: rgb(0, 0, 0);">Ahora se espera conocer&nbsp;</span><strong style="color: rgb(0, 0, 0);">los resultados de los estudios histopatológicos, bioquímicos y toxicológicos&nbsp;</strong><span style="color: rgb(0, 0, 0);">que también se hicieron en la autopsia, para confirmar si el músico estaba drogado y alcoholizado, como se sospecha según los testimonios de quienes lo vieron en el hotel y también por lo que encontró la Policía dentro de la habitación.</span></p><p><span style="color: rgb(0, 0, 0);">En este punto, se pidió el análisis del contenido del estómago, alcohol y tóxicos en sangre, humor vítreo, bilis, hisopado nasal y orina para determinación de alcoholes y tóxicos.</span></p><p><span style="color: rgb(0, 0, 0);"><img src="https://www.clarin.com/img/2024/10/16/20GlK1P9Zw_720x0__1.jpg" height="480">La puerta del hotel, rodeada de fanáticos de Liam Payne. Foto: Enrique García Medina.</span></p><p><span style="color: rgb(0, 0, 0);">Entre otras cosas, en el cuarto había una botella de champagne y una botella de whisky semivacías. Además, pastillas (de Clonazepam y otras), un polvo blanco que sería cocaína, fragmentos de latas quemadas (que podrían haber sido usadas para fumar la droga), papel metálico, un encendedor y un teléfono celular, del que se realizarán pericias.</span></p><p><span style="color: rgb(0, 0, 0);">La habitación presentaba importantes destrozos, como la pantalla del televisor LED. Los testigos advirtieron los ruidos y avisaron a los responsables del hotel.</span></p><p><span style="color: rgb(0, 0, 0);">En la bañera de la suite Deluxe encontraron más restos de vela y papel aluminio, cuyo fondo estaba manchado y con algunas quemaduras.</span></p><p><span style="color: rgb(0, 0, 0);"><img src="https://www.clarin.com/img/2024/10/17/mEaMYitM-_720x0__1.jpg" height="480">Los fans, en la puerta del hotel. Foto: Luciano Thieberger.</span></p><p><span style="color: rgb(0, 0, 0);">Los forenses determinaron que "</span><em style="color: rgb(0, 0, 0);">las 25 lesiones descriptas en la autopsia son compatibles con aquellas producidas por caída de altura</em><span style="color: rgb(0, 0, 0);">". Y que el músico no tenía lesiones del "</span><em style="color: rgb(0, 0, 0);">tipo defensivas</em><span style="color: rgb(0, 0, 0);">" y que todas las lesiones que tenía en el cuerpo eran "</span><em style="color: rgb(0, 0, 0);">vitales y de producción contemporánea entre sí</em><span style="color: rgb(0, 0, 0);">", por lo que se descartaría la intervención de terceras personas.</span></p><p><span style="color: rgb(0, 0, 0);">Otro de los datos clave para la investigación es que, por la posición en la que encontraron el cuerpo, Payne no intentó protegerse. Por eso, consideran que habría caído en "</span><strong style="color: rgb(0, 0, 0);"><em>estado de semi o total inconsciencia</em></strong><span style="color: rgb(0, 0, 0);">".</span></p><p><span style="color: rgb(0, 0, 0);">Las declaraciones de cinco testigos se realizaron en la fiscalía y fueron de tres trabajadores del hotel y de dos mujeres que habían estado con el músico en su habitación horas antes de la tragedia.</span></p><p><span style="color: rgb(0, 0, 0);">Junto a él había estado su novia, la influencer estadounidense&nbsp;</span><strong style="color: rgb(0, 0, 0);">Kate Cassidy (25),</strong><span style="color: rgb(0, 0, 0);">&nbsp;quien se fue a Miami dos días antes de la tragedia.</span></p><p><span style="color: rgb(0, 0, 0);">El encargado comunicó que que el huésped estaba "sobrepasado de drogas".</span></p><p><span style="color: rgb(0, 0, 0);">Payne había llegado a la Ciudad de Buenos Aires para hacer una aparición en el show que dio su ex compañero de banda, el irlandés&nbsp;</span><strong style="color: rgb(0, 0, 0);">Niall Horan (31)</strong><span style="color: rgb(0, 0, 0);">, el 2 de octubre en el Movistar Arena.</span></p><p><span style="color: rgb(0, 0, 0);">Después del primer llamado al 911, el empleado del hotel volvió a contactarse y dijo: "</span><em style="color: rgb(0, 0, 0);">Tenemos a un huésped que está sobrepasado de droga y alcohol, y cuando está consciente está rompiendo toda la habitación. Necesitamos que manden a alguien, por favor</em><span style="color: rgb(0, 0, 0);">". Cuando llegaron, ya era tarde.</span></p><p><em style="color: rgb(0, 0, 0);">EMJ</em></p>', '', 'rechazado', 'tiene errrores ortograficos', 3, '2024-10-17', 2);


--
-- Data for Name: cms_backend_comentario; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cms_backend_comentario VALUES (8, 'quiero verle a chayanne', 8, 1, NULL, 'https://lh3.googleusercontent.com/a/ACg8ocL06SHyqJ1glWQshwKcg2k5buY_udvo0_a8Rx4e93opc9NfUw=s96-c');
INSERT INTO public.cms_backend_comentario VALUES (9, 'quiero ir con mi Mamaaa', 8, 2, NULL, 'https://lh3.googleusercontent.com/a/ACg8ocKcm1ZzAc8r3INbTV0xtKaNHCa_120ZvEjWlCz6G-PuXKYrig=s96-c');


--
-- Data for Name: cms_backend_historial; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cms_backend_historial VALUES (1, '2024-10-17 22:36:06.481924-03', 'Se creó el contenido', 5, 2, 'borrador');
INSERT INTO public.cms_backend_historial VALUES (2, '2024-10-17 23:49:11.511845-03', 'Se modificó el contenido', 5, 3, 'borrador');
INSERT INTO public.cms_backend_historial VALUES (3, '2024-10-17 23:52:29.400105-03', 'Se rechazó el contenido porque: No está bien redactado, volver a revisar', 5, 6, 'borrador');
INSERT INTO public.cms_backend_historial VALUES (4, '2024-10-24 22:13:12.497151-03', 'El contenido se publicó', 5, 1, 'borrador');
INSERT INTO public.cms_backend_historial VALUES (6, '2024-10-24 22:56:28.572813-03', 'Se creó el contenido', 7, 2, 'borrador');
INSERT INTO public.cms_backend_historial VALUES (7, '2024-10-24 22:58:59.036468-03', 'El contenido se publicó', 7, 6, 'borrador');
INSERT INTO public.cms_backend_historial VALUES (8, '2024-10-24 22:59:47.920773-03', 'El contenido se inactivó', 7, 6, 'borrador');
INSERT INTO public.cms_backend_historial VALUES (9, '2024-10-24 23:16:23.327053-03', 'El contenido se inactivó', 5, 6, 'borrador');
INSERT INTO public.cms_backend_historial VALUES (10, '2024-10-24 23:33:01.23001-03', 'El contenido se publicó', 7, 6, 'borrador');
INSERT INTO public.cms_backend_historial VALUES (11, '2024-10-25 13:35:29.007209-03', 'Se creó el contenido', 8, 2, 'borrador');
INSERT INTO public.cms_backend_historial VALUES (12, '2024-10-25 13:46:46.333382-03', 'El contenido se publicó', 8, 6, 'borrador');
INSERT INTO public.cms_backend_historial VALUES (13, '2024-10-25 16:11:31.970681-03', 'Se creó el contenido', 9, 2, 'borrador');
INSERT INTO public.cms_backend_historial VALUES (14, '2024-10-25 16:13:24.516647-03', 'El contenido se publicó', 9, 6, 'borrador');
INSERT INTO public.cms_backend_historial VALUES (15, '2024-10-31 00:03:44.322164-03', 'El contenido se inactivó', 9, 1, 'inactivo');
INSERT INTO public.cms_backend_historial VALUES (16, '2024-10-31 00:05:59.13335-03', 'Se creó el contenido', 10, 1, 'en_revision');
INSERT INTO public.cms_backend_historial VALUES (17, '2024-10-31 00:07:15.852973-03', 'Se rechazó el contenido porque: no es coherente', 10, 1, 'rechazado');
INSERT INTO public.cms_backend_historial VALUES (18, '2024-10-31 00:07:41.802841-03', 'Se modificó el contenido', 10, 1, 'en_revision');
INSERT INTO public.cms_backend_historial VALUES (19, '2024-10-31 00:16:01.161083-03', 'Se modificó el contenido', 10, 1, 'borrador');
INSERT INTO public.cms_backend_historial VALUES (20, '2024-10-31 00:17:59.096808-03', 'El contenido guardó en borrador', 10, 1, 'borrador');
INSERT INTO public.cms_backend_historial VALUES (21, '2024-10-31 00:18:18.386077-03', 'El contenido se envió a revisión', 10, 1, 'en_revision');
INSERT INTO public.cms_backend_historial VALUES (22, '2024-10-31 00:18:34.076061-03', 'El contenido se publicó', 10, 1, 'aprobado');
INSERT INTO public.cms_backend_historial VALUES (23, '2024-11-03 15:44:25.986355-03', 'El contenido se publicó', 5, 1, 'aprobado');
INSERT INTO public.cms_backend_historial VALUES (24, '2024-11-07 00:17:02.658767-03', 'El contenido se publicó', 9, 1, 'aprobado');
INSERT INTO public.cms_backend_historial VALUES (25, '2024-11-07 20:23:10.240426-03', 'El contenido se inactivó', 9, 1, 'inactivo');
INSERT INTO public.cms_backend_historial VALUES (26, '2024-11-07 20:33:47.435348-03', 'El contenido se inactivó', 5, 1, 'inactivo');
INSERT INTO public.cms_backend_historial VALUES (27, '2024-11-07 20:39:27.695334-03', 'El contenido se inactivó', 10, 1, 'inactivo');
INSERT INTO public.cms_backend_historial VALUES (28, '2024-11-07 20:41:17.514867-03', 'El contenido se inactivó', 8, 1, 'inactivo');
INSERT INTO public.cms_backend_historial VALUES (29, '2024-11-07 20:41:53.135652-03', 'El contenido se inactivó', 10, 1, 'inactivo');
INSERT INTO public.cms_backend_historial VALUES (30, '2024-11-07 20:43:44.280784-03', 'El contenido se inactivó', 9, 1, 'inactivo');
INSERT INTO public.cms_backend_historial VALUES (31, '2024-11-07 20:45:01.835253-03', 'El contenido se envió a revisión', 5, 1, 'en_revision');
INSERT INTO public.cms_backend_historial VALUES (32, '2024-11-07 20:45:36.341687-03', 'Se creó el contenido', 11, 1, 'en_revision');
INSERT INTO public.cms_backend_historial VALUES (33, '2024-11-07 20:45:53.544443-03', 'El contenido se envió a revisión', 11, 1, 'en_revision');
INSERT INTO public.cms_backend_historial VALUES (34, '2024-11-07 20:46:02.128059-03', 'El contenido se publicó', 11, 1, 'aprobado');
INSERT INTO public.cms_backend_historial VALUES (35, '2024-11-07 20:52:49.860326-03', 'El contenido se inactivó', 11, 1, 'inactivo');
INSERT INTO public.cms_backend_historial VALUES (36, '2024-11-07 20:55:26.391789-03', 'El contenido se inactivó', 7, 1, 'inactivo');
INSERT INTO public.cms_backend_historial VALUES (37, '2024-11-07 20:59:38.74473-03', 'Se rechazó el contenido porque: tiene errrores ortograficos', 5, 1, 'rechazado');


--
-- Data for Name: cms_backend_like; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cms_backend_like VALUES (2, '2024-10-24 23:35:35.565216-03', 7, 2);
INSERT INTO public.cms_backend_like VALUES (3, '2024-11-02 22:44:36.865147-03', 5, 1);
INSERT INTO public.cms_backend_like VALUES (4, '2024-11-02 22:45:08.654516-03', 7, 7);
INSERT INTO public.cms_backend_like VALUES (5, '2024-11-02 22:46:35.555144-03', 8, 7);
INSERT INTO public.cms_backend_like VALUES (6, '2024-11-03 13:16:01.500442-03', 7, 1);
INSERT INTO public.cms_backend_like VALUES (7, '2024-11-03 15:45:36.111971-03', 5, 5);
INSERT INTO public.cms_backend_like VALUES (8, '2024-11-07 20:21:27.156136-03', 8, 1);
INSERT INTO public.cms_backend_like VALUES (9, '2024-11-07 20:22:56.392556-03', 9, 1);
INSERT INTO public.cms_backend_like VALUES (11, '2024-11-07 20:57:08.484195-03', 8, 2);


--
-- Data for Name: cms_backend_parametro; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: cms_backend_permiso; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cms_backend_permiso VALUES (1, 'CREAR_USUARIO');
INSERT INTO public.cms_backend_permiso VALUES (2, 'EDITAR_USUARIO');
INSERT INTO public.cms_backend_permiso VALUES (3, 'EDITAR_ROL');
INSERT INTO public.cms_backend_permiso VALUES (4, 'CREAR_ROL');
INSERT INTO public.cms_backend_permiso VALUES (5, 'EDITAR_CATEGORIA');
INSERT INTO public.cms_backend_permiso VALUES (6, 'CREAR_CATEGORIA');
INSERT INTO public.cms_backend_permiso VALUES (7, 'EDITAR_CONTENIDO');
INSERT INTO public.cms_backend_permiso VALUES (8, 'CREAR_CONTENIDO');
INSERT INTO public.cms_backend_permiso VALUES (9, 'PUBLICAR_CONTENIDO');
INSERT INTO public.cms_backend_permiso VALUES (10, 'RECHAZAR_CONTENIDO');
INSERT INTO public.cms_backend_permiso VALUES (11, 'ELIMINAR_USUARIO');
INSERT INTO public.cms_backend_permiso VALUES (12, 'ELIMINAR_ROL');
INSERT INTO public.cms_backend_permiso VALUES (13, 'ELIMINAR_CATEGORIA');
INSERT INTO public.cms_backend_permiso VALUES (14, 'INACTIVAR_CONTENIDO');
INSERT INTO public.cms_backend_permiso VALUES (15, 'LISTAR_CONTENIDO');
INSERT INTO public.cms_backend_permiso VALUES (16, 'LISTAR_CATEGORIA');
INSERT INTO public.cms_backend_permiso VALUES (17, 'LISTAR_ROL');
INSERT INTO public.cms_backend_permiso VALUES (18, 'LISTAR_USUARIO');
INSERT INTO public.cms_backend_permiso VALUES (19, 'VER_PAGINA_PRINCIPAL');
INSERT INTO public.cms_backend_permiso VALUES (20, 'LISTAR_MONITOREO');


--
-- Data for Name: cms_backend_rol; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cms_backend_rol VALUES (5, 'suscriptor');
INSERT INTO public.cms_backend_rol VALUES (2, 'autor');
INSERT INTO public.cms_backend_rol VALUES (4, 'editor');
INSERT INTO public.cms_backend_rol VALUES (3, 'publicador');
INSERT INTO public.cms_backend_rol VALUES (1, 'admin');


--
-- Data for Name: cms_backend_rol_permisos; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cms_backend_rol_permisos VALUES (1, 1, 1);
INSERT INTO public.cms_backend_rol_permisos VALUES (2, 1, 2);
INSERT INTO public.cms_backend_rol_permisos VALUES (3, 1, 3);
INSERT INTO public.cms_backend_rol_permisos VALUES (4, 1, 4);
INSERT INTO public.cms_backend_rol_permisos VALUES (5, 1, 5);
INSERT INTO public.cms_backend_rol_permisos VALUES (6, 1, 6);
INSERT INTO public.cms_backend_rol_permisos VALUES (7, 1, 7);
INSERT INTO public.cms_backend_rol_permisos VALUES (8, 1, 8);
INSERT INTO public.cms_backend_rol_permisos VALUES (9, 1, 9);
INSERT INTO public.cms_backend_rol_permisos VALUES (10, 1, 10);
INSERT INTO public.cms_backend_rol_permisos VALUES (11, 1, 11);
INSERT INTO public.cms_backend_rol_permisos VALUES (12, 1, 12);
INSERT INTO public.cms_backend_rol_permisos VALUES (13, 1, 13);
INSERT INTO public.cms_backend_rol_permisos VALUES (14, 1, 14);
INSERT INTO public.cms_backend_rol_permisos VALUES (15, 1, 15);
INSERT INTO public.cms_backend_rol_permisos VALUES (16, 1, 16);
INSERT INTO public.cms_backend_rol_permisos VALUES (17, 1, 17);
INSERT INTO public.cms_backend_rol_permisos VALUES (18, 1, 18);
INSERT INTO public.cms_backend_rol_permisos VALUES (19, 1, 19);
INSERT INTO public.cms_backend_rol_permisos VALUES (20, 2, 8);
INSERT INTO public.cms_backend_rol_permisos VALUES (21, 2, 15);
INSERT INTO public.cms_backend_rol_permisos VALUES (22, 3, 9);
INSERT INTO public.cms_backend_rol_permisos VALUES (23, 3, 14);
INSERT INTO public.cms_backend_rol_permisos VALUES (24, 3, 15);
INSERT INTO public.cms_backend_rol_permisos VALUES (25, 4, 15);
INSERT INTO public.cms_backend_rol_permisos VALUES (26, 4, 7);
INSERT INTO public.cms_backend_rol_permisos VALUES (27, 5, 19);
INSERT INTO public.cms_backend_rol_permisos VALUES (28, 2, 19);
INSERT INTO public.cms_backend_rol_permisos VALUES (29, 3, 19);
INSERT INTO public.cms_backend_rol_permisos VALUES (30, 4, 19);
INSERT INTO public.cms_backend_rol_permisos VALUES (31, 3, 17);
INSERT INTO public.cms_backend_rol_permisos VALUES (32, 1, 20);


--
-- Data for Name: cms_backend_usuario_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cms_backend_usuario_roles VALUES (1, 1, 1);
INSERT INTO public.cms_backend_usuario_roles VALUES (2, 2, 2);
INSERT INTO public.cms_backend_usuario_roles VALUES (3, 3, 4);
INSERT INTO public.cms_backend_usuario_roles VALUES (5, 5, 5);
INSERT INTO public.cms_backend_usuario_roles VALUES (6, 6, 3);
INSERT INTO public.cms_backend_usuario_roles VALUES (7, 7, 5);


--
-- Data for Name: cms_backend_vista; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.cms_backend_vista VALUES (1, '2024-11-06 21:09:18.148078-03', 7, 7);
INSERT INTO public.cms_backend_vista VALUES (2, '2024-11-07 00:02:31.544912-03', 8, 7);
INSERT INTO public.cms_backend_vista VALUES (3, '2024-11-07 00:03:40.002009-03', 7, 3);
INSERT INTO public.cms_backend_vista VALUES (4, '2024-11-07 00:04:21.812081-03', 5, 2);
INSERT INTO public.cms_backend_vista VALUES (5, '2024-11-07 00:17:17.532089-03', 10, 1);
INSERT INTO public.cms_backend_vista VALUES (6, '2024-11-07 00:17:54.175038-03', 9, 1);
INSERT INTO public.cms_backend_vista VALUES (7, '2024-11-07 20:09:14.178105-03', 7, 1);
INSERT INTO public.cms_backend_vista VALUES (8, '2024-11-07 20:17:38.287433-03', 5, 1);
INSERT INTO public.cms_backend_vista VALUES (9, '2024-11-07 20:17:50.152307-03', 8, 1);
INSERT INTO public.cms_backend_vista VALUES (10, '2024-11-07 20:56:48.308411-03', 8, 2);
INSERT INTO public.cms_backend_vista VALUES (11, '2024-11-07 20:57:30.55563-03', 10, 2);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.django_migrations VALUES (1, 'contenttypes', '0001_initial', '2024-09-21 17:46:53.776681-04');
INSERT INTO public.django_migrations VALUES (2, 'auth', '0001_initial', '2024-09-21 17:46:53.953339-04');
INSERT INTO public.django_migrations VALUES (3, 'admin', '0001_initial', '2024-09-21 17:46:54.006318-04');
INSERT INTO public.django_migrations VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2024-09-21 17:46:54.010838-04');
INSERT INTO public.django_migrations VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2024-09-21 17:46:54.02463-04');
INSERT INTO public.django_migrations VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2024-09-21 17:46:54.041998-04');
INSERT INTO public.django_migrations VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2024-09-21 17:46:54.057831-04');
INSERT INTO public.django_migrations VALUES (8, 'auth', '0003_alter_user_email_max_length', '2024-09-21 17:46:54.063758-04');
INSERT INTO public.django_migrations VALUES (9, 'auth', '0004_alter_user_username_opts', '2024-09-21 17:46:54.074164-04');
INSERT INTO public.django_migrations VALUES (10, 'auth', '0005_alter_user_last_login_null', '2024-09-21 17:46:54.081691-04');
INSERT INTO public.django_migrations VALUES (11, 'auth', '0006_require_contenttypes_0002', '2024-09-21 17:46:54.082835-04');
INSERT INTO public.django_migrations VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2024-09-21 17:46:54.093448-04');
INSERT INTO public.django_migrations VALUES (13, 'auth', '0008_alter_user_username_max_length', '2024-09-21 17:46:54.115209-04');
INSERT INTO public.django_migrations VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2024-09-21 17:46:54.126604-04');
INSERT INTO public.django_migrations VALUES (15, 'auth', '0010_alter_group_name_max_length', '2024-09-21 17:46:54.139996-04');
INSERT INTO public.django_migrations VALUES (16, 'auth', '0011_update_proxy_permissions', '2024-09-21 17:46:54.149229-04');
INSERT INTO public.django_migrations VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2024-09-21 17:46:54.157496-04');
INSERT INTO public.django_migrations VALUES (18, 'cms_backend', '0001_initial', '2024-09-21 17:46:54.174473-04');
INSERT INTO public.django_migrations VALUES (19, 'cms_backend', '0002_alter_parametro_valor', '2024-09-21 17:46:54.178853-04');
INSERT INTO public.django_migrations VALUES (20, 'cms_backend', '0003_categoria', '2024-09-21 17:46:54.204476-04');
INSERT INTO public.django_migrations VALUES (21, 'cms_backend', '0004_contenido_subcategoria', '2024-09-21 17:46:54.242755-04');
INSERT INTO public.django_migrations VALUES (22, 'cms_backend', '0005_permiso_rol_usuario', '2024-09-21 17:46:54.370525-04');
INSERT INTO public.django_migrations VALUES (23, 'cms_backend', '0006_remove_usuario_last_login_remove_usuario_password', '2024-09-21 17:46:54.375225-04');
INSERT INTO public.django_migrations VALUES (24, 'cms_backend', '0007_contenido_subcategoria', '2024-09-21 17:46:54.394513-04');
INSERT INTO public.django_migrations VALUES (25, 'cms_backend', '0008_contenido_fecha', '2024-09-21 17:46:54.408631-04');
INSERT INTO public.django_migrations VALUES (26, 'cms_backend', '0009_contenido_autor', '2024-09-21 17:46:54.426999-04');
INSERT INTO public.django_migrations VALUES (27, 'sessions', '0001_initial', '2024-09-21 17:46:54.455168-04');
INSERT INTO public.django_migrations VALUES (28, 'cms_backend', '0010_comentario', '2024-10-04 13:20:01.558853-04');
INSERT INTO public.django_migrations VALUES (29, 'cms_backend', '0011_comentario_reply_to', '2024-10-04 13:20:01.580359-04');
INSERT INTO public.django_migrations VALUES (30, 'cms_backend', '0012_comentario_avatarurl', '2024-10-04 13:20:01.587589-04');
INSERT INTO public.django_migrations VALUES (31, 'cms_backend', '0013_historial', '2024-10-17 22:00:38.245801-03');
INSERT INTO public.django_migrations VALUES (32, 'cms_backend', '0014_like', '2024-10-17 22:00:38.2884-03');
INSERT INTO public.django_migrations VALUES (33, 'cms_backend', '0015_historial_estado', '2024-10-30 23:52:44.637568-03');
INSERT INTO public.django_migrations VALUES (34, 'cms_backend', '0002_vista', '2024-11-06 21:05:39.981746-03');


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 72, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, false);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: cms_backend_categoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cms_backend_categoria_id_seq', 5, true);


--
-- Name: cms_backend_comentario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cms_backend_comentario_id_seq', 9, true);


--
-- Name: cms_backend_contenido_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cms_backend_contenido_id_seq', 11, true);


--
-- Name: cms_backend_historial_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cms_backend_historial_id_seq', 37, true);


--
-- Name: cms_backend_like_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cms_backend_like_id_seq', 11, true);


--
-- Name: cms_backend_parametro_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cms_backend_parametro_id_seq', 1, false);


--
-- Name: cms_backend_permiso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cms_backend_permiso_id_seq', 20, true);


--
-- Name: cms_backend_rol_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cms_backend_rol_id_seq', 6, true);


--
-- Name: cms_backend_rol_permisos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cms_backend_rol_permisos_id_seq', 34, true);


--
-- Name: cms_backend_subcategoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cms_backend_subcategoria_id_seq', 9, true);


--
-- Name: cms_backend_usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cms_backend_usuario_id_seq', 8, true);


--
-- Name: cms_backend_usuario_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cms_backend_usuario_roles_id_seq', 9, true);


--
-- Name: cms_backend_vista_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cms_backend_vista_id_seq', 11, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 18, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 34, true);


--
-- PostgreSQL database dump complete
--

