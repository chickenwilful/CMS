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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (2,'Agency'),(1,'CallOperator'),(4,'CMSAdmin'),(3,'Rescue Agency');
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
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (30,1,25),(31,1,26),(32,1,27),(33,1,28),(34,1,29),(26,1,33),(27,1,34),(28,1,35),(29,1,36),(10,2,33),(11,2,34),(12,2,35),(13,2,36),(14,3,26),(16,3,29),(15,3,35),(21,4,25),(22,4,26),(23,4,27),(24,4,28),(25,4,29),(17,4,33),(18,4,34),(19,4,35),(20,4,36);
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
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add emergency situation',7,'add_emergencysituation'),(20,'Can change emergency situation',7,'change_emergencysituation'),(21,'Can delete emergency situation',7,'delete_emergencysituation'),(22,'Can add event',8,'add_event'),(23,'Can change event',8,'change_event'),(24,'Can delete event',8,'delete_event'),(25,'STORM - event create',8,'event_create'),(26,'STORM - event retrieve',8,'event_retrieve'),(27,'STORM - event update',8,'event_update'),(28,'STORM - event delete',8,'event_delete'),(29,'STORM - event list',8,'event_list'),(30,'Can add Post',9,'add_post'),(31,'Can change Post',9,'change_post'),(32,'Can delete Post',9,'delete_post'),(33,'STORM - post create',9,'post_create'),(34,'STORM - post update',9,'post_update'),(35,'STORM - post list',9,'post_list'),(36,'STORM - post delete',9,'post_delete'),(37,'Can add user profile',10,'add_userprofile'),(38,'Can change user profile',10,'change_userprofile'),(39,'Can delete user profile',10,'delete_userprofile'),(40,'Can add social token',11,'add_socialtoken'),(41,'Can change social token',11,'change_socialtoken'),(42,'Can delete social token',11,'delete_socialtoken'),(43,'Can add user object permission',12,'add_userobjectpermission'),(44,'Can change user object permission',12,'change_userobjectpermission'),(45,'Can delete user object permission',12,'delete_userobjectpermission'),(46,'Can add group object permission',13,'add_groupobjectpermission'),(47,'Can change group object permission',13,'change_groupobjectpermission'),(48,'Can delete group object permission',13,'delete_groupobjectpermission'),(49,'STORM - post retrieve',9,'post_retrieve');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (-1,'','2014-03-06 15:38:37',0,'AnonymousUser','','','',0,1,'2014-03-06 15:38:37'),(1,'pbkdf2_sha256$12000$oXVimc5noSsn$bZZOA2EyPIEKPYFcL8zi9vKI0HqnCJycWCIhsnVDNFw=','2014-03-09 17:41:13',1,'admin','','','admin@gmail.com',1,1,'2014-03-06 15:38:36'),(2,'pbkdf2_sha256$12000$B1AWmLiYf1jb$2geaPStsTEqC/uM+uNLzQXRSmsnkbUBWkXgGTnqK7ew=','2014-03-09 19:07:25',0,'yen','','','',1,1,'2014-03-06 15:47:54'),(3,'pbkdf2_sha256$12000$Sbs5OE7pk4ER$VRwVmjoVNJz8ZiTOR+qnkLALD5ctJ8kvRONvwxeU36U=','2014-03-09 19:57:20',0,'yen1','','','',0,1,'2014-03-09 19:57:20'),(4,'pbkdf2_sha256$12000$CWX8WQlnFTUS$Mr6hVCIQkzrorfqrJH2NAcvI+WqDqGbqDK5QRpbj9a4=','2014-03-09 19:59:18',0,'yen2','','','',0,1,'2014-03-09 19:59:18'),(5,'pbkdf2_sha256$12000$1Z4ZQa7PXJQ6$l3ebB158rNjJdagFPMYBvkQNJOisRJlk/ArlwTMqIuo=','2014-03-09 20:01:14',0,'yen3','','','',0,1,'2014-03-09 20:01:14');
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
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (6,2,1);
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
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (3,2,35);
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
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2014-03-06 15:41:10',1,3,'1','CallOperator',1,''),(2,'2014-03-06 15:41:40',1,3,'2','Agency',1,''),(3,'2014-03-06 15:42:56',1,3,'3','Rescue Agency',1,''),(4,'2014-03-06 15:43:42',1,3,'4','CMSAdmin',1,''),(5,'2014-03-06 15:47:55',1,4,'2','yen',1,''),(6,'2014-03-06 15:48:34',1,4,'2','yen',2,'Changed is_staff and groups.'),(7,'2014-03-06 15:52:00',1,4,'2','yen',2,'No fields changed.'),(8,'2014-03-06 15:52:18',1,3,'1','CallOperator',2,'No fields changed.'),(9,'2014-03-06 16:07:24',1,4,'2','yen',2,'Changed user_permissions.'),(10,'2014-03-06 16:08:03',1,4,'2','yen',2,'Changed user_permissions.'),(11,'2014-03-06 16:08:41',1,4,'2','yen',2,'Changed user_permissions.'),(12,'2014-03-06 16:10:16',1,4,'2','yen',2,'No fields changed.');
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'emergency situation','event','emergencysituation'),(8,'event','event','event'),(9,'Post','post','post'),(10,'user profile','storm_user','userprofile'),(11,'social token','socialnetwork','socialtoken'),(12,'user object permission','guardian','userobjectpermission'),(13,'group object permission','guardian','groupobjectpermission');
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
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('a3td4em8duom0pzkbc7mx8qhdloltnt3','M2YwNTM4M2E1MmY3YjlhNzJhZDUyZmY5ZDMwMTI1MTNkMmQ5MTVlMzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6Mn0=','2014-03-23 19:07:25'),('t6wgeb3lp0fo70yydqfs0h42xazjop0z','NjJmMTk3NzhjNmJiNGU5YTExMDYyOTI2OWRiM2M0YTFiY2FmOTc0NDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-03-20 16:09:58');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_emergencysituation`
--

LOCK TABLES `event_emergencysituation` WRITE;
/*!40000 ALTER TABLE `event_emergencysituation` DISABLE KEYS */;
INSERT INTO `event_emergencysituation` VALUES (1,'Haze'),(2,'Bird Flu');
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
  `caller_name` varchar(255) NOT NULL,
  `caller_phone_number` varchar(255) NOT NULL,
  `postal_code` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `event_event_403d8ff3` (`type_id`),
  KEY `event_event_0c98d849` (`created_by_id`),
  CONSTRAINT `type_id_refs_id_30003863` FOREIGN KEY (`type_id`) REFERENCES `event_emergencysituation` (`id`),
  CONSTRAINT `created_by_id_refs_id_557a7f7d` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_event`
