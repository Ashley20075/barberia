-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: barberspringfield_db
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `administracion_sitio`
--

DROP TABLE IF EXISTS `administracion_sitio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `administracion_sitio` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre_marca` varchar(100) NOT NULL,
  `eslogan` varchar(200) NOT NULL,
  `hero_titulo` varchar(200) NOT NULL,
  `hero_descripcion` longtext NOT NULL,
  `hero_imagen_1_url` varchar(200) NOT NULL,
  `hero_imagen_2_url` varchar(200) NOT NULL,
  `hero_imagen_3_url` varchar(200) NOT NULL,
  `servicios_titulo` varchar(150) NOT NULL,
  `servicios_subtitulo` varchar(255) NOT NULL,
  `barberos_titulo` varchar(150) NOT NULL,
  `barberos_subtitulo` varchar(255) NOT NULL,
  `nosotros_titulo` varchar(200) NOT NULL,
  `nosotros_parrafo_1` longtext NOT NULL,
  `nosotros_parrafo_2` longtext NOT NULL,
  `nosotros_punto_1` varchar(150) NOT NULL,
  `nosotros_punto_2` varchar(150) NOT NULL,
  `nosotros_punto_3` varchar(150) NOT NULL,
  `nosotros_imagen_url` varchar(200) NOT NULL,
  `testimonios_titulo` varchar(150) NOT NULL,
  `testimonios_subtitulo` varchar(255) NOT NULL,
  `testimonio_1` longtext NOT NULL,
  `testimonio_1_autor` varchar(100) NOT NULL,
  `testimonio_2` longtext NOT NULL,
  `testimonio_2_autor` varchar(100) NOT NULL,
  `testimonio_3` longtext NOT NULL,
  `testimonio_3_autor` varchar(100) NOT NULL,
  `cta_titulo` varchar(200) NOT NULL,
  `cta_descripcion` longtext NOT NULL,
  `cta_boton` varchar(80) NOT NULL,
  `footer_descripcion` longtext NOT NULL,
  `horario` longtext NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `telefono` varchar(50) NOT NULL,
  `email` varchar(254) NOT NULL,
  `noticias_titulo` varchar(100) NOT NULL,
  `noticias_descripcion` longtext NOT NULL,
  `copyright_texto` varchar(255) NOT NULL,
  `actualizado` datetime(6) NOT NULL,
  `hero_imagen_1_archivo` varchar(100) DEFAULT NULL,
  `hero_imagen_1_fuente` varchar(10) NOT NULL,
  `hero_imagen_2_archivo` varchar(100) DEFAULT NULL,
  `hero_imagen_2_fuente` varchar(10) NOT NULL,
  `hero_imagen_3_archivo` varchar(100) DEFAULT NULL,
  `hero_imagen_3_fuente` varchar(10) NOT NULL,
  `nosotros_imagen_archivo` varchar(100) DEFAULT NULL,
  `nosotros_imagen_fuente` varchar(10) NOT NULL,
  `mapa_embed_url` varchar(200) NOT NULL,
  `fachada_imagen_url` varchar(200) NOT NULL,
  `fachada_imagen_archivo` varchar(100) DEFAULT NULL,
  `fachada_imagen_fuente` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administracion_sitio`
--

LOCK TABLES `administracion_sitio` WRITE;
/*!40000 ALTER TABLE `administracion_sitio` DISABLE KEYS */;
INSERT INTO `administracion_sitio` VALUES (1,'BarberSpringfield','✂️ CORTES CON PERSONALIDAD','Estilo & Elegancia','Vive la experiencia de una barbería tradicional con técnicas modernas. Atención personalizada, ambiente único y los mejores acabados.','https://i.pinimg.com/1200x/91/d6/03/91d6037c183ccc9644cdd59a70857524.jpg','https://images.unsplash.com/photo-1599351431202-1e0f0137899a?q=80&w=1200&auto=format&fit=crop','https://images.unsplash.com/photo-1517832606299-7ae9b720a186?q=80&w=1200&auto=format&fit=crop','Servicios Populares','Cada corte, cada arreglo, hecho con precisión y dedicación','Nuestros Barberos','Profesionales apasionados por su arte','Más que una barbería, un legado','Desde 2012, BarberSpringfield es el punto de encuentro para los hombres que valoran la estética, la tradición y la buena conversación.','Con un ambiente que fusiona lo vintage con lo moderno, cada visita es una experiencia sensorial.','Profesionales certificados','Productos premium importados','Higiene y esterilización garantizada','https://www.beautymarket.es/imagen/min35798.jpg','Lo que dicen nuestros clientes','Más de 500 reseñas nos respaldan','Excelente servicio, el barbero entendió exactamente lo que quería.','Javier M.','Llevo años buscando un lugar así. El corte Fade perfecto. 100% recomendado.','Andrés L.','La mejor barbería de la zona. Precios justos y te dan una cerveza mientras esperas.','Camila R.','¿Listo para un cambio de look?','Reserva tu cita ahora y obtén un 15% de descuento en tu primer corte.','Reservar mi espacio','Cortes modernos, atención personalizada y calidad garantizada.','Lun - Vie: 9:00 AM - 8:00 PM\r\nSábados: 10:00 AM - 6:00 PM\r\nDomingos: Cerrado','Calle 36B Sur # 5-50','+57 301 234 5678','barberspringfield@gmail.com','Noticias','Promociones y tips de cuidado masculino.','© 2025 BarberSpringfield | Estilo & Elegancia - Todos los derechos reservados','2026-09-23 03:24:42.234000','home/b1.jpeg','archivo','home/b2.jpeg','archivo','','url','home/b2_ezDQgc7.jpeg','archivo','https://www.google.com/maps?q=4.5621815%2C-74.1041294&output=embed','','home/fachada_barberia.jpeg','archivo');
/*!40000 ALTER TABLE `administracion_sitio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (3,'Barberos');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add cita',7,'add_cita'),(26,'Can change cita',7,'change_cita'),(27,'Can delete cita',7,'delete_cita'),(28,'Can view cita',7,'view_cita'),(29,'Can add servicio',8,'add_servicio'),(30,'Can change servicio',8,'change_servicio'),(31,'Can delete servicio',8,'delete_servicio'),(32,'Can view servicio',8,'view_servicio'),(33,'Can add Suscriptor al newsletter',9,'add_suscriptornewsletter'),(34,'Can change Suscriptor al newsletter',9,'change_suscriptornewsletter'),(35,'Can delete Suscriptor al newsletter',9,'delete_suscriptornewsletter'),(36,'Can view Suscriptor al newsletter',9,'view_suscriptornewsletter'),(37,'Can add Barbero',10,'add_barbero'),(38,'Can change Barbero',10,'change_barbero'),(39,'Can delete Barbero',10,'delete_barbero'),(40,'Can view Barbero',10,'view_barbero'),(41,'Can add Cliente',11,'add_cliente'),(42,'Can change Cliente',11,'change_cliente'),(43,'Can delete Cliente',11,'delete_cliente'),(44,'Can view Cliente',11,'view_cliente'),(45,'Can add perfil',12,'add_perfil'),(46,'Can change perfil',12,'change_perfil'),(47,'Can delete perfil',12,'delete_perfil'),(48,'Can view perfil',12,'view_perfil'),(49,'Can add Contenido de inicio',13,'add_sitio'),(50,'Can change Contenido de inicio',13,'change_sitio'),(51,'Can delete Contenido de inicio',13,'delete_sitio'),(52,'Can view Contenido de inicio',13,'view_sitio'),(53,'Can add producto',14,'add_producto'),(54,'Can change producto',14,'change_producto'),(55,'Can delete producto',14,'delete_producto'),(56,'Can view producto',14,'view_producto'),(57,'Can add movimiento inventario',15,'add_movimientoinventario'),(58,'Can change movimiento inventario',15,'change_movimientoinventario'),(59,'Can delete movimiento inventario',15,'delete_movimientoinventario'),(60,'Can view movimiento inventario',15,'view_movimientoinventario'),(61,'Can add Cuenta de Google conectada',16,'add_cuentagoogle'),(62,'Can change Cuenta de Google conectada',16,'change_cuentagoogle'),(63,'Can delete Cuenta de Google conectada',16,'delete_cuentagoogle'),(64,'Can view Cuenta de Google conectada',16,'view_cuentagoogle'),(65,'Can add Evento de Google Calendar por cita',17,'add_citaeventogoogle'),(66,'Can change Evento de Google Calendar por cita',17,'change_citaeventogoogle'),(67,'Can delete Evento de Google Calendar por cita',17,'delete_citaeventogoogle'),(68,'Can view Evento de Google Calendar por cita',17,'view_citaeventogoogle'),(69,'Can add Notificación',18,'add_notificacion'),(70,'Can change Notificación',18,'change_notificacion'),(71,'Can delete Notificación',18,'delete_notificacion'),(72,'Can view Notificación',18,'view_notificacion'),(73,'Can add Suscripción a turno',19,'add_suscripcionturno'),(74,'Can change Suscripción a turno',19,'change_suscripcionturno'),(75,'Can delete Suscripción a turno',19,'delete_suscripcionturno'),(76,'Can view Suscripción a turno',19,'view_suscripcionturno');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (19,'pbkdf2_sha256$1500000$HBTJbqTCDa74rAiXZ0WRE2$5BaaEkyCX1rmLAorVx/Eb2I4OqmHkQPl6u/ZsPo18vw=','2026-10-07 14:20:37.969000',1,'nicool','','','nicool@gmail.com',1,1,'2026-06-25 12:15:30.504000'),(20,'pbkdf2_sha256$1500000$O7yyKmBeO3bn9HDOYzh2qI$e8NSc6xfKJOm/Z5xBwPgDb1sPDDi9d47h5UIWbuRz3w=','2026-09-23 16:30:25.689000',0,'yampol@gmail.com','Yampol','Bonilla','yampol@gmail.com',0,1,'2026-07-31 06:51:21.573000'),(21,'pbkdf2_sha256$1500000$VOFqgMFCnAMR5smVhmVxGe$l6elE6rXogF2n9xplFaKquFfF90T9IQEoVB3KjPn8TE=','2026-09-23 16:27:06.336000',0,'camilo@gmail.com','camilo','ladino','camilo@gmail.com',0,1,'2026-07-31 08:35:22.166000'),(22,'pbkdf2_sha256$1500000$ZeJ3VOQJnoCQfR9GS2HrdT$rm/0MxyHF8GmV8nholCRten1XVTpsYqc0LEKfXnAkPM=','2026-10-07 16:18:26.419000',0,'samuel@gmail.com','samuel','tellez','samuel@gmail.com',0,1,'2026-08-03 03:00:50.547000'),(23,'pbkdf2_sha256$1500000$jqa7v5LegMRzvFmPaDxjia$Q2zCVqHdBac3/kPO6pnB7hfb2KeauOZsJXcwN8v+Wms=','2026-09-07 00:48:43.647000',0,'alex@gmail.com','Alex','Rodriguez','alex@gmail.com',0,0,'2026-08-04 23:48:15.276000'),(24,'pbkdf2_sha256$1500000$xoKPOnNKA4GLz3hzhNtxhq$QZ8i/zASiq8kh7cFt025NEBKRA3/oc/PTMQIt8+4oCc=','2026-09-23 16:30:40.004000',0,'felipe@gmail.com','Felipe','Casas','felipe@gmail.com',0,1,'2026-08-04 23:50:54.968000'),(25,'pbkdf2_sha256$1500000$2dpmjUWxRvQnRiiyQqkz0h$07GH4vLz7LdGhTn7EKz4McrQ2SlCUmvxXBUbKfIWTdM=','2026-10-07 13:25:06.185000',0,'jeison@gmail.com','Jeison','Cruz','jeison@gmail.com',0,1,'2026-08-05 11:59:55.999000'),(26,'pbkdf2_sha256$1500000$wNUFqSwLWIE2EEySQA4wAY$EfRevfN+m5FRQSAD/dUaxtA1Pl7UaLC7AlMliIkSKSY=','2026-09-23 00:34:05.997000',0,'juan@gmail.com','Juan','Carlos','juan@gmail.com',0,1,'2026-09-16 14:50:42.226000'),(27,'pbkdf2_sha256$1500000$G7Ioc3xXN7vpUddA5kmSda$mSUyMnp1j6aQIpC3cbh+8Ka3OrZWcLsqF8r56Nj3Xb4=','2026-09-22 22:40:50.249000',1,'felipead','','','felipe@gmail.com',1,1,'2026-09-22 22:10:50.233000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (7,24,3),(8,25,3),(9,26,3);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `barberos_barbero`
--

