-- MySQL dump 10.13  Distrib 5.1.57, for apple-darwin11.0.0 (i386)
--
-- Host: localhost    Database: treeio
-- ------------------------------------------------------
-- Server version	5.1.57

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
-- Table structure for table `account_notification`
--

DROP TABLE IF EXISTS `account_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recipient_id` int(11) NOT NULL,
  `body` longtext,
  `ntype` varchar(1) NOT NULL,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_notification_fcd09624` (`recipient_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_notification`
--

LOCK TABLES `account_notification` WRITE;
/*!40000 ALTER TABLE `account_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_notificationsetting`
--

DROP TABLE IF EXISTS `account_notificationsetting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_notificationsetting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner_id` int(11) NOT NULL,
  `ntype` varchar(1) NOT NULL,
  `next_date` date DEFAULT NULL,
  `last_datetime` datetime NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `owner_id` (`owner_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_notificationsetting`
--

LOCK TABLES `account_notificationsetting` WRITE;
/*!40000 ALTER TABLE `account_notificationsetting` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_notificationsetting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_notificationsetting_modules`
--

DROP TABLE IF EXISTS `account_notificationsetting_modules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_notificationsetting_modules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notificationsetting_id` int(11) NOT NULL,
  `module_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `notificationsetting_id` (`notificationsetting_id`,`module_id`),
  KEY `account_notificationsetting_modules_2577b508` (`notificationsetting_id`),
  KEY `account_notificationsetting_modules_f53ed95e` (`module_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_notificationsetting_modules`
--

LOCK TABLES `account_notificationsetting_modules` WRITE;
/*!40000 ALTER TABLE `account_notificationsetting_modules` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_notificationsetting_modules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_consumer`
--

