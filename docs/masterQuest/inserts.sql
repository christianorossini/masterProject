-- MySQL dump 10.13  Distrib 5.7.28, for Linux (x86_64)
--
-- Host: localhost    Database: masterquestdb
-- ------------------------------------------------------
-- Server version	5.7.28-0ubuntu0.18.04.4

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
-- Dumping data for table `ms_dtModel`
--

LOCK TABLES `ms_dtModel` WRITE;
/*!40000 ALTER TABLE `ms_dtModel` DISABLE KEYS */;
INSERT INTO `ms_dtModel` VALUES (1,'dt1.png',4,4,'CountLineCode,CountDeclMethodPublic'),(2,'dt2.png',3,2,''),(3,'dt3.png',4,3,''),(4,'dt4.png',4,3,''),(5,'dt5.png',3,3,''),(6,'dt6.png',6,6,'');
/*!40000 ALTER TABLE `ms_dtModel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ms_task`
--

LOCK TABLES `ms_task` WRITE;
/*!40000 ALTER TABLE `ms_task` DISABLE KEYS */;
INSERT INTO `ms_task` VALUES (3,'C','gc','asdfds','Public Class','cassandra','org.apache.tools.ant.DirectoryScanner',1,1),(4,'M','lm','asdsad','Public Method','nutch','org.apache.cassandra.metrics.ClientRequestMetrics',1,2),(5,'C','cdsbp','sfdsdf','Private Method','ant','org.apache.tools.ant.Project',2,3),(6,'M','lm','sfd','Public Method','nutch','org.apache.cassandra.service.StorageService',2,4),(7,'C','lm','asfdsdfdsf','Public Method','cassandra','org.apache.cassandra.service.StorageService',1,5),(8,'C','gc','sdfasdf','Public Method','nutch','org.apache.tools.ant.DirectoryScanner',2,6);
/*!40000 ALTER TABLE `ms_task` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-09 11:27:47
