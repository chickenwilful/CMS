CREATE DATABASE  IF NOT EXISTS `storm` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `storm`;
-- MySQL dump 10.13  Distrib 5.6.13, for Win32 (x86)
--
-- Host: localhost    Database: storm
-- ------------------------------------------------------
-- Server version	5.6.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (2,'Agency'),(4,'CallOperator'),(1,'CMSAdmin'),(5,'PMOfficer'),(3,'RescueAgency');
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
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `permission_id_refs_id_6ba0f519` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,1,5),(6,1,6),(7,1,7),(8,1,8),(9,1,9),(10,1,10),(11,1,11),(12,1,12),(13,1,13),(14,1,14),(15,1,15),(16,1,16),(17,1,17),(18,1,18),(19,1,19),(20,1,20),(21,1,21),(22,1,22),(23,1,23),(24,1,24),(25,1,25),(26,1,26),(27,1,27),(28,1,28),(29,1,29),(30,1,30),(31,1,31),(32,1,32),(33,1,33),(34,1,34),(35,1,35),(36,1,36),(37,1,37),(38,1,38),(39,1,39),(40,1,40),(41,1,41),(42,1,42),(43,1,43),(53,2,33),(54,2,34),(55,2,35),(56,2,36),(57,2,37),(46,3,26),(47,3,29),(60,4,25),(61,4,26),(62,4,27),(63,4,28),(64,4,29),(58,4,35),(59,4,37);
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
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add emergency situation',7,'add_emergencysituation'),(20,'Can change emergency situation',7,'change_emergencysituation'),(21,'Can delete emergency situation',7,'delete_emergencysituation'),(22,'Can add event',8,'add_event'),(23,'Can change event',8,'change_event'),(24,'Can delete event',8,'delete_event'),(25,'STORM - event create',8,'event_create'),(26,'STORM - event retrieve',8,'event_retrieve'),(27,'STORM - event update',8,'event_update'),(28,'STORM - event delete',8,'event_delete'),(29,'STORM - event list',8,'event_list'),(30,'Can add Post',9,'add_post'),(31,'Can change Post',9,'change_post'),(32,'Can delete Post',9,'delete_post'),(33,'STORM - post create',9,'post_create'),(34,'STORM - post update',9,'post_update'),(35,'STORM - post list',9,'post_list'),(36,'STORM - post delete',9,'post_delete'),(37,'STORM - post retrieve',9,'post_retrieve'),(38,'Can add user profile',10,'add_userprofile'),(39,'Can change user profile',10,'change_userprofile'),(40,'Can delete user profile',10,'delete_userprofile'),(41,'Can add social token',11,'add_socialtoken'),(42,'Can change social token',11,'change_socialtoken'),(43,'Can delete social token',11,'delete_socialtoken');
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
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$12000$zaUi9os2cAfi$xA9XuWgG0keDmJxFyR/Tj/FjtheDmwtPj9MOwzpli+Q=','2014-04-03 10:04:27',1,'admin','','','admin@email.com',1,1,'2014-03-22 09:30:39'),(6,'pbkdf2_sha256$12000$3RUT8JtxITqM$X0yJstO8tVusnpkDE9ToAmOfuBg3xQ886t0PNenkFnU=','2014-03-26 15:11:15',0,'calloperator1','calloperator1','calloperator1','calloperator1@hotmail.com',0,1,'2014-03-26 15:11:15'),(7,'pbkdf2_sha256$12000$XPxVMPehfi9t$hecjmtCClCH/62z8MgpfezANKDgfTpaoei13zELNNDM=','2014-03-26 15:11:44',0,'calloperator2','calloperator2','calloperator2','calloperator2@hotmail.com',0,1,'2014-03-26 15:11:44'),(8,'pbkdf2_sha256$12000$EJGU326V1HC6$9YScsPqB1b0FA0fVJJgKtAz9tWZ8npM6cuUeZB7jci0=','2014-03-26 15:12:03',0,'calloperator3','calloperator3','calloperator3','calloperator3@hotmail.com',0,1,'2014-03-26 15:12:03'),(9,'pbkdf2_sha256$12000$qbVkznSArjBN$7tA5A/7GHkYVYUL/Iq6tknPc6hCkL6TUqCVsY+Mrcb0=','2014-03-26 15:12:29',0,'pm_treasurer','pm_treasurer','pm_treasurer','pm_treasurer@edu.sg',0,1,'2014-03-26 15:12:29'),(10,'pbkdf2_sha256$12000$6WMhm9o3L51R$MzpjYqWWp52twOmp6ZQsyVBaCQ/gX3uLiYecedwi/6o=','2014-03-26 15:12:58',0,'pm_converser','pm_converser','pm_converser','pm_converser@gmail.com',0,1,'2014-03-26 15:12:58'),(11,'pbkdf2_sha256$12000$rx8Tao8VRGKX$y3J4AEhECPxmAEA1bzjqYk4rrhBpXUShEX77VpqCGtI=','2014-03-26 15:13:30',0,'pm_translator','pm_translator','pm_translator','pm_translator@hotmail.com',0,1,'2014-03-26 15:13:30'),(12,'pbkdf2_sha256$12000$PHCg5340ju0T$/OvBJ0eodJZX4RFTzCB486MQ13Uay7h4bXwfC5cljc0=','2014-03-26 15:13:52',0,'nea','nea','nea','nea@hotmail.com',0,1,'2014-03-26 15:13:52'),(13,'pbkdf2_sha256$12000$K8F12xyOR0qw$eEzkaAi6BBVnPDZcr9QtFux/As1OGv8W1pcTOJ3DAzQ=','2014-03-26 15:15:10',0,'ministry_environment_water','ministry_environment_water','ministry_environment_water','ministry_environment_water@hotmail.com',0,1,'2014-03-26 15:15:10'),(14,'pbkdf2_sha256$12000$wcVvdOMR9Qug$wUh2sy4CXd5062gTkuBddhcmL8p6JEbsBuRPlVd9blM=','2014-03-26 15:15:50',0,'weather_portal','weather_portal','weather_portal','weather_portal@sg.com',0,1,'2014-03-26 15:15:50'),(15,'pbkdf2_sha256$12000$SBtFYyZwJkpN$js53iJBcOPCCD9Gbe9AOcp+Apjvq1GrPrJ5qXYAXsYc=','2014-03-26 15:16:20',0,'spca','spca','spca','spca@edu.sg',0,1,'2014-03-26 15:16:20'),(16,'pbkdf2_sha256$12000$pm0vVgQcURVf$oRywjhZv0fR/LVAUbp2nTLl3FuFwyzAAlBf+QmAzqac=','2014-03-26 15:16:58',0,'scdf','scdf','scdf','scdf@gmail.com',0,1,'2014-03-26 15:16:58'),(17,'pbkdf2_sha256$12000$CG4D3gg5oOiP$5d5rAwf0qGpf5P+LBzGfzHHjDlajXCfEVKtuTazcrn0=','2014-03-26 15:17:29',0,'maritime_search_rescue','maritime_search_rescue','maritime_search_rescue','maritime_search_rescue@hotmail.com',0,1,'2014-03-26 15:17:29');
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
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `group_id_refs_id_274b862c` (`group_id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (10,1,1),(11,6,4),(12,7,4),(13,8,4),(14,9,5),(15,10,5),(16,11,5),(17,12,2),(18,13,2),(19,14,2),(20,15,3),(21,16,3),(22,17,3);
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
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `permission_id_refs_id_35d9ac25` (`permission_id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_refs_id_c0d12874` (`user_id`),
  KEY `content_type_id_refs_id_93d2d1f8` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2014-03-22 09:31:44',1,3,'1','CMSAdmin',1,''),(2,'2014-03-22 09:32:20',1,3,'2','Agency',1,''),(3,'2014-03-22 09:32:36',1,3,'3','Rescue Agency',1,''),(4,'2014-03-22 09:32:47',1,3,'4','CallOperator',1,''),(5,'2014-03-22 09:32:54',1,3,'3','RescueAgency',2,'Changed name.'),(6,'2014-03-22 09:33:02',1,3,'5','PMOfficer',1,''),(7,'2014-03-22 09:33:45',1,4,'2','emergency_ambulance',1,''),(8,'2014-03-22 09:34:12',1,4,'2','emergency_ambulance',2,'Changed email and groups.'),(9,'2014-03-22 09:34:13',1,4,'2','emergency_ambulance',2,'No fields changed.'),(10,'2014-03-22 09:34:43',1,10,'1','UserProfile object',1,''),(11,'2014-03-22 09:34:50',1,10,'1','UserProfile object',2,'No fields changed.'),(12,'2014-03-22 09:42:23',1,4,'3','rescue_and_evacuation',1,''),(13,'2014-03-22 09:43:35',1,4,'4','scdf',1,''),(14,'2014-03-22 09:43:52',1,4,'4','scdf',2,'Changed email.'),(15,'2014-03-22 09:44:12',1,10,'2','UserProfile object',1,''),(16,'2014-03-22 09:44:29',1,10,'3','UserProfile object',1,''),(17,'2014-03-22 09:45:04',1,7,'1','Dengue',1,''),(18,'2014-03-22 09:45:11',1,7,'2','Gas Leak',1,''),(19,'2014-03-22 09:45:38',1,7,'3','Fire',1,''),(20,'2014-03-22 09:45:46',1,7,'2','Gas_Leak',2,'Changed name.'),(21,'2014-03-22 14:08:40',1,4,'2','emergency_ambulance',2,'No fields changed.'),(22,'2014-03-22 14:08:47',1,4,'3','rescue_and_evacuation',2,'Changed groups.'),(23,'2014-03-22 14:08:54',1,4,'4','scdf',2,'Changed groups.'),(24,'2014-03-22 15:25:20',1,3,'3','RescueAgency',2,'Changed permissions.'),(25,'2014-03-22 15:59:28',1,4,'5','calloperator1',1,''),(26,'2014-03-22 15:59:49',1,4,'5','calloperator1',2,'Changed groups.'),(27,'2014-03-22 16:24:55',1,3,'3','RescueAgency',2,'No fields changed.'),(28,'2014-03-22 16:26:12',1,8,'4','title',2,'Changed related_to.'),(29,'2014-03-22 16:26:19',1,8,'2','title',2,'Changed related_to.'),(30,'2014-03-22 17:36:26',1,3,'4','CallOperator',2,'Changed permissions.'),(31,'2014-03-22 17:42:59',1,4,'4','scdf',2,'No fields changed.'),(32,'2014-03-22 17:43:21',1,3,'2','Agency',2,'Changed permissions.'),(33,'2014-03-22 17:44:05',1,3,'4','CallOperator',2,'Changed permissions.'),(34,'2014-03-24 06:12:59',1,4,'1','admin',2,'Changed groups.'),(35,'2014-03-24 06:13:31',1,4,'1','admin',2,'No fields changed.'),(36,'2014-03-24 06:59:02',1,4,'1','admin',2,'No fields changed.'),(37,'2014-03-26 15:10:46',1,4,'5','calloperator1',3,''),(38,'2014-03-26 15:10:46',1,4,'2','emergency_ambulance',3,''),(39,'2014-03-26 15:10:46',1,4,'3','rescue_and_evacuation',3,''),(40,'2014-03-26 15:10:46',1,4,'4','scdf',3,''),(41,'2014-03-26 15:11:15',1,4,'6','calloperator1',1,''),(42,'2014-03-26 15:11:32',1,4,'6','calloperator1',2,'Changed first_name, last_name, email and groups.'),(43,'2014-03-26 15:11:44',1,4,'7','calloperator2',1,''),(44,'2014-03-26 15:11:54',1,4,'7','calloperator2',2,'Changed first_name, last_name, email and groups.'),(45,'2014-03-26 15:12:03',1,4,'8','calloperator3',1,''),(46,'2014-03-26 15:12:13',1,4,'8','calloperator3',2,'Changed first_name, last_name, email and groups.'),(47,'2014-03-26 15:12:29',1,4,'9','pm_treasurer',1,''),(48,'2014-03-26 15:12:41',1,4,'9','pm_treasurer',2,'Changed first_name, last_name, email and groups.'),(49,'2014-03-26 15:12:58',1,4,'10','pm_converser',1,''),(50,'2014-03-26 15:13:08',1,4,'10','pm_converser',2,'Changed first_name, last_name, email and groups.'),(51,'2014-03-26 15:13:30',1,4,'11','pm_translator',1,''),(52,'2014-03-26 15:13:39',1,4,'11','pm_translator',2,'Changed first_name, last_name, email and groups.'),(53,'2014-03-26 15:13:52',1,4,'12','nea',1,''),(54,'2014-03-26 15:14:07',1,4,'12','nea',2,'Changed first_name, last_name, email and groups.'),(55,'2014-03-26 15:15:10',1,4,'13','ministry_environment_water',1,''),(56,'2014-03-26 15:15:19',1,4,'13','ministry_environment_water',2,'Changed first_name, last_name, email and groups.'),(57,'2014-03-26 15:15:51',1,4,'14','weather_portal',1,''),(58,'2014-03-26 15:16:00',1,4,'14','weather_portal',2,'Changed first_name, last_name, email and groups.'),(59,'2014-03-26 15:16:20',1,4,'15','spca',1,''),(60,'2014-03-26 15:16:33',1,4,'15','spca',2,'Changed first_name, last_name, email and groups.'),(61,'2014-03-26 15:16:58',1,4,'16','scdf',1,''),(62,'2014-03-26 15:17:08',1,4,'16','scdf',2,'Changed first_name, last_name, email and groups.'),(63,'2014-03-26 15:17:29',1,4,'17','maritime_search_rescue',1,''),(64,'2014-03-26 15:17:38',1,4,'17','maritime_search_rescue',2,'Changed first_name, last_name, email and groups.'),(65,'2014-03-26 15:18:00',1,7,'4','Accident',1,''),(66,'2014-03-26 15:18:22',1,8,'4','title',3,''),(67,'2014-03-26 15:18:22',1,8,'3','Fire in NTU',3,''),(68,'2014-03-26 15:18:22',1,8,'2','title',3,''),(69,'2014-03-26 15:18:22',1,8,'1','title',3,''),(70,'2014-03-26 15:19:21',1,8,'5','Marina Bay Suites fire: Two bodies found charred inside service lift',1,''),(71,'2014-03-26 15:19:30',1,8,'5','Marina Bay Suites fire: Two bodies found charred inside service lift',2,'Changed address.'),(72,'2014-03-26 15:20:53',1,8,'6','Singapore pollution record after Indonesia fires cause regional haze',1,''),(73,'2014-03-26 15:22:11',1,8,'7','Haze Shrouds Singapore and Malaysia',1,''),(74,'2014-03-26 15:23:42',1,8,'8','Gas leak detected in Bukit Merah; supply to 23 homes affected',1,''),(75,'2014-03-26 15:24:25',1,8,'9','PowerGas considering an appeal against $1.5 million fine imposed for gas leak',1,''),(76,'2014-03-26 15:24:49',1,8,'9','PowerGas considering an appeal against $1.5 million fine imposed for gas leak',2,'Changed postal_code and address.'),(77,'2014-03-26 15:26:08',1,8,'10','Pipeline leak disrupts gas supply on Jurong Island',1,''),(78,'2014-03-26 15:27:17',1,8,'11','Dengue epidemic in Singapore',1,''),(79,'2014-03-26 15:28:29',1,8,'12','Dengue cases remain high, with 656 so far this week',1,''),(80,'2014-03-26 15:29:48',1,8,'13','Dengue Fever on the Rise in Singapore',1,''),(81,'2014-03-26 15:31:10',1,8,'14','MPV driver crashes into 7-Eleven store at Dunearn Road because he mistook accelerator for brakes',1,''),(82,'2014-03-26 15:32:15',1,8,'15','Man who killed 4 in CTE accident identified',1,''),(83,'2014-03-26 15:33:06',1,8,'16','BKE accident leaves 2 injured and car ablaze',1,''),(84,'2014-03-26 15:34:04',1,10,'4','UserProfile object',1,''),(85,'2014-03-26 15:34:08',1,10,'4','UserProfile object',2,'No fields changed.'),(86,'2014-03-26 15:34:23',1,10,'5','UserProfile object',1,''),(87,'2014-03-26 15:34:34',1,10,'6','UserProfile object',1,''),(88,'2014-03-26 15:35:00',1,10,'7','UserProfile object',1,''),(89,'2014-03-26 15:35:28',1,10,'8','UserProfile object',1,''),(90,'2014-03-26 15:35:47',1,10,'9','UserProfile object',1,''),(91,'2014-03-26 15:36:08',1,10,'10','UserProfile object',1,''),(92,'2014-03-26 15:36:20',1,10,'11','UserProfile object',1,''),(93,'2014-03-26 15:36:31',1,10,'12','UserProfile object',1,''),(94,'2014-03-26 15:36:46',1,10,'13','UserProfile object',1,''),(95,'2014-03-26 15:37:16',1,10,'14','UserProfile object',1,''),(96,'2014-03-26 15:37:32',1,10,'15','UserProfile object',1,''),(97,'2014-03-26 15:40:06',1,10,'16','UserProfile object',1,''),(98,'2014-03-26 15:40:29',1,9,'6','wqdqwd',3,''),(99,'2014-03-26 15:40:29',1,9,'5','wqdqwd',3,''),(100,'2014-03-26 15:40:29',1,9,'4','wdqwd',3,''),(101,'2014-03-26 15:40:29',1,9,'3','qfqwfqw',3,''),(102,'2014-03-26 15:40:29',1,9,'2','qweqweq',3,''),(103,'2014-03-26 15:40:29',1,9,'1','wdw',3,''),(104,'2014-03-26 15:41:35',1,9,'8','Air pollution particulates promote hardening of the arteries and cardiovascular disease',1,''),(105,'2014-03-26 15:43:00',1,9,'9','Blaming China for mercury pollution is not solving the problem',1,''),(106,'2014-03-26 15:43:43',1,9,'10','The Battle Over Water',1,''),(107,'2014-03-26 15:44:22',1,9,'11','Air quality index in moderate range, as Singapore experiences slight haze',1,''),(108,'2014-03-26 15:45:27',1,9,'12','Soil Pollution A Cause For Concern?',1,''),(109,'2014-03-26 15:46:11',1,9,'13','Lightning Strike Fires Reignite Debate Over Gas Pipe Safety',1,''),(110,'2014-03-26 15:46:58',1,9,'14','Deadly gas leaks and aging pipes are growing problem',1,''),(111,'2014-03-26 15:48:10',1,9,'15','Two-year-old Cambodian girl dies of bird flu',1,''),(112,'2014-03-26 15:48:45',1,9,'16','229 dengue cases reported last week',1,''),(113,'2014-03-26 15:49:31',1,9,'17','Noise Pollution Control',1,''),(114,'2014-03-26 15:51:54',1,9,'18','Squatters into Citizens: The 1961 Bukit Ho Swee Fire and the Making of Modern Singapore',1,''),(115,'2014-03-26 15:53:58',1,9,'19','Dengue in Singapore',1,'');
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
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'emergency situation','event','emergencysituation'),(8,'event','event','event'),(9,'Post','post','post'),(10,'user profile','storm_user','userprofile'),(11,'social token','socialnetwork','socialtoken');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
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
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('82vl7ncwf5efgad1i19rg0fcipzp716t','ZmU4NDVhYTA1ZjM3ODk1ZTkwY2UzNzllZTgzNGM5MDJiNWQ0NzA5ZTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6NH0=','2014-04-07 07:06:47'),('b3vjd9jycmr8fqfhhuh0itma6t2qqhf0','OGNhNWU4ZWQ1OGFmOGQ4MTliNTI2NGZmMmU1MzI5YTE0YmUxY2VmMTp7fQ==','2014-04-09 15:54:07'),('giicq5k30x7dbdmdj3xfwubf6lpj0jf1','NjJmMTk3NzhjNmJiNGU5YTExMDYyOTI2OWRiM2M0YTFiY2FmOTc0NDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-04-05 13:12:56'),('kduoru9e9glr44axg59nw990fm9okrpx','NjJmMTk3NzhjNmJiNGU5YTExMDYyOTI2OWRiM2M0YTFiY2FmOTc0NDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-04-17 10:04:27'),('qaf92reqdyvt2mrqzis96avpajqb4fvg','NjJmMTk3NzhjNmJiNGU5YTExMDYyOTI2OWRiM2M0YTFiY2FmOTc0NDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-04-07 10:05:33');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_emergencysituation`
--

DROP TABLE IF EXISTS `event_emergencysituation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_emergencysituation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_emergencysituation`
--

LOCK TABLES `event_emergencysituation` WRITE;
/*!40000 ALTER TABLE `event_emergencysituation` DISABLE KEYS */;
INSERT INTO `event_emergencysituation` VALUES (1,'Dengue'),(2,'Gas_Leak'),(3,'Fire'),(4,'Accident');
/*!40000 ALTER TABLE `event_emergencysituation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_event`
--

DROP TABLE IF EXISTS `event_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext,
  `created_by_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `reporter_name` varchar(255) DEFAULT NULL,
  `reporter_phone_number` varchar(255) DEFAULT NULL,
  `postal_code` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by_id_refs_id_557a7f7d` (`created_by_id`),
  KEY `type_id_refs_id_30003863` (`type_id`),
  CONSTRAINT `type_id_refs_id_30003863` FOREIGN KEY (`type_id`) REFERENCES `event_emergencysituation` (`id`),
  CONSTRAINT `created_by_id_refs_id_557a7f7d` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_event`
--

LOCK TABLES `event_event` WRITE;
/*!40000 ALTER TABLE `event_event` DISABLE KEYS */;
INSERT INTO `event_event` VALUES (7,3,'Haze Shrouds Singapore and Malaysia','Smoke from forest fires in Indonesia has choked neighboring Singapore and Malaysia, prompting Singaporean officials to press Jakarta for urgent action against the haze that has pushed the city-state\'s air pollution to the worst level in 16 years. \r\n\r\nThe haze, blown from fires in Sumatra Island, hit Singapore and Peninsular Malaysia over the weekend and lifted air-pollution indexes in both countries into \"unhealthy\" territory. Iconic skyscrapers in Singapore\'s business district remained shrouded in smog Tuesday and some residents donned masks and stayed indoors. \r\n\r\nIn Singapore, the three-hour Pollutant Standards Index—a measure developed by the U.S. Environmental Protection Agency—peaked at 155 Monday night, the highest reading since September 1997 during Southeast Asia\'s worst air-pollution crisis. In Malaysia, the Air Pollutant Index rose as high as 161 on Saturday in Malacca. The smog is Malaysia\'s worst since 2005, when authorities declared a state of emergency in two areas. \r\n\r\nSingapore\'s National Environment Agency said the current bout of haze was due to \"drier weather conditions\" leading to \"an escalation in hot-spot activities mainly over central Sumatra,\" with as many as 138 hot spots indicating fires detected Sunday. \r\n\r\nThe agency said it has urged Indonesia to study \"urgent measures\" to tackle the haze, and has advised residents—particularly children, the elderly and those with heart or lung diseases—to cut back on strenuous and prolonged outdoor activity. Singapore\'s air quality remained at \"unhealthy\" levels as of 11 p.m. local time Tuesday, despite a short-lived improvement to \"moderate\" levels in the afternoon. \r\n\r\nIn Malaysia, authorities said API readings in three areas in the southern state of Johor remained in the \"unhealthy\" range, including the Pasir Gudang district with a reading of 148. For both Singapore and Malaysia, readings within the 51 to 100 range indicate \"moderate\" air quality, while 101 to 200 point to \"unhealthy\" conditions. Measurements between 201 and 300 represent a \"very unhealthy\" status, while readings above 300 indicate \"hazardous.\" \r\n\r\nCross-border haze is a recurring problem for Singapore and Malaysia since the 1980s, as prevailing winds blow over smoke from the seasonal burning of forest and peat in Sumatra. Singapore, a wealthy financial center reputed for its clean and green environment, is usually affected by haze in September and October, although the timing and severity varies. \r\n\r\nThe city-state\'s air quality last reached \"unhealthy\" levels in October 2010. The region\'s worst air-quality crisis occurred in September 1997, when Singapore\'s PSI spiked to a record high of 226, thanks to Indonesian forest fires set as a cheap but illegal way to clear land for plantations. \r\n\r\nThe burning triggered widespread anger in Southeast Asia, and caused billions of dollars in losses. While subsistence farmers and accidental causes have also been blamed, academics say most fires have been detected in plantation areas owned or to be used by palm oil companies.\r\n		',13,'2014-03-26 15:22:11','yen','99812723','520110','53 , Ang Mo Kio Ave 3 , #B2-26, Ang Mo Kio Hub , SINGAPORE  569933'),(10,2,'Pipeline leak disrupts gas supply in Four Season Hotel','A leak from an onshore gas pipeline - apparently caused by a third-party contractor - disrupted Indonesian natural gas supplies to some users including generating company PowerSeraya and seven petrochemical plants on Jurong Island. The pipeline, owned and operated by SP PowerGas, was transporting gas imported by Sembcorp from Indonesia\'s Natuna. \r\n\r\nThe pipeline leak, which occured at the junction of Sakra Road and Jurong Island Highway just before noon yesterday led authorities to shut traffic in and out of the petrochemicals island for about four hours on safety grounds. This affected thousands, as some 38,000 workers (8,000 full-time) reportedly enter Jurong Island daily. A JTC spokesman told BT that the authorities partially lifted the traffic clampdown sometime after 4 pm yesterday to and from the island which houses \"biggies\" like Shell, ExxonMobil and PetroChina. \r\n\r\nPowerGas is the sole licensed gas transporter and gas system operator in Singapore, delivering both natural gas and town gas. It owns the gas transmission and distribution networks here including 2,900 km of underground pipelines. BT understands that the 24-inch pipeline involved transports gas from one of the onshore gas receiving terminals to several of Sembcorp\'s customers on Jurong Island. \r\n\r\nChannel NewsAsia reported that the Singapore Civil Defence Force (SCDF) received a call about the gas leak at 12.18 pm yesterday. Two fire engines and a support vehicle were at the scene within five minutes, with personnel using water jets to suppress the gas leak.\r\n\r\nSaying that it was first notified about the gas leak at 11.55 am, a PowerGas spokesman added that there was no injury or fire resulting from the incident.\"PowerGas did not conduct any excavation works at the vicinity and was not carrying out any maintenance works to the affected pipeline at the time of the incident,\" the spokesman added. \"The gas pipeline damage could be caused by a third party contractor. PowerGas is investigating the cause of the damage and is working to restore the gas supply as soon as possible,\" he said. \r\n\r\nIt added that electricity generation has not been affected as the genco involved switched to an alternative fuel for power generation.When contacted, PowerSeraya chief executive John Ng confirmed that \"we had to switch one of our combined cycle gas turbines to use diesel instead.\" \r\n\r\nThe genco runs four CCGT plants, which means that operationally, a quarter of its power station was affected.While diesel costs more than gas, \"our priority is to make sure we can meet electricity demand,\" he told BT, adding that demand, especially for air-conditioning, was up yesterday as it was a very hot day.\r\n',8,'2014-03-26 15:26:08','Ly Phan','92737212','248646','190 Orchard Blvd, Singapore'),(13,1,'Dengue outbreak at Hall 7, NTU','A diminutive pest is threatening Singapore with an outsize bite, bringing this city-state to the cusp of its worst-yet tropical disease outbreak. The aedes mosquito, the carrier of the potentially fatal dengue fever, has been a constant nuisance for this Southeast Asian city-state. But the threat looms unusually large this year, and health officials are urging residents to take extra precautions. \r\n\r\nSo far this year, Singapore\'s health ministry has recorded more dengue cases than the 4,632 reported in the whole of 2012. Though there have been no deaths, weekly counts rose to 510 cases in the week that ended April 20, a new peak for 2013 and the highest since Singapore\'s worst dengue outbreak in 2005. Singapore is entering its peak dengue season, from May to October, in which warmer temperatures help the dengue virus multiply faster. \r\n\r\nHealth officials are concerned that weekly cases could jump above the record high of 713, or even breach the 1,000 mark. Dengue fever, a viral infection endemic to tropical and subtropical climates, is characterized by high fever, body aches and intense headache. In Singapore, the virus is transmitted to humans mainly by the female Aedes aegypti mosquito, an urban-dwelling pest that lays its eggs in stagnant water. \r\n\r\nNo vaccine or specific treatment is available for dengue, although severe cases may require patients to get intravenous rehydration to ensure adequate levels of body fluid. About 500,000 people with severe dengue require hospitalization globally each year, of which about 2.5% will die, according to the World Health Organization. But early detection and access to medical care can bring fatality rates below 1%.\r\n\r\nThe city-state maintains a strict disease and mosquito surveillance regime, as well as tough penalties for residents who fail to clear mosquito-breeding sites in their homes. Immunity to dengue is low in Singapore\'s population because of the intensive dengue-carrier controls, \"making the population vulnerable to outbreaks,\" said Ng Lee Ching, director of the Environmental Health Institute at Singapore\'s National Environment Agency.',6,'2014-03-26 15:29:48','zhiwei','92772636','637717','30 Nanyang Link, Singapore'),(16,4,'BKE accident in NUS campus','A car caught fire in NUS campus on Friday afternoon. Police said it was involved in an accident with another car and a tipper truck. Police said it was involved in an accident with another car and a tipper truck. \r\n\r\nThe Singapore Civil Defence Force (SCDF) said it was alerted at about 1.20pm. The accident happened along the BKE towards the Pan Island Expressway (PIE), before the Bukit Panjang exit. \r\n\r\nFirefighters appeared on the scene and put out the blaze with one hose reel. SCDF said a man and a woman, both in their 20s, were sent conscious to National University Hospital. Channel NewsAsia understands the pair had sustained their injuries in the accident prior to the fire, rather than from the flames.\r\n\r\n',14,'2014-03-26 15:33:06','zhiwei','92772636','119077','National University of Singapore');
/*!40000 ALTER TABLE `event_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_event_related_to`
--

DROP TABLE IF EXISTS `event_event_related_to`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_event_related_to` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `event_id` (`event_id`,`user_id`),
  KEY `user_id_refs_id_c187fb5e` (`user_id`),
  CONSTRAINT `event_id_refs_id_eedfb948` FOREIGN KEY (`event_id`) REFERENCES `event_event` (`id`),
  CONSTRAINT `user_id_refs_id_c187fb5e` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_event_related_to`
--

LOCK TABLES `event_event_related_to` WRITE;
/*!40000 ALTER TABLE `event_event_related_to` DISABLE KEYS */;
INSERT INTO `event_event_related_to` VALUES (12,7,13),(16,10,8),(19,13,6),(22,16,14);
/*!40000 ALTER TABLE `event_event_related_to` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guardian_groupobjectpermission`
--

DROP TABLE IF EXISTS `guardian_groupobjectpermission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `guardian_groupobjectpermission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_id` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `object_pk` varchar(255) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`,`object_pk`),
  KEY `guardian_groupobjectpermission_83d7f98b` (`permission_id`),
  KEY `guardian_groupobjectpermission_37ef4eb4` (`content_type_id`),
  KEY `guardian_groupobjectpermission_5f412f9a` (`group_id`),
  CONSTRAINT `content_type_id_refs_id_ca873eba` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `group_id_refs_id_d890d4d6` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_ab04ab90` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guardian_groupobjectpermission`
--

LOCK TABLES `guardian_groupobjectpermission` WRITE;
/*!40000 ALTER TABLE `guardian_groupobjectpermission` DISABLE KEYS */;
/*!40000 ALTER TABLE `guardian_groupobjectpermission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guardian_userobjectpermission`
--

DROP TABLE IF EXISTS `guardian_userobjectpermission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `guardian_userobjectpermission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_id` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `object_pk` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`,`object_pk`),
  KEY `guardian_userobjectpermission_83d7f98b` (`permission_id`),
  KEY `guardian_userobjectpermission_37ef4eb4` (`content_type_id`),
  KEY `guardian_userobjectpermission_6340c63c` (`user_id`),
  CONSTRAINT `content_type_id_refs_id_ccf6cb3f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `permission_id_refs_id_720a4b21` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_29f71157` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guardian_userobjectpermission`
--

LOCK TABLES `guardian_userobjectpermission` WRITE;
/*!40000 ALTER TABLE `guardian_userobjectpermission` DISABLE KEYS */;
/*!40000 ALTER TABLE `guardian_userobjectpermission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_post`
--

DROP TABLE IF EXISTS `post_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post_post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `imageLink` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `isPublished` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by_id_refs_id_6bf93826` (`created_by_id`),
  KEY `type_id_refs_id_666d278b` (`type_id`),
  CONSTRAINT `type_id_refs_id_666d278b` FOREIGN KEY (`type_id`) REFERENCES `event_emergencysituation` (`id`),
  CONSTRAINT `created_by_id_refs_id_6bf93826` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_post`
--

LOCK TABLES `post_post` WRITE;
/*!40000 ALTER TABLE `post_post` DISABLE KEYS */;
INSERT INTO `post_post` VALUES (8,3,'Air pollution particulates promote hardening of the arteries and cardiovascular disease','As heart disease marches on as the leading killer of Americans and those in western societies, researchers isolate yet another factor to be implicated in the advancement of this largely preventable disease. Poor diet, lack of physical activity, smoking and environmental and household pollutants all promote metabolic dysfunction that lead to ultimate arterial deterioration and an untimely death.\r\n\r\n Fortunately, health-minded individuals can make changes to prevent and even reverse heart disease. A research team from the University of Michigan School of Public Health has shown that long term exposure to air pollution may be linked to heart attacks and strokes by speeding up atherosclerosis, commonly known as \"hardening of the arteries\".\r\n\r\nLead author of the study, Dr. Sara Adar and her team have published their findings in the journal, PLOS Medicine. Dr. Adar noted \"Our findings help us to understand how it is that exposures to air pollution may cause the increases in heart attacks and strokes observed by other studies.\"  The scientists followed 5,362 people between the ages of 45 and 84 from six U.S. metropolitan areas enrolled as part of the Multi-Ethnic Study of Atherosclerosis and Air Pollution. \r\n\r\nNone of the participants had a pre-existing history of heart disease at the outset of the study. The researchers were able to link estimated air pollution levels at each person\'s house with two ultrasound measurements of blood vessel elasticity, separated by about three years.\r\n','http://www.naturalnews.com/gallery/300X250/Transportation/Air-Pollution-Exhaust-Pipe-Smoke.jpg','2014-03-26 15:41:35',6,1),(9,3,'Blaming China for mercury pollution is not solving the problem','Eighty-seven percent of all mercury falling on the United States comes from outside the country. Two thirds of worldwide mercury contamination comes from industrial pollution from Asia as mercury in the air settles into lakes, streams, and oceans. \r\n\r\nThere is a global reservoir of airborne mercury circulating worldwide and it is estimated that the annual input of mercury into this reservoir is a whopping 4,900 tons. \r\n\r\nState and federal officials are grappling with the fact that most of the mercury pollution comes from sources around the world and especially from large numbers of coal-fired power plants being built in China. \r\n\r\nIn the news lately is the State of Florida\'s Jan Mandrup-Poulsen, of the Watershed Protection Section who says, \"If we were to look at all the mercury sources in Florida and turn them all off, we wouldn\'t solve the mercury problem in Florida.\" As the State of Florida debates new environmental regulations, David Guest of Earthjustice, said the attempt to blame the bulk of the problem on other countries was ridiculous and allowed state regulators to avoid imposing tighter controls on the Florida power plants.\r\n','http://www.naturalnews.com/gallery/dir/Industrial/global-warming-smokestack.jpg','2014-03-26 15:43:00',7,1),(10,4,'The Battle Over Water','Dirty water is the world\'s biggest health risk, and continues to threaten both quality of life and public health in the United States. \r\n\r\nWhen water from rain and melting snow runs off roofs and roads into our rivers, it picks up toxic chemicals, dirt, trash and disease-carrying organisms along the way. \r\n\r\nMany of our water resources also lack basic protections, making them vulnerable to pollution from factory farms, industrial plants, and activities like fracking. This can lead to drinking water contamination, habitat degradation and beach closures.','http://www.nrdc.org/water/images/water-effluent.jpg','2014-03-26 15:43:43',8,1),(11,3,'Air quality index in moderate range, as Singapore experiences slight haze','Air quality in Singapore yesterday reached its worst level since the start of the year, with the haze affecting visibility in some areas and leaving a smell of smoke.The Pollutant Standards Index\'s (PSI) three-hour reading had gone from \"good\" - 31 at 9am - to \"moderate\" by 6pm, hitting a high of 71 at 8pm and falling to 61 two hours later. \r\n\r\nOn Thursday, the National Environment Agency (NEA) said that the transition from the Northeast Monsoon to the inter-monsoon period in the second half of March \"may pose some risk of transboundary haze affecting Singapore\". \r\n\r\nThe Riau province of Sumatra has been shrouded in dense haze over recent days as farmers set fires to clear land during the dry spell. On March 5, NEA detected six hotspots in Sumatra, Indonesia and 47 hotspots in peninsular Malaysia. \r\n\r\nBut it added that the low hotspot count for Sumatra was due to cloud cover and partial satellite coverage.\r\n','http://www.straitstimes.com/sites/straitstimes.com/files/imagecache/story-gallery-featured/20140307/sjc01haze73e.jpg','2014-03-26 15:44:22',17,1),(12,4,'Soil Pollution A Cause For Concern?','With the rise of concrete buildings and roads, one part of the Earth that we rarely see is the soil. It has many different names, such as dirt, mud and ground. \r\n\r\nHowever, it is definitely very important to us. The plants that feed us grow in soil and keeping it healthy is essential to maintaining a beautiful planet. However, like all other forms of nature, soil also suffers from pollution. The pollution of soil is a common thing these days, and it happens due to the presence of man made elements. \r\n\r\nThe main reason why the soil becomes contaminated is due to the presence of man made waste. The waste produced from nature itself such as dead plants, carcasses of animals and rotten fruits and vegetables only adds to the fertility of the soil. However, our waste products are full of chemicals that are not originally found in nature and lead to soil pollution. \r\n\r\n1. Industrial Activity: Industrial activity has been the biggest contributor to the problem in the last century, especially since the amount of mining and manufacturing has increased. \r\n\r\nMost industries are dependent on extracting minerals from the Earth. Whether it is iron ore or coal, the by products are contaminated and they are not disposed off in a manner that can be considered safe. As a result, the industrial waste lingers in the soil surface for a long time and makes it unsuitable for use.\r\n','http://www.conserve-energy-future.com/wp-content/uploads/2013/07/soil_pollution.jpg','2014-03-26 15:45:27',13,1),(13,3,'Lightning Strike Fires Reignite Debate Over Gas Pipe Safety','Ross and Meg Rushing were entertaining a friend at their brand-new home in Lubbock, Texas, on Aug. 24, 2012, when a clap of thunder appeared to set off their burglar alarm.Unable to turn it off, Ross Rushing and his friend, Brennen Teel, went to the garage to get a ladder so they could disable the system. “That’s when the explosion happened,” Rushing recalled. \r\n\r\n“Honestly, I thought I was dead immediately.” Rushing was able to climb out from under the buckled garage door, but couldn’t locate Teel in the thick black smoke that was now pouring from the home. Firefighters later found his body at the rear of the garage. \r\n\r\nInvestigators believe he opened the drop-down attic staircase, not realizing the attic was ablaze. Oxygen rushed in, causing a back-draft explosion that killed the 31-year-old Teel, a resident of Heath, Texas, they said. Meg and Ross Rushing escaped the fire that destroyed their home in Lubbock, Texas. \r\n\r\nBut their friend, Brennen Teel, above, who had been visiting for the night did not. He died in the couple\'s garage in a fire and explosion allegedly caused by the failure of flexible piping carrying natural gas following a lightning strike.\r\n','http://media4.s-nbcnews.com/j/newscms/2014_12/258646/140317-pipe-explosions-teel-cover-inline_0e1b5f111b1b65de48185efed34a4431.nbcnews-ux-640-480.jpg','2014-03-26 15:46:11',12,1),(14,2,'Deadly gas leaks and aging pipes are growing problem','With the Bravest still on the scene, the place blew up. Three people were injured, including a firefighter and the homeowner who later said everything exploded when he opened his basement door. The entire neighborhood near Delaware St. in Dongan Hills had to be evacuated. \r\n\r\nThat was just one of 38 “incidents” stemming from natural gas leaks in New York City between 2004 and February 2014. In the last decade, gas leaks have resulted in three other fatalities and 12 injuries across the city. \r\n\r\nSeveral people were critically injured. As the investigation continues into the cause of last week’s East Harlem blast that resulted in eight deaths and more than 50 injuries, increased attention has been paid on the danger of natural gas, which now provides 65% of the heat and hot water to New York City households. \r\n\r\nThat percentage has increased in recent years.As the investigation continues into the cause of last week’s East Harlem blast that resulted in eight deaths and more than 50 injuries, increased attention has been paid on the danger of natural gas, which now provides 65% of the heat and hot water to New York City households. That percentage has increased in recent years. \r\n\r\nA Daily News review of records filed with the federal Pipeline and Hazardous Materials Safety Administration found that gas leaks occur fairly frequently in the city, with injuries occurring on a regular basis due to pinholes, punctures and all-around failures of gas mains and the service lines that connect to homes. \r\n\r\nWith Con Edison alone, records show there have been more than 105,000 gas leaks in the city from 2009 through February. Federal records show that included nearly 12,000 that were caused by corroded pipes, some of which are more than 100 years old.\r\n','http://assets.nydailynews.com/polopoly_fs/1.1722994.1394928251!/img/httpImage/image.jpg_gen/derivatives/landscape_635/gasline16n-4-web.jpg','2014-03-26 15:46:58',10,1),(15,4,'Two-year-old Cambodian girl dies of bird flu','A two-year-old Cambodian girl has died from bird flu, becoming the country\'s fourth confirmed fatality -- all children -- from the deadly virus this year, health authorities said on Monday. The girl from the southern province of Kampot died on Friday a day after she was admitted to hospital, the health ministry said in a joint statement with the World Health Organisation (WHO). \r\n\r\nTests confirmed she had contracted the H5N1 virus, it said, adding the girl had direct contact with dead chickens in a village where most of the poultry had perished over the last few weeks. Health Minister Mam Bunheng urged parents to ensure their children do not touch birds. \"Avian influenza H5N1 remains a serious threat to the health of all Cambodians and more so for children,\" he said in the statement. \r\n\r\nThe disease typically spreads from birds to humans through direct contact. But experts fear it could mutate into a form easily transmissible between humans, with the potential to trigger a pandemic. Authorities have struggled to control bird flu outbreaks in Cambodia. \r\n\r\nIt recorded 14 deaths from the illness last year, the deadliest outbreak of the virus in the country since 2003. An eight-year-old boy from the eastern province of Kratie died in February. His two-year-old sister died the same day but authorities said tests could not be carried out to confirm she had the virus.		\r\n','http://www.naturalnews.com/gallery/BirdFlu/14.jpg','2014-03-26 15:48:10',11,1),(16,1,'229 dengue cases reported last week','The number of dengue cases reported last week went up compared to the week before. There were 229 cases from March 9 to March 15, up from the 210 cases reported in the week of March 2 to March 8.  \r\n\r\nLatest figures from the Health Ministry show there were 229 cases from March 9 to March 15, up from the 210 cases reported in the week of March 2 to March 8. \r\n\r\nSo far, there have been 38 new cases reported this week. This brings the total number of cases this year to 3,351.\r\n','http://therealsingapore.com/sites/default/files/field/image/Latest-Dengue-Fever-in-Lahore-Punjab-Dengue-Report-Updates2.jpg','2014-03-26 15:48:45',9,1),(17,4,'Noise Pollution Control','In land-scarce Singapore, developments often have to be carried out near residential areas and other Noise Sensitive Receivers (NSRs) such as hospitals, schools, etc. \r\n\r\nTo ensure that our construction works do not affect residents and businesses, noise levels are continuously monitored and kept within the National Environment Agency (NEA) permissible levels. \r\n\r\nContractors must comply with the following noise pollution control requirements: Prior to the commencement of works, contractors are required to carry out a baseline noise survey for one week, on a 24-hour basis, to establish the background noise levels. \r\n\r\nA Noise Management Plan must be submitted before any construction work is started. The plans must include the baseline noise record, indicate the Noise Sensitive Receivers (NSRs) and proposed mitigation measures and public relation strategies to handle noise matters. \r\n\r\nThroughout the construction duration, contractors must implement all practicable measures while continuously monitoring the noise levels closely. For effective noise control, the main focus should be on control at source supplemented with control at pathway.','http://www.lta.gov.sg/content/dam/ltaweb/corp/Industry/img/earth_control8.JPG','2014-03-26 15:49:31',16,1),(18,3,'Squatters into Citizens: The 1961 Bukit Ho Swee Fire and the Making of Modern Singapore','The crowded, bustling, \'squatter\' kampongs so familiar across Southeast Asia have long since disappeared from Singapore, leaving few visible traces of their historical influence on the life in the city-state. In one such settlement, located in an area known as Bukit Ho Swee, a great fire in 1961 destroyed the kampong and left 16,000 people homeless, creating a national emergency that led to the first big public housing project of the new Housing and Development Board (HDB). \r\n\r\nHDB flats now house more than four-fifths of the Singapore population, making the aftermath of the Bukit Ho Swee fire a seminal event in modern Singapore.','http://www.nus.edu.sg/nuspress/images/Squatters-into-Citizens-Front-Cover.jpg','2014-03-26 15:51:54',16,1),(19,1,'Dengue in Singapore','The number of new dengue cases is continuing to fall, with 306 reported last week.','http://www.straitstimes.com/sites/straitstimes.com/files/imagecache/listing-page-large/20130730/36478.jpg','2014-03-26 15:53:58',14,1);
/*!40000 ALTER TABLE `post_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialnetwork_socialtoken`
--

DROP TABLE IF EXISTS `socialnetwork_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialnetwork_socialtoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `site` varchar(255) NOT NULL,
  `main_token` varchar(255) NOT NULL,
  `sub_token` varchar(255) DEFAULT NULL,
  `expiry_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialnetwork_socialtoken`
--

LOCK TABLES `socialnetwork_socialtoken` WRITE;
/*!40000 ALTER TABLE `socialnetwork_socialtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialnetwork_socialtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `storm_user_userprofile`
--

DROP TABLE IF EXISTS `storm_user_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `storm_user_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `phone_number` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_123684c7` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `storm_user_userprofile`
--

LOCK TABLES `storm_user_userprofile` WRITE;
/*!40000 ALTER TABLE `storm_user_userprofile` DISABLE KEYS */;
INSERT INTO `storm_user_userprofile` VALUES (4,1,'98172721','Administrator'),(5,6,'91721122','Call Operator 1'),(6,7,'9187712','Call Operator 2'),(7,17,'91821771','Maritime Search & Rescue'),(8,13,'91721727','Ministry of Environment & Water Resources'),(9,12,'9181288','National Environment Agency'),(10,10,'9281123','Prime Minister Converser'),(11,11,'91182881','Prime Minister Translator'),(12,9,'91818818','Prime Minister Treasurer'),(13,16,'91981991','Singapore Civil Defence Force'),(14,15,'1800 819 1811','Singapore Prevention of Cruelty to Animals'),(15,14,'9181812','Singapore Weather Portal'),(16,8,'97171662','Call Operator 3');
/*!40000 ALTER TABLE `storm_user_userprofile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-04-03 18:14:37
