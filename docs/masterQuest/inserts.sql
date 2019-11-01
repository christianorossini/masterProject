-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: localhost    Database: masterquestdb
-- ------------------------------------------------------
-- Server version	5.7.27-0ubuntu0.18.04.1

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
INSERT INTO `ms_dtModel` VALUES (4,'gc.png','sdfsdf','safdsf');
/*!40000 ALTER TABLE `ms_dtModel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ms_dtModel_tasks`
--

LOCK TABLES `ms_dtModel_tasks` WRITE;
/*!40000 ALTER TABLE `ms_dtModel_tasks` DISABLE KEYS */;
INSERT INTO `ms_dtModel_tasks` VALUES (1,4,'1');
/*!40000 ALTER TABLE `ms_dtModel_tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ms_question`
--

LOCK TABLES `ms_question` WRITE;
/*!40000 ALTER TABLE `ms_question` DISABLE KEYS */;
INSERT INTO `ms_question` VALUES (5,'How does the model classify the folowing observation?',1),(6,'What is the code smell classification?',2),(7,'How difficult was the task?',3);
/*!40000 ALTER TABLE `ms_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ms_task`
--

LOCK TABLES `ms_task` WRITE;
/*!40000 ALTER TABLE `ms_task` DISABLE KEYS */;
INSERT INTO `ms_task` VALUES ('1','Classify','CL');
/*!40000 ALTER TABLE `ms_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ms_task_questions`
--

LOCK TABLES `ms_task_questions` WRITE;
/*!40000 ALTER TABLE `ms_task_questions` DISABLE KEYS */;
INSERT INTO `ms_task_questions` VALUES (3,'1',5),(4,'1',6),(5,'1',7);
/*!40000 ALTER TABLE `ms_task_questions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-10-28 10:24:06