--

LOCK TABLES `event_event` WRITE;
/*!40000 ALTER TABLE `event_event` DISABLE KEYS */;
INSERT INTO `event_event` VALUES (1,1,'title','eefef',2,'2014-03-09 18:30:01','caller_name','caller_phone_number','default postal code'),(2,2,'bird Fluuuu','w',2,'2014-03-09 18:32:30','caller_name','caller_phone_number','default postal code');
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
  KEY `event_event_related_to_a41e20fe` (`event_id`),
  KEY `event_event_related_to_6340c63c` (`user_id`),
  CONSTRAINT `event_id_refs_id_eedfb948` FOREIGN KEY (`event_id`) REFERENCES `event_event` (`id`),
  CONSTRAINT `user_id_refs_id_c187fb5e` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_event_related_to`
--

LOCK TABLES `event_event_related_to` WRITE;
/*!40000 ALTER TABLE `event_event_related_to` DISABLE KEYS */;
INSERT INTO `event_event_related_to` VALUES (3,1,-1),(1,1,1),(2,1,2);
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
  `title` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `imageLink` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `isShared` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `post_post_0c98d849` (`created_by_id`),
  CONSTRAINT `created_by_id_refs_id_6bf93826` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_post`
--

LOCK TABLES `post_post` WRITE;
/*!40000 ALTER TABLE `post_post` DISABLE KEYS */;
INSERT INTO `post_post` VALUES (1,'post 11','posttststststs','wef','2014-03-06 15:46:38',1,0),(2,'post 1','post 2','','2014-03-09 17:40:11',1,1);
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
  `phone_number` varchar(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_123684c7` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `storm_user_userprofile`
--

LOCK TABLES `storm_user_userprofile` WRITE;
/*!40000 ALTER TABLE `storm_user_userprofile` DISABLE KEYS */;
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

-- Dump completed on 2014-03-12 20:18:32