DROP TABLE IF EXISTS `barberos_barbero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `barberos_barbero` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `cedula` varchar(20) NOT NULL,
  `especialidad` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `dia_descanso` varchar(3) NOT NULL,
  `dias_laborales` varchar(50) NOT NULL,
  `duracion_cita` int(11) NOT NULL,
  `jornada_fin` time(6) NOT NULL,
  `jornada_inicio` time(6) NOT NULL,
  `tiempo_entre_citas` int(11) NOT NULL,
  `imagen_url` varchar(200) NOT NULL,
  `calificacion` decimal(2,1) NOT NULL,
  `numero_resenas` int(10) unsigned NOT NULL CHECK (`numero_resenas` >= 0),
  `instagram` varchar(200) NOT NULL,
  `facebook` varchar(200) NOT NULL,
  `whatsapp` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cedula` (`cedula`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `barberos_barbero`
--

LOCK TABLES `barberos_barbero` WRITE;
/*!40000 ALTER TABLE `barberos_barbero` DISABLE KEYS */;
INSERT INTO `barberos_barbero` VALUES (9,'Jeison Cruz','8965342','General','98752176','jeison@gmail.com','2026-08-05 12:07:40.536000',1,'DOM','LUN,MAR,MIE,JUE,VIE,SAB',30,'18:00:00.000000','08:00:00.000000',15,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPYtMev0mwPWV5P8RZLWaCH0phOAurFw4TGAtP8sa7TDkK3y1iP1S4NuU&s=10',5.0,0,'','',''),(12,'Felipe Casas','45238976','General','08725148','felipe@gmail.com','2026-09-16 14:32:35.414000',1,'DOM','LUN,MAR,MIE,JUE,VIE,SAB',30,'18:00:00.000000','08:00:00.000000',15,'',5.0,0,'','',''),(16,'Juan Carlos','56874320','General','','juan@gmail.com','2026-09-23 00:33:41.927000',1,'DOM','LUN,MAR,MIE,JUE,VIE,SAB',30,'18:00:00.000000','08:00:00.000000',15,'',5.0,0,'','',''),(17,'felipe casas','5654324564','General','3432343234','felipecasas69@gmail.com','2026-09-23 15:10:47.578000',1,'DOM','LUN,MAR,MIE,JUE,VIE,SAB',30,'18:00:00.000000','08:00:00.000000',15,'',5.0,0,'','','');
/*!40000 ALTER TABLE `barberos_barbero` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `citas_cita`
--

DROP TABLE IF EXISTS `citas_cita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `citas_cita` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `cliente_id` bigint(20) NOT NULL,
  `servicio_id` bigint(20) NOT NULL,
  `hora` varchar(20) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `barbero_id` bigint(20) DEFAULT NULL,
  `fecha` date NOT NULL,
  `adicionales` varchar(200) NOT NULL,
  `productos` varchar(200) NOT NULL,
  `duracion_total` int(10) unsigned NOT NULL CHECK (`duracion_total` >= 0),
  `recordatorio_enviado` tinyint(1) NOT NULL,
  `historial_archivado` tinyint(1) NOT NULL,
  `analisis_ia` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`analisis_ia`)),
  PRIMARY KEY (`id`),
  KEY `citas_cita_barbero_id_341c5323` (`barbero_id`),
  KEY `citas_cita_cliente_id_c277d0e3` (`cliente_id`),
  KEY `citas_cita_servicio_id_e2034bca` (`servicio_id`),
  CONSTRAINT `citas_cita_barbero_id_341c5323_fk_barberos_barbero_id` FOREIGN KEY (`barbero_id`) REFERENCES `barberos_barbero` (`id`),
  CONSTRAINT `citas_cita_cliente_id_c277d0e3_fk_clientes_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `clientes_cliente` (`id`),
  CONSTRAINT `citas_cita_servicio_id_e2034bca_fk` FOREIGN KEY (`servicio_id`) REFERENCES `citas_servicio` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=123 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `citas_cita`
--

LOCK TABLES `citas_cita` WRITE;
/*!40000 ALTER TABLE `citas_cita` DISABLE KEYS */;
INSERT INTO `citas_cita` VALUES (36,23,6,'08:00 AM','Finalizada',NULL,'2026-08-04','Cejas, Diseño y líneas','Ninguno',45,0,1,'{}'),(37,23,6,'08:00 AM','Finalizada',NULL,'2026-08-05','Cejas, Diseño y líneas','Ninguno',45,0,1,'{}'),(38,21,6,'08:00 AM','Cancelada',NULL,'2026-08-05','Cejas, Diseño y líneas','Ninguno',45,0,1,'{}'),(39,25,6,'08:00 AM','Finalizada',NULL,'2026-08-05','Cejas, Diseño y líneas','Ninguno',45,0,1,'{}'),(40,25,6,'08:00 AM','Cancelada',NULL,'2026-08-05','Cejas, Diseño y líneas','Ninguno',45,0,1,'{}'),(41,23,6,'09:00 AM','Finalizada',NULL,'2026-08-27','Cejas, Diseño y líneas','Ninguno',45,0,1,'{}'),(42,23,2,'08:00 AM','Cancelada',NULL,'2026-08-06','Ninguno','Ninguno',35,0,1,'{}'),(43,23,2,'08:00 AM','Finalizada',NULL,'2026-08-05','Ninguno','Ninguno',35,0,1,'{}'),(44,23,2,'08:00 AM','Cancelada',NULL,'2026-08-11','Ninguno','Ninguno',35,0,1,'{}'),(45,23,6,'08:00 AM','Cancelada',NULL,'2026-08-11','Cejas, Diseño y líneas','Ninguno',45,0,1,'{}'),(46,23,5,'01:15 PM','Cancelada',NULL,'2026-08-11','Cejas','Ninguno',40,1,1,'{}'),(47,23,2,'08:00 AM','Cancelada',NULL,'2026-08-12','Cejas, Diseño y líneas','Ninguno',45,0,1,'{}'),(48,25,2,'08:00 AM','Cancelada',9,'2026-08-12','Arreglo de barba, Cejas, Diseño y líneas','Ninguno',50,0,1,'{}'),(49,25,2,'01:15 PM','Pendiente',NULL,'2026-08-12','Ninguno','Ninguno',35,1,0,'{}'),(50,23,6,'08:00 AM','Cancelada',NULL,'2026-08-12','Cejas','Ninguno',40,0,1,'{}'),(51,23,6,'08:00 AM','Cancelada',NULL,'2026-08-12','Cejas','Ninguno',40,0,1,'{}'),(52,23,2,'08:00 AM','Cancelada',NULL,'2026-08-12','Cejas','Ninguno',40,0,1,'{}'),(53,23,2,'08:00 AM','Cancelada',NULL,'2026-08-12','Ninguno','Ninguno',35,0,1,'{}'),(54,23,6,'09:00 AM','Cancelada',NULL,'2026-08-12','Ninguno','Ninguno',35,0,1,'{}'),(55,23,2,'09:00 AM','Cancelada',NULL,'2026-08-12','Ninguno','Ninguno',35,1,1,'{}'),(57,23,6,'11:15 AM','Cancelada',NULL,'2026-08-21','Ninguno','Ninguno',35,1,1,'{}'),(60,24,2,'08:00 AM','Cancelada',NULL,'2020-01-01','Ninguno','Ninguno',30,0,1,'{}'),(61,24,2,'08:00 AM','Cancelada',NULL,'2020-01-02','Ninguno','Ninguno',30,0,1,'{}'),(62,24,2,'08:00 AM','Cancelada',NULL,'2020-01-03','Ninguno','Ninguno',30,0,1,'{}'),(63,24,2,'08:00 AM','Cancelada',NULL,'2020-01-04','Ninguno','Ninguno',30,0,1,'{}'),(64,24,2,'08:00 AM','Cancelada',NULL,'2020-01-05','Ninguno','Ninguno',30,0,1,'{}'),(65,24,2,'08:00 AM','Cancelada',NULL,'2020-01-06','Ninguno','Ninguno',30,0,1,'{}'),(66,24,2,'08:00 AM','Cancelada',NULL,'2020-01-07','Ninguno','Ninguno',30,0,1,'{}'),(67,24,2,'08:00 AM','Cancelada',NULL,'2020-01-08','Ninguno','Ninguno',30,0,1,'{}'),(68,24,2,'08:00 AM','Cancelada',NULL,'2020-01-09','Ninguno','Ninguno',30,0,1,'{}'),(69,24,2,'08:00 AM','Cancelada',NULL,'2020-01-10','Ninguno','Ninguno',30,0,1,'{}'),(70,24,2,'08:00 AM','Cancelada',NULL,'2020-01-11','Ninguno','Ninguno',30,0,1,'{}'),(71,24,2,'08:00 AM','Cancelada',NULL,'2020-01-12','Ninguno','Ninguno',30,0,1,'{}'),(72,24,2,'08:00 AM','Cancelada',NULL,'2020-01-13','Ninguno','Ninguno',30,0,1,'{}'),(73,24,2,'08:00 AM','Cancelada',NULL,'2020-01-14','Ninguno','Ninguno',30,0,1,'{}'),(74,24,2,'08:00 AM','Cancelada',NULL,'2020-01-15','Ninguno','Ninguno',30,0,1,'{}'),(75,21,2,'09:45 AM','Cancelada',12,'2026-09-16','Arreglo de barba','Ninguno',40,0,1,'{}'),(76,23,6,'08:00 AM','Cancelada',9,'2026-09-17','Arreglo de barba','Ninguno',40,0,1,'{}'),(77,21,5,'08:00 AM','Cancelada',12,'2026-09-16','Arreglo de barba','Ninguno',40,0,1,'{}'),(78,22,2,'09:00 AM','Cancelada',12,'2026-09-16','Arreglo de barba','Ninguno',40,0,0,'{}'),(79,22,6,'11:45 AM','Cancelada',9,'2026-09-16','Cejas','Ninguno',40,0,1,'{}'),(80,21,3,'08:00 AM','Cancelada',9,'2026-09-16','Cejas','Ninguno',40,0,1,'{}'),(81,21,6,'08:00 AM','Cancelada',9,'2026-09-16','Cejas','Ninguno',40,0,1,'{}'),(82,21,2,'08:00 AM','Cancelada',9,'2026-09-16','Cejas','Ninguno',40,0,1,'{}'),(83,21,5,'08:00 AM','Cancelada',9,'2026-09-16','Cejas','Ninguno',40,0,1,'{}'),(84,21,2,'10:30 AM','Cancelada',9,'2026-09-17','Ninguno','Ninguno',35,0,1,'{}'),(85,23,2,'09:20 AM','Cancelada',9,'2026-09-19','Ninguno','Ninguno',40,0,1,'{}'),(86,21,2,'09:20 AM','Cancelada',9,'2026-09-18','Ninguno','Ninguno',40,0,1,'{}'),(87,23,2,'08:00 AM','Cancelada',9,'2026-09-18','Ninguno','Ninguno',40,0,1,'{}'),(88,23,6,'09:30 AM','Cancelada',12,'2026-09-23','Arreglo de barba','Ninguno',45,0,1,'{}'),(89,23,3,'11:40 AM','Cancelada',12,'2026-09-22','Arreglo de barba, Cejas, Diseño y líneas','Ninguno',55,0,1,'{}'),(90,22,2,'10:45 AM','Cancelada',9,'2026-09-18','Arreglo de barba, Cejas, Diseño y líneas','Ninguno',55,0,0,'{}'),(91,23,4,'08:00 AM','Cancelada',12,'2026-09-19','Arreglo de barba','Ninguno',45,0,1,'{}'),(92,23,2,'08:00 AM','Finalizada',12,'2026-09-19','Arreglo de barba, Cejas','Ninguno',50,0,1,'{\"observaciones\": [\"Cabello corto con estilo rapado en los laterales y ligeramente m\\u00e1s largo en la parte superior.\", \"L\\u00ednea del cabello frontal visible y definida.\", \"Textura de cabello liso y corto.\", \"Rostro con estructura angulosa y mand\\u00edbula marcada.\"], \"recomendaciones\": [{\"nombre\": \"Buzz Cut\", \"motivo\": \"Mantiene la practicidad del estilo actual y complementa la estructura angulosa del rostro.\", \"mantenimiento\": \"Bajo\", \"pedido_barbero\": \"Un corte rapado uniforme en toda la cabeza, n\\u00famero 2 en los lados y 3 arriba.\"}, {\"nombre\": \"Crop Texturizado\", \"motivo\": \"Aporta un toque moderno aprovechando la longitud superior para dar algo de textura frontal.\", \"mantenimiento\": \"Medio\", \"pedido_barbero\": \"Degradado bajo en los laterales, manteniendo textura y un poco de longitud en la parte superior para peinar hacia adelante.\"}, {\"nombre\": \"Fade Cl\\u00e1sico\", \"motivo\": \"Define los contornos laterales manteniendo la parte superior limpia y de f\\u00e1cil manejo.\", \"mantenimiento\": \"Medio\", \"pedido_barbero\": \"Un desvanecido lateral limpio desde la piel, dejando la parte superior corta y ordenada.\"}], \"aviso\": \"Estas son recomendaciones orientativas y el resultado final debe ser validado por tu barbero.\"}'),(93,21,2,'08:50 AM','Confirmada',12,'2026-09-19','Arreglo de barba, Cejas','Ninguno',50,0,0,'{\"observaciones\": [\"Cabello muy corto con textura densa y apariencia uniforme.\", \"L\\u00ednea del cabello frontal bien definida y recta.\", \"Estilo actual rapado al ras con bajo volumen visible.\"], \"recomendaciones\": [{\"nombre\": \"Buzz Cut con desvanecido\", \"motivo\": \"Mantiene la longitud corta actual a\\u00f1adiendo un detalle moderno en los laterales con degradado.\", \"mantenimiento\": \"Bajo\", \"pedido_barbero\": \"Un buzz cut uniforme arriba con un desvanecimiento medio en los costados y la nuca.\"}, {\"nombre\": \"Cesar corto\", \"motivo\": \"Permite conservar los laterales cortos mientras se deja ligeramente m\\u00e1s longitud y definici\\u00f3n en la l\\u00ednea frontal.\", \"mantenimiento\": \"Medio\", \"pedido_barbero\": \"Corte estilo Cesar corto con textura arriba y una l\\u00ednea frontal recta bien marcada.\"}, {\"nombre\": \"Rapado completo al cero\", \"motivo\": \"Una opci\\u00f3n cl\\u00e1sica y limpia que aprovecha la forma natural de la cabeza y la estructura visible.\", \"mantenimiento\": \"Bajo\", \"pedido_barbero\": \"Rapado total al cero en toda la cabeza sin transiciones.\"}], \"aviso\": \"Estas son recomendaciones orientativas y el barbero debe validar el resultado final.\"}'),(94,22,4,'02:00 PM','Finalizada',12,'2026-09-23','Ninguno','Ninguno',40,0,0,'{}'),(95,23,4,'12:10 PM','Finalizada',12,'2026-09-23','Cejas, Diseño y líneas','Ninguno',50,0,1,'{}'),(96,23,2,'10:00 AM','Finalizada',12,'2026-09-23','Ninguno','Ninguno',40,0,1,'{}'),(97,23,4,'10:00 AM','Finalizada',12,'2026-09-24','Ninguno','Ninguno',40,0,1,'{}'),(98,23,2,'08:00 AM','Finalizada',12,'2026-09-25','Ninguno','Ninguno',40,0,1,'{}'),(99,23,2,'08:00 AM','Finalizada',12,'2026-09-26','Ninguno','Ninguno',40,0,1,'{}'),(100,23,2,'08:00 AM','Finalizada',12,'2026-09-28','Ninguno','Ninguno',40,0,1,'{}'),(101,23,2,'08:00 AM','Finalizada',12,'2026-09-29','Ninguno','Ninguno',40,0,1,'{}'),(102,23,2,'08:00 AM','Finalizada',12,'2026-09-30','Ninguno','Ninguno',40,0,1,'{}'),(103,23,2,'08:00 AM','Finalizada',12,'2026-10-01','Ninguno','Ninguno',40,0,1,'{}'),(104,23,2,'08:00 AM','Finalizada',12,'2026-10-02','Ninguno','Ninguno',40,0,1,'{}'),(105,22,2,'10:00 AM','Finalizada',12,'2026-09-23','Ninguno','Ninguno',40,0,0,'{}'),(106,22,2,'08:00 AM','Finalizada',12,'2026-09-24','Ninguno','Ninguno',40,0,0,'{}'),(107,22,2,'08:00 AM','Finalizada',12,'2026-09-25','Ninguno','Ninguno',40,0,0,'{}'),(108,22,2,'08:00 AM','Finalizada',12,'2026-09-26','Ninguno','Ninguno',40,0,0,'{}'),(109,22,2,'08:00 AM','Finalizada',12,'2026-09-28','Ninguno','Ninguno',40,0,0,'{}'),(110,22,2,'08:00 AM','Finalizada',12,'2026-09-29','Ninguno','Ninguno',40,0,0,'{}'),(111,22,2,'08:00 AM','Finalizada',12,'2026-09-30','Ninguno','Ninguno',40,0,0,'{}'),(112,22,2,'08:00 AM','Finalizada',12,'2026-10-01','Ninguno','Ninguno',40,0,0,'{}'),(113,22,2,'08:00 AM','Finalizada',12,'2026-10-02','Ninguno','Ninguno',40,0,0,'{}'),(114,22,2,'08:00 AM','Cancelada',12,'2026-10-07','Ninguno','Ninguno',40,0,0,'{}'),(115,22,2,'08:00 AM','Finalizada',12,'2026-09-24','Ninguno','Ninguno',40,0,0,'{}'),(118,23,4,'01:00 PM','Cancelada',12,'2026-09-25','Arreglo de barba, Cejas','Ninguno',50,0,1,'{}'),(119,22,2,'11:20 AM','Pendiente',12,'2026-09-23','Cejas, Diseño y líneas','Ninguno',50,0,0,'{}'),(120,23,2,'08:45 AM','Cancelada',12,'2026-10-07','Cejas','Ninguno',45,0,1,'{}'),(121,23,2,'08:00 AM','Finalizada',12,'2026-10-07','Ninguno','Ninguno',40,0,1,'{}'),(122,23,2,'08:40 AM','Cancelada',9,'2026-10-07','Ninguno','Ninguno',40,0,1,'{}');
/*!40000 ALTER TABLE `citas_cita` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `citas_servicio`
--

DROP TABLE IF EXISTS `citas_servicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `citas_servicio` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `precio` int(10) unsigned NOT NULL,
  `duracion` int(10) unsigned NOT NULL,
  `imagen` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `citas_servicio_duracion_ae8c1a6d_check` CHECK (`duracion` >= 0),
  CONSTRAINT `citas_servicio_precio_3520d973_check` CHECK (`precio` >= 0)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `citas_servicio`
--

LOCK TABLES `citas_servicio` WRITE;
/*!40000 ALTER TABLE `citas_servicio` DISABLE KEYS */;
INSERT INTO `citas_servicio` VALUES (2,'Mullet','Corto por los lados, largo por detras. Estilo retro moderno con mucha personalidad.',18000,40,'https://i.imgur.com/k1iWPM0.jpg'),(3,'Corte Clasico','Tu le explicas al barbero lo que quieres. Corte personalizado a tu medida.',18000,45,'https://i.imgur.com/XlGkJ10.jpg'),(4,'Buzz Cut','Muy corto y parejo en toda la cabeza. Fresco, limpio y de bajo mantenimiento.',18000,30,'https://i.imgur.com/ZSb52bD.jpg'),(5,'Corte Texturizado','Con capas y movimiento natural. Ideal para cabello rizado o con volumen.',18000,45,'https://i.imgur.com/OKGKQfq.jpg'),(6,'Taper Fade','Degradado limpio desde la sien hasta la nuca. El corte más pedido del momento.',18000,40,'https://i.imgur.com/aplGgFF.jpg'),(9,'Adicionales','Cejas-\r\nDiseño\r\n-Barba',5000,5,'https://i.imgur.com/Ls8ndQr.png');
/*!40000 ALTER TABLE `citas_servicio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `citas_suscriptornewsletter`
--

DROP TABLE IF EXISTS `citas_suscriptornewsletter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `citas_suscriptornewsletter` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `creado` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `citas_suscriptornewsletter`
--

LOCK TABLES `citas_suscriptornewsletter` WRITE;
/*!40000 ALTER TABLE `citas_suscriptornewsletter` DISABLE KEYS */;
/*!40000 ALTER TABLE `citas_suscriptornewsletter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes_cliente`
--

DROP TABLE IF EXISTS `clientes_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clientes_cliente` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `cedula` varchar(20) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `correo_confirmado` tinyint(1) NOT NULL,
  `cortes_completados` int(10) unsigned NOT NULL CHECK (`cortes_completados` >= 0),
  `cortes_para_recompensa` int(10) unsigned NOT NULL CHECK (`cortes_para_recompensa` >= 0),
  `recompensas_disponibles` int(10) unsigned NOT NULL CHECK (`recompensas_disponibles` >= 0),
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `cedula` (`cedula`),
  CONSTRAINT `clientes_cliente_user_id_a58c2f33_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes_cliente`
--

LOCK TABLES `clientes_cliente` WRITE;
/*!40000 ALTER TABLE `clientes_cliente` DISABLE KEYS */;
INSERT INTO `clientes_cliente` VALUES (6,'nicool','','','nicool@gmail.com','2026-07-02 11:58:14.773000',1,19,1,0,0,0),(21,'Yampol Bonilla','10123456789','3016052994','yampol@gmail.com','2026-07-31 06:51:22.405000',1,20,1,0,0,0),(22,'camilo ladino','121448515','3215448455','camilo@gmail.com','2026-07-31 08:35:22.879000',1,21,1,0,0,0),(23,'samuel tellez','1016717153','3219215407','samuel@gmail.com','2026-08-03 03:00:57.296000',1,22,1,0,0,0),(24,'Alex Rodriguez','5623478','1234567890','alex@gmail.com','2026-08-04 23:48:19.815000',1,23,1,0,0,0),(25,'Felipe Casas','45238976','08725148','felipe@gmail.com','2026-08-04 23:50:59.704000',1,24,1,0,0,0),(26,'Jeison Cruz','8965342','98752176','jeison@gmail.com','2026-08-05 11:59:57.188000',1,25,1,0,0,0),(32,'Juan Carlos','56874320','','juan@gmail.com','2026-09-16 14:50:43.248000',1,26,1,0,0,0);
/*!40000 ALTER TABLE `clientes_cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-06-25 13:20:52.312000','1','Taper Fade',1,'[{\"added\": {}}]',8,19),(2,'2026-06-25 13:21:44.962000','2','Mullet',1,'[{\"added\": {}}]',8,19),(3,'2026-06-25 13:22:53.194000','3','Corte Clasico',1,'[{\"added\": {}}]',8,19),(4,'2026-06-25 13:24:03.300000','4','Buzz Cut',1,'[{\"added\": {}}]',8,19),(5,'2026-06-25 13:24:50.659000','5','Corte Texturizado',1,'[{\"added\": {}}]',8,19),(6,'2026-09-16 14:52:30.116000','13','Juan Carlos',1,'[{\"added\": {}}]',10,19),(7,'2026-09-16 15:13:53.989000','13','Juan Carlos',3,'',10,19),(8,'2026-09-22 14:43:12.398000','32','nicoole@gmail.com',3,'',4,19),(9,'2026-09-22 14:43:12.398000','34','nicoolperdomo752@gmail.com',3,'',4,19),(10,'2026-09-22 14:43:12.398000','33','tellezsamuel2102@gmail.com',3,'',4,19),(11,'2026-09-22 14:44:07.756000','36','tellezsamuel2102@gmail.com',3,'',4,19),(12,'2026-09-22 22:41:27.705000','5','Corte Texturizado',2,'[{\"changed\": {\"fields\": [\"Imagen\"]}}]',8,27),(13,'2026-09-22 22:41:29.439000','5','Corte Texturizado',2,'[]',8,27),(14,'2026-09-22 22:41:43.837000','9','Adicionales',2,'[{\"changed\": {\"fields\": [\"Imagen\"]}}]',8,27),(15,'2026-09-22 22:41:45.563000','9','Adicionales',2,'[]',8,27),(16,'2026-09-22 22:41:55.954000','4','Buzz Cut',2,'[{\"changed\": {\"fields\": [\"Imagen\"]}}]',8,27),(17,'2026-09-22 22:41:57.155000','4','Buzz Cut',2,'[]',8,27),(18,'2026-09-22 22:42:09.536000','3','Corte Clasico',2,'[{\"changed\": {\"fields\": [\"Imagen\"]}}]',8,27),(19,'2026-09-22 22:42:11.695000','3','Corte Clasico',2,'[]',8,27),(20,'2026-09-22 22:42:34.488000','2','Mullet',2,'[{\"changed\": {\"fields\": [\"Imagen\"]}}]',8,27),(21,'2026-09-22 22:42:35.602000','2','Mullet',2,'[]',8,27),(22,'2026-09-22 22:42:52.775000','6','Taper Fade',2,'[{\"changed\": {\"fields\": [\"Imagen\"]}}]',8,27),(23,'2026-09-22 22:42:54.082000','6','Taper Fade',2,'[]',8,27),(24,'2026-09-22 22:42:58.124000','5','Corte Texturizado',2,'[]',8,27),(25,'2026-09-23 15:28:32.521000','41','felipecasas69@gmail.com',3,'',4,19),(26,'2026-09-23 15:28:32.521000','40','ladinodilan57@gmail.com',3,'',4,19),(27,'2026-09-23 15:28:32.521000','37','nicoolperdomo300@gmail.com',3,'',4,19),(28,'2026-09-23 15:28:32.521000','42','nicoolperdomo752@gmail.com',3,'',4,19),(29,'2026-09-23 15:28:32.521000','38','tellezsamuel2102@gmail.com',3,'',4,19),(30,'2026-09-23 15:28:36.222000','41','felipecasas69@gmail.com',3,'',4,19),(31,'2026-09-23 15:28:36.222000','40','ladinodilan57@gmail.com',3,'',4,19),(32,'2026-09-23 15:28:36.222000','37','nicoolperdomo300@gmail.com',3,'',4,19),(33,'2026-09-23 15:28:36.222000','42','nicoolperdomo752@gmail.com',3,'',4,19),(34,'2026-09-23 15:28:36.223000','38','tellezsamuel2102@gmail.com',3,'',4,19);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(13,'administracion','sitio'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(10,'barberos','barbero'),(7,'citas','cita'),(8,'citas','servicio'),(9,'citas','suscriptornewsletter'),(11,'clientes','cliente'),(5,'contenttypes','contenttype'),(17,'googlecalendar','citaeventogoogle'),(16,'googlecalendar','cuentagoogle'),(15,'inventario','movimientoinventario'),(14,'inventario','producto'),(18,'notificaciones','notificacion'),(19,'notificaciones','suscripcionturno'),(6,'sessions','session'),(12,'usuarios','perfil');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-10-15 15:52:15.354389'),(2,'auth','0001_initial','2026-10-15 15:52:15.769424'),(3,'admin','0001_initial','2026-10-15 15:52:15.858186'),(4,'admin','0002_logentry_remove_auto_add','2026-10-15 15:52:15.865697'),(5,'admin','0003_logentry_add_action_flag_choices','2026-10-15 15:52:15.871214'),(6,'administracion','0001_initial','2026-10-15 15:52:15.886728'),(7,'administracion','0002_rename_hero_imagen_1_sitio_hero_imagen_1_url_and_more','2026-10-15 15:52:16.068091'),(8,'administracion','0003_sitio_mapa_y_fachada','2026-10-15 15:52:16.134319'),(9,'administracion','0004_alter_sitio_mapa_embed_url','2026-10-15 15:52:16.141835'),(10,'contenttypes','0002_remove_content_type_name','2026-10-15 15:52:16.227232'),(11,'auth','0002_alter_permission_name_max_length','2026-10-15 15:52:16.295254'),(12,'auth','0003_alter_user_email_max_length','2026-10-15 15:52:16.311382'),(13,'auth','0004_alter_user_username_opts','2026-10-15 15:52:16.322003'),(14,'auth','0005_alter_user_last_login_null','2026-10-15 15:52:16.374605'),(15,'auth','0006_require_contenttypes_0002','2026-10-15 15:52:16.379130'),(16,'auth','0007_alter_validators_add_error_messages','2026-10-15 15:52:16.389640'),(17,'auth','0008_alter_user_username_max_length','2026-10-15 15:52:16.405760'),(18,'auth','0009_alter_user_last_name_max_length','2026-10-15 15:52:16.422850'),(19,'auth','0010_alter_group_name_max_length','2026-10-15 15:52:16.439952'),(20,'auth','0011_update_proxy_permissions','2026-10-15 15:52:16.454518'),(21,'auth','0012_alter_user_first_name_max_length','2026-10-15 15:52:16.474291'),(22,'barberos','0001_initial','2026-10-15 15:52:16.499666'),(23,'barberos','0002_barbero_dia_descanso_barbero_dias_laborales_and_more','2026-10-15 15:52:16.543509'),(24,'barberos','0003_barbero_home_fields','2026-10-15 15:52:16.684350'),(25,'clientes','0001_initial','2026-10-15 15:52:16.707255'),(26,'clientes','0002_delete_cita','2026-10-15 15:52:16.724550'),(27,'clientes','0003_initial','2026-10-15 15:52:17.018186'),(28,'citas','0001_initial','2026-10-15 15:52:17.034068'),(29,'citas','0002_cita_barbero_cita_fecha_alter_cita_estado','2026-10-15 15:52:17.060223'),(30,'citas','0003_alter_cita_id','2026-10-15 15:52:17.092214'),(31,'citas','0004_barbero_producto_servicio','2026-10-15 15:52:17.137138'),(32,'citas','0005_cita_adicionales','2026-10-15 15:52:17.147288'),(33,'citas','0006_alter_barbero_id_alter_cita_id_alter_producto_id_and_more','2026-10-15 15:52:17.263809'),(34,'citas','0007_alter_cita_estado','2026-10-15 15:52:17.266657'),(35,'citas','0008_alter_cita_estado','2026-10-15 15:52:17.270199'),(36,'citas','0009_delete_producto_alter_servicio_duracion','2026-10-15 15:52:17.278172'),(37,'citas','0010_cita_productos','2026-10-15 15:52:17.287485'),(38,'citas','0011_delete_barbero_alter_cita_barbero_alter_cita_cliente_and_more','2026-10-15 15:52:17.731317'),(39,'citas','0012_alter_cita_id_alter_servicio_id','2026-10-15 15:52:18.248111'),(40,'citas','0013_alter_cita_options_alter_cita_adicionales_and_more','2026-10-15 15:52:18.323895'),(41,'citas','0014_alter_cita_adicionales_alter_cita_barbero_and_more','2026-10-15 15:52:18.470609'),(42,'citas','0015_alter_cita_id_alter_servicio_id','2026-10-15 15:52:18.749330'),(43,'citas','0016_alter_cita_id_alter_servicio_id','2026-10-15 15:52:18.952120'),(44,'citas','0017_alter_cita_id_alter_servicio_id','2026-10-15 15:52:19.245499'),(45,'citas','0018_alter_cita_id_alter_servicio_id','2026-10-15 15:52:19.456709'),(46,'citas','0019_alter_cita_id_alter_servicio_id','2026-10-15 15:52:19.670384'),(47,'citas','0020_cita_duracion_total','2026-10-15 15:52:19.694984'),(48,'citas','0021_remove_cita_duracion_total','2026-10-15 15:52:19.716310'),(49,'citas','0022_cita_duracion_total','2026-10-15 15:52:19.741523'),(50,'citas','0023_remove_cita_cita_unica_por_barbero','2026-10-15 15:52:19.852358'),(51,'citas','0024_cita_recordatorio_enviado','2026-10-15 15:52:19.875516'),(52,'citas','0025_cita_historial_archivado','2026-10-15 15:52:19.914802'),(53,'citas','0026_cita_analisis_ia','2026-10-15 15:52:19.946363'),(54,'citas','0027_suscriptornewsletter','2026-10-15 15:52:19.970556'),(55,'citas','0028_alter_suscriptornewsletter_creado','2026-10-15 15:52:19.973558'),(56,'citas','0029_servicio_imagen','2026-10-15 15:52:19.984462'),(57,'clientes','0004_cliente_user_nullable','2026-10-15 15:52:20.200645'),(58,'clientes','0005_cliente_correo_confirmado','2026-10-15 15:52:20.223275'),(59,'clientes','0006_cliente_cortes_completados_and_more','2026-10-15 15:52:20.258202'),(60,'googlecalendar','0001_initial','2026-10-15 15:52:20.417138'),(61,'inventario','0001_initial','2026-10-15 15:52:20.425819'),(62,'inventario','0002_servicioproducto','2026-10-15 15:52:20.515517'),(63,'inventario','0003_producto_stock_minimo_alter_producto_stock_and_more','2026-10-15 15:52:20.624658'),(64,'inventario','0004_remove_salidainventario_producto_and_more','2026-10-15 15:52:21.074729'),(65,'inventario','0005_alter_movimientoinventario_options_and_more','2026-10-15 15:52:21.139870'),(66,'inventario','0006_alter_movimientoinventario_id_alter_producto_id','2026-10-15 15:52:21.450731'),(67,'inventario','0007_alter_movimientoinventario_id_alter_producto_id','2026-10-15 15:52:21.661873'),(68,'inventario','0008_alter_movimientoinventario_id_alter_producto_id','2026-10-15 15:52:21.996487'),(69,'inventario','0009_alter_movimientoinventario_id_alter_producto_id','2026-10-15 15:52:22.332936'),(70,'inventario','0010_alter_movimientoinventario_id_alter_producto_id','2026-10-15 15:52:22.516749'),(71,'inventario','0011_alter_movimientoinventario_id_alter_producto_id','2026-10-15 15:52:22.714263'),(72,'inventario','0012_alter_producto_stock_actual','2026-10-15 15:52:22.717262'),(73,'notificaciones','0001_initial','2026-10-15 15:52:22.800458'),(74,'notificaciones','0002_suscripcionturno','2026-10-15 15:52:22.953211'),(75,'notificaciones','0003_alter_notificacion_mensaje','2026-10-15 15:52:23.010051'),(76,'sessions','0001_initial','2026-10-15 15:52:23.053134'),(77,'usuarios','0001_initial','2026-10-15 15:52:23.195280');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('22qzyrjqtcqsbq823qrcghwg1ig9k4h5','.eJxVjDsOwjAQBe_iGln-rR1T0nMGa-1d4wCKpXwqxN0hUgpo38y8l0i4rS1tC89pJHEWWpx-t4zlwdMO6I7TrcvSp3Ues9wVedBFXjvx83K4fwcNl_atVSikQTkDwcSCVlnwtTqrIxllGYCokDeYgwLta-QAtjirMDLjwIN4fwDACTds:1wjbq4:SuTXSBOY3_kOn57mfcsktNAW4N-OjS8vKIRlWEUfb9Q','2026-07-28 12:02:16.438000'),('2ztu957fj80qq7ry7vv5tdpd24w4hxj7','.eJxVjDsOwjAQBe_iGlnrz8o2JT1nsHb9wQHkSHFSIe4OkVJA-2bmvUSkbW1xG2WJUxZnocTpd2NKj9J3kO_Ub7NMc1-XieWuyIMOeZ1zeV4O9--g0Wjf2kHw2UBg5SEYdGiVNyrpUCpa8Jg1egJgh8TGmOoqa82qgq0MCFm8P6BsNqI:1x9PGO:KGKAn9bGofxS24HnxLtGf_IIrVelH53BOHN2Yl4jA_M','2026-10-07 15:52:04.055000'),('31h1f3ecgn25g65ilglsas8lay71grdq','.eJxVjEEOwiAQAP_C2ZBVKIhH731Ds7C7UjWQlPZk_LuS9KDXmcm81ITbmqet8TLNpC7qNKjDL4yYHly6oTuWW9WplnWZo-6J3m3TYyV-Xvf2b5Cx5f41yVhgQAgORNCwB3IOkj0OgATi3ZmCd18lwmR8pCBswYEJViyp9wcHxTho:1x6qik:qumCMoUcayUI4pzQSv_nnJHS17InLsGPcIWeqBaM3IE','2026-09-30 14:34:46.164000'),('4kil6pvp37ptnk4v5o53xt2efquh9snl','.eJxVjEEOwiAQRe_C2hCYMlNw6d4zEDoMtmpKUtqV8e7apAvd_vfef6mYtnWMW5MlTlmdFTh1-h2HxA-Zd5Lvab5VzXVel2nQu6IP2vS1ZnleDvfvYExt_NaBQDJRMQM66KFAsgAUvOeOmNGHzljbsSNbjEFGWzCQ9CYLBhCP6v0B2wM2xA:1x3NFV:NLy5ttsASsuCN4QhT_Hj6HCmGDKN1a8MoTm3oBVHXIE','2026-09-21 00:30:13.782000'),('5axfsc942ojyp8vii5ftytlh25czp4qy','.eJxVjMsOwiAURP-FtSHA5enSfb-BXF5SNZCUdmX8d9ukC53lnDPzJh63tfpt5MXPiVyJEOTyWwaMz9wOkh7Y7p3G3tZlDvRQ6EkHnXrKr9vp_h1UHHVfa1ksV0Kh4BK1Y1ybpAszCtyelIsCG5VDBrpEMJxJkNKIkLgBxbIlny_MKjZn:1wu8mX:C5-2Q1d0iBxRs9FxSOUZPM5n2hmlPKMiAPxt67MIsrw','2026-08-26 13:14:09.474000'),('5fwdkbc0xm831snyq9hq2wg08z9nau71','.eJxVjEsOAiEQRO_C2pABGm1cuvcMpJuPjBpIhpmV8e5KMgtdVr1X9RKetrX4rafFz1GchVbi8FsyhUeqg8Q71VuTodV1mVkORe60y2uL6XnZ3b-DQr2MddQ5JoKEbNkRZAUBM4KdFBrLmANpVsa4kFkFIHtKymGe8BvAwlG8PzBCOGc:1x9PYo:U9G-5s1qt7Fz1kC5ICgOb-Cdw6GhPMFlCpYM9S3Evew','2026-10-07 16:11:06.435000'),('5l9we71wqles7j29joff1sewv1yazsep','.eJxVjEEOwiAQRe_C2hCgDA4u3XsGMoVBqgaS0q6Md7dNutDte-__twi0LiWsnecwJXERWpx-2UjxyXUX6UH13mRsdZmnUe6JPGyXt5b4dT3av4NCvWxrhAFsytawzdkZtPoMMTkEZ9WGmYzXYBwmP2StcABQno1Czypbciw-X7zCNs0:1wf6BC:gVDV3pLYxea_F2QwIoi2pwS3diMw5sWzL20pztPOycs','2026-07-16 01:25:26.556000'),('5prtwl25ymn4tmrrudlp6icku3pmbfl9','.eJxVjEEOwiAQRe_C2hAGCqUu3XsGMsMMUjVtUtqV8e7apAvd_vfef6mE21rT1mRJI6uzsqBOvyNhfsi0E77jdJt1nqd1GUnvij5o09eZ5Xk53L-Diq1-62hc9uCNDERke7IsHsQFYlsAwHZd7kxP5DCEIr0vOETnPBgOzCUO6v0B_6039w:1x3NH4:tJxwMO84nkoiEAuRihPjAIBuzKg6AEYDDe8SLqMciEA','2026-09-21 00:31:50.205000'),('612thj0vku6jdxo7t766jkgfhrmxpqq7','.eJxVjMsOwiAQRf-FtSHlDS7d-w1kgBmpGkhKuzL-uzbpQrf3nHNfLMK21rgNXOJc2JlJwU6_Y4L8wLaTcod26zz3ti5z4rvCDzr4tRd8Xg7376DCqN8apTEUwDrtnaKQvIbJaEClQ5J2Kig1ASlUSiZHxnubUBQqmTQ6K4C9PwLnOHc:1x6rhw:TjSU0qlWMBioiRBW_Pcu16gzXbRH0nzgNWYzUxhUWGk','2026-09-30 15:38:00.087000'),('6pzh1ha2bd9mwshp5vmwyn28yc9bg3uv','e30:1wzItO:y2qXRK2e696k303LPO1TUVR7LoUPSZGuJ-FPtsu0XFI','2026-09-09 19:02:34.715000'),('6uc4ih2w9ixpdnmhctt2c5k4hl5mf06v','.eJxVjEEOwiAQRe_C2pABgQGX7nsGMgNUqoYmpV0Z765NutDtf-_9l4i0rTVuvSxxyuIilDj9bkzpUdoO8p3abZZpbusysdwVedAuhzmX5_Vw_w4q9fqttUMGk41nzAG8A486MVAIZ0s-B2UNgcIxWXDekGONIyqtEiAbZYN4fwC2-jaC:1wzjhS:JRGc5RUzWelBNjbdOp3Md1PWeCtSEhGo5YehvJEYLLw','2026-09-10 23:40:02.828000'),('75rlrnvt8cg1qaqoqlhhdcw85d1l4var','.eJxVjMEOwiAQRP-FsyEUllI8eu83kF1YpGpoUtqT8d9tkx70NMm8N_MWAbe1hK3xEqYkrkKDuPyWhPHJ9SDpgfU-yzjXdZlIHoo8aZPjnPh1O92_g4Kt7GvwHUSXoyXFXbLQayR0qnc6WzUwgM-RDRhrsrd7qsQ6k88GI4GGQXy-_YU31w:1x1Mhc:gXQ_RWBrR12kQhED5VrtQiLc6d3dhH2mOY8BYFvYmuI','2026-09-15 11:30:56.599000'),('77d7p65ssbe7k9hukou3fq1x59izv2ub','.eJxVjEEOwiAQAP_C2ZBVKIhH731Ds7C7UjWQlPZk_LuS9KDXmcm81ITbmqet8TLNpC7qNKjDL4yYHly6oTuWW9WplnWZo-6J3m3TYyV-Xvf2b5Cx5f41yVhgQAgORNCwB3IOkj0OgATi3ZmCd18lwmR8pCBswYEJViyp9wcHxTho:1x9O98:CuzBHadNMp-3QQerWCpJ4zITfox2LsUuWLAczm54GAw','2026-10-07 14:40:30.221000'),('7gsbs76mgt0rtg3knn4w7vynp616ihgi','.eJxVjEEOwiAQRe_C2pABgQGX7nsGMgNUqoYmpV0Z765NutDtf-_9l4i0rTVuvSxxyuIilDj9bkzpUdoO8p3abZZpbusysdwVedAuhzmX5_Vw_w4q9fqttUMGk41nzAG8A486MVAIZ0s-B2UNgcIxWXDekGONIyqtEiAbZYN4fwC2-jaC:1x1Mhc:Mz7vy20E_pGfEPLd7Y4CeEfUxtCfQu9Th3VEbtPcQrI','2026-09-15 11:30:56.424000'),('7qvsbmzd4w1pbvv6bmbyyewazv84ved7','.eJxVjDsOwjAQBe_iGlmy1_GHkp4zWOvdBQeQI8VJFXF3iJQC2jczb1MZ16XmtcucR1ZnZdTpdytIT2k74Ae2-6Rpass8Fr0r-qBdXyeW1-Vw_w4q9vqtYwIG9hbER7pZJ8jkGUoxxkUH5DgNIYWIEJIjkkgFnQzBUgDyktT7A-gpOCA:1wclHk:STp5eZz5WQ3wS5AsWIGCTlDsx3ib8bSaUtOqB1JwjMg','2026-07-09 14:42:32.576000'),('8mdsud9ns7729wakp6xrz6a8z7goyk3b','.eJx1kz1vGzEMhv8KoflwsGs7cbwlbjMlQJdObWBQEm0z1YmGPq51gvz3QvI1ObfJooGS-PLhSz6rDea03-RIYcNWrdSnmWrGQY3mJ_lyYx_R76Q14lNg3ZYn7XAb23ux5G6Gt2cJ9hj3Je92OjfzqZ0botn8ys5wttCkzXQ6W1wtZsv5crmYXKKdG6sv9BLnlrZ6cqGXhshcXV6oRqFHx5HjhlGtnpXoSKFHw-IpqtV3tUZNzgl0-QhGQhIw4iHR75QDgiUfsVWNuvuRJxOynkrMgRl-bYP4hA40kwdLW_Zs6_tbCR3CjjwFdPVLkJiCgPTo0GJVCRh3EqHDYNBKbNVDowIZ6cjbtxKflZdOB1IrdZOfnmCdU_19i5ZUozpJ3ItaqXv0ickTZI_gxO84ZVuZEI5wCJVgahIbbCBQRJfQWwGH4N7o_hKNYTr0iTx3TD4VpRt8FNWoA1m2stEYNIUS_-arHIEudWbPWwkdAfmiccByE_OBAkuoBLn0LPboybAV0Pgo9bFEcJhK5yi26qUZdWCNFDHAujg1hr8-BOnJ7LFInbkHRxgZdrL4gAGLOhrUaAUoppBN-WMF0ME2kE_0Hvo9Wf6InWJiJzCUWADfwz7ZMZTYwCBA1YkKbsvJ3YHlX_g7-VVdh6_ZsT3j_0wxoan0pek4Hrmh1bGmKYQxJ3aDLU_iEdhvT-Udx43_n_7a1a5_bPzbFmEIrE9jPrb5lOpkdV2aYfiL8usQxtfpKx14aBT2HIvOl5gwQiyrc74mIKEkxsQ9xpPjQ3VgSRP06NhiKPFAMbtUJLfs0bXq5eUPtGSy1Q:1x99o8:gMCVUFRlIS-9S7cMGDsCY9Vd7zM811-IaKAaOF8qoMM','2026-10-06 23:21:52.802000'),('amiyllosdptmsendo4iscbzud4bsfd6n','.eJxVjEEOwiAQRe_C2hCYMlNw6d4zEDoMtmpKUtqV8e7apAvd_vfef6mYtnWMW5MlTlmdFTh1-h2HxA-Zd5Lvab5VzXVel2nQu6IP2vS1ZnleDvfvYExt_NaBQDJRMQM66KFAsgAUvOeOmNGHzljbsSNbjEFGWzCQ9CYLBhCP6v0B2wM2xA:1x3NXP:voXhjmfz_yvRXSeeJHWzyjGPRH05VP2Fhiu3BZfgtjo','2026-09-21 00:48:43.653000'),('b1jpp20b0gg36lfwzz75lhwl67hm80us','.eJxVjEEOwiAQRe_C2pAi0IJL956BzDBTqRpISrsy3l1IutDdz38v7y0C7FsKe-U1LCQu4qzF6fdEiE_OndAD8r3IWPK2Lii7Ig9a5a0Qv66H-xdIUFPvzspEo8hEZm08adAWGaNS2nqrnXHODhM0TjiiA0M849BW86OfRvH5AhM-OMg:1x7aC8:8Rqtmhq8NRI5QxZM9BBf7KwfttQ1XhOyefeyU4b7HgA','2026-10-02 15:08:08.853000'),('baptahb4vxwq66sa7k9hhe34hvxkivyq','.eJxVjEEOwiAQAP_C2ZAWYQWP3vsGsrssUjU0Ke3J-HdD0oNeZybzVhH3rcS9yRrnpK7Kq9MvI-Sn1C7SA-t90bzUbZ1J90QftulpSfK6He3foGArfZtHMp4xA8tgAbIJF-sEAhrwTlBsYPLBZwAHlM6cGcRSonHAAIjq8wX3hDi0:1wmBsm:k5Mv1r24J_IZaIYuKw1oq3SGLYpARRQlvwSnBXRYFOw','2026-08-04 14:55:44.173000'),('dau190wnnremolvwz6vn37cpo5hw65a0','.eJxVjEEOwiAURO_C2hDkF7Eu3fcMBP58pGpoUtqV8e7apAvdzntvXirEdSlhbTKHEeqi7EkdfscU-SF1I7jHeps0T3WZx6Q3Re-06WGCPK-7-3dQYivf2rPPmZw34i1AXcTR91YAGLaczpQtOXHsmRjZse16SY7EGBhAnHp_AClmOSM:1x91wh:xGhgBNNAIdamqie0US5172cmPYsfmM2PorEz0OAkbQ4','2026-10-06 14:58:11.773000'),('erowglgt0n9xgk66mjyhk5nxxffm3689','.eJxVjDsOwjAQBe_iGlkbxxtsSvqcIXrOrnEAJVI-FeLuECkFtG9m3st02NbSbYvO3SDmYhyb0--Y0D903IncMd4m20_jOg_J7oo96GLbSfR5Pdy_g4KlfGuKNc7Bg7I20TGk4twwAIbXpvbeC1PoHRLBQUNVUxSXY06OSJTN-wMEBTgc:1wu7tD:vZ0JwReTV4zZP5uHNy6Jy4sxHloSTVCxUxtRkGlpP4A','2026-08-26 12:16:59.968000'),('g4dw59ehfx7i0wmp3kzvdr3uf5lu76bu','.eJxVjDsOwjAQBe_iGlnrz8o2JT1nsHb9wQHkSHFSIe4OkVJA-2bmvUSkbW1xG2WJUxZnocTpd2NKj9J3kO_Ub7NMc1-XieWuyIMOeZ1zeV4O9--g0Wjf2kHw2UBg5SEYdGiVNyrpUCpa8Jg1egJgh8TGmOoqa82qgq0MCFm8P6BsNqI:1x3uZH:aYGhFbxfUfp2ToomeIF2OQoO4hfq_LGkRH_GDwjfTPU','2026-09-22 12:04:51.238000'),('gdc02vhy8t2akhkpbce9ynqbvbj7ydau','.eJxVjEEOwiAQRe_C2pAi0IJL956BzDBTqRpISrsy3l1IutDdz38v7y0C7FsKe-U1LCQu4qzF6fdEiE_OndAD8r3IWPK2Lii7Ig9a5a0Qv66H-xdIUFPvzspEo8hEZm08adAWGaNS2nqrnXHODhM0TjiiA0M849BW86OfRvH5AhM-OMg:1x9PB8:6bSmVe-Y4HYdBJlnBLH4bY45gzrqkzprEUtfttMxzMQ','2026-10-07 15:46:38.689000'),('gqlhk3f682w5jzmu8x7nmhz6p06cyjan','.eJxVjMsOwiAURP-FtSHA5enSfb-BXF5SNZCUdmX8d9ukC53lnDPzJh63tfpt5MXPiVyJEOTyWwaMz9wOkh7Y7p3G3tZlDvRQ6EkHnXrKr9vp_h1UHHVfa1ksV0Kh4BK1Y1ybpAszCtyelIsCG5VDBrpEMJxJkNKIkLgBxbIlny_MKjZn:1x9P6i:AXIkVb5vIXEsrYZzb9ICeQtcRHrE8TaS1xF8KVp5y1Y','2026-10-07 15:42:04.128000'),('gybb9pq43khc7oly1xooh145s0ykh3ii','.eJxVjDsOwjAQBe_iGlnrz8o2JT1nsHb9wQHkSHFSIe4OkVJA-2bmvUSkbW1xG2WJUxZnocTpd2NKj9J3kO_Ub7NMc1-XieWuyIMOeZ1zeV4O9--g0Wjf2kHw2UBg5SEYdGiVNyrpUCpa8Jg1egJgh8TGmOoqa82qgq0MCFm8P6BsNqI:1x7aNF:t0auRrFTP0oAcmCouN9g_uS1M3256b6ptvc5pSuaTSc','2026-10-02 15:19:37.722000'),('h1d0l09xb7k03uu933gb0zz35rnkq0td','.eJxVjMsOgjAQAP9lz6bZlRYoR-9-Q7OPKqgpCYWT8d8NCQe9zkzmDYm3dUxbzUuaDAY4N3D6hcL6zGU39uByn53OZV0mcXviDlvddbb8uhzt32DkOsIA6jVEH33juQ2oZogWmChgLxQlGLEY5Wxy89ELRmq7aB13FHpFRfh8AQH0N_E:1wxRWX:Ks7A5GS1ThP51h74rf58j7gD3ZH6RNMpvGBzPspuYb0','2026-09-04 15:51:17.492000'),('hmyvegzv9tkzpe23ejldasbo1pavebbm','.eJyVk09vGzcQxb_KgOeFYFWyI6un2G2CADECFM2pDYRZclaiw-WsZ0ihtuHvXgwl2zLaHHJbLP-8937z-Og2WMtuU5VkE4Nbu18Wrjv92aP_TtlWwi3mLc885yKxn9mW2XFVZzccKF0d9765YIe6s3uH-dIv52HpiRbLy7DAxXlPvZ_PF-eX54vVcrU6P3uHYelDf9GvcBlo6M8u-pUn8pfvLlznMGOKGnUT0a0fHfdKskcfOZO69V_uGntKiWGs9-BZCoPnDIX-KVUQAmVFuIea48Ay0sx17vPf9eyMQiZbTuCPFwzCuWCCQEPMMWC7xw4hCAXOgTCgnf-DtQhDIJiEJ5aDF6C7GlPsBQNqOyuoW1bAvK0JhRT2UWOfSGfuW-eEPI-Uw2uUR5d57IXc2l3Vhwe4rsV1buQS9-zW7gZziZQJEkLivI2lBkBfKqaX8BZVSDEVhIQK6SWqvuSyrwTSQlicEXOhHMdIuZjOFd6y69xEIQbe9Cg9if3_mpsEnZDGBJ6EoX3VzEAZCgfTblgfsIPj9ZQDQ-JGprBkVugjZRhRPAbWmXvqTgB8wEBgThpJzgH1lMV7yzXMbVNrJmohEzeBhIUEEym0SIIKSoCT8J78rnl7bscBmdaJJLL8H4wbCvFHNALpHjP5GBh6s_piILDCvQnl6rGDQLfY4iNMaASfFSHFLQmOlA1rm9XczsvWBnlwGR9a7d7QuUZSlMMQTrH8ZiM-FOS148-9NpA1w0R3lQ74GIbUWpsYhHxhuKsGdJwSmafGirRI9Q3XgD5i-llMh9K8hrGRPj9TSv-xsDMRwEDJNAzjm5kK9Xh7LMy3zuE-qun8rgUVeDq-RbXSiLnDEveov5qaVnsWGmmcpPUGSoWjVZvd-69_fvn85eOna5sSwh5TDCjmUaidDQxDzEbg6elfVYjdWw:1x99lr:C8KjUyC8NRJiW0wOdCuoSbflvxbZM3qechz7BHxz2zo','2026-10-06 23:19:31.040000'),('hu26bylklrfiv08bemqq9i0rr7ru3fqd','.eJxVjMEOwiAQRP-FsyEUllI8eu83kF1YpGpoUtqT8d9tkx70NMm8N_MWAbe1hK3xEqYkrkKDuPyWhPHJ9SDpgfU-yzjXdZlIHoo8aZPjnPh1O92_g4Kt7GvwHUSXoyXFXbLQayR0qnc6WzUwgM-RDRhrsrd7qsQ6k88GI4GGQXy-_YU31w:1x1Bjc:inT80I9hpEvk6JmVjP6Kob_qGwjiVauxJXVeQLxU4pw','2026-09-14 23:48:16.670000'),('ijczrusnb8naapj74c0bfguyilb94qaf','.eJxVjDsOwjAQBe_iGlnrz8o2JT1nsHb9wQHkSHFSIe4OkVJA-2bmvUSkbW1xG2WJUxZnocTpd2NKj9J3kO_Ub7NMc1-XieWuyIMOeZ1zeV4O9--g0Wjf2kHw2UBg5SEYdGiVNyrpUCpa8Jg1egJgh8TGmOoqa82qgq0MCFm8P6BsNqI:1x9Nfn:V4rEiSqBoh9tQgeL3W4pE-QfpUkbl4qVTJZZ0YJRs1w','2026-10-07 14:10:11.361000'),('io3lh6oaa288s5zvkkgyssnknxvvdcog','.eJxVjDkOwjAQAP-yNbLi205Jzxuitb2LA8iWclSIv6NIKaCdGc0bJty3Ou0rLdNcYAQl4fILE-YntcOUB7Z7F7m3bZmTOBJx2lXceqHX9Wz_BhXXCiOQspYjOm-C1xxTMDhYg6RNTMoNhZRhZE1aq-TZhuASycIlsyHvJMLnCwLnOHc:1x9BLW:FhgaJowSg5AJGVdxAiEplBPkj6wyvaout1JOIvzJ1KU','2026-10-07 01:00:26.177000'),('iqzonbgq0anijid9kaf9m4h2uci8r89w','.eJxVjMsKwjAQAP9lzxI2jyVJj979hpDNw1QlhaY9if8uhR70OjPMG0Lctxb2UdYwZ5hAwuWXcUzP0g-RH7HfF5GWvq0ziyMRpx3ituTyup7t36DF0WACi95ljZ6lQ6_JkpFOy6R8qWTQUVbkIiJbiqy1rrayUiwrmspImOHzBaBsNqI:1x3b5D:HC0rfAWlNQtjL4AzpOWHlDauUB0c61y8avhFW9VUSQw','2026-09-21 15:16:31.575000'),('l47nveu23i5xiy3e49x895scr6zfu47e','.eJxVjDsOwyAQRO9CHSE-xkDK9D4DWmA3OIlAMnYV5e6xJRdJM8W8N_NmAba1hK3jEubMrkxpdvktI6Qn1oPkB9R746nVdZkjPxR-0s6nlvF1O92_gwK97GuvrCChjDCExoMlJ0mP0e4pdHagcZRAWWjwmJMlElqSMQN6OaD0jn2--mU33w:1wtlJ6:Xk8YL04XoTca1eJL6wQOKmpuDq1EbdRPLQLfA6UMkV0','2026-08-25 12:10:12.936000'),('lli5lovops22u1wqg4maf466cvlkzi70','.eJxVjEEOwiAQRe_C2pAi0IJL956BzDBTqRpISrsy3l1IutDdz38v7y0C7FsKe-U1LCQu4qzF6fdEiE_OndAD8r3IWPK2Lii7Ig9a5a0Qv66H-xdIUFPvzspEo8hEZm08adAWGaNS2nqrnXHODhM0TjiiA0M849BW86OfRvH5AhM-OMg:1xETRx:QzZ7feC7qEpUoUp7ZEkA4tparaXdsiv6-llwexNw-z4','2026-10-21 15:20:57.427000'),('lm9c512cejsi1dytqvypc5f1upikx4r5','.eJxVjMsKg0AMAP8l57Kgifvw2Hu_YckmabUtCq6epP9eBA_tdWaYHTJv65C3akseFXpo4PLLCsvLpkPok6fH7GSe1mUs7kjcaau7zWrv69n-DQauA_QQEyqqb9F8lHtLxipesZSmoUgopKkLKUTGkEjEohQm60IrAcVbgs8X6Ck4IA:1wewv0:F3g_elHzpJeAGMeew73MTgT3LaWr2WAIZzFFkEkJ1h0','2026-07-15 15:32:06.239000'),('n0zsytso0mitqv7grak11n6rjzq94khm','.eJxVjEEOwiAQRe_C2pABgQGX7nsGMgNUqoYmpV0Z765NutDtf-_9l4i0rTVuvSxxyuIilDj9bkzpUdoO8p3abZZpbusysdwVedAuhzmX5_Vw_w4q9fqttUMGk41nzAG8A486MVAIZ0s-B2UNgcIxWXDekGONIyqtEiAbZYN4fwC2-jaC:1wzjhM:polBVOZbS6qbtI6Vv1ThTyWTHN_98-q3VVka1mZbino','2026-09-10 23:39:56.820000'),('nwqvqu0zd155fltosho4wvz16raizhwu','.eJxVjEEOwiAQAP_C2ZBVKIhH776BLOyuVA0kpT0Z_25IetDrzGTeKuK2lrh1XuJM6qJOkzr8woT5yXUYemC9N51bXZc56ZHo3XZ9a8Sv697-DQr2Mr4mGwsMCMGBCBr2QM5BtscJkEC8O1PwTgRFmIxPFIQtODDBiiX1-QIHxTho:1x7mYc:sjs1nP11E1pep8kNdeUOyi9cD7N3V8M5LbLw2v09uNw','2026-10-03 04:20:10.596000'),('or7bfb78exl7yjecs37v26conjy2ovoa','.eJxVjEEOwiAQAP_C2ZBVKIhH776BLOyuVA0kpT0Z_25IetDrzGTeKuK2lrh1XuJM6qJOkzr8woT5yXUYemC9N51bXZc56ZHo3XZ9a8Sv697-DQr2Mr4mGwsMCMGBCBr2QM5BtscJkEC8O1PwTgRFmIxPFIQtODDBiiX1-QIHxTho:1x7mjf:cdw7WeyhKORFcIH4sPnOiZR5LfcKTx86LyDaMUvIf_c','2026-10-03 04:31:35.799000'),('p9tvicp17xpkzs2dkwkuyo30k1mkgydq','.eJxVjDsOwjAQBe_iGlnYsde7lPQ5Q7TrDw4gR8qnQtwdIqWA9s3Me6mBt7UO25LnYUzqokCdfjfh-MhtB-nO7TbpOLV1HkXvij7oovsp5ef1cP8OKi_1W5MBNITOeuOLQPEuWQGKGABLOKNhtoJeuuBiSYAEXRBHHEioJI_q_QG5vTcg:1wclnU:87e2fyAfmMAx1_mpopKBE-ItpDR6lB1bqd5eX6ygta8','2026-07-09 15:15:20.123000'),('ppu8j3q4ne9epb5e42gb1pi0ftyg4y3d','.eJxVjDsOwjAQBe_iGlnrz8o2JT1nsHb9wQHkSHFSIe4OkVJA-2bmvUSkbW1xG2WJUxZnocTpd2NKj9J3kO_Ub7NMc1-XieWuyIMOeZ1zeV4O9--g0Wjf2kHw2UBg5SEYdGiVNyrpUCpa8Jg1egJgh8TGmOoqa82qgq0MCFm8P6BsNqI:1x9PtK:seg_CYWAEvqN4fRnKlQgcMS7BpgzS2TOhPlmXMAEUU0','2026-10-07 16:32:18.139000'),('qqix4jycpvpzrlsqhb0lhm2jqp5drppu','.eJxVjEEOwiAQAP_C2ZBVKIhH731Ds7C7UjWQlPZk_LuS9KDXmcm81ITbmqet8TLNpC7qNKjDL4yYHly6oTuWW9WplnWZo-6J3m3TYyV-Xvf2b5Cx5f41yVhgQAgORNCwB3IOkj0OgATi3ZmCd18lwmR8pCBswYEJViyp9wcHxTho:1x9Nwb:lWD1OVvPptiOspXmYtXv_B8ynAHPTTkdaXHZhA88mDw','2026-10-07 14:27:33.518000'),('r2xne2rn2xg0oqrzey96zqre6ebutgjs','.eJxVjMEOwiAQRP-FsyEUllI8eu83kF1YpGpoUtqT8d9tkx70NMm8N_MWAbe1hK3xEqYkrkKDuPyWhPHJ9SDpgfU-yzjXdZlIHoo8aZPjnPh1O92_g4Kt7GvwHUSXoyXFXbLQayR0qnc6WzUwgM-RDRhrsrd7qsQ6k88GI4GGQXy-_YU31w:1x1MhT:WRtWgezQARC16dYo0Nv1xFcyIV3-yqm1w_BeJqz-QxE','2026-09-15 11:30:47.473000'),('raor40a2i0vswb7e1vs41g1a9839b1zb','.eJxVjMsKwjAQAP9lzxI2jyVJj979hpDNw1QlhaY9if8uhR70OjPMG0Lctxb2UdYwZ5hAwuWXcUzP0g-RH7HfF5GWvq0ziyMRpx3ituTyup7t36DF0WACi95ljZ6lQ6_JkpFOy6R8qWTQUVbkIiJbiqy1rrayUiwrmspImOHzBaBsNqI:1x3axX:t1ASXDWvEZtO7rYgD_cpzhvxRhgfNfMl1fDZpaIGqkI','2026-09-21 15:08:35.273000'),('s0hegxnstaid7gxf5dxyha0fgc8qyp0a','.eJxVjDsOgzAQBe_iOrLAiz-kTM8ZrN31EpNERsJQRbl7QKJI2jcz760ibmuOW5UlTkldlVeX342Qn1IOkB5Y7rPmuazLRPpQ9EmrHuYkr9vp_h1krHmvKYXWBQIk7hsUsSzeupGlJxgJfENgxAdgcR2QFc_GArepQ8O7jurzBRXFOU0:1wlwoa:kGJO9lOFnegBkkgnW1FOHntDMqjrsUAtYt7R-MMpGWY','2026-08-03 22:50:24.829000'),('sb3r76ls9hiou1u2x16jcqnvmt26jgjs','.eJxVjMEOwiAQRP-FsyEUllI8eu83kF1YpGpoUtqT8d9tkx70NMm8N_MWAbe1hK3xEqYkrkKDuPyWhPHJ9SDpgfU-yzjXdZlIHoo8aZPjnPh1O92_g4Kt7GvwHUSXoyXFXbLQayR0qnc6WzUwgM-RDRhrsrd7qsQ6k88GI4GGQXy-_YU31w:1x1BjU:u8Ga5umWvz2eJZAs6NT8Fr6Jtk_tiZIMErvtm3bH5Tw','2026-09-14 23:48:08.891000'),('sgrc5mlgv3nf98d3p88o75ex64bwwec8','.eJxVjDsOwjAQBe_iGlnrz8o2JT1nsHb9wQHkSHFSIe4OkVJA-2bmvUSkbW1xG2WJUxZnocTpd2NKj9J3kO_Ub7NMc1-XieWuyIMOeZ1zeV4O9--g0Wjf2kHw2UBg5SEYdGiVNyrpUCpa8Jg1egJgh8TGmOoqa82qgq0MCFm8P6BsNqI:1x6UNP:7MV0ONZOtvdI56VId2ekCRYfJOwrE4iPVe50TjaAcDE','2026-09-29 14:43:15.265000'),('t4tumftngbjwfs92c713268dhry3cexr','.eJxVjMEOwiAQRP-FsyEUllI8eu83kF1YpGpoUtqT8d9tkx70NMm8N_MWAbe1hK3xEqYkrkKDuPyWhPHJ9SDpgfU-yzjXdZlIHoo8aZPjnPh1O92_g4Kt7GvwHUSXoyXFXbLQayR0qnc6WzUwgM-RDRhrsrd7qsQ6k88GI4GGQXy-_YU31w:1x1Mh2:JmI15HNArevo0I6e7sDC4yTejvFKDa7pWql9NoSioiI','2026-09-15 11:30:20.138000'),('tgajm2ufec9tfa6bmda57q3jgrsfxgk4','.eJxVjEEOwiAQRe_C2pABgQGX7nsGMgNUqoYmpV0Z765NutDtf-_9l4i0rTVuvSxxyuIilDj9bkzpUdoO8p3abZZpbusysdwVedAuhzmX5_Vw_w4q9fqttUMGk41nzAG8A486MVAIZ0s-B2UNgcIxWXDekGONIyqtEiAbZYN4fwC2-jaC:1wzupH:9R0RBH2gn-ajr4_bU21dTWIYMqu9rqt_3wepsSGHwyA','2026-09-11 11:32:51.100000'),('tri9vt5anasdieqatklkzjlmebwwn53y','.eJxVjEEOgjAQRe_StWloC-3g0j1naKYzg0VNSSisjHcXEha6_e-9_1YRtzXHrcoSJ1ZXZZ26_I4J6SnlIPzAcp81zWVdpqQPRZ-06mFmed1O9-8gY817bQJyR2iEhBlSB9R33hvyZLlpnRjGthkBRtcLg4UkwVJjYZe8C5DU5wsoSjhF:1wtw5M:XoI9hyXb5Y8kO0Pw69Gg281QTS2iRY8NCjQf-grMpyI','2026-08-25 23:40:44.628000'),('uhmm6waow7pt643bhtk9mrj1drlpzi1h','.eJxVjEEOwiAQRe_C2pABgQGX7nsGMgNUqoYmpV0Z765NutDtf-_9l4i0rTVuvSxxyuIilDj9bkzpUdoO8p3abZZpbusysdwVedAuhzmX5_Vw_w4q9fqttUMGk41nzAG8A486MVAIZ0s-B2UNgcIxWXDekGONIyqtEiAbZYN4fwC2-jaC:1x0k39:4RBj-f3a4WjZR2V93ngx7T8dILc3bzmxDyW5Whhr0r8','2026-09-13 18:14:35.369000'),('v1abgwxlrwi73h2zkpra12me6oezakqd','.eJxVjDEOAiEQAP9CbQgBYVlLe99AlgXk1EBy3FXGvxuSK7SdmcxbBNq3GvaR17AkcRHaiNMvjMTP3KZJD2r3Lrm3bV2inIk87JC3nvLrerR_g0qjzi94pWK0zmGxjLlYYodKayjaGEBEdoWJnCUCUB4jQ7HlrBJoJO3F5wv5MDfH:1wrF9R:R3Rkga8m-x02a-jm_xDeU7wMmNKBQKFtTsm9LUigfaQ','2026-08-18 13:25:49.681000'),('v746x50j6p40m4y23no86i0atsv7407t','.eJxVjMEOwiAQRP-FsyEUllI8eu83kF1YpGpoUtqT8d9tkx70NMm8N_MWAbe1hK3xEqYkrkKDuPyWhPHJ9SDpgfU-yzjXdZlIHoo8aZPjnPh1O92_g4Kt7GvwHUSXoyXFXbLQayR0qnc6WzUwgM-RDRhrsrd7qsQ6k88GI4GGQXy-_YU31w:1x1MhI:tJueGBMRP0Ds35Ya8BOokhalTe2NPq6BsO49gqKvwoQ','2026-09-15 11:30:36.150000'),('vebkhn3glt351wgig0j3sc39cp1o3fhu','.eJxVjDkOwjAQAP-yNbJ8HynpeYO19to4gBwpTirE31GkFNDOjOYNEfetxX2UNc4EE0gJl1-YMD9LPww9sN8Xlpe-rXNiR8JOO9htofK6nu3foOFoMIHV1QsjDUqh0QYurCNbuTMqhBCoVKN8NgG5sjUrJ7hWWjuZSDhlePHw-QLMKjZn:1x7Wtt:lF9F3qZ8VeQs2r15EEN5HXRD2p-RxKWy0gINgnrTquE','2026-10-02 11:37:05.375000'),('wgd7ypul7nknwi7cx3xn6q08mbftlrcc','.eJxVjMsOwiAQRf-FtSHlDS7d-w1kgBmpGkhKuzL-uzbpQrf3nHNfLMK21rgNXOJc2JlJwU6_Y4L8wLaTcod26zz3ti5z4rvCDzr4tRd8Xg7376DCqN8apTEUwDrtnaKQvIbJaEClQ5J2Kig1ASlUSiZHxnubUBQqmTQ6K4C9PwLnOHc:1x6pMQ:J4iiyZnhs_6OofLK_VwNoRH1y-7XeO4MsbEYmdNWroI','2026-09-30 13:07:38.176000'),('wk7dryqhtc0mvrzann4y8l11plg8anwg','.eJxVjEEOwiAQRe_C2pAi0IJL956BzDBTqRpISrsy3l1IutDdz38v7y0C7FsKe-U1LCQu4qzF6fdEiE_OndAD8r3IWPK2Lii7Ig9a5a0Qv66H-xdIUFPvzspEo8hEZm08adAWGaNS2nqrnXHODhM0TjiiA0M849BW86OfRvH5AhM-OMg:1xEULa:ZkEt_XJMz5NWDNw4FIyN2VaarxBAIQANDlPgiJq1umA','2026-10-21 16:18:26.424000'),('x6fgox286a0afp11jahpxkff6j4r5cf9','.eJxVjMsOwiAQRf-FtSHyBpfu-w1kGAapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKc2YVpyU6_YwJ8UNtJvkO7dY69rcuc-K7wgw4-9UzP6-H-HVQY9VuTRktFBSVdSkL5QNKhN0KjJHkGyN6UrH12ZME6LF7oopQjQzIgBWTvDxGbOIM:1x9Ojp:XOtPYpDtluKf90BpxIYnMiuS-EeZESprlRVzqmE-7K4','2026-10-07 15:18:25.844000'),('xo283a1vies0a3vb0u958xk1eavj386p','e30:1wcj2c:ZnYgGOrER7QxcOAAL3WG4w9IuKHKLg2yfl6Gg9Lh-0Y','2026-07-09 12:18:46.457000'),('xq81di4g36oqk076pys9xy5uul0f120d','.eJxVjDsOwjAQBe_iGlnrz8o2JT1nsHb9wQHkSHFSIe4OkVJA-2bmvUSkbW1xG2WJUxZnocTpd2NKj9J3kO_Ub7NMc1-XieWuyIMOeZ1zeV4O9--g0Wjf2kHw2UBg5SEYdGiVNyrpUCpa8Jg1egJgh8TGmOoqa82qgq0MCFm8P6BsNqI:1x6sO6:dDHAgcdD2VGl3O12-PimfWviSLJ1KOhd5mqB0r_9jPA','2026-09-30 16:21:34.254000'),('yq8ky7e6vtuudgsmq3z0sxoqutp7jq8b','.eJxVjMEOwiAQRP-FsyEUllI8eu83kF1YpGpoUtqT8d9tkx70NMm8N_MWAbe1hK3xEqYkrkKDuPyWhPHJ9SDpgfU-yzjXdZlIHoo8aZPjnPh1O92_g4Kt7GvwHUSXoyXFXbLQayR0qnc6WzUwgM-RDRhrsrd7qsQ6k88GI4GGQXy-_YU31w:1x1BjV:Xh1HmKXg2Up5WszcEedzmdOow6esvcB-A36b53V1rWQ','2026-09-14 23:48:09.220000'),('yw32d48woz6g09q3qi9rd1a0fxobrxv8','.eJxVjEEOwiAQRe_C2pABgQGX7nsGMgNUqoYmpV0Z765NutDtf-_9l4i0rTVuvSxxyuIilDj9bkzpUdoO8p3abZZpbusysdwVedAuhzmX5_Vw_w4q9fqttUMGk41nzAG8A486MVAIZ0s-B2UNgcIxWXDekGONIyqtEiAbZYN4fwC2-jaC:1wzjhb:IKqbh68MvevTB4jNTAJDFRTLxedq0LaQMB7Up1CSx5U','2026-09-10 23:40:11.574000'),('zb599ut3pa0sdtg7sktcrn2y71fg21m0','.eJxVjMsKwjAQAP9lzxI2jyVJj979hpDNw1QlhaY9if8uhR70OjPMG0Lctxb2UdYwZ5hAwuWXcUzP0g-RH7HfF5GWvq0ziyMRpx3ituTyup7t36DF0WACi95ljZ6lQ6_JkpFOy6R8qWTQUVbkIiJbiqy1rrayUiwrmspImOHzBaBsNqI:1x6V8k:xVaDdvlwIfH6FAyMB05VI3iDwJSZq0BJTTAwwLoi2Xs','2026-09-29 15:32:10.484000');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `googlecalendar_citaeventogoogle`
--

DROP TABLE IF EXISTS `googlecalendar_citaeventogoogle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `googlecalendar_citaeventogoogle` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `calendar_id` varchar(255) NOT NULL,
  `event_id` varchar(255) NOT NULL,
  `creado` datetime(6) NOT NULL,
  `cita_id` bigint(20) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `googlecalendar_citaeventogoogle_cita_id_usuario_id_b365beeb_uniq` (`cita_id`,`usuario_id`),
  KEY `googlecalendar_citae_usuario_id_b648d68c_fk_auth_user` (`usuario_id`),
  CONSTRAINT `googlecalendar_citae_cita_id_3b5c7de0_fk_citas_cit` FOREIGN KEY (`cita_id`) REFERENCES `citas_cita` (`id`),
  CONSTRAINT `googlecalendar_citae_usuario_id_b648d68c_fk_auth_user` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `googlecalendar_citaeventogoogle`
--

LOCK TABLES `googlecalendar_citaeventogoogle` WRITE;
/*!40000 ALTER TABLE `googlecalendar_citaeventogoogle` DISABLE KEYS */;
INSERT INTO `googlecalendar_citaeventogoogle` VALUES (10,'primary','mre89juig7tosv1qipdo3co37s','2026-09-23 15:56:03.849000',119,19),(11,'primary','kenvc8ul8norpjc67glb6l61fg','2026-09-23 15:56:05.536000',119,21);
/*!40000 ALTER TABLE `googlecalendar_citaeventogoogle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `googlecalendar_cuentagoogle`
--

DROP TABLE IF EXISTS `googlecalendar_cuentagoogle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `googlecalendar_cuentagoogle` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `token_acceso` longtext NOT NULL,
  `token_refresco` longtext NOT NULL,
  `token_uri` varchar(200) NOT NULL,
  `client_id` varchar(255) NOT NULL,
  `client_secret` varchar(255) NOT NULL,
  `scopes` varchar(500) NOT NULL,
  `expiracion` datetime(6) DEFAULT NULL,
  `email_google` varchar(254) NOT NULL,
  `fecha_conexion` datetime(6) NOT NULL,
  `fecha_actualizacion` datetime(6) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `googlecalendar_cuentagoogle_usuario_id_483757d0_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `googlecalendar_cuentagoogle`
--

LOCK TABLES `googlecalendar_cuentagoogle` WRITE;
/*!40000 ALTER TABLE `googlecalendar_cuentagoogle` DISABLE KEYS */;
/*!40000 ALTER TABLE `googlecalendar_cuentagoogle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario_movimientoinventario`
--

DROP TABLE IF EXISTS `inventario_movimientoinventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventario_movimientoinventario` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `tipo` varchar(10) NOT NULL,
  `cantidad` int(10) unsigned NOT NULL CHECK (`cantidad` >= 0),
  `fecha` datetime(6) NOT NULL,
  `nota` longtext DEFAULT NULL,
  `producto_id` bigint(20) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `proveedor` varchar(200) DEFAULT NULL,
  `stock_anterior` int(10) unsigned NOT NULL CHECK (`stock_anterior` >= 0),
  `stock_nuevo` int(10) unsigned NOT NULL CHECK (`stock_nuevo` >= 0),
  PRIMARY KEY (`id`),
  KEY `inventario_movimient_usuario_id_6ba25fdb_fk_auth_user` (`usuario_id`),
  KEY `inventario_movimientoinventario_producto_id_cec1a696_fk` (`producto_id`),
  CONSTRAINT `inventario_movimient_usuario_id_6ba25fdb_fk_auth_user` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `inventario_movimientoinventario_producto_id_cec1a696_fk` FOREIGN KEY (`producto_id`) REFERENCES `inventario_producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_movimientoinventario`
--

LOCK TABLES `inventario_movimientoinventario` WRITE;
/*!40000 ALTER TABLE `inventario_movimientoinventario` DISABLE KEYS */;
INSERT INTO `inventario_movimientoinventario` VALUES (1,'ENTRADA',20,'2026-06-25 08:00:00.000000','entrada',2,19,'no c',40,60),(2,'ENTRADA',12,'2026-06-25 09:42:00.000000','',1,19,'codensa',14,26),(3,'ENTRADA',10,'2026-06-26 11:48:00.000000','dsasaa',3,19,'hjf',10,20),(4,'SALIDA',5,'2026-06-27 09:50:00.000000','gfg',3,19,'fghjk',5,0),(5,'ENTRADA',10,'2026-06-25 09:50:00.000000','j',3,19,'j',15,25),(6,'ENTRADA',20,'2026-07-02 06:10:00.000000','',1,19,'gjhjk',34,54),(7,'SALIDA',20,'2026-07-14 07:02:00.000000','',1,19,'dddd',34,14),(8,'SALIDA',10,'2026-07-31 08:06:00.000000','',1,19,'.....',14,4),(9,'ENTRADA',2,'2026-07-31 08:07:00.000000','',1,19,NULL,4,6),(11,'SALIDA',5,'2026-07-31 09:46:00.000000','',1,19,'...',7,2),(12,'ENTRADA',28,'2026-08-04 19:53:00.000000','',2,19,'..',10,38),(13,'ENTRADA',12,'2026-09-16 15:16:00.000000','',1,19,'gthrt',2,14),(14,'ENTRADA',6,'2026-10-07 13:14:00.000000','',1,19,'tyj',14,20),(15,'SALIDA',10,'2026-10-07 13:15:00.000000','',1,19,NULL,20,10),(16,'SALIDA',2,'2026-10-07 14:20:00.000000','',1,19,NULL,10,8),(17,'SALIDA',4,'2026-10-07 14:26:00.000000','',1,19,NULL,8,4);
/*!40000 ALTER TABLE `inventario_movimientoinventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario_producto`
--

DROP TABLE IF EXISTS `inventario_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventario_producto` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `stock_minimo` int(10) unsigned NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `descripcion` longtext DEFAULT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `stock_actual` int(10) unsigned NOT NULL CHECK (`stock_actual` >= 0),
  PRIMARY KEY (`id`),
  CONSTRAINT `inventario_producto_stock_minimo_1d35972c_check` CHECK (`stock_minimo` >= 0)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_producto`
--

LOCK TABLES `inventario_producto` WRITE;
/*!40000 ALTER TABLE `inventario_producto` DISABLE KEYS */;
INSERT INTO `inventario_producto` VALUES (1,'Cera Cabello',5,1,'ejemplo','2026-06-25 12:34:48.902000',2500.00,4),(2,'Pomada para el Cabello',5,1,'s un producto de estilizado diseñado para moldear el cabello y mantener el peinado firme durante todo el día sin dejar el pelo rígido o acartonado. Su fórmula a base de agua es ideal porque proporciona un acabado limpio, permite','2026-06-25 12:59:28.008000',30000.00,10),(3,'peine',5,1,'peine','2026-06-25 14:47:12.193000',1000.00,15),(5,'Tijeras',5,1,'Cortan','2026-09-16 15:18:54.347000',5000.00,5);
/*!40000 ALTER TABLE `inventario_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notificaciones_notificacion`
--

DROP TABLE IF EXISTS `notificaciones_notificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notificaciones_notificacion` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `mensaje` longtext NOT NULL,
  `leida` tinyint(1) NOT NULL,
  `creada` datetime(6) NOT NULL,
  `cita_id` bigint(20) DEFAULT NULL,
  `usuario_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notificaciones_notificacion_cita_id_b71e9545_fk_citas_cita_id` (`cita_id`),
  KEY `notificaciones_notificacion_usuario_id_4bc090a3_fk_auth_user_id` (`usuario_id`),
  CONSTRAINT `notificaciones_notificacion_cita_id_b71e9545_fk_citas_cita_id` FOREIGN KEY (`cita_id`) REFERENCES `citas_cita` (`id`),
  CONSTRAINT `notificaciones_notificacion_usuario_id_4bc090a3_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=188 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notificaciones_notificacion`
--

LOCK TABLES `notificaciones_notificacion` WRITE;
/*!40000 ALTER TABLE `notificaciones_notificacion` DISABLE KEYS */;
INSERT INTO `notificaciones_notificacion` VALUES (1,'Tu cita del 14/09/2026 a las 11:00 AM (Mullet) fue cancelada.',1,'2026-08-30 18:14:27.640000',NULL,23),(2,'Se liberó un turno: 14/09/2026 a las 11:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-08-30 18:14:27.643000',NULL,23),(3,'Tu cita del 01/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:20.049000',60,23),(4,'Se liberó un turno: 01/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:20.051000',60,23),(5,'Tu cita del 02/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:20.055000',61,23),(6,'Se liberó un turno: 02/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:20.056000',61,23),(7,'Tu cita del 03/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:20.060000',62,23),(8,'Se liberó un turno: 03/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:20.061000',62,23),(9,'Tu cita del 04/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:20.066000',63,23),(10,'Se liberó un turno: 04/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:20.067000',63,23),(11,'Tu cita del 05/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:20.071000',64,23),(12,'Se liberó un turno: 05/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:20.072000',64,23),(13,'Tu cita del 06/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:20.077000',65,23),(14,'Se liberó un turno: 06/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:20.078000',65,23),(15,'Tu cita del 07/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:20.082000',66,23),(16,'Se liberó un turno: 07/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:20.083000',66,23),(17,'Tu cita del 08/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:20.087000',67,23),(18,'Se liberó un turno: 08/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:20.088000',67,23),(19,'Tu cita del 09/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:20.092000',68,23),(20,'Se liberó un turno: 09/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:20.094000',68,23),(21,'Tu cita del 10/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:20.098000',69,23),(22,'Se liberó un turno: 10/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:20.099000',69,23),(23,'Tu cita del 11/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:20.105000',70,23),(24,'Se liberó un turno: 11/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:20.106000',70,23),(25,'Tu cita del 12/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:20.110000',71,23),(26,'Se liberó un turno: 12/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:20.111000',71,23),(27,'Tu cita del 13/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:20.116000',72,23),(28,'Se liberó un turno: 13/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:20.117000',72,23),(29,'Tu cita del 14/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:20.121000',73,23),(30,'Se liberó un turno: 14/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:20.122000',73,23),(31,'Tu cita del 15/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:20.127000',74,23),(32,'Se liberó un turno: 15/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:20.128000',74,23),(33,'Tu cita del 01/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:36.071000',NULL,23),(34,'Se liberó un turno: 01/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:36.072000',NULL,23),(35,'Tu cita del 02/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:36.076000',NULL,23),(36,'Se liberó un turno: 02/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:36.077000',NULL,23),(37,'Tu cita del 03/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:36.081000',NULL,23),(38,'Se liberó un turno: 03/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:36.082000',NULL,23),(39,'Tu cita del 04/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:36.086000',NULL,23),(40,'Se liberó un turno: 04/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:36.087000',NULL,23),(41,'Tu cita del 05/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:36.091000',NULL,23),(42,'Se liberó un turno: 05/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:36.092000',NULL,23),(43,'Tu cita del 06/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:36.096000',NULL,23),(44,'Se liberó un turno: 06/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:36.097000',NULL,23),(45,'Tu cita del 07/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:36.100000',NULL,23),(46,'Se liberó un turno: 07/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:36.101000',NULL,23),(47,'Tu cita del 08/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:36.105000',NULL,23),(48,'Se liberó un turno: 08/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:36.106000',NULL,23),(49,'Tu cita del 09/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:36.110000',NULL,23),(50,'Se liberó un turno: 09/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:36.111000',NULL,23),(51,'Tu cita del 10/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:36.115000',NULL,23),(52,'Se liberó un turno: 10/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:36.116000',NULL,23),(53,'Tu cita del 11/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:36.121000',NULL,23),(54,'Se liberó un turno: 11/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:36.123000',NULL,23),(55,'Tu cita del 12/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:36.127000',NULL,23),(56,'Se liberó un turno: 12/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:36.128000',NULL,23),(57,'Tu cita del 13/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:36.131000',NULL,23),(58,'Se liberó un turno: 13/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:36.132000',NULL,23),(59,'Tu cita del 14/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:36.136000',NULL,23),(60,'Se liberó un turno: 14/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:36.137000',NULL,23),(61,'Tu cita del 15/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:36.141000',NULL,23),(62,'Se liberó un turno: 15/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:36.142000',NULL,23),(63,'Tu cita del 01/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:47.391000',NULL,23),(64,'Se liberó un turno: 01/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:47.392000',NULL,23),(65,'Tu cita del 02/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:47.396000',NULL,23),(66,'Se liberó un turno: 02/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:47.397000',NULL,23),(67,'Tu cita del 03/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:47.401000',NULL,23),(68,'Se liberó un turno: 03/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:47.402000',NULL,23),(69,'Tu cita del 04/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:47.406000',NULL,23),(70,'Se liberó un turno: 04/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:47.407000',NULL,23),(71,'Tu cita del 05/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:47.411000',NULL,23),(72,'Se liberó un turno: 05/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:47.412000',NULL,23),(73,'Tu cita del 06/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:47.416000',NULL,23),(74,'Se liberó un turno: 06/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:47.417000',NULL,23),(75,'Tu cita del 07/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:47.421000',NULL,23),(76,'Se liberó un turno: 07/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:47.422000',NULL,23),(77,'Tu cita del 08/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:47.426000',NULL,23),(78,'Se liberó un turno: 08/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:47.427000',NULL,23),(79,'Tu cita del 09/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:47.431000',NULL,23),(80,'Se liberó un turno: 09/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:47.432000',NULL,23),(81,'Tu cita del 10/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:47.436000',NULL,23),(82,'Se liberó un turno: 10/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:47.437000',NULL,23),(83,'Tu cita del 11/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:47.443000',NULL,23),(84,'Se liberó un turno: 11/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:47.444000',NULL,23),(85,'Tu cita del 12/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:47.448000',NULL,23),(86,'Se liberó un turno: 12/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:47.449000',NULL,23),(87,'Tu cita del 13/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:47.453000',NULL,23),(88,'Se liberó un turno: 13/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:47.454000',NULL,23),(89,'Tu cita del 14/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:47.458000',NULL,23),(90,'Se liberó un turno: 14/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:47.458000',NULL,23),(91,'Tu cita del 15/01/2020 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-01 11:30:47.462000',NULL,23),(92,'Se liberó un turno: 15/01/2020 a las 08:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-01 11:30:47.464000',NULL,23),(94,'Se liberó un turno: 21/08/2026 a las 11:15 AM (Taper Fade). Ya puedes ofrecerlo a otro cliente.',0,'2026-09-15 11:59:38.560000',57,23),(95,'Tu cita del 16/09/2026 a las 09:45 AM (Mullet) fue cancelada.',1,'2026-09-16 14:54:23.419000',75,20),(96,'Se liberó un turno: 16/09/2026 a las 09:45 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-16 14:54:23.421000',75,24),(97,'Tu cita del 16/09/2026 a las 09:00 AM (Mullet) fue cancelada.',1,'2026-09-16 14:55:45.509000',78,21),(98,'Se liberó un turno: 16/09/2026 a las 09:00 AM (Mullet). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-16 14:55:45.510000',78,24),(99,'Tu cita del 16/09/2026 a las 08:00 AM (Corte Texturizado) fue cancelada.',1,'2026-09-16 14:57:17.808000',77,20),(100,'Se liberó un turno: 16/09/2026 a las 08:00 AM (Corte Texturizado). Ya puedes ofrecerlo a otro cliente.',1,'2026-09-16 14:57:17.809000',77,24),(101,'Tu cita del 16/09/2026 a las 11:45 AM (Taper Fade) fue cancelada.',1,'2026-09-16 14:59:10.569000',79,21),(103,'Tu cita del 16/09/2026 a las 08:00 AM (Corte Clasico) fue cancelada.',1,'2026-09-16 15:51:16.123000',80,20),(105,'Tu cita del 16/09/2026 a las 08:00 AM (Taper Fade) fue cancelada.',1,'2026-09-16 15:51:40.775000',81,20),(107,'Tu cita del 16/09/2026 a las 08:00 AM (Mullet) fue cancelada.',1,'2026-09-16 15:52:02.223000',82,20),(109,'Tu cita del 16/09/2026 a las 08:00 AM (Corte Texturizado) fue cancelada.',1,'2026-09-16 15:53:03.401000',83,20),(111,'Tu cita del 17/09/2026 a las 10:30 AM fue cancelada. El turno del 17/09/2026 a las 10:30 AM con Jeison Cruz (Mullet) quedó disponible nuevamente.',1,'2026-09-18 11:27:08.054000',84,20),(112,'Tu cita con Yampol Bonilla fue cancelada. Este turno quedó libre: 17/09/2026 a las 10:30 AM (Mullet).',1,'2026-09-18 11:27:08.221000',84,25),(115,'Tu cita con samuel tellez fue cancelada. Este turno quedó libre: 17/09/2026 a las 08:00 AM (Taper Fade).',1,'2026-09-18 11:27:28.504000',76,25),(118,'Tu cita con samuel tellez fue cancelada. Este turno quedó libre: 19/09/2026 a las 09:20 AM (Mullet).',1,'2026-09-18 11:30:47.809000',85,25),(121,'Tu cita con samuel tellez fue cancelada. Este turno quedó libre: 18/09/2026 a las 08:00 AM (Mullet).',1,'2026-09-18 11:31:57.055000',87,25),(123,'Tu cita del 18/09/2026 a las 10:45 AM fue cancelada. El turno del 18/09/2026 a las 10:45 AM con Jeison Cruz (Mullet) quedó disponible nuevamente.',1,'2026-09-18 21:33:39.598000',90,21),(124,'Tu cita con camilo ladino fue cancelada. Este turno quedó libre: 18/09/2026 a las 10:45 AM (Mullet).',1,'2026-09-18 21:33:39.603000',90,25),(126,'Tu cita del 19/09/2026 a las 08:00 AM fue cancelada. El turno del 19/09/2026 a las 08:00 AM con Felipe Casas (Buzz Cut) quedó disponible nuevamente.',1,'2026-09-19 03:17:08.461000',91,22),(127,'Tu cita con samuel tellez fue cancelada. Este turno quedó libre: 19/09/2026 a las 08:00 AM (Buzz Cut).',1,'2026-09-19 03:17:08.462000',91,24),(129,'Tu cita del 22/09/2026 a las 11:40 AM fue cancelada. El turno del 22/09/2026 a las 11:40 AM con Felipe Casas (Corte Clasico) quedó disponible nuevamente.',1,'2026-09-19 03:17:10.155000',89,22),(130,'Tu cita con samuel tellez fue cancelada. Este turno quedó libre: 22/09/2026 a las 11:40 AM (Corte Clasico).',1,'2026-09-19 03:17:10.156000',89,24),(132,'Tu cita del 23/09/2026 a las 09:30 AM fue cancelada. El turno del 23/09/2026 a las 09:30 AM con Felipe Casas (Taper Fade) quedó disponible nuevamente.',1,'2026-09-19 03:17:11.551000',88,22),(133,'Tu cita con samuel tellez fue cancelada. Este turno quedó libre: 23/09/2026 a las 09:30 AM (Taper Fade).',1,'2026-09-19 03:17:11.552000',88,24),(135,'🆕 Nueva cita: samuel tellez el 19/09/2026 a las 08:00 AM. Servicio: Mullet. El cliente realizó un análisis con AutoAI. Puedes consultar el análisis en la cita.',1,'2026-09-19 03:18:04.804000',92,24),(136,'🆕 Nueva cita: Yampol Bonilla el 19/09/2026 a las 08:50 AM. Servicio: Mullet. El cliente realizó un análisis con AutoAI. Puedes consultar el análisis en la cita.',1,'2026-09-19 04:31:23.561000',93,24),(137,'Tu cita del 18/09/2026 a las 09:20 AM fue cancelada. El turno del 18/09/2026 a las 09:20 AM con Jeison Cruz (Mullet) quedó disponible nuevamente.',1,'2026-09-23 03:28:29.065000',86,20),(138,'Tu cita con Yampol Bonilla fue cancelada. Este turno quedó libre: 18/09/2026 a las 09:20 AM (Mullet).',0,'2026-09-23 03:28:29.068000',86,25),(140,'El turno del 18/09/2026 a las 09:20 AM con Jeison Cruz (Mullet) quedó disponible nuevamente.',0,'2026-09-23 03:28:29.070000',86,27),(141,'🆕 Nueva cita: camilo ladino el 23/09/2026 a las 02:00 PM. Servicio: Buzz Cut.',1,'2026-09-23 14:27:14.300000',94,24),(142,'🆕 Nueva cita: samuel tellez el 23/09/2026 a las 12:10 PM. Servicio: Buzz Cut.',1,'2026-09-23 14:34:53.192000',95,24),(143,'🆕 Nueva cita: samuel tellez el 23/09/2026 a las 10:00 AM. Servicio: Mullet.',1,'2026-09-23 14:36:06.874000',96,24),(144,'🆕 Nueva cita: samuel tellez el 24/09/2026 a las 10:00 AM. Servicio: Buzz Cut.',1,'2026-09-23 14:36:17.320000',97,24),(145,'🆕 Nueva cita: samuel tellez el 25/09/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:36:28.108000',98,24),(146,'🆕 Nueva cita: samuel tellez el 26/09/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:36:34.562000',99,24),(147,'🆕 Nueva cita: samuel tellez el 28/09/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:36:40.314000',100,24),(148,'🆕 Nueva cita: samuel tellez el 29/09/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:36:45.795000',101,24),(149,'🆕 Nueva cita: samuel tellez el 30/09/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:36:52.819000',102,24),(150,'🆕 Nueva cita: samuel tellez el 01/10/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:37:04.213000',103,24),(151,'🆕 Nueva cita: samuel tellez el 02/10/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:37:11.283000',104,24),(152,'🎉 ¡Felicitaciones! Completaste 10 cortes. Tu próximo corte será gratis.',1,'2026-09-23 14:38:02.241000',104,22),(153,'🆕 Nueva cita: camilo ladino el 23/09/2026 a las 10:00 AM. Servicio: Mullet.',1,'2026-09-23 14:38:41.425000',105,24),(154,'🆕 Nueva cita: camilo ladino el 24/09/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:38:47.932000',106,24),(155,'🆕 Nueva cita: camilo ladino el 25/09/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:38:54.630000',107,24),(156,'🆕 Nueva cita: camilo ladino el 26/09/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:39:10.521000',108,24),(157,'🆕 Nueva cita: camilo ladino el 28/09/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:39:23.187000',109,24),(158,'🆕 Nueva cita: camilo ladino el 29/09/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:39:31.553000',110,24),(159,'🆕 Nueva cita: camilo ladino el 30/09/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:39:37.662000',111,24),(160,'🆕 Nueva cita: camilo ladino el 01/10/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:39:52.785000',112,24),(161,'🆕 Nueva cita: camilo ladino el 02/10/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:40:01.067000',113,24),(162,'🆕 Nueva cita: camilo ladino el 07/10/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 14:40:20.076000',114,24),(163,'🆕 Nueva cita: camilo ladino el 24/09/2026 a las 08:00 AM. Servicio: Mullet.',1,'2026-09-23 15:06:19.242000',115,24),(164,'🎉 ¡Felicitaciones! Completaste 10 cortes. Tu próximo corte será gratis.',1,'2026-09-23 15:14:49.847000',115,21),(165,'🆕 Nueva cita: ashley velandia el 23/09/2026 a las 10:40 AM. Servicio: Mullet.',0,'2026-09-23 15:18:43.500000',NULL,25),(166,'🆕 Nueva cita: ashley velandia el 24/09/2026 a las 08:45 AM. Servicio: Mullet.',0,'2026-09-23 15:19:07.962000',NULL,25),(167,'🆕 Nueva cita: samuel tellez el 25/09/2026 a las 01:00 PM. Servicio: Buzz Cut.',1,'2026-09-23 15:55:39.298000',118,24),(168,'🆕 Nueva cita: camilo ladino el 23/09/2026 a las 11:20 AM. Servicio: Mullet.',1,'2026-09-23 15:56:05.540000',119,24),(169,'Tu cita del 25/09/2026 a las 01:00 PM fue cancelada. El turno del 25/09/2026 a las 01:00 PM con Felipe Casas (Buzz Cut) quedó disponible nuevamente.',1,'2026-10-07 12:32:29.739000',118,22),(170,'Tu cita con samuel tellez fue cancelada. Este turno quedó libre: 25/09/2026 a las 01:00 PM (Buzz Cut).',0,'2026-10-07 12:32:29.740000',118,24),(172,'El turno del 25/09/2026 a las 01:00 PM con Felipe Casas (Buzz Cut) quedó disponible nuevamente.',0,'2026-10-07 12:32:29.741000',118,27),(173,'🆕 Nueva cita: samuel tellez el 07/10/2026 a las 08:45 AM. Servicio: Mullet.',0,'2026-10-07 12:38:30.076000',120,24),(174,'Tu cita del 07/10/2026 a las 08:45 AM fue cancelada. El turno del 07/10/2026 a las 08:45 AM con Felipe Casas (Mullet) quedó disponible nuevamente.',1,'2026-10-07 12:47:28.151000',120,22),(175,'Tu cita con samuel tellez fue cancelada. Este turno quedó libre: 07/10/2026 a las 08:45 AM (Mullet).',0,'2026-10-07 12:47:28.158000',120,24),(177,'El turno del 07/10/2026 a las 08:45 AM con Felipe Casas (Mullet) quedó disponible nuevamente.',0,'2026-10-07 12:47:28.171000',120,27),(178,'Tu cita del 07/10/2026 a las 08:00 AM fue cancelada. El turno del 07/10/2026 a las 08:00 AM con Felipe Casas (Mullet) quedó disponible nuevamente.',0,'2026-10-07 12:48:04.804000',114,21),(179,'Tu cita con camilo ladino fue cancelada. Este turno quedó libre: 07/10/2026 a las 08:00 AM (Mullet).',0,'2026-10-07 12:48:04.812000',114,24),(181,'El turno del 07/10/2026 a las 08:00 AM con Felipe Casas (Mullet) quedó disponible nuevamente.',0,'2026-10-07 12:48:04.823000',114,27),(182,'🆕 Nueva cita: samuel tellez el 07/10/2026 a las 08:00 AM. Servicio: Mullet.',0,'2026-10-07 12:50:02.360000',121,24),(183,'🆕 Nueva cita: samuel tellez el 07/10/2026 a las 08:40 AM. Servicio: Mullet.',0,'2026-10-07 13:24:01.525000',122,25),(184,'Tu cita del 07/10/2026 a las 08:40 AM fue cancelada. El turno del 07/10/2026 a las 08:40 AM con Jeison Cruz (Mullet) quedó disponible nuevamente.',0,'2026-10-07 16:01:14.818000',122,22),(185,'Tu cita con samuel tellez fue cancelada. Este turno quedó libre: 07/10/2026 a las 08:40 AM (Mullet).',0,'2026-10-07 16:01:14.826000',122,25),(186,'El turno del 07/10/2026 a las 08:40 AM con Jeison Cruz (Mullet) quedó disponible nuevamente.',0,'2026-10-07 16:01:14.832000',122,19),(187,'El turno del 07/10/2026 a las 08:40 AM con Jeison Cruz (Mullet) quedó disponible nuevamente.',0,'2026-10-07 16:01:14.837000',122,27);
/*!40000 ALTER TABLE `notificaciones_notificacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notificaciones_suscripcionturno`
--

DROP TABLE IF EXISTS `notificaciones_suscripcionturno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notificaciones_suscripcionturno` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `hora` varchar(20) NOT NULL,
  `creada` datetime(6) NOT NULL,
  `barbero_id` bigint(20) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_suscripcion_turno_usuario` (`usuario_id`,`barbero_id`,`fecha`,`hora`),
  KEY `notificaciones_suscr_barbero_id_5bce0509_fk_barberos_` (`barbero_id`),
  CONSTRAINT `notificaciones_suscr_barbero_id_5bce0509_fk_barberos_` FOREIGN KEY (`barbero_id`) REFERENCES `barberos_barbero` (`id`),
  CONSTRAINT `notificaciones_suscr_usuario_id_88be728c_fk_auth_user` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notificaciones_suscripcionturno`
--

LOCK TABLES `notificaciones_suscripcionturno` WRITE;
/*!40000 ALTER TABLE `notificaciones_suscripcionturno` DISABLE KEYS */;
/*!40000 ALTER TABLE `notificaciones_suscripcionturno` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios_perfil`
--

DROP TABLE IF EXISTS `usuarios_perfil`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios_perfil` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `cedula` varchar(20) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cedula` (`cedula`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `usuarios_perfil_usuario_id_ca6ea2f9_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_perfil`
--

LOCK TABLES `usuarios_perfil` WRITE;
/*!40000 ALTER TABLE `usuarios_perfil` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios_perfil` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'barberspringfield_db'
--

--
-- Dumping routines for database 'barberspringfield_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-15 11:05:16
