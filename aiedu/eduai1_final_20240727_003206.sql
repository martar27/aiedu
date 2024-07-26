-- MySQL dump 10.13  Distrib 9.0.0, for Win64 (x86_64)
--
-- Host: localhost    Database: eduai1
-- ------------------------------------------------------
-- Server version	9.0.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `goals`
--

DROP TABLE IF EXISTS `goals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) DEFAULT NULL,
  `session_id` varchar(36) DEFAULT NULL,
  `content` text,
  `version` int DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  `feedback` text,
  `is_comprehensible` tinyint(1) DEFAULT NULL,
  `is_valid` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `goals_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_profile` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goals`
--

LOCK TABLES `goals` WRITE;
/*!40000 ALTER TABLE `goals` DISABLE KEYS */;
INSERT INTO `goals` VALUES (2,'kasutaja1','6ea00ce0-93f9-4a30-b3c1-c507954eb099','tahaks midagi head teha',1,'2024-07-26 21:17:13','Kas see eesmärk on sinu jaoks saavutatav seitsme nädala jooksul? Kas sa usud, et sul õnnestub see eesmärk saavutada? Kas selle eesmärgi saavutamine teeb sulle heameelt? Ära lase end heidutada, kui esimene vastus ei tundu lihtne! Oluline on uskuda endasse ja oma võimetesse. Ole järjepidev ja usalda iseennast. Aita mul mõista, mida sa silmas pead, kui soovid midagi head teha - kas sa oled mõelnud mõnele konkreetsel viisil teistele abistamisele või midagi muud?',0,0),(3,'kasutaja1','6ea00ce0-93f9-4a30-b3c1-c507954eb099','ma tahaks koolis midagi head teha, õpetaja jaoks või klassikaaslaste jaoks',2,'2024-07-26 21:17:47','Kas see eesmärk on saavutatav, et teha midagi head koolis õpetaja või klassikaaslaste jaoks seitsme nädala jooksul? Kas sa usud, et sul õnnestub see saavutada ning kas selle eesmärgi saavutamine teeks sulle rõõmu? Kui jah, siis võiksid mõelda sellele, mida sa saaksid teha, et aidata teisi või toetada oma õpetajat. Ole avatud uutele võimalustele ja mõtle, kuidas saaksid oma kooli ümbritsevat keskkonda paremaks muuta või kedagi aidata. Ole julge ja loov ning naudi seda positiivset mõju, mida saad teistele luua!',0,0),(4,'kasutaja1','6ea00ce0-93f9-4a30-b3c1-c507954eb099','ma tahn õpetajat aidata',3,'2024-07-26 21:18:42','Kas see eesmärk on saavutatav seitsme nädala jooksul? Kas sul on olemas vajalikud oskused ja võimalused õpetajat aidata?\n\nKas sa usud, et sa suudad selle eesmärgi saavutada seitsme nädalaga? Kas sul on piisav motivatsioon ja tahe õpetajat aidata?\n\nKas selle eesmärgi saavutamine teeb sulle heameelt? Kas sa tunned rõõmu ja rahulolu, kui sa õpetajat aidates midagi head saavutad?\n\nMõtle nende küsimuste üle ja tea, et on täiesti mõistlik aidata õpetajat, kui see teeb sulle rõõmu ja kui sul on vajalikud oskused selleks olemas. Aita endale selgeks teha, miks see eesmärk on sulle oluline ja kuidas sa saaksid selle saavutamiseks panustada.',0,0),(5,'kasutaja1','6ea00ce0-93f9-4a30-b3c1-c507954eb099','ma tahan õpetajal õpetada aidata',4,'2024-07-26 21:19:14','Kas see eesmärk on saavutatav seitsme nädala jooksul?\n\nKas sa usud, et sa suudad eesmärgi saavutada seitsme nädalaga?\n\nKas see eesmärk tekitab sulle rõõmu või heameelt?\n\nJulgustan sind mõtlema sellele, kuidas õpetajale õpetada, kuidas saaksid teda aidata. Kas sa tead, millist tuge või abi sul vaja võiks minna, et seda eesmärki saavutada? Ole avatud suhtlemisel ja püüa leida võimalusi, kuidas saaksid õpetajat aidata õpetamisel. Ära karda küsida õpetajalt nõu või toetust selle eesmärgi saavutamiseks. Sinu algatus ja visadus võivad sind lähemale viia oma eesmärgi täitmisele.',1,0);
/*!40000 ALTER TABLE `goals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interactions`
--

DROP TABLE IF EXISTS `interactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interactions` (
  `interaction_id` varchar(36) NOT NULL,
  `session_id` varchar(36) DEFAULT NULL,
  `user_id` varchar(50) DEFAULT NULL,
  `interaction_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `interaction_text` text,
  `llm_response` text,
  `llm_model_spec` text,
  PRIMARY KEY (`interaction_id`),
  KEY `session_id` (`session_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `interactions_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `user_sessions` (`session_id`),
  CONSTRAINT `interactions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user_profile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interactions`
--

LOCK TABLES `interactions` WRITE;
/*!40000 ALTER TABLE `interactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `interactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profile`
--

DROP TABLE IF EXISTS `user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_profile` (
  `user_id` varchar(50) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `creation_date` timestamp NULL DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `same_school` varchar(50) DEFAULT NULL,
  `grades` int DEFAULT NULL,
  `user_type_id` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `user_type_id` (`user_type_id`),
  CONSTRAINT `user_profile_ibfk_1` FOREIGN KEY (`user_type_id`) REFERENCES `user_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_profile`
--

LOCK TABLES `user_profile` WRITE;
/*!40000 ALTER TABLE `user_profile` DISABLE KEYS */;
INSERT INTO `user_profile` VALUES ('kasutaja1','testuser','Test User','testuser@example.com','2024-07-26 21:17:08','Other',30,'No',85,2);
/*!40000 ALTER TABLE `user_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_sessions`
--

DROP TABLE IF EXISTS `user_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_sessions` (
  `session_id` varchar(36) NOT NULL,
  `user_id` varchar(50) DEFAULT NULL,
  `start_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `end_time` timestamp NULL DEFAULT NULL,
  `session_token` text,
  PRIMARY KEY (`session_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_profile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_sessions`
--

LOCK TABLES `user_sessions` WRITE;
/*!40000 ALTER TABLE `user_sessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_type`
--

DROP TABLE IF EXISTS `user_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_type` (
  `id` int NOT NULL,
  `user_type` varchar(50) NOT NULL,
  `text` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_type` (`user_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_type`
--

LOCK TABLES `user_type` WRITE;
/*!40000 ALTER TABLE `user_type` DISABLE KEYS */;
INSERT INTO `user_type` VALUES (1,'pupil_1','A pupil who only has retrieval access to the database.'),(2,'pupil_2','A pupil who has read/write access to the database.'),(3,'student','A student who has read/write access to the database.'),(4,'teacher','A user who can create educational content.'),(5,'admin','The G-word goes here');
/*!40000 ALTER TABLE `user_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-27  0:32:06