DROP TABLE IF EXISTS `api_consumer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_consumer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `key` varchar(18) NOT NULL,
  `secret` varchar(32) NOT NULL,
  `status` varchar(16) NOT NULL,
  `owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `api_consumer_5d52dd10` (`owner_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_consumer`
--

LOCK TABLES `api_consumer` WRITE;
/*!40000 ALTER TABLE `api_consumer` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_consumer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_nonce`
--

DROP TABLE IF EXISTS `api_nonce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_nonce` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token_key` varchar(18) NOT NULL,
  `consumer_key` varchar(18) NOT NULL,
  `key` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_nonce`
--

LOCK TABLES `api_nonce` WRITE;
/*!40000 ALTER TABLE `api_nonce` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_nonce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_token`
--

DROP TABLE IF EXISTS `api_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_token` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(18) NOT NULL,
  `secret` varchar(32) NOT NULL,
  `verifier` varchar(10) NOT NULL,
  `token_type` int(11) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `consumer_id` int(11) DEFAULT NULL,
  `callback` varchar(255) DEFAULT NULL,
  `callback_confirmed` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_token_fbfc09f1` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_token`
--

LOCK TABLES `api_token` WRITE;
/*!40000 ALTER TABLE `api_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_token` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
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
  KEY `auth_group_permissions_425ae3c4` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
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
  KEY `auth_permission_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=262 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add message',4,'add_message'),(11,'Can change message',4,'change_message'),(12,'Can delete message',4,'delete_message'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add site',7,'add_site'),(20,'Can change site',7,'change_site'),(21,'Can delete site',7,'delete_site'),(22,'Can add log entry',8,'add_logentry'),(23,'Can change log entry',8,'change_logentry'),(24,'Can delete log entry',8,'delete_logentry'),(25,'Can add access entity',9,'add_accessentity'),(26,'Can change access entity',9,'change_accessentity'),(27,'Can delete access entity',9,'delete_accessentity'),(28,'Can add group',10,'add_group'),(29,'Can change group',10,'change_group'),(30,'Can delete group',10,'delete_group'),(31,'Can add user',11,'add_user'),(32,'Can change user',11,'change_user'),(33,'Can delete user',11,'delete_user'),(34,'Can add invitation',12,'add_invitation'),(35,'Can change invitation',12,'change_invitation'),(36,'Can delete invitation',12,'delete_invitation'),(37,'Can add tag',13,'add_tag'),(38,'Can change tag',13,'change_tag'),(39,'Can delete tag',13,'delete_tag'),(40,'Can add comment',14,'add_comment'),(41,'Can change comment',14,'change_comment'),(42,'Can delete comment',14,'delete_comment'),(43,'Can add object',15,'add_object'),(44,'Can change object',15,'change_object'),(45,'Can delete object',15,'delete_object'),(46,'Can add revision',16,'add_revision'),(47,'Can change revision',16,'change_revision'),(48,'Can delete revision',16,'delete_revision'),(49,'Can add revision field',17,'add_revisionfield'),(50,'Can change revision field',17,'change_revisionfield'),(51,'Can delete revision field',17,'delete_revisionfield'),(52,'Can add update record',18,'add_updaterecord'),(53,'Can change update record',18,'change_updaterecord'),(54,'Can delete update record',18,'delete_updaterecord'),(55,'Can add module',19,'add_module'),(56,'Can change module',19,'change_module'),(57,'Can delete module',19,'delete_module'),(58,'Can add perspective',20,'add_perspective'),(59,'Can change perspective',20,'change_perspective'),(60,'Can delete perspective',20,'delete_perspective'),(61,'Can add module setting',21,'add_modulesetting'),(62,'Can change module setting',21,'change_modulesetting'),(63,'Can delete module setting',21,'delete_modulesetting'),(64,'Can add location',22,'add_location'),(65,'Can change location',22,'change_location'),(66,'Can delete location',22,'delete_location'),(67,'Can add page folder',23,'add_pagefolder'),(68,'Can change page folder',23,'change_pagefolder'),(69,'Can delete page folder',23,'delete_pagefolder'),(70,'Can add page',24,'add_page'),(71,'Can change page',24,'change_page'),(72,'Can delete page',24,'delete_page'),(73,'Can add widget',25,'add_widget'),(74,'Can change widget',25,'change_widget'),(75,'Can delete widget',25,'delete_widget'),(76,'Can add folder',26,'add_folder'),(77,'Can change folder',26,'change_folder'),(78,'Can delete folder',26,'delete_folder'),(79,'Can add file',27,'add_file'),(80,'Can change file',27,'change_file'),(81,'Can delete file',27,'delete_file'),(82,'Can add document',28,'add_document'),(83,'Can change document',28,'change_document'),(84,'Can delete document',28,'delete_document'),(85,'Can add web link',29,'add_weblink'),(86,'Can change web link',29,'change_weblink'),(87,'Can delete web link',29,'delete_weblink'),(88,'Can add event',30,'add_event'),(89,'Can change event',30,'change_event'),(90,'Can delete event',30,'delete_event'),(91,'Can add invitation',31,'add_invitation'),(92,'Can change invitation',31,'change_invitation'),(93,'Can delete invitation',31,'delete_invitation'),(94,'Can add currency',32,'add_currency'),(95,'Can change currency',32,'change_currency'),(96,'Can delete currency',32,'delete_currency'),(97,'Can add tax',33,'add_tax'),(98,'Can change tax',33,'change_tax'),(99,'Can delete tax',33,'delete_tax'),(100,'Can add category',34,'add_category'),(101,'Can change category',34,'change_category'),(102,'Can delete category',34,'delete_category'),(103,'Can add asset',35,'add_asset'),(104,'Can change asset',35,'change_asset'),(105,'Can delete asset',35,'delete_asset'),(106,'Can add account',36,'add_account'),(107,'Can change account',36,'change_account'),(108,'Can delete account',36,'delete_account'),(109,'Can add equity',37,'add_equity'),(110,'Can change equity',37,'change_equity'),(111,'Can delete equity',37,'delete_equity'),(112,'Can add liability',38,'add_liability'),(113,'Can change liability',38,'change_liability'),(114,'Can delete liability',38,'delete_liability'),(115,'Can add transaction',39,'add_transaction'),(116,'Can change transaction',39,'change_transaction'),(117,'Can delete transaction',39,'delete_transaction'),(118,'Can add contact field',40,'add_contactfield'),(119,'Can change contact field',40,'change_contactfield'),(120,'Can delete contact field',40,'delete_contactfield'),(121,'Can add contact type',41,'add_contacttype'),(122,'Can change contact type',41,'change_contacttype'),(123,'Can delete contact type',41,'delete_contacttype'),(124,'Can add contact',42,'add_contact'),(125,'Can change contact',42,'change_contact'),(126,'Can delete contact',42,'delete_contact'),(127,'Can add contact value',43,'add_contactvalue'),(128,'Can change contact value',43,'change_contactvalue'),(129,'Can delete contact value',43,'delete_contactvalue'),(130,'Can add item field',44,'add_itemfield'),(131,'Can change item field',44,'change_itemfield'),(132,'Can delete item field',44,'delete_itemfield'),(133,'Can add item type',45,'add_itemtype'),(134,'Can change item type',45,'change_itemtype'),(135,'Can delete item type',45,'delete_itemtype'),(136,'Can add item status',46,'add_itemstatus'),(137,'Can change item status',46,'change_itemstatus'),(138,'Can delete item status',46,'delete_itemstatus'),(139,'Can add item',47,'add_item'),(140,'Can change item',47,'change_item'),(141,'Can delete item',47,'delete_item'),(142,'Can add item value',48,'add_itemvalue'),(143,'Can change item value',48,'change_itemvalue'),(144,'Can delete item value',48,'delete_itemvalue'),(145,'Can add item servicing',49,'add_itemservicing'),(146,'Can change item servicing',49,'change_itemservicing'),(147,'Can delete item servicing',49,'delete_itemservicing'),(148,'Can add knowledge folder',50,'add_knowledgefolder'),(149,'Can change knowledge folder',50,'change_knowledgefolder'),(150,'Can delete knowledge folder',50,'delete_knowledgefolder'),(151,'Can add knowledge category',51,'add_knowledgecategory'),(152,'Can change knowledge category',51,'change_knowledgecategory'),(153,'Can delete knowledge category',51,'delete_knowledgecategory'),(154,'Can add knowledge item',52,'add_knowledgeitem'),(155,'Can change knowledge item',52,'change_knowledgeitem'),(156,'Can delete knowledge item',52,'delete_knowledgeitem'),(157,'Can add template',53,'add_template'),(158,'Can change template',53,'change_template'),(159,'Can delete template',53,'delete_template'),(160,'Can add mailing list',54,'add_mailinglist'),(161,'Can change mailing list',54,'change_mailinglist'),(162,'Can delete mailing list',54,'delete_mailinglist'),(163,'Can add Stream',55,'add_messagestream'),(164,'Can change Stream',55,'change_messagestream'),(165,'Can delete Stream',55,'delete_messagestream'),(166,'Can add message',56,'add_message'),(167,'Can change message',56,'change_message'),(168,'Can delete message',56,'delete_message'),(169,'Can add project',57,'add_project'),(170,'Can change project',57,'change_project'),(171,'Can delete project',57,'delete_project'),(172,'Can add task status',58,'add_taskstatus'),(173,'Can change task status',58,'change_taskstatus'),(174,'Can delete task status',58,'delete_taskstatus'),(175,'Can add milestone',59,'add_milestone'),(176,'Can change milestone',59,'change_milestone'),(177,'Can delete milestone',59,'delete_milestone'),(178,'Can add task',60,'add_task'),(179,'Can change task',60,'change_task'),(180,'Can delete task',60,'delete_task'),(181,'Can add task time slot',61,'add_tasktimeslot'),(182,'Can change task time slot',61,'change_tasktimeslot'),(183,'Can delete task time slot',61,'delete_tasktimeslot'),(184,'Can add report',62,'add_report'),(185,'Can change report',62,'change_report'),(186,'Can delete report',62,'delete_report'),(187,'Can add chart',63,'add_chart'),(188,'Can change chart',63,'change_chart'),(189,'Can delete chart',63,'delete_chart'),(190,'Can add sale status',64,'add_salestatus'),(191,'Can change sale status',64,'change_salestatus'),(192,'Can delete sale status',64,'delete_salestatus'),(193,'Can add product',65,'add_product'),(194,'Can change product',65,'change_product'),(195,'Can delete product',65,'delete_product'),(196,'Can add sale source',66,'add_salesource'),(197,'Can change sale source',66,'change_salesource'),(198,'Can delete sale source',66,'delete_salesource'),(199,'Can add lead',67,'add_lead'),(200,'Can change lead',67,'change_lead'),(201,'Can delete lead',67,'delete_lead'),(202,'Can add opportunity',68,'add_opportunity'),(203,'Can change opportunity',68,'change_opportunity'),(204,'Can delete opportunity',68,'delete_opportunity'),(205,'Can add sale order',69,'add_saleorder'),(206,'Can change sale order',69,'change_saleorder'),(207,'Can delete sale order',69,'delete_saleorder'),(208,'Can add subscription',70,'add_subscription'),(209,'Can change subscription',70,'change_subscription'),(210,'Can delete subscription',70,'delete_subscription'),(211,'Can add ordered product',71,'add_orderedproduct'),(212,'Can change ordered product',71,'change_orderedproduct'),(213,'Can delete ordered product',71,'delete_orderedproduct'),(214,'Can add ticket status',72,'add_ticketstatus'),(215,'Can change ticket status',72,'change_ticketstatus'),(216,'Can delete ticket status',72,'delete_ticketstatus'),(217,'Can add service',73,'add_service'),(218,'Can change service',73,'change_service'),(219,'Can delete service',73,'delete_service'),(220,'Can add service level agreement',74,'add_servicelevelagreement'),(221,'Can change service level agreement',74,'change_servicelevelagreement'),(222,'Can delete service level agreement',74,'delete_servicelevelagreement'),(223,'Can add service agent',75,'add_serviceagent'),(224,'Can change service agent',75,'change_serviceagent'),(225,'Can delete service agent',75,'delete_serviceagent'),(226,'Can add ticket queue',76,'add_ticketqueue'),(227,'Can change ticket queue',76,'change_ticketqueue'),(228,'Can delete ticket queue',76,'delete_ticketqueue'),(229,'Can add ticket',77,'add_ticket'),(230,'Can change ticket',77,'change_ticket'),(231,'Can delete ticket',77,'delete_ticket'),(232,'Can add ticket record',78,'add_ticketrecord'),(233,'Can change ticket record',78,'change_ticketrecord'),(234,'Can delete ticket record',78,'delete_ticketrecord'),(235,'Can add captcha store',79,'add_captchastore'),(236,'Can change captcha store',79,'change_captchastore'),(237,'Can delete captcha store',79,'delete_captchastore'),(238,'Can add migration history',80,'add_migrationhistory'),(239,'Can change migration history',80,'change_migrationhistory'),(240,'Can delete migration history',80,'delete_migrationhistory'),(241,'Can add config setting',81,'add_configsetting'),(242,'Can change config setting',81,'change_configsetting'),(243,'Can delete config setting',81,'delete_configsetting'),(244,'Can add nonce',82,'add_nonce'),(245,'Can change nonce',82,'change_nonce'),(246,'Can delete nonce',82,'delete_nonce'),(247,'Can add consumer',83,'add_consumer'),(248,'Can change consumer',83,'change_consumer'),(249,'Can delete consumer',83,'delete_consumer'),(250,'Can add token',84,'add_token'),(251,'Can change token',84,'change_token'),(252,'Can delete token',84,'delete_token'),(253,'Can add attachment',85,'add_attachment'),(254,'Can change attachment',85,'change_attachment'),(255,'Can delete attachment',85,'delete_attachment'),(256,'Can add notification',86,'add_notification'),(257,'Can change notification',86,'change_notification'),(258,'Can delete notification',86,'delete_notification'),(259,'Can add notification setting',87,'add_notificationsetting'),(260,'Can change notification setting',87,'change_notificationsetting'),(261,'Can delete notification setting',87,'delete_notificationsetting');
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
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'admin','','','support@giteso.com','sha1$44a35$6bb92794882aeb2ee99339a98babf097f04a09aa',1,1,1,'2011-10-20 17:44:43','2011-02-22 23:19:11');
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
  KEY `auth_user_groups_403f60f` (`user_id`),
  KEY `auth_user_groups_425ae3c4` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
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
  KEY `auth_user_user_permissions_403f60f` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `captcha_captchastore`
--

DROP TABLE IF EXISTS `captcha_captchastore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `captcha_captchastore` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `challenge` varchar(32) NOT NULL,
  `response` varchar(32) NOT NULL,
  `hashkey` varchar(40) NOT NULL,
  `expiration` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hashkey` (`hashkey`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `captcha_captchastore`
--

LOCK TABLES `captcha_captchastore` WRITE;
/*!40000 ALTER TABLE `captcha_captchastore` DISABLE KEYS */;
/*!40000 ALTER TABLE `captcha_captchastore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_accessentity`
--

DROP TABLE IF EXISTS `core_accessentity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_accessentity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `last_updated` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_accessentity`
--

LOCK TABLES `core_accessentity` WRITE;
/*!40000 ALTER TABLE `core_accessentity` DISABLE KEYS */;
INSERT INTO `core_accessentity` VALUES (1,'2011-02-22 23:52:04'),(2,'2011-02-22 23:27:48');
/*!40000 ALTER TABLE `core_accessentity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_attachment`
--

DROP TABLE IF EXISTS `core_attachment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_attachment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(64) NOT NULL,
  `attached_object_id` int(11) DEFAULT NULL,
  `attached_record_id` int(11) DEFAULT NULL,
  `attached_file` varchar(100) NOT NULL,
  `mimetype` varchar(64) NOT NULL,
  `created` datetime NOT NULL,
  `uploaded_by_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_attachment_e3a19ead` (`attached_object_id`),
  KEY `core_attachment_ab32d207` (`attached_record_id`),
  KEY `core_attachment_e43a31e7` (`uploaded_by_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_attachment`
--

LOCK TABLES `core_attachment` WRITE;
/*!40000 ALTER TABLE `core_attachment` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_attachment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_comment`
--

DROP TABLE IF EXISTS `core_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author_id` int(11) DEFAULT NULL,
  `body` longtext,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_comment_337b96ff` (`author_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_comment`
--

LOCK TABLES `core_comment` WRITE;
/*!40000 ALTER TABLE `core_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_comment_dislikes`
--

DROP TABLE IF EXISTS `core_comment_dislikes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_comment_dislikes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `comment_id` (`comment_id`,`user_id`),
  KEY `core_comment_dislikes_64c238ac` (`comment_id`),
  KEY `core_comment_dislikes_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_comment_dislikes`
--

LOCK TABLES `core_comment_dislikes` WRITE;
/*!40000 ALTER TABLE `core_comment_dislikes` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_comment_dislikes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_comment_likes`
--

DROP TABLE IF EXISTS `core_comment_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_comment_likes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `comment_id` (`comment_id`,`user_id`),
  KEY `core_comment_likes_64c238ac` (`comment_id`),
  KEY `core_comment_likes_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_comment_likes`
--

LOCK TABLES `core_comment_likes` WRITE;
/*!40000 ALTER TABLE `core_comment_likes` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_comment_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_configsetting`
--

DROP TABLE IF EXISTS `core_configsetting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_configsetting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `value` longtext,
  `last_updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_configsetting`
--

LOCK TABLES `core_configsetting` WRITE;
/*!40000 ALTER TABLE `core_configsetting` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_configsetting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_group`
--

DROP TABLE IF EXISTS `core_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_group` (
  `accessentity_ptr_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `details` longtext,
  PRIMARY KEY (`accessentity_ptr_id`),
  KEY `core_group_63f17a16` (`parent_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_group`
--

LOCK TABLES `core_group` WRITE;
/*!40000 ALTER TABLE `core_group` DISABLE KEYS */;
INSERT INTO `core_group` VALUES (2,'General',NULL,NULL);
/*!40000 ALTER TABLE `core_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_invitation`
--

DROP TABLE IF EXISTS `core_invitation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_invitation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(75) NOT NULL,
  `key` varchar(256) NOT NULL,
  `sender_id` int(11) DEFAULT NULL,
  `default_group_id` int(11) DEFAULT NULL,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_invitation_6fe0a617` (`sender_id`),
  KEY `core_invitation_10b9ccc2` (`default_group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_invitation`
--

LOCK TABLES `core_invitation` WRITE;
/*!40000 ALTER TABLE `core_invitation` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_invitation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_location`
--

DROP TABLE IF EXISTS `core_location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_location` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(512) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `core_location_63f17a16` (`parent_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_location`
--

LOCK TABLES `core_location` WRITE;
/*!40000 ALTER TABLE `core_location` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_module`
--

DROP TABLE IF EXISTS `core_module`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_module` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `title` varchar(256) NOT NULL,
  `details` longtext NOT NULL,
  `url` varchar(512) NOT NULL,
  `display` tinyint(1) NOT NULL,
  `system` tinyint(1) NOT NULL,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_module`
--

LOCK TABLES `core_module` WRITE;
/*!40000 ALTER TABLE `core_module` DISABLE KEYS */;
INSERT INTO `core_module` VALUES (72,'treeio.infrastructure','Infrastructure','Manage infrastructure (fixed assets)','/infrastructure/',1,0),(71,'treeio.projects','Projects','Manage your projects','/projects/',1,0),(68,'treeio.knowledge','Knowledge','Manage your knowledge','/knowledge/',1,0),(69,'treeio.core','Administration','Core Administration','/admin/',1,1),(70,'treeio.sales','Sales & Stock','Sales and Client Relationship Management','/sales/',1,0),(66,'treeio.reports','Reports','Create Reports','/reports/',1,0),(67,'treeio.identities','Contacts','Manage users, groups, companies and corresponding contacts','/contacts/',1,1),(63,'treeio.messaging','Messaging','Sending messages','/messaging/',1,0),(64,'treeio.events','Calendar','Manage events and calendars','/calendar/',1,1),(65,'treeio.account','Account','User Account','/account/',1,1),(61,'treeio.documents','Documents','Manage documents','/documents/',1,0),(62,'treeio.news','News','Internal and external news','/news/',1,0),(73,'treeio.services','Service Support','Service delivery and support management','/services/',1,0),(74,'treeio.finance','Finance','Manage finance','/finance/',1,0);
/*!40000 ALTER TABLE `core_module` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_modulesetting`
--

DROP TABLE IF EXISTS `core_modulesetting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_modulesetting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) NOT NULL,
  `label` varchar(512) NOT NULL,
  `perspective_id` int(11) DEFAULT NULL,
  `module_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `value` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_modulesetting_35c9d965` (`perspective_id`),
  KEY `core_modulesetting_ac126a2` (`module_id`),
  KEY `core_modulesetting_403f60f` (`user_id`),
  KEY `core_modulesetting_425ae3c4` (`group_id`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_modulesetting`
--

LOCK TABLES `core_modulesetting` WRITE;
/*!40000 ALTER TABLE `core_modulesetting` DISABLE KEYS */;
INSERT INTO `core_modulesetting` VALUES (23,'default_perspective','default_perspective',NULL,69,NULL,2,'15');
/*!40000 ALTER TABLE `core_modulesetting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_object`
--

DROP TABLE IF EXISTS `core_object`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_object` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creator_id` int(11) DEFAULT NULL,
  `object_name` varchar(512) DEFAULT NULL,
  `object_type` varchar(512) DEFAULT NULL,
  `trash` tinyint(1) NOT NULL,
  `last_updated` datetime NOT NULL,
  `date_created` datetime NOT NULL,
  `nuvius_resource` longtext,
  PRIMARY KEY (`id`),
  KEY `core_object_685aee7` (`creator_id`)
) ENGINE=MyISAM AUTO_INCREMENT=75 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_object`
--

LOCK TABLES `core_object` WRITE;
/*!40000 ALTER TABLE `core_object` DISABLE KEYS */;
INSERT INTO `core_object` VALUES (72,1,'Infrastructure','treeio.core.models.Module',0,'2011-10-20 17:44:25','2011-10-20 17:44:25',NULL),(68,1,'Knowledge','treeio.core.models.Module',0,'2011-10-20 17:44:25','2011-10-20 17:44:25',NULL),(69,1,'Administration','treeio.core.models.Module',0,'2011-10-20 17:44:25','2011-10-20 17:44:25',NULL),(70,1,'Sales & Stock','treeio.core.models.Module',0,'2011-10-20 17:44:25','2011-10-20 17:44:25',NULL),(71,1,'Projects','treeio.core.models.Module',0,'2011-10-20 17:44:25','2011-10-20 17:44:25',NULL),(67,1,'Contacts','treeio.core.models.Module',0,'2011-10-20 17:44:25','2011-10-20 17:44:25',NULL),(66,1,'Reports','treeio.core.models.Module',0,'2011-10-20 17:44:25','2011-10-20 17:44:25',NULL),(63,1,'Messaging','treeio.core.models.Module',0,'2011-10-20 17:44:25','2011-10-20 17:44:25',NULL),(64,1,'Calendar','treeio.core.models.Module',0,'2011-10-20 17:44:25','2011-10-20 17:44:25',NULL),(65,1,'Account','treeio.core.models.Module',0,'2011-10-20 17:44:25','2011-10-20 17:44:25',NULL),(61,1,'Documents','treeio.core.models.Module',0,'2011-10-20 17:44:25','2011-10-20 17:44:25',NULL),(62,1,'News','treeio.core.models.Module',0,'2011-10-20 17:44:25','2011-10-20 17:44:25',NULL),(15,NULL,'Default','hardtree.core.models.Perspective',0,'2011-02-22 23:19:44','2011-02-22 23:19:44',NULL),(16,NULL,'Address','hardtree.identities.models.ContactField',0,'2011-02-22 23:22:25','2011-02-22 23:22:25',NULL),(17,NULL,'E-mail','hardtree.identities.models.ContactField',0,'2011-02-22 23:22:48','2011-02-22 23:22:48',NULL),(18,NULL,'Phone','hardtree.identities.models.ContactField',0,'2011-02-22 23:23:06','2011-02-22 23:23:06',NULL),(19,NULL,'Website','hardtree.identities.models.ContactField',0,'2011-02-22 23:23:30','2011-02-22 23:23:30',NULL),(20,NULL,'Picture','hardtree.identities.models.ContactField',0,'2011-02-22 23:23:54','2011-02-22 23:23:54',NULL),(21,NULL,'Company','hardtree.identities.models.ContactType',0,'2011-02-22 23:24:32','2011-02-22 23:24:32',NULL),(22,NULL,'Department','hardtree.identities.models.ContactType',0,'2011-02-22 23:24:53','2011-02-22 23:24:53',NULL),(23,NULL,'Person','hardtree.identities.models.ContactType',0,'2011-02-22 23:25:03','2011-02-22 23:25:03',NULL),(24,1,'Company','hardtree.identities.models.Contact',0,'2011-02-22 23:25:53','2011-02-22 23:25:53',NULL),(25,1,'Admin','hardtree.identities.models.Contact',0,'2011-02-23 00:25:31','2011-02-22 23:26:31',NULL),(26,NULL,'Open','hardtree.projects.models.TaskStatus',0,'2011-02-22 23:29:56','2011-02-22 23:29:56',NULL),(27,NULL,'Awaits Spec','hardtree.projects.models.TaskStatus',0,'2011-02-22 23:30:10','2011-02-22 23:30:10',NULL),(28,NULL,'Failed','hardtree.projects.models.TaskStatus',0,'2011-02-22 23:30:23','2011-02-22 23:30:23',NULL),(29,NULL,'Complete','hardtree.projects.models.TaskStatus',0,'2011-02-22 23:30:34','2011-02-22 23:30:34',NULL),(30,NULL,'Open','hardtree.services.models.TicketStatus',0,'2011-02-22 23:31:19','2011-02-22 23:31:19',NULL),(31,NULL,'Pending Caller','hardtree.services.models.TicketStatus',0,'2011-02-22 23:31:33','2011-02-22 23:31:33',NULL),(32,NULL,'Pending Supplier','hardtree.services.models.TicketStatus',0,'2011-02-22 23:31:49','2011-02-22 23:31:49',NULL),(33,NULL,'Won\'t Fix','hardtree.services.models.TicketStatus',0,'2011-02-22 23:32:02','2011-02-22 23:32:02',NULL),(34,NULL,'Closed','hardtree.services.models.TicketStatus',0,'2011-02-22 23:32:19','2011-02-22 23:32:19',NULL),(35,NULL,'admin','hardtree.services.models.ServiceAgent',0,'2011-02-22 23:32:40','2011-02-22 23:32:40',NULL),(36,NULL,'Default','hardtree.documents.models.Folder',0,'2011-02-22 23:33:18','2011-02-22 23:33:18',NULL),(37,NULL,'$    United States of America, Dollars','hardtree.finance.models.Currency',0,'2011-02-22 23:40:34','2011-02-22 23:33:59',NULL),(38,NULL,'Default','hardtree.finance.models.Account',0,'2011-02-22 23:39:50','2011-02-22 23:34:23',NULL),(39,NULL,'General','hardtree.messaging.models.MessageStream',0,'2011-02-22 23:40:46','2011-02-22 23:40:46',NULL),(40,NULL,'ServiceDesk','hardtree.services.models.TicketQueue',0,'2011-02-22 23:54:36','2011-02-22 23:54:36',NULL),(41,NULL,'Advertisement','hardtree.sales.models.SaleSource',0,'2011-02-23 00:45:39','2011-02-23 00:40:10',NULL),(43,NULL,'Colleague','hardtree.sales.models.SaleSource',0,'2011-02-23 00:41:14','2011-02-23 00:41:14',NULL),(44,NULL,'Friend','hardtree.sales.models.SaleSource',0,'2011-02-23 00:41:35','2011-02-23 00:41:35',NULL),(45,NULL,'Search Engine','hardtree.sales.models.SaleSource',0,'2011-02-23 00:41:46','2011-02-23 00:41:46',NULL),(46,NULL,'Other','hardtree.sales.models.SaleSource',0,'2011-02-23 00:45:54','2011-02-23 00:41:57',NULL),(47,NULL,'Open','hardtree.sales.models.SaleStatus',0,'2011-02-23 00:46:54','2011-02-23 00:42:44',NULL),(48,NULL,'Paused','hardtree.sales.models.SaleStatus',0,'2011-02-23 00:47:07','2011-02-23 00:43:20',NULL),(49,NULL,'Closed','hardtree.sales.models.SaleStatus',0,'2011-02-23 00:49:06','2011-02-23 00:43:38',NULL),(50,NULL,'Failed','hardtree.sales.models.SaleStatus',0,'2011-02-23 00:47:24','2011-02-23 00:43:59',NULL),(51,NULL,'Active','hardtree.infrastructure.models.ItemStatus',0,'2011-08-19 23:28:29','2011-08-19 23:28:29',NULL),(52,NULL,'Unused','hardtree.infrastructure.models.ItemStatus',0,'2011-08-19 23:28:53','2011-08-19 23:28:53',NULL),(53,NULL,'Removed','hardtree.infrastructure.models.ItemStatus',0,'2011-08-19 23:29:19','2011-08-19 23:29:19',NULL),(54,NULL,'IP Address','hardtree.infrastructure.models.ItemField',0,'2011-08-19 23:29:50','2011-08-19 23:29:50',NULL),(55,NULL,'Hostname','hardtree.infrastructure.models.ItemField',0,'2011-08-19 23:30:09','2011-08-19 23:30:09',NULL),(56,NULL,'Workstation','hardtree.infrastructure.models.ItemType',0,'2011-08-19 23:33:47','2011-08-19 23:30:55',NULL),(57,NULL,'Operating System','hardtree.infrastructure.models.ItemField',0,'2011-08-19 23:32:12','2011-08-19 23:32:12',NULL),(58,NULL,'Date Installed','hardtree.infrastructure.models.ItemField',0,'2011-08-19 23:33:06','2011-08-19 23:33:06',NULL),(59,NULL,'Server','hardtree.infrastructure.models.ItemType',0,'2011-08-19 23:34:32','2011-08-19 23:34:32',NULL),(60,NULL,'Default','hardtree.knowledge.models.KnowledgeFolder',0,'2011-08-19 23:36:38','2011-08-19 23:36:38',NULL),(73,1,'Service Support','treeio.core.models.Module',0,'2011-10-20 17:44:25','2011-10-20 17:44:25',NULL),(74,1,'Finance','treeio.core.models.Module',0,'2011-10-20 17:44:26','2011-10-20 17:44:25',NULL);
/*!40000 ALTER TABLE `core_object` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_object_comments`
--

DROP TABLE IF EXISTS `core_object_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_object_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `comment_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `object_id` (`object_id`,`comment_id`),
  KEY `core_object_comments_7d61c803` (`object_id`),
  KEY `core_object_comments_64c238ac` (`comment_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_object_comments`
--

LOCK TABLES `core_object_comments` WRITE;
/*!40000 ALTER TABLE `core_object_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_object_comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_object_dislikes`
--

DROP TABLE IF EXISTS `core_object_dislikes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_object_dislikes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `object_id` (`object_id`,`user_id`),
  KEY `core_object_dislikes_7d61c803` (`object_id`),
  KEY `core_object_dislikes_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_object_dislikes`
--

LOCK TABLES `core_object_dislikes` WRITE;
/*!40000 ALTER TABLE `core_object_dislikes` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_object_dislikes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_object_full_access`
--

DROP TABLE IF EXISTS `core_object_full_access`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_object_full_access` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `accessentity_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `object_id` (`object_id`,`accessentity_id`),
  KEY `core_object_full_access_7d61c803` (`object_id`),
  KEY `core_object_full_access_1b579059` (`accessentity_id`)
) ENGINE=MyISAM AUTO_INCREMENT=101 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_object_full_access`
--

LOCK TABLES `core_object_full_access` WRITE;
/*!40000 ALTER TABLE `core_object_full_access` DISABLE KEYS */;
INSERT INTO `core_object_full_access` VALUES (15,16,1),(16,17,1),(17,18,1),(18,19,1),(19,20,1),(20,21,1),(21,22,1),(22,23,1),(23,24,1),(24,25,1),(25,26,1),(26,26,2),(27,27,1),(28,27,2),(29,28,1),(30,28,2),(31,29,1),(32,29,2),(33,30,1),(34,30,2),(35,31,1),(36,31,2),(37,32,1),(38,32,2),(39,33,1),(40,33,2),(41,34,1),(42,34,2),(43,35,1),(44,35,2),(45,36,1),(46,36,2),(47,37,1),(48,37,2),(49,38,1),(50,38,2),(51,39,1),(52,39,2),(53,40,1),(54,40,2),(55,41,1),(56,41,2),(59,43,1),(60,43,2),(61,44,1),(62,44,2),(63,45,1),(64,45,2),(65,46,1),(66,46,2),(67,47,1),(68,47,2),(69,48,1),(70,48,2),(71,49,1),(72,49,2),(73,50,1),(74,50,2),(89,15,1),(90,15,2),(91,16,2),(92,17,2),(93,18,2),(94,19,2),(95,20,2),(96,21,2),(97,22,2),(98,23,2),(99,24,2),(100,25,2);
/*!40000 ALTER TABLE `core_object_full_access` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_object_likes`
--

DROP TABLE IF EXISTS `core_object_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_object_likes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `object_id` (`object_id`,`user_id`),
  KEY `core_object_likes_7d61c803` (`object_id`),
  KEY `core_object_likes_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_object_likes`
--

LOCK TABLES `core_object_likes` WRITE;
/*!40000 ALTER TABLE `core_object_likes` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_object_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_object_links`
--

DROP TABLE IF EXISTS `core_object_links`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_object_links` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_object_id` int(11) NOT NULL,
  `to_object_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `from_object_id` (`from_object_id`,`to_object_id`),
  KEY `core_object_links_588440ad` (`from_object_id`),
  KEY `core_object_links_6b596a5e` (`to_object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_object_links`
--

LOCK TABLES `core_object_links` WRITE;
/*!40000 ALTER TABLE `core_object_links` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_object_links` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_object_read_access`
--

DROP TABLE IF EXISTS `core_object_read_access`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_object_read_access` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `accessentity_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `object_id` (`object_id`,`accessentity_id`),
  KEY `core_object_read_access_7d61c803` (`object_id`),
  KEY `core_object_read_access_1b579059` (`accessentity_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_object_read_access`
--

LOCK TABLES `core_object_read_access` WRITE;
/*!40000 ALTER TABLE `core_object_read_access` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_object_read_access` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_object_subscribers`
--

DROP TABLE IF EXISTS `core_object_subscribers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_object_subscribers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `object_id` (`object_id`,`user_id`),
  KEY `core_object_subscribers_7d61c803` (`object_id`),
  KEY `core_object_subscribers_403f60f` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_object_subscribers`
--

LOCK TABLES `core_object_subscribers` WRITE;
/*!40000 ALTER TABLE `core_object_subscribers` DISABLE KEYS */;
INSERT INTO `core_object_subscribers` VALUES (1,15,1),(2,21,1),(3,22,1),(4,23,1),(5,24,1),(6,25,1),(7,26,1),(8,27,1),(9,28,1),(10,29,1),(11,35,1),(12,36,1),(13,37,1),(14,38,1),(15,39,1),(16,40,1),(17,51,1),(18,52,1),(19,53,1),(20,56,1),(21,59,1),(22,60,1);
/*!40000 ALTER TABLE `core_object_subscribers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_object_tags`
--

DROP TABLE IF EXISTS `core_object_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_object_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `object_id` (`object_id`,`tag_id`),
  KEY `core_object_tags_7d61c803` (`object_id`),
  KEY `core_object_tags_3747b463` (`tag_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_object_tags`
--

LOCK TABLES `core_object_tags` WRITE;
/*!40000 ALTER TABLE `core_object_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_object_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_page`
--

DROP TABLE IF EXISTS `core_page`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_page` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `title` varchar(256) NOT NULL,
  `folder_id` int(11) NOT NULL,
  `body` longtext NOT NULL,
  `published` tinyint(1) NOT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `core_page_4e5f642` (`folder_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_page`
--

LOCK TABLES `core_page` WRITE;
/*!40000 ALTER TABLE `core_page` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_page` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_pagefolder`
--

DROP TABLE IF EXISTS `core_pagefolder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_pagefolder` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `details` longtext NOT NULL,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_pagefolder`
--

LOCK TABLES `core_pagefolder` WRITE;
/*!40000 ALTER TABLE `core_pagefolder` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_pagefolder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_perspective`
--

DROP TABLE IF EXISTS `core_perspective`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_perspective` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `details` longtext NOT NULL,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_perspective`
--

LOCK TABLES `core_perspective` WRITE;
/*!40000 ALTER TABLE `core_perspective` DISABLE KEYS */;
INSERT INTO `core_perspective` VALUES (15,'Default','');
/*!40000 ALTER TABLE `core_perspective` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_perspective_modules`
--

DROP TABLE IF EXISTS `core_perspective_modules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_perspective_modules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `perspective_id` int(11) NOT NULL,
  `module_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `perspective_id` (`perspective_id`,`module_id`),
  KEY `core_perspective_modules_35c9d965` (`perspective_id`),
  KEY `core_perspective_modules_ac126a2` (`module_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_perspective_modules`
--

LOCK TABLES `core_perspective_modules` WRITE;
/*!40000 ALTER TABLE `core_perspective_modules` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_perspective_modules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_revision`
--

DROP TABLE IF EXISTS `core_revision`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_revision` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `previous_id` int(11) DEFAULT NULL,
  `object_id` int(11) NOT NULL,
  `change_type` varchar(512) DEFAULT NULL,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `previous_id` (`previous_id`),
  KEY `core_revision_7d61c803` (`object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_revision`
--

LOCK TABLES `core_revision` WRITE;
/*!40000 ALTER TABLE `core_revision` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_revision` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_revisionfield`
--

DROP TABLE IF EXISTS `core_revisionfield`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_revisionfield` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `revision_id` int(11) NOT NULL,
  `field_type` varchar(512) DEFAULT NULL,
  `field` varchar(512) DEFAULT NULL,
  `value` longtext,
  `value_key_id` int(11) DEFAULT NULL,
  `value_key_acc_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_revisionfield_202bdc7f` (`revision_id`),
  KEY `core_revisionfield_e0f80ba` (`value_key_id`),
  KEY `core_revisionfield_57486250` (`value_key_acc_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_revisionfield`
--

LOCK TABLES `core_revisionfield` WRITE;
/*!40000 ALTER TABLE `core_revisionfield` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_revisionfield` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_revisionfield_value_m2m`
--

DROP TABLE IF EXISTS `core_revisionfield_value_m2m`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_revisionfield_value_m2m` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `revisionfield_id` int(11) NOT NULL,
  `object_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `revisionfield_id` (`revisionfield_id`,`object_id`),
  KEY `core_revisionfield_value_m2m_770dbea8` (`revisionfield_id`),
  KEY `core_revisionfield_value_m2m_7d61c803` (`object_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_revisionfield_value_m2m`
--

LOCK TABLES `core_revisionfield_value_m2m` WRITE;
/*!40000 ALTER TABLE `core_revisionfield_value_m2m` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_revisionfield_value_m2m` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_revisionfield_value_m2m_acc`
--

DROP TABLE IF EXISTS `core_revisionfield_value_m2m_acc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_revisionfield_value_m2m_acc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `revisionfield_id` int(11) NOT NULL,
  `accessentity_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `revisionfield_id` (`revisionfield_id`,`accessentity_id`),
  KEY `core_revisionfield_value_m2m_acc_770dbea8` (`revisionfield_id`),
  KEY `core_revisionfield_value_m2m_acc_1b579059` (`accessentity_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_revisionfield_value_m2m_acc`
--

LOCK TABLES `core_revisionfield_value_m2m_acc` WRITE;
/*!40000 ALTER TABLE `core_revisionfield_value_m2m_acc` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_revisionfield_value_m2m_acc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_tag`
--

DROP TABLE IF EXISTS `core_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) NOT NULL,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_tag`
--

LOCK TABLES `core_tag` WRITE;
/*!40000 ALTER TABLE `core_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_updaterecord`
--

DROP TABLE IF EXISTS `core_updaterecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_updaterecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author_id` int(11) DEFAULT NULL,
  `sender_id` int(11) DEFAULT NULL,
  `record_type` varchar(32) NOT NULL,
  `url` varchar(512) DEFAULT NULL,
  `body` longtext,
  `score` int(11) NOT NULL,
  `format_message` longtext,
  `format_strings` longtext,
  `date_created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_updaterecord_337b96ff` (`author_id`),
  KEY `core_updaterecord_6fe0a617` (`sender_id`)
) ENGINE=MyISAM AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_updaterecord`
--

LOCK TABLES `core_updaterecord` WRITE;
/*!40000 ALTER TABLE `core_updaterecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_updaterecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_updaterecord_about`
--

DROP TABLE IF EXISTS `core_updaterecord_about`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_updaterecord_about` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updaterecord_id` int(11) NOT NULL,
  `object_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `updaterecord_id` (`updaterecord_id`,`object_id`),
  KEY `core_updaterecord_about_2153f678` (`updaterecord_id`),
  KEY `core_updaterecord_about_7d61c803` (`object_id`)
) ENGINE=MyISAM AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_updaterecord_about`
--

LOCK TABLES `core_updaterecord_about` WRITE;
/*!40000 ALTER TABLE `core_updaterecord_about` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_updaterecord_about` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_updaterecord_comments`
--

DROP TABLE IF EXISTS `core_updaterecord_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_updaterecord_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updaterecord_id` int(11) NOT NULL,
  `comment_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `updaterecord_id` (`updaterecord_id`,`comment_id`),
  KEY `core_updaterecord_comments_2153f678` (`updaterecord_id`),
  KEY `core_updaterecord_comments_64c238ac` (`comment_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_updaterecord_comments`
--

LOCK TABLES `core_updaterecord_comments` WRITE;
/*!40000 ALTER TABLE `core_updaterecord_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_updaterecord_comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_updaterecord_dislikes`
--

DROP TABLE IF EXISTS `core_updaterecord_dislikes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_updaterecord_dislikes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updaterecord_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `updaterecord_id` (`updaterecord_id`,`user_id`),
  KEY `core_updaterecord_dislikes_2153f678` (`updaterecord_id`),
  KEY `core_updaterecord_dislikes_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_updaterecord_dislikes`
--

LOCK TABLES `core_updaterecord_dislikes` WRITE;
/*!40000 ALTER TABLE `core_updaterecord_dislikes` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_updaterecord_dislikes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_updaterecord_likes`
--

DROP TABLE IF EXISTS `core_updaterecord_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_updaterecord_likes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updaterecord_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `updaterecord_id` (`updaterecord_id`,`user_id`),
  KEY `core_updaterecord_likes_2153f678` (`updaterecord_id`),
  KEY `core_updaterecord_likes_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_updaterecord_likes`
--

LOCK TABLES `core_updaterecord_likes` WRITE;
/*!40000 ALTER TABLE `core_updaterecord_likes` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_updaterecord_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_updaterecord_recipients`
--

DROP TABLE IF EXISTS `core_updaterecord_recipients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_updaterecord_recipients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updaterecord_id` int(11) NOT NULL,
  `accessentity_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `updaterecord_id` (`updaterecord_id`,`accessentity_id`),
  KEY `core_updaterecord_recipients_2153f678` (`updaterecord_id`),
  KEY `core_updaterecord_recipients_1b579059` (`accessentity_id`)
) ENGINE=MyISAM AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_updaterecord_recipients`
--

LOCK TABLES `core_updaterecord_recipients` WRITE;
/*!40000 ALTER TABLE `core_updaterecord_recipients` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_updaterecord_recipients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user`
--

DROP TABLE IF EXISTS `core_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_user` (
  `accessentity_ptr_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `user_id` int(11) NOT NULL,
  `default_group_id` int(11) DEFAULT NULL,
  `disabled` tinyint(1) NOT NULL,
  `last_access` datetime NOT NULL,
  PRIMARY KEY (`accessentity_ptr_id`),
  KEY `core_user_403f60f` (`user_id`),
  KEY `core_user_10b9ccc2` (`default_group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user`
--

LOCK TABLES `core_user` WRITE;
/*!40000 ALTER TABLE `core_user` DISABLE KEYS */;
INSERT INTO `core_user` VALUES (1,'admin',1,2,0,'2011-02-22 23:19:11');
/*!40000 ALTER TABLE `core_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user_other_groups`
--

DROP TABLE IF EXISTS `core_user_other_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_user_other_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `core_user_other_groups_403f60f` (`user_id`),
  KEY `core_user_other_groups_425ae3c4` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user_other_groups`
--

LOCK TABLES `core_user_other_groups` WRITE;
/*!40000 ALTER TABLE `core_user_other_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user_other_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_widget`
--

DROP TABLE IF EXISTS `core_widget`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `core_widget` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `perspective_id` int(11) NOT NULL,
  `module_name` varchar(256) NOT NULL,
  `widget_name` varchar(256) NOT NULL,
  `weight` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_widget_403f60f` (`user_id`),
  KEY `core_widget_35c9d965` (`perspective_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_widget`
--

LOCK TABLES `core_widget` WRITE;
/*!40000 ALTER TABLE `core_widget` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_widget` ENABLE KEYS */;
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
  KEY `django_admin_log_403f60f` (`user_id`),
  KEY `django_admin_log_1bb8f392` (`content_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
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
) ENGINE=MyISAM AUTO_INCREMENT=88 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'message','auth','message'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'site','sites','site'),(8,'log entry','admin','logentry'),(9,'access entity','core','accessentity'),(10,'group','core','group'),(11,'user','core','user'),(12,'invitation','core','invitation'),(13,'tag','core','tag'),(14,'comment','core','comment'),(15,'object','core','object'),(16,'revision','core','revision'),(17,'revision field','core','revisionfield'),(18,'update record','core','updaterecord'),(19,'module','core','module'),(20,'perspective','core','perspective'),(21,'module setting','core','modulesetting'),(22,'location','core','location'),(23,'page folder','core','pagefolder'),(24,'page','core','page'),(25,'widget','core','widget'),(26,'folder','documents','folder'),(27,'file','documents','file'),(28,'document','documents','document'),(29,'web link','documents','weblink'),(30,'event','events','event'),(31,'invitation','events','invitation'),(32,'currency','finance','currency'),(33,'tax','finance','tax'),(34,'category','finance','category'),(35,'asset','finance','asset'),(36,'account','finance','account'),(37,'equity','finance','equity'),(38,'liability','finance','liability'),(39,'transaction','finance','transaction'),(40,'contact field','identities','contactfield'),(41,'contact type','identities','contacttype'),(42,'contact','identities','contact'),(43,'contact value','identities','contactvalue'),(44,'item field','infrastructure','itemfield'),(45,'item type','infrastructure','itemtype'),(46,'item status','infrastructure','itemstatus'),(47,'item','infrastructure','item'),(48,'item value','infrastructure','itemvalue'),(49,'item servicing','infrastructure','itemservicing'),(50,'knowledge folder','knowledge','knowledgefolder'),(51,'knowledge category','knowledge','knowledgecategory'),(52,'knowledge item','knowledge','knowledgeitem'),(53,'template','messaging','template'),(54,'mailing list','messaging','mailinglist'),(55,'Stream','messaging','messagestream'),(56,'message','messaging','message'),(57,'project','projects','project'),(58,'task status','projects','taskstatus'),(59,'milestone','projects','milestone'),(60,'task','projects','task'),(61,'task time slot','projects','tasktimeslot'),(62,'report','reports','report'),(63,'chart','reports','chart'),(64,'sale status','sales','salestatus'),(65,'product','sales','product'),(66,'sale source','sales','salesource'),(67,'lead','sales','lead'),(68,'opportunity','sales','opportunity'),(69,'sale order','sales','saleorder'),(70,'subscription','sales','subscription'),(71,'ordered product','sales','orderedproduct'),(72,'ticket status','services','ticketstatus'),(73,'service','services','service'),(74,'service level agreement','services','servicelevelagreement'),(75,'service agent','services','serviceagent'),(76,'ticket queue','services','ticketqueue'),(77,'ticket','services','ticket'),(78,'ticket record','services','ticketrecord'),(79,'captcha store','captcha','captchastore'),(80,'migration history','south','migrationhistory'),(81,'config setting','core','configsetting'),(82,'nonce','api','nonce'),(83,'consumer','api','consumer'),(84,'token','api','token'),(85,'attachment','core','attachment'),(86,'notification','account','notification'),(87,'notification setting','account','notificationsetting');
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('ff7097cc228f3b4663f4acd220919b67','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5lYzQ5Zjc5ZWU3ZGYxOGE4MGZl\nODFkYzY5NjJjNGMwMQ==\n','2011-03-09 00:25:15'),('19380c9896c778e115efd013ba946c31','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5lYzQ5Zjc5ZWU3ZGYxOGE4MGZl\nODFkYzY5NjJjNGMwMQ==\n','2011-03-08 23:42:14'),('4b5e12c1ba6e484233c4b32e889ecf12','gAJ9cQEuZGU4NTQxZWIyZjZkZjQwZDRhZmZhNDRmOGViMmZhNmM=\n','2011-03-30 17:29:12'),('6ab27b1d374d1b8e25cd5b6cb1ff0d2d','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5lYzQ5Zjc5ZWU3ZGYxOGE4MGZl\nODFkYzY5NjJjNGMwMQ==\n','2011-03-10 21:19:09'),('ad06d52c216fd5310ac9dc4e2c946962','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5lYzQ5Zjc5ZWU3ZGYxOGE4MGZl\nODFkYzY5NjJjNGMwMQ==\n','2011-03-11 01:55:10'),('93a869e12cb4ee3804dc10f372f235f3','gAJ9cQEuZGU4NTQxZWIyZjZkZjQwZDRhZmZhNDRmOGViMmZhNmM=\n','2011-03-30 17:29:12'),('c8d3c725b35ba2a192708a983acacbc1','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5lYzQ5Zjc5ZWU3ZGYxOGE4MGZl\nODFkYzY5NjJjNGMwMQ==\n','2011-03-24 20:36:38'),('eacead8005108a20d89c5e31e8f4b29b','gAJ9cQEuZGU4NTQxZWIyZjZkZjQwZDRhZmZhNDRmOGViMmZhNmM=\n','2011-03-24 20:39:44'),('b20caff9ebf139ee3e508bb7982c7a69','gAJ9cQEuZGU4NTQxZWIyZjZkZjQwZDRhZmZhNDRmOGViMmZhNmM=\n','2011-03-24 20:48:48'),('7b4479f32db743c2b018b32acf1b7ec3','gAJ9cQEuZGU4NTQxZWIyZjZkZjQwZDRhZmZhNDRmOGViMmZhNmM=\n','2011-03-24 20:58:48'),('75ec6723eaecde69ea9bf27829880a24','gAJ9cQEuZGU4NTQxZWIyZjZkZjQwZDRhZmZhNDRmOGViMmZhNmM=\n','2011-03-30 17:29:12'),('4cb9bc7eed3156ba097e9250650c8ff0','gAJ9cQEuZGU4NTQxZWIyZjZkZjQwZDRhZmZhNDRmOGViMmZhNmM=\n','2011-03-30 17:29:12'),('6f2dc8e56ec71d43ab0dc397d7f0498e','gAJ9cQEuZGU4NTQxZWIyZjZkZjQwZDRhZmZhNDRmOGViMmZhNmM=\n','2011-03-30 17:29:12'),('364e328417a5576b4eec000c763e860d','gAJ9cQEuZGU4NTQxZWIyZjZkZjQwZDRhZmZhNDRmOGViMmZhNmM=\n','2011-03-30 17:29:12'),('089565cf91aae142dfa5b464fde2b13f','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5lYzQ5Zjc5ZWU3ZGYxOGE4MGZl\nODFkYzY5NjJjNGMwMQ==\n','2011-03-31 00:46:47'),('6f1c8983b453466cccaae75b213a8224','YmQzMGFkYTQ1Yjk4MzQ1MTdjMDhhY2E1MzAyY2M2M2UzYTJkZTI1YTqAAn1xAS4=\n','2011-08-24 22:52:20'),('c65b7f7a1f5c901d64595672554a0305','MWQ0NDNiMGY5NGFmMDY2ZWMyYTUxOTgyYmZiMDUzN2Q4M2U4M2VjYjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2011-09-02 23:20:57'),('b987971a3b49921cb7d526c1e5b19529','MWQ0NDNiMGY5NGFmMDY2ZWMyYTUxOTgyYmZiMDUzN2Q4M2U4M2VjYjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2011-11-03 17:44:43');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documents_document`
--

DROP TABLE IF EXISTS `documents_document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `documents_document` (
  `object_ptr_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `folder_id` int(11) NOT NULL,
  `body` longtext,
  PRIMARY KEY (`object_ptr_id`),
  KEY `documents_document_4e5f642` (`folder_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents_document`
--

LOCK TABLES `documents_document` WRITE;
/*!40000 ALTER TABLE `documents_document` DISABLE KEYS */;
/*!40000 ALTER TABLE `documents_document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documents_file`
--

DROP TABLE IF EXISTS `documents_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `documents_file` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `folder_id` int(11) NOT NULL,
  `content` varchar(100) NOT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `documents_file_4e5f642` (`folder_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents_file`
--

LOCK TABLES `documents_file` WRITE;
/*!40000 ALTER TABLE `documents_file` DISABLE KEYS */;
/*!40000 ALTER TABLE `documents_file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documents_folder`
--

DROP TABLE IF EXISTS `documents_folder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `documents_folder` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `documents_folder_63f17a16` (`parent_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents_folder`
--

LOCK TABLES `documents_folder` WRITE;
/*!40000 ALTER TABLE `documents_folder` DISABLE KEYS */;
INSERT INTO `documents_folder` VALUES (36,'Default',NULL);
/*!40000 ALTER TABLE `documents_folder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documents_weblink`
--

DROP TABLE IF EXISTS `documents_weblink`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `documents_weblink` (
  `object_ptr_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `folder_id` int(11) NOT NULL,
  `url` varchar(255) NOT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `documents_weblink_4e5f642` (`folder_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents_weblink`
--

LOCK TABLES `documents_weblink` WRITE;
/*!40000 ALTER TABLE `documents_weblink` DISABLE KEYS */;
/*!40000 ALTER TABLE `documents_weblink` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_event`
--

DROP TABLE IF EXISTS `events_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `events_event` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `location_id` int(11) DEFAULT NULL,
  `details` longtext,
  `start` datetime DEFAULT NULL,
  `end` datetime NOT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `events_event_319d859` (`location_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_event`
--

LOCK TABLES `events_event` WRITE;
/*!40000 ALTER TABLE `events_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events_invitation`
--

DROP TABLE IF EXISTS `events_invitation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `events_invitation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contact_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `events_invitation_170b8823` (`contact_id`),
  KEY `events_invitation_1647d06b` (`event_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events_invitation`
--

LOCK TABLES `events_invitation` WRITE;
/*!40000 ALTER TABLE `events_invitation` DISABLE KEYS */;
/*!40000 ALTER TABLE `events_invitation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finance_account`
--

DROP TABLE IF EXISTS `finance_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `finance_account` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(512) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `balance` decimal(20,2) NOT NULL,
  `balance_currency_id` int(11) NOT NULL,
  `balance_display` decimal(20,2) NOT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`),
  KEY `finance_account_5d52dd10` (`owner_id`),
  KEY `finance_account_7bf469f2` (`balance_currency_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finance_account`
--

LOCK TABLES `finance_account` WRITE;
/*!40000 ALTER TABLE `finance_account` DISABLE KEYS */;
INSERT INTO `finance_account` VALUES (38,'Default',24,'0.00',37,'0.00','');
/*!40000 ALTER TABLE `finance_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finance_asset`
--

DROP TABLE IF EXISTS `finance_asset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `finance_asset` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(512) NOT NULL,
  `asset_type` varchar(32) NOT NULL,
  `initial_value` decimal(20,2) NOT NULL,
  `lifetime` decimal(20,0) DEFAULT NULL,
  `endlife_value` decimal(20,2) DEFAULT NULL,
  `depreciation_rate` decimal(4,2) DEFAULT NULL,
  `depreciation_type` varchar(32) DEFAULT NULL,
  `purchase_date` date DEFAULT NULL,
  `current_value` decimal(20,2) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`),
  KEY `finance_asset_5d52dd10` (`owner_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finance_asset`
--

LOCK TABLES `finance_asset` WRITE;
/*!40000 ALTER TABLE `finance_asset` DISABLE KEYS */;
/*!40000 ALTER TABLE `finance_asset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finance_category`
--

DROP TABLE IF EXISTS `finance_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `finance_category` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(512) NOT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finance_category`
--

LOCK TABLES `finance_category` WRITE;
/*!40000 ALTER TABLE `finance_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `finance_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finance_currency`
--

DROP TABLE IF EXISTS `finance_currency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `finance_currency` (
  `object_ptr_id` int(11) NOT NULL,
  `code` varchar(3) NOT NULL,
  `name` varchar(255) NOT NULL,
  `symbol` varchar(1) DEFAULT NULL,
  `factor` decimal(10,4) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finance_currency`
--

LOCK TABLES `finance_currency` WRITE;
/*!40000 ALTER TABLE `finance_currency` DISABLE KEYS */;
INSERT INTO `finance_currency` VALUES (37,'USD','United States of America, Dollars','$','1.0000',1,1);
/*!40000 ALTER TABLE `finance_currency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finance_equity`
--

DROP TABLE IF EXISTS `finance_equity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `finance_equity` (
  `object_ptr_id` int(11) NOT NULL,
  `equity_type` varchar(32) NOT NULL,
  `issue_price` decimal(20,2) NOT NULL,
  `sell_price` decimal(20,2) NOT NULL,
  `issuer_id` int(11) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `amount` int(10) unsigned NOT NULL,
  `purchase_date` date NOT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`),
  KEY `finance_equity_8372547` (`issuer_id`),
  KEY `finance_equity_5d52dd10` (`owner_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finance_equity`
--

LOCK TABLES `finance_equity` WRITE;
/*!40000 ALTER TABLE `finance_equity` DISABLE KEYS */;
/*!40000 ALTER TABLE `finance_equity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finance_liability`
--

DROP TABLE IF EXISTS `finance_liability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `finance_liability` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(512) NOT NULL,
  `source_id` int(11) NOT NULL,
  `target_id` int(11) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `account_id` int(11) NOT NULL,
  `due_date` date DEFAULT NULL,
  `value` decimal(20,2) NOT NULL,
  `value_currency_id` int(11) NOT NULL,
  `value_display` decimal(20,2) NOT NULL,
  `details` longtext NOT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `finance_liability_7607617b` (`source_id`),
  KEY `finance_liability_6ca73769` (`target_id`),
  KEY `finance_liability_42dc49bc` (`category_id`),
  KEY `finance_liability_6f2fe10e` (`account_id`),
  KEY `finance_liability_4eab3821` (`value_currency_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finance_liability`
--

LOCK TABLES `finance_liability` WRITE;
/*!40000 ALTER TABLE `finance_liability` DISABLE KEYS */;
/*!40000 ALTER TABLE `finance_liability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finance_tax`
--

DROP TABLE IF EXISTS `finance_tax`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `finance_tax` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(512) NOT NULL,
  `rate` decimal(4,2) NOT NULL,
  `compound` tinyint(1) NOT NULL,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finance_tax`
--

LOCK TABLES `finance_tax` WRITE;
/*!40000 ALTER TABLE `finance_tax` DISABLE KEYS */;
/*!40000 ALTER TABLE `finance_tax` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finance_transaction`
--

DROP TABLE IF EXISTS `finance_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `finance_transaction` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(512) NOT NULL,
  `source_id` int(11) NOT NULL,
  `target_id` int(11) NOT NULL,
  `liability_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `account_id` int(11) NOT NULL,
  `datetime` datetime NOT NULL,
  `value` decimal(20,2) NOT NULL,
  `value_currency_id` int(11) NOT NULL,
  `value_display` decimal(20,2) NOT NULL,
  `details` longtext NOT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `finance_transaction_7607617b` (`source_id`),
  KEY `finance_transaction_6ca73769` (`target_id`),
  KEY `finance_transaction_61993948` (`liability_id`),
  KEY `finance_transaction_42dc49bc` (`category_id`),
  KEY `finance_transaction_6f2fe10e` (`account_id`),
  KEY `finance_transaction_4eab3821` (`value_currency_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finance_transaction`
--

LOCK TABLES `finance_transaction` WRITE;
/*!40000 ALTER TABLE `finance_transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `finance_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `identities_contact`
--

DROP TABLE IF EXISTS `identities_contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `identities_contact` (
  `object_ptr_id` int(11) NOT NULL,
  `contact_type_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `related_user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `identities_contact_5cd23a67` (`contact_type_id`),
  KEY `identities_contact_63f17a16` (`parent_id`),
  KEY `identities_contact_85bdf8d` (`related_user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `identities_contact`
--

LOCK TABLES `identities_contact` WRITE;
/*!40000 ALTER TABLE `identities_contact` DISABLE KEYS */;
INSERT INTO `identities_contact` VALUES (24,21,'Company',NULL,NULL),(25,23,'Admin',NULL,1);
/*!40000 ALTER TABLE `identities_contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `identities_contactfield`
--

DROP TABLE IF EXISTS `identities_contactfield`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `identities_contactfield` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `label` varchar(256) NOT NULL,
  `field_type` varchar(64) NOT NULL,
  `required` tinyint(1) NOT NULL,
  `allowed_values` longtext,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `identities_contactfield`
--

LOCK TABLES `identities_contactfield` WRITE;
/*!40000 ALTER TABLE `identities_contactfield` DISABLE KEYS */;
INSERT INTO `identities_contactfield` VALUES (16,'address','Address','details',0,NULL,''),(17,'email','E-mail','email',0,NULL,''),(18,'phone','Phone','phone',0,NULL,''),(19,'url','Website','url',0,NULL,''),(20,'picture','Picture','picture',0,NULL,'');
/*!40000 ALTER TABLE `identities_contactfield` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `identities_contacttype`
--

DROP TABLE IF EXISTS `identities_contacttype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `identities_contacttype` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `slug` varchar(256) NOT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `identities_contacttype`
--

LOCK TABLES `identities_contacttype` WRITE;
/*!40000 ALTER TABLE `identities_contacttype` DISABLE KEYS */;
INSERT INTO `identities_contacttype` VALUES (21,'Company','company',''),(22,'Department','department',''),(23,'Person','person','');
/*!40000 ALTER TABLE `identities_contacttype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `identities_contacttype_fields`
--

DROP TABLE IF EXISTS `identities_contacttype_fields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `identities_contacttype_fields` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contacttype_id` int(11) NOT NULL,
  `contactfield_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `contacttype_id` (`contacttype_id`,`contactfield_id`),
  KEY `identities_contacttype_fields_1cddf5f9` (`contacttype_id`),
  KEY `identities_contacttype_fields_3910dcc8` (`contactfield_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `identities_contacttype_fields`
--

LOCK TABLES `identities_contacttype_fields` WRITE;
/*!40000 ALTER TABLE `identities_contacttype_fields` DISABLE KEYS */;
INSERT INTO `identities_contacttype_fields` VALUES (1,21,16),(2,21,17),(3,21,18),(4,21,19),(5,21,20),(6,22,16),(7,22,17),(8,22,18),(9,22,19),(10,23,16),(11,23,17),(12,23,18),(13,23,19),(14,23,20);
/*!40000 ALTER TABLE `identities_contacttype_fields` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `identities_contactvalue`
--

DROP TABLE IF EXISTS `identities_contactvalue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `identities_contactvalue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `field_id` int(11) NOT NULL,
  `contact_id` int(11) NOT NULL,
  `value` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `identities_contactvalue_4b60cce9` (`field_id`),
  KEY `identities_contactvalue_170b8823` (`contact_id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `identities_contactvalue`
--

LOCK TABLES `identities_contactvalue` WRITE;
/*!40000 ALTER TABLE `identities_contactvalue` DISABLE KEYS */;
INSERT INTO `identities_contactvalue` VALUES (1,16,24,''),(2,17,24,''),(3,18,24,''),(4,20,24,''),(5,19,24,''),(15,19,25,''),(14,20,25,''),(13,18,25,''),(12,17,25,''),(11,16,25,'');
/*!40000 ALTER TABLE `identities_contactvalue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `infrastructure_item`
--

DROP TABLE IF EXISTS `infrastructure_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `infrastructure_item` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(512) NOT NULL,
  `item_type_id` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `manufacturer_id` int(11) DEFAULT NULL,
  `supplier_id` int(11) DEFAULT NULL,
  `location_id` int(11) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `asset_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `infrastructure_item_38d6fbe9` (`item_type_id`),
  KEY `infrastructure_item_44224078` (`status_id`),
  KEY `infrastructure_item_63f17a16` (`parent_id`),
  KEY `infrastructure_item_4ac7f441` (`manufacturer_id`),
  KEY `infrastructure_item_6ad0ca34` (`supplier_id`),
  KEY `infrastructure_item_319d859` (`location_id`),
  KEY `infrastructure_item_5d52dd10` (`owner_id`),
  KEY `infrastructure_item_7696bc7d` (`asset_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `infrastructure_item`
--

LOCK TABLES `infrastructure_item` WRITE;
/*!40000 ALTER TABLE `infrastructure_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `infrastructure_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `infrastructure_itemfield`
--

DROP TABLE IF EXISTS `infrastructure_itemfield`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `infrastructure_itemfield` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `label` varchar(256) NOT NULL,
  `field_type` varchar(64) NOT NULL,
  `required` tinyint(1) NOT NULL,
  `allowed_values` longtext,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `infrastructure_itemfield`
--

LOCK TABLES `infrastructure_itemfield` WRITE;
/*!40000 ALTER TABLE `infrastructure_itemfield` DISABLE KEYS */;
INSERT INTO `infrastructure_itemfield` VALUES (54,'ip-address','IP Address','text',0,NULL,''),(55,'hostname','Hostname','text',0,NULL,''),(57,'os','Operating System','text',0,NULL,''),(58,'setup_date','Date Installed','date',0,NULL,'');
/*!40000 ALTER TABLE `infrastructure_itemfield` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `infrastructure_itemservicing`
--

DROP TABLE IF EXISTS `infrastructure_itemservicing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `infrastructure_itemservicing` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `supplier_id` int(11) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `details` longtext NOT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `infrastructure_itemservicing_6ad0ca34` (`supplier_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `infrastructure_itemservicing`
--

LOCK TABLES `infrastructure_itemservicing` WRITE;
/*!40000 ALTER TABLE `infrastructure_itemservicing` DISABLE KEYS */;
/*!40000 ALTER TABLE `infrastructure_itemservicing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `infrastructure_itemservicing_items`
--

DROP TABLE IF EXISTS `infrastructure_itemservicing_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `infrastructure_itemservicing_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `itemservicing_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `itemservicing_id` (`itemservicing_id`,`item_id`),
  KEY `infrastructure_itemservicing_items_2b23f90a` (`itemservicing_id`),
  KEY `infrastructure_itemservicing_items_67b70d25` (`item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `infrastructure_itemservicing_items`
--

LOCK TABLES `infrastructure_itemservicing_items` WRITE;
/*!40000 ALTER TABLE `infrastructure_itemservicing_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `infrastructure_itemservicing_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `infrastructure_itemservicing_payments`
--

DROP TABLE IF EXISTS `infrastructure_itemservicing_payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `infrastructure_itemservicing_payments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `itemservicing_id` int(11) NOT NULL,
  `transaction_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `itemservicing_id` (`itemservicing_id`,`transaction_id`),
  KEY `infrastructure_itemservicing_payments_2b23f90a` (`itemservicing_id`),
  KEY `infrastructure_itemservicing_payments_45d19ab3` (`transaction_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `infrastructure_itemservicing_payments`
--

LOCK TABLES `infrastructure_itemservicing_payments` WRITE;
/*!40000 ALTER TABLE `infrastructure_itemservicing_payments` DISABLE KEYS */;
/*!40000 ALTER TABLE `infrastructure_itemservicing_payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `infrastructure_itemstatus`
--

DROP TABLE IF EXISTS `infrastructure_itemstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `infrastructure_itemstatus` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `details` longtext,
  `active` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `infrastructure_itemstatus`
--

LOCK TABLES `infrastructure_itemstatus` WRITE;
/*!40000 ALTER TABLE `infrastructure_itemstatus` DISABLE KEYS */;
INSERT INTO `infrastructure_itemstatus` VALUES (51,'Active','',1,0),(52,'Unused','',0,0),(53,'Removed','',0,1);
/*!40000 ALTER TABLE `infrastructure_itemstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `infrastructure_itemtype`
--

DROP TABLE IF EXISTS `infrastructure_itemtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `infrastructure_itemtype` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(512) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`),
  KEY `infrastructure_itemtype_63f17a16` (`parent_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `infrastructure_itemtype`
--

LOCK TABLES `infrastructure_itemtype` WRITE;
/*!40000 ALTER TABLE `infrastructure_itemtype` DISABLE KEYS */;
INSERT INTO `infrastructure_itemtype` VALUES (56,'Workstation',NULL,''),(59,'Server',NULL,'');
/*!40000 ALTER TABLE `infrastructure_itemtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `infrastructure_itemtype_fields`
--

DROP TABLE IF EXISTS `infrastructure_itemtype_fields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `infrastructure_itemtype_fields` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `itemtype_id` int(11) NOT NULL,
  `itemfield_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `itemtype_id` (`itemtype_id`,`itemfield_id`),
  KEY `infrastructure_itemtype_fields_6668c917` (`itemtype_id`),
  KEY `infrastructure_itemtype_fields_3b3854d6` (`itemfield_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `infrastructure_itemtype_fields`
--

LOCK TABLES `infrastructure_itemtype_fields` WRITE;
/*!40000 ALTER TABLE `infrastructure_itemtype_fields` DISABLE KEYS */;
INSERT INTO `infrastructure_itemtype_fields` VALUES (4,56,58),(3,56,57),(5,56,54),(6,56,55),(7,59,57),(8,59,58),(9,59,54),(10,59,55);
/*!40000 ALTER TABLE `infrastructure_itemtype_fields` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `infrastructure_itemvalue`
--

DROP TABLE IF EXISTS `infrastructure_itemvalue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `infrastructure_itemvalue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `field_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `value` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `infrastructure_itemvalue_4b60cce9` (`field_id`),
  KEY `infrastructure_itemvalue_67b70d25` (`item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `infrastructure_itemvalue`
--

LOCK TABLES `infrastructure_itemvalue` WRITE;
/*!40000 ALTER TABLE `infrastructure_itemvalue` DISABLE KEYS */;
/*!40000 ALTER TABLE `infrastructure_itemvalue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knowledge_knowledgecategory`
--

DROP TABLE IF EXISTS `knowledge_knowledgecategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `knowledge_knowledgecategory` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `details` longtext,
  `treepath` varchar(800) NOT NULL,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knowledge_knowledgecategory`
--

LOCK TABLES `knowledge_knowledgecategory` WRITE;
/*!40000 ALTER TABLE `knowledge_knowledgecategory` DISABLE KEYS */;
/*!40000 ALTER TABLE `knowledge_knowledgecategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knowledge_knowledgefolder`
--

DROP TABLE IF EXISTS `knowledge_knowledgefolder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `knowledge_knowledgefolder` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `details` longtext,
  `parent_id` int(11) DEFAULT NULL,
  `treepath` varchar(800) NOT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `knowledge_knowledgefolder_63f17a16` (`parent_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knowledge_knowledgefolder`
--

LOCK TABLES `knowledge_knowledgefolder` WRITE;
/*!40000 ALTER TABLE `knowledge_knowledgefolder` DISABLE KEYS */;
INSERT INTO `knowledge_knowledgefolder` VALUES (60,'Default','',NULL,'default/');
/*!40000 ALTER TABLE `knowledge_knowledgefolder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knowledge_knowledgeitem`
--

DROP TABLE IF EXISTS `knowledge_knowledgeitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `knowledge_knowledgeitem` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `folder_id` int(11) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `body` longtext,
  `treepath` varchar(800) NOT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `knowledge_knowledgeitem_4e5f642` (`folder_id`),
  KEY `knowledge_knowledgeitem_42dc49bc` (`category_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knowledge_knowledgeitem`
--

LOCK TABLES `knowledge_knowledgeitem` WRITE;
/*!40000 ALTER TABLE `knowledge_knowledgeitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `knowledge_knowledgeitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messaging_mailinglist`
--

DROP TABLE IF EXISTS `messaging_mailinglist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messaging_mailinglist` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` longtext,
  `from_contact_id` int(11) NOT NULL,
  `opt_in_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `messaging_mailinglist_3286f8f1` (`from_contact_id`),
  KEY `messaging_mailinglist_283e3c13` (`opt_in_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messaging_mailinglist`
--

LOCK TABLES `messaging_mailinglist` WRITE;
/*!40000 ALTER TABLE `messaging_mailinglist` DISABLE KEYS */;
/*!40000 ALTER TABLE `messaging_mailinglist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messaging_mailinglist_members`
--

DROP TABLE IF EXISTS `messaging_mailinglist_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messaging_mailinglist_members` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mailinglist_id` int(11) NOT NULL,
  `contact_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mailinglist_id` (`mailinglist_id`,`contact_id`),
  KEY `messaging_mailinglist_members_5ae64d68` (`mailinglist_id`),
  KEY `messaging_mailinglist_members_170b8823` (`contact_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messaging_mailinglist_members`
--

LOCK TABLES `messaging_mailinglist_members` WRITE;
/*!40000 ALTER TABLE `messaging_mailinglist_members` DISABLE KEYS */;
/*!40000 ALTER TABLE `messaging_mailinglist_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messaging_message`
--

DROP TABLE IF EXISTS `messaging_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messaging_message` (
  `object_ptr_id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `body` longtext NOT NULL,
  `author_id` int(11) NOT NULL,
  `stream_id` int(11) DEFAULT NULL,
  `reply_to_id` int(11) DEFAULT NULL,
  `mlist_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `messaging_message_337b96ff` (`author_id`),
  KEY `messaging_message_7371fd6` (`stream_id`),
  KEY `messaging_message_2710e4f4` (`reply_to_id`),
  KEY `messaging_message_10ae7b98` (`mlist_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messaging_message`
--

LOCK TABLES `messaging_message` WRITE;
/*!40000 ALTER TABLE `messaging_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `messaging_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messaging_message_read_by`
--

DROP TABLE IF EXISTS `messaging_message_read_by`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messaging_message_read_by` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `message_id` (`message_id`,`user_id`),
  KEY `messaging_message_read_by_38373776` (`message_id`),
  KEY `messaging_message_read_by_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messaging_message_read_by`
--

LOCK TABLES `messaging_message_read_by` WRITE;
/*!40000 ALTER TABLE `messaging_message_read_by` DISABLE KEYS */;
/*!40000 ALTER TABLE `messaging_message_read_by` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messaging_message_recipients`
--

DROP TABLE IF EXISTS `messaging_message_recipients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messaging_message_recipients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message_id` int(11) NOT NULL,
  `contact_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `message_id` (`message_id`,`contact_id`),
  KEY `messaging_message_recipients_38373776` (`message_id`),
  KEY `messaging_message_recipients_170b8823` (`contact_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messaging_message_recipients`
--

LOCK TABLES `messaging_message_recipients` WRITE;
/*!40000 ALTER TABLE `messaging_message_recipients` DISABLE KEYS */;
/*!40000 ALTER TABLE `messaging_message_recipients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messaging_messagestream`
--

DROP TABLE IF EXISTS `messaging_messagestream`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messaging_messagestream` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `incoming_server_name` varchar(255) DEFAULT NULL,
  `incoming_server_type` varchar(255) DEFAULT NULL,
  `incoming_server_username` varchar(255) DEFAULT NULL,
  `incoming_password` varchar(255) DEFAULT NULL,
  `outgoing_email` varchar(255) DEFAULT NULL,
  `outgoing_server_name` varchar(255) DEFAULT NULL,
  `outgoing_server_type` varchar(255) DEFAULT NULL,
  `outgoing_server_username` varchar(255) DEFAULT NULL,
  `outgoing_password` varchar(255) DEFAULT NULL,
  `faulty` tinyint(1) NOT NULL,
  `last_checked` datetime DEFAULT NULL,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messaging_messagestream`
--

LOCK TABLES `messaging_messagestream` WRITE;
/*!40000 ALTER TABLE `messaging_messagestream` DISABLE KEYS */;
INSERT INTO `messaging_messagestream` VALUES (39,'General','',NULL,'','','','',NULL,'','',0,NULL);
/*!40000 ALTER TABLE `messaging_messagestream` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messaging_template`
--

DROP TABLE IF EXISTS `messaging_template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messaging_template` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `body` longtext NOT NULL,
  `subject` varchar(255) NOT NULL,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messaging_template`
--

LOCK TABLES `messaging_template` WRITE;
/*!40000 ALTER TABLE `messaging_template` DISABLE KEYS */;
/*!40000 ALTER TABLE `messaging_template` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects_milestone`
--

DROP TABLE IF EXISTS `projects_milestone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projects_milestone` (
  `object_ptr_id` int(11) NOT NULL,
  `project_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status_id` int(11) NOT NULL,
  `details` longtext,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `projects_milestone_499df97c` (`project_id`),
  KEY `projects_milestone_44224078` (`status_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects_milestone`
--

LOCK TABLES `projects_milestone` WRITE;
/*!40000 ALTER TABLE `projects_milestone` DISABLE KEYS */;
/*!40000 ALTER TABLE `projects_milestone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects_project`
--

DROP TABLE IF EXISTS `projects_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projects_project` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `manager_id` int(11) DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`),
  KEY `projects_project_63f17a16` (`parent_id`),
  KEY `projects_project_501a2222` (`manager_id`),
  KEY `projects_project_4a4e8ffb` (`client_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects_project`
--

LOCK TABLES `projects_project` WRITE;
/*!40000 ALTER TABLE `projects_project` DISABLE KEYS */;
/*!40000 ALTER TABLE `projects_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects_task`
--

DROP TABLE IF EXISTS `projects_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projects_task` (
  `object_ptr_id` int(11) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `project_id` int(11) NOT NULL,
  `milestone_id` int(11) DEFAULT NULL,
  `status_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `details` longtext,
  `caller_id` int(11) DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `priority` int(11) NOT NULL,
  `estimated_time` int(11) DEFAULT NULL,
  `depends_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `projects_task_63f17a16` (`parent_id`),
  KEY `projects_task_499df97c` (`project_id`),
  KEY `projects_task_6305d6e1` (`milestone_id`),
  KEY `projects_task_44224078` (`status_id`),
  KEY `projects_task_8be43a3` (`caller_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects_task`
--

LOCK TABLES `projects_task` WRITE;
/*!40000 ALTER TABLE `projects_task` DISABLE KEYS */;
/*!40000 ALTER TABLE `projects_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects_task_assigned`
--

DROP TABLE IF EXISTS `projects_task_assigned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projects_task_assigned` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`,`user_id`),
  KEY `projects_task_assigned_3ff01bab` (`task_id`),
  KEY `projects_task_assigned_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects_task_assigned`
--

LOCK TABLES `projects_task_assigned` WRITE;
/*!40000 ALTER TABLE `projects_task_assigned` DISABLE KEYS */;
/*!40000 ALTER TABLE `projects_task_assigned` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects_taskstatus`
--

DROP TABLE IF EXISTS `projects_taskstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projects_taskstatus` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `details` longtext,
  `active` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects_taskstatus`
--

LOCK TABLES `projects_taskstatus` WRITE;
/*!40000 ALTER TABLE `projects_taskstatus` DISABLE KEYS */;
INSERT INTO `projects_taskstatus` VALUES (26,'Open','',1,0),(27,'Awaits Spec','',0,0),(28,'Failed','',1,1),(29,'Complete','',0,1);
/*!40000 ALTER TABLE `projects_taskstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects_tasktimeslot`
--

DROP TABLE IF EXISTS `projects_tasktimeslot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projects_tasktimeslot` (
  `object_ptr_id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `time_from` datetime NOT NULL,
  `time_to` datetime DEFAULT NULL,
  `timezone` int(11) NOT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`),
  KEY `projects_tasktimeslot_3ff01bab` (`task_id`),
  KEY `projects_tasktimeslot_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects_tasktimeslot`
--

LOCK TABLES `projects_tasktimeslot` WRITE;
/*!40000 ALTER TABLE `projects_tasktimeslot` DISABLE KEYS */;
/*!40000 ALTER TABLE `projects_tasktimeslot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports_chart`
--

DROP TABLE IF EXISTS `reports_chart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reports_chart` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `report_id` int(11) NOT NULL,
  `options` longtext,
  PRIMARY KEY (`object_ptr_id`),
  KEY `reports_chart_29fa1030` (`report_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports_chart`
--

LOCK TABLES `reports_chart` WRITE;
/*!40000 ALTER TABLE `reports_chart` DISABLE KEYS */;
/*!40000 ALTER TABLE `reports_chart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports_report`
--

DROP TABLE IF EXISTS `reports_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reports_report` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(512) NOT NULL,
  `model` longtext,
  `content` longtext,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports_report`
--

LOCK TABLES `reports_report` WRITE;
/*!40000 ALTER TABLE `reports_report` DISABLE KEYS */;
/*!40000 ALTER TABLE `reports_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_lead`
--

DROP TABLE IF EXISTS `sales_lead`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_lead` (
  `object_ptr_id` int(11) NOT NULL,
  `contact_id` int(11) NOT NULL,
  `source_id` int(11) DEFAULT NULL,
  `contact_method` varchar(32) NOT NULL,
  `status_id` int(11) NOT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`),
  KEY `sales_lead_170b8823` (`contact_id`),
  KEY `sales_lead_7607617b` (`source_id`),
  KEY `sales_lead_44224078` (`status_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_lead`
--

LOCK TABLES `sales_lead` WRITE;
/*!40000 ALTER TABLE `sales_lead` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_lead` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_lead_assigned`
--

DROP TABLE IF EXISTS `sales_lead_assigned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_lead_assigned` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lead_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lead_id` (`lead_id`,`user_id`),
  KEY `sales_lead_assigned_7438796e` (`lead_id`),
  KEY `sales_lead_assigned_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_lead_assigned`
--

LOCK TABLES `sales_lead_assigned` WRITE;
/*!40000 ALTER TABLE `sales_lead_assigned` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_lead_assigned` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_lead_products_interested`
--

DROP TABLE IF EXISTS `sales_lead_products_interested`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_lead_products_interested` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lead_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lead_id` (`lead_id`,`product_id`),
  KEY `sales_lead_products_interested_7438796e` (`lead_id`),
  KEY `sales_lead_products_interested_44bdf3ee` (`product_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_lead_products_interested`
--

LOCK TABLES `sales_lead_products_interested` WRITE;
/*!40000 ALTER TABLE `sales_lead_products_interested` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_lead_products_interested` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_opportunity`
--

DROP TABLE IF EXISTS `sales_opportunity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_opportunity` (
  `object_ptr_id` int(11) NOT NULL,
  `lead_id` int(11) DEFAULT NULL,
  `contact_id` int(11) NOT NULL,
  `source_id` int(11) DEFAULT NULL,
  `expected_date` date DEFAULT NULL,
  `closed_date` date DEFAULT NULL,
  `status_id` int(11) NOT NULL,
  `probability` decimal(3,0) DEFAULT NULL,
  `amount` decimal(20,2) NOT NULL,
  `amount_currency_id` int(11) NOT NULL,
  `amount_display` decimal(20,2) NOT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`),
  KEY `sales_opportunity_7438796e` (`lead_id`),
  KEY `sales_opportunity_170b8823` (`contact_id`),
  KEY `sales_opportunity_7607617b` (`source_id`),
  KEY `sales_opportunity_44224078` (`status_id`),
  KEY `sales_opportunity_3af8ff09` (`amount_currency_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_opportunity`
--

LOCK TABLES `sales_opportunity` WRITE;
/*!40000 ALTER TABLE `sales_opportunity` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_opportunity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_opportunity_assigned`
--

DROP TABLE IF EXISTS `sales_opportunity_assigned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_opportunity_assigned` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `opportunity_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opportunity_id` (`opportunity_id`,`user_id`),
  KEY `sales_opportunity_assigned_324f1350` (`opportunity_id`),
  KEY `sales_opportunity_assigned_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_opportunity_assigned`
--

LOCK TABLES `sales_opportunity_assigned` WRITE;
/*!40000 ALTER TABLE `sales_opportunity_assigned` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_opportunity_assigned` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_opportunity_products_interested`
--

DROP TABLE IF EXISTS `sales_opportunity_products_interested`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_opportunity_products_interested` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `opportunity_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opportunity_id` (`opportunity_id`,`product_id`),
  KEY `sales_opportunity_products_interested_324f1350` (`opportunity_id`),
  KEY `sales_opportunity_products_interested_44bdf3ee` (`product_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_opportunity_products_interested`
--

LOCK TABLES `sales_opportunity_products_interested` WRITE;
/*!40000 ALTER TABLE `sales_opportunity_products_interested` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_opportunity_products_interested` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_orderedproduct`
--

DROP TABLE IF EXISTS `sales_orderedproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_orderedproduct` (
  `object_ptr_id` int(11) NOT NULL,
  `subscription_id` int(11) DEFAULT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` decimal(30,2) NOT NULL,
  `discount` decimal(4,2) NOT NULL,
  `tax_id` int(11) DEFAULT NULL,
  `rate` decimal(20,2) NOT NULL,
  `rate_display` decimal(20,2) NOT NULL,
  `order_id` int(11) NOT NULL,
  `description` longtext,
  `fulfilled` tinyint(1) NOT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `sales_orderedproduct_104f5ac1` (`subscription_id`),
  KEY `sales_orderedproduct_44bdf3ee` (`product_id`),
  KEY `sales_orderedproduct_2af098d0` (`tax_id`),
  KEY `sales_orderedproduct_7cc8fcf5` (`order_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_orderedproduct`
--

LOCK TABLES `sales_orderedproduct` WRITE;
/*!40000 ALTER TABLE `sales_orderedproduct` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_orderedproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_product`
--

DROP TABLE IF EXISTS `sales_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_product` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(512) NOT NULL,
  `product_type` varchar(32) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `code` varchar(512) DEFAULT NULL,
  `supplier_id` int(11) DEFAULT NULL,
  `supplier_code` int(11) DEFAULT NULL,
  `buy_price` decimal(20,2) NOT NULL,
  `sell_price` decimal(20,2) NOT NULL,
  `stock_quantity` int(11) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `runout_action` varchar(32) DEFAULT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`),
  KEY `sales_product_63f17a16` (`parent_id`),
  KEY `sales_product_6ad0ca34` (`supplier_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_product`
--

LOCK TABLES `sales_product` WRITE;
/*!40000 ALTER TABLE `sales_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_saleorder`
--

DROP TABLE IF EXISTS `sales_saleorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_saleorder` (
  `object_ptr_id` int(11) NOT NULL,
  `reference` varchar(512) DEFAULT NULL,
  `datetime` datetime NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `opportunity_id` int(11) DEFAULT NULL,
  `source_id` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  `currency_id` int(11) NOT NULL,
  `total` decimal(20,2) NOT NULL,
  `total_display` decimal(20,2) NOT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`),
  KEY `sales_saleorder_4a4e8ffb` (`client_id`),
  KEY `sales_saleorder_324f1350` (`opportunity_id`),
  KEY `sales_saleorder_7607617b` (`source_id`),
  KEY `sales_saleorder_44224078` (`status_id`),
  KEY `sales_saleorder_41f657b3` (`currency_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_saleorder`
--

LOCK TABLES `sales_saleorder` WRITE;
/*!40000 ALTER TABLE `sales_saleorder` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_saleorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_saleorder_assigned`
--

DROP TABLE IF EXISTS `sales_saleorder_assigned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_saleorder_assigned` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `saleorder_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `saleorder_id` (`saleorder_id`,`user_id`),
  KEY `sales_saleorder_assigned_3f831eee` (`saleorder_id`),
  KEY `sales_saleorder_assigned_403f60f` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_saleorder_assigned`
--

LOCK TABLES `sales_saleorder_assigned` WRITE;
/*!40000 ALTER TABLE `sales_saleorder_assigned` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_saleorder_assigned` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_saleorder_payment`
--

DROP TABLE IF EXISTS `sales_saleorder_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_saleorder_payment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `saleorder_id` int(11) NOT NULL,
  `transaction_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `saleorder_id` (`saleorder_id`,`transaction_id`),
  KEY `sales_saleorder_payment_3f831eee` (`saleorder_id`),
  KEY `sales_saleorder_payment_45d19ab3` (`transaction_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_saleorder_payment`
--

LOCK TABLES `sales_saleorder_payment` WRITE;
/*!40000 ALTER TABLE `sales_saleorder_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_saleorder_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_salesource`
--

DROP TABLE IF EXISTS `sales_salesource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_salesource` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(512) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_salesource`
--

LOCK TABLES `sales_salesource` WRITE;
/*!40000 ALTER TABLE `sales_salesource` DISABLE KEYS */;
INSERT INTO `sales_salesource` VALUES (41,'Advertisement',1,''),(43,'Colleague',1,''),(44,'Friend',1,''),(45,'Search Engine',1,''),(46,'Other',1,'');
/*!40000 ALTER TABLE `sales_salesource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_salestatus`
--

DROP TABLE IF EXISTS `sales_salestatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_salestatus` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(512) NOT NULL,
  `use_leads` tinyint(1) NOT NULL,
  `use_opportunities` tinyint(1) NOT NULL,
  `use_sales` tinyint(1) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_salestatus`
--

LOCK TABLES `sales_salestatus` WRITE;
/*!40000 ALTER TABLE `sales_salestatus` DISABLE KEYS */;
INSERT INTO `sales_salestatus` VALUES (47,'Open',1,1,1,1,0,''),(48,'Paused',1,1,1,1,0,''),(49,'Closed',1,1,1,1,0,''),(50,'Failed',1,1,1,0,0,'');
/*!40000 ALTER TABLE `sales_salestatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_subscription`
--

DROP TABLE IF EXISTS `sales_subscription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales_subscription` (
  `object_ptr_id` int(11) NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `start` date NOT NULL,
  `expiry` date DEFAULT NULL,
  `cycle_period` varchar(32) NOT NULL,
  `cycle_end` date DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `details` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `sales_subscription_4a4e8ffb` (`client_id`),
  KEY `sales_subscription_44bdf3ee` (`product_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_subscription`
--

LOCK TABLES `sales_subscription` WRITE;
/*!40000 ALTER TABLE `sales_subscription` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_subscription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_service`
--

DROP TABLE IF EXISTS `services_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_service` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`),
  KEY `services_service_63f17a16` (`parent_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_service`
--

LOCK TABLES `services_service` WRITE;
/*!40000 ALTER TABLE `services_service` DISABLE KEYS */;
/*!40000 ALTER TABLE `services_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_serviceagent`
--

DROP TABLE IF EXISTS `services_serviceagent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_serviceagent` (
  `object_ptr_id` int(11) NOT NULL,
  `related_user_id` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `occupied` tinyint(1) NOT NULL,
  `available_from` time DEFAULT NULL,
  `available_to` time DEFAULT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `services_serviceagent_85bdf8d` (`related_user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_serviceagent`
--

LOCK TABLES `services_serviceagent` WRITE;
/*!40000 ALTER TABLE `services_serviceagent` DISABLE KEYS */;
INSERT INTO `services_serviceagent` VALUES (35,1,1,0,NULL,NULL);
/*!40000 ALTER TABLE `services_serviceagent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_servicelevelagreement`
--

DROP TABLE IF EXISTS `services_servicelevelagreement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_servicelevelagreement` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `service_id` int(11) NOT NULL,
  `default` tinyint(1) NOT NULL,
  `response_time` int(10) unsigned DEFAULT NULL,
  `uptime_rate` double DEFAULT NULL,
  `available_from` time DEFAULT NULL,
  `available_to` time DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `provider_id` int(11) NOT NULL,
  PRIMARY KEY (`object_ptr_id`),
  KEY `services_servicelevelagreement_6f1d73c2` (`service_id`),
  KEY `services_servicelevelagreement_4a4e8ffb` (`client_id`),
  KEY `services_servicelevelagreement_261a2069` (`provider_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_servicelevelagreement`
--

LOCK TABLES `services_servicelevelagreement` WRITE;
/*!40000 ALTER TABLE `services_servicelevelagreement` DISABLE KEYS */;
/*!40000 ALTER TABLE `services_servicelevelagreement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_ticket`
--

DROP TABLE IF EXISTS `services_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_ticket` (
  `object_ptr_id` int(11) NOT NULL,
  `reference` varchar(256) NOT NULL,
  `name` varchar(256) NOT NULL,
  `caller_id` int(11) DEFAULT NULL,
  `urgency` int(11) NOT NULL,
  `priority` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  `service_id` int(11) DEFAULT NULL,
  `sla_id` int(11) DEFAULT NULL,
  `queue_id` int(11) DEFAULT NULL,
  `message_id` int(11) DEFAULT NULL,
  `details` longtext,
  `resolution` longtext,
  PRIMARY KEY (`object_ptr_id`),
  KEY `services_ticket_8be43a3` (`caller_id`),
  KEY `services_ticket_44224078` (`status_id`),
  KEY `services_ticket_6f1d73c2` (`service_id`),
  KEY `services_ticket_27af21d3` (`sla_id`),
  KEY `services_ticket_1e72d6b8` (`queue_id`),
  KEY `services_ticket_38373776` (`message_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_ticket`
--

LOCK TABLES `services_ticket` WRITE;
/*!40000 ALTER TABLE `services_ticket` DISABLE KEYS */;
/*!40000 ALTER TABLE `services_ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_ticket_assigned`
--

DROP TABLE IF EXISTS `services_ticket_assigned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_ticket_assigned` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ticket_id` int(11) NOT NULL,
  `serviceagent_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ticket_id` (`ticket_id`,`serviceagent_id`),
  KEY `services_ticket_assigned_2f04b9de` (`ticket_id`),
  KEY `services_ticket_assigned_65c05e58` (`serviceagent_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_ticket_assigned`
--

LOCK TABLES `services_ticket_assigned` WRITE;
/*!40000 ALTER TABLE `services_ticket_assigned` DISABLE KEYS */;
/*!40000 ALTER TABLE `services_ticket_assigned` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_ticketqueue`
--

DROP TABLE IF EXISTS `services_ticketqueue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_ticketqueue` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `default_ticket_status_id` int(11) DEFAULT NULL,
  `default_ticket_priority` int(11) NOT NULL,
  `default_service_id` int(11) DEFAULT NULL,
  `waiting_time` int(10) unsigned DEFAULT NULL,
  `next_queue_id` int(11) DEFAULT NULL,
  `ticket_code` varchar(8) DEFAULT NULL,
  `message_stream_id` int(11) DEFAULT NULL,
  `details` longtext,
  PRIMARY KEY (`object_ptr_id`),
  KEY `services_ticketqueue_63f17a16` (`parent_id`),
  KEY `services_ticketqueue_cb5f7ee` (`default_ticket_status_id`),
  KEY `services_ticketqueue_5e176084` (`default_service_id`),
  KEY `services_ticketqueue_14bbbe51` (`next_queue_id`),
  KEY `services_ticketqueue_10cb5376` (`message_stream_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_ticketqueue`
--

LOCK TABLES `services_ticketqueue` WRITE;
/*!40000 ALTER TABLE `services_ticketqueue` DISABLE KEYS */;
INSERT INTO `services_ticketqueue` VALUES (40,'ServiceDesk',1,NULL,30,3,NULL,NULL,NULL,'',NULL,'');
/*!40000 ALTER TABLE `services_ticketqueue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_ticketrecord`
--

DROP TABLE IF EXISTS `services_ticketrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_ticketrecord` (
  `updaterecord_ptr_id` int(11) NOT NULL,
  `message_id` int(11) DEFAULT NULL,
  `notify` tinyint(1) NOT NULL,
  PRIMARY KEY (`updaterecord_ptr_id`),
  KEY `services_ticketrecord_38373776` (`message_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_ticketrecord`
--

LOCK TABLES `services_ticketrecord` WRITE;
/*!40000 ALTER TABLE `services_ticketrecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `services_ticketrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_ticketstatus`
--

DROP TABLE IF EXISTS `services_ticketstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_ticketstatus` (
  `object_ptr_id` int(11) NOT NULL,
  `name` varchar(256) NOT NULL,
  `details` longtext,
  `active` tinyint(1) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`object_ptr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_ticketstatus`
--

LOCK TABLES `services_ticketstatus` WRITE;
/*!40000 ALTER TABLE `services_ticketstatus` DISABLE KEYS */;
INSERT INTO `services_ticketstatus` VALUES (30,'Open','',1,0),(31,'Pending Caller','',0,0),(32,'Pending Supplier','',0,0),(33,'Won\'t Fix','',1,1),(34,'Closed','',0,1);
/*!40000 ALTER TABLE `services_ticketstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `south_migrationhistory`
--

DROP TABLE IF EXISTS `south_migrationhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `south_migrationhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(255) NOT NULL,
  `migration` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=43 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `south_migrationhistory`
--

LOCK TABLES `south_migrationhistory` WRITE;
/*!40000 ALTER TABLE `south_migrationhistory` DISABLE KEYS */;
INSERT INTO `south_migrationhistory` VALUES (1,'account','0001_initial','2011-07-31 15:25:07'),(2,'core','0001_initial','2011-07-31 15:25:07'),(3,'core','0002_auto__del_notification__add_comment__add_tag__add_revisionfield__add_r','2011-07-31 15:25:07'),(4,'core','0003_treeiocore','2011-07-31 15:25:07'),(5,'core','0004_auto__del_field_object_user','2011-07-31 15:25:07'),(6,'core','0005_auto__del_field_group_id__chg_field_group_accessentity_ptr__del_field_','2011-07-31 15:25:07'),(7,'core','0006_auto__add_configsetting','2011-07-31 15:25:07'),(8,'api','0001_initial','2011-07-31 15:25:07'),(9,'api','0002_auto__add_field_consumer_owner','2011-07-31 15:25:07'),(10,'documents','0001_initial','2011-07-31 15:25:07'),(11,'events','0001_initial','2011-07-31 15:25:07'),(12,'finance','0001_initial','2011-07-31 15:25:07'),(13,'finance','0002_auto__add_currency__add_tax__add_field_liability_value_currency__add_f','2011-07-31 15:25:07'),(14,'finance','0003_treeiocurrency','2011-07-31 15:25:07'),(15,'identities','0001_initial','2011-07-31 15:25:07'),(16,'identities','0002_auto__chg_field_contact_related_user','2011-07-31 15:25:07'),(17,'identities','0003_related_accessentity','2011-07-31 15:25:07'),(18,'identities','0004_auto__del_field_contact_related_group','2011-07-31 15:25:07'),(19,'infrastructure','0001_initial','2011-07-31 15:25:07'),(20,'knowledge','0001_initial','2011-07-31 15:25:07'),(21,'messaging','0001_initial','2011-07-31 15:25:07'),(22,'messaging','0002_auto__add_mailinglist__add_template__add_field_message_mlist__chg_fiel','2011-07-31 15:25:07'),(23,'messaging','0003_merge_emailbox_stream','2011-07-31 15:25:07'),(24,'messaging','0004_auto__del_emailbox__del_field_messagestream_email_outgoing__del_field_','2011-07-31 15:25:07'),(25,'news','0001_initial','2011-07-31 15:25:07'),(26,'projects','0001_initial','2011-07-31 15:25:07'),(27,'projects','0002_updaterecords','2011-07-31 15:25:07'),(28,'projects','0003_auto__add_field_tasktimeslot_user','2011-07-31 15:25:07'),(29,'projects','0004_timeslots','2011-07-31 15:25:07'),(30,'projects','0005_auto__del_taskrecord','2011-07-31 15:25:07'),(31,'reports','0001_initial','2011-07-31 15:25:07'),(32,'reports','0002_auto__del_template__add_chart__del_field_report_template__add_field_re','2011-07-31 15:25:07'),(33,'reports','0003_delete_old','2011-07-31 15:25:07'),(34,'sales','0001_initial','2011-07-31 15:25:07'),(35,'sales','0002_auto__del_updaterecord__add_field_orderedproduct_tax__add_field_ordere','2011-07-31 15:25:07'),(36,'sales','0003_treeiocurrency','2011-07-31 15:25:07'),(42,'sales','0004_auto__chg_field_orderedproduct_quantity','2011-08-08 18:07:32'),(38,'services','0001_initial','2011-07-31 15:25:07'),(39,'services','0002_auto__add_field_ticketrecord_updaterecord_ptr','2011-07-31 15:25:07'),(40,'services','0003_updaterecords','2011-07-31 15:25:07'),(41,'services','0004_auto__del_field_ticketrecord_record_type__del_field_ticketrecord_detai','2011-07-31 15:25:07');
/*!40000 ALTER TABLE `south_migrationhistory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-10-20 17:52:24
