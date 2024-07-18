-- MySQL dump 10.13  Distrib 9.0.0, for Win64 (x86_64)
--
-- Host: localhost    Database: mysql_db
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
  `user_id` int DEFAULT NULL,
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goals`
--

LOCK TABLES `goals` WRITE;
/*!40000 ALTER TABLE `goals` DISABLE KEYS */;
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
  `user_id` int DEFAULT NULL,
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
INSERT INTO `interactions` VALUES ('00be9641-5363-4814-852d-28207b83869c','d263de95-9d5a-464b-a1fb-4d3e4d8ebcd3',1,'2024-07-07 15:31:57','tere','Tere! Kuidas ma saan teid aidata?','GPT3.5'),('09f0c49c-57ed-4a1e-81fe-a6e8328f2f81','99acfef9-e728-4edf-b92d-e8552d3c4646',1,'2024-07-07 11:10:42','veepiisa-efekt, mis see on? räägi lähemalt','Veepiisa-efekt on nähtus, kus vesi võib tunduda pinnalt peegeldunud objektist suurem või lähemal, kui see tegelikult on. See optiline illusioon tekib tänu valguse murdumisele ja peegeldumisele veepinnalt. Veepiisa-efekti võib kogeda eriti selgelt näiteks kalade vaatlemisel veekogus või ujudes basseinis, kus veepind suurendab või lähendab objekte veidi tavapärasest erinevalt.','GPT3.5'),('0f8a4d61-55c2-4860-b00e-d1fa05e39418','90b985c0-3f34-44f7-b481-e5af5977bb47',1,'2024-07-07 16:12:04','tere ja headaega','Tere! Kui sul tekib hiljem küsimusi või vajad abi, siis ära kõhkle mind uuesti külastamast. Head aega!','GPT3.5'),('23562d0d-cd40-42af-8b9d-73c7b7353a69','d263de95-9d5a-464b-a1fb-4d3e4d8ebcd3',1,'2024-07-07 15:32:19','tere jälle','Tere! Kuidas ma saaksin sind aidata?','GPT3.5'),('266009ed-3147-4864-bb12-34e7e0f6c00d','99acfef9-e728-4edf-b92d-e8552d3c4646',1,'2024-07-07 11:13:15','see tundub jah päris efektiivne. roosad põlvikud peaksid seda efekti ju tugevadama, vähemalt varem on nii  olnud, ja pljud uuringud näitavad seda','Kahjuks ma ei saa aru, millest te räägite. Kas saaksite palun selgitada või täpsustada, mida mõtlete? Siis saaksin teid paremini aidata.','GPT3.5'),('28909fb6-dec2-4f54-81e5-6a1c3be94f9b','23da3b40-e170-4850-b10f-0fb29929bf99',1,'2024-07-07 11:38:49','ohh, kahju. kas ma saan siis kutsuda oma päästja endale appi','Vabandust, ma ei saa teile füüsilist abi pakkuda. Kas saan teid muul moel abistada?','GPT3.5'),('3567513a-5dbc-4e59-9a8f-ce6b951cd0ab','4b587070-c84d-43a3-aeff-a2b5ebf53d5f',1,'2024-07-07 15:27:26','heiehei?','Hello! How can I assist you today?','GPT3.5'),('429d97b0-66b1-4d01-abd8-db2b89e45ae3','9c8232af-e40f-4fc5-b799-11cb1f99f1fb',1,'2024-07-07 15:30:43','tere','Tere! Kuidas saan sind aidata?','GPT3.5'),('4fdd714f-b3e6-446c-9d8e-e215a3ed5d6f','99acfef9-e728-4edf-b92d-e8552d3c4646',1,'2024-07-07 11:09:32','Tere päevast, on soe ja tuuline, aga mis teha????','Tere! Kui ilm on soe ja tuuline, võiksite mõelda välitingimustes tegevuste peale, näiteks piknikule minna, jalutama minna, jalgrattaga sõita või rannas aega veeta. Alternatiivselt võite külastada mõnda kohalikku parki või aiapidu. Oleneb, mis teile meeldib teha ja mis võimalused teie piirkonnas on. Kas ma saan teid veel kuidagi aidata?','GPT3.5'),('5247303c-0ee4-4908-b2ef-8fe2ac1ee1fa','6ce58447-17e8-4777-b1cd-a6da037d6245',1,'2024-07-07 15:01:10','kui loed küsimused kokku, ssis mis numbri sa saad?','Kui liidad kokku numbritena kirjutatud küsimused, saad tulemuseks summa, mis vastab küsimuste arvule. Näiteks, kui sul on 5 küsimust ja kirjutad need numbritena (1+2+3+4+5), siis summa on 15. Palun anna teada, kui sul on vaja veel mõnda abi või selgitust!','GPT3.5'),('5f164006-53cc-419e-bf4d-1c7eaccdb67e','6ce58447-17e8-4777-b1cd-a6da037d6245',1,'2024-07-07 15:01:50','aga kui ma liidan vastupdi nad kokku 5+4+3+2+1 siis see ju ei ole loogiline, oled nõus?','Jah, kui liidad arve vastupidises järjekorras, siis tulemus võib olla erinev. Näiteks kui liidad arve 5+4+3+2+1, siis summa oleks 15, mitte 5 nagu tavaliselt. See on seotud kommutatiivsuse omadusega matemaatikas, mis tähendab, et liitmine on tehtejuht, kus järjestus ei mõjuta tulemust.','GPT3.5'),('869274c0-c70d-41c8-8981-c105ee7fc94f','6ce58447-17e8-4777-b1cd-a6da037d6245',1,'2024-07-07 15:02:21','aga kas see on ka oogiline','Vabandan, kuid ma ei saa aru, mida te mõtlete sõnaga \"oogiline\". Kas saaksite selgitada või küsida küsimust teisiti?','GPT3.5'),('8e15a4be-0ca9-46c8-a964-37615c65d8eb','23da3b40-e170-4850-b10f-0fb29929bf99',1,'2024-07-07 11:38:10','häda ongi käes, mida nüüd teha?','Hädaolukorras tuleks esmalt püsida rahulik ja võtta aega olukorra hindamiseks. Kui vajad kiiret abi, helista hädaabinumbril 112. Anna operaatorile täpne informatsioon oma asukohast ja mida juhtunud on. Jää liikudes võimaluse korral kohapeale, et saaksid kiiresti abi saabuvatele päästjatele juhatada. Samuti hoiata teisi inimesi lähedalt ohust, kui see on võimalik.','GPT3.5'),('8e888c8f-f8c0-494e-84cf-9145d1080347','6ce58447-17e8-4777-b1cd-a6da037d6245',1,'2024-07-07 15:00:46','proovin - et mitmes see küsimus nüüd on siin reas','Vabandust, ma ei saa aru, mida täpselt soovite. Kas saaksite oma küsimust täpsustada? Kuidas saan teid aidata?','GPT3.5'),('9489b688-5f0e-4ae5-8c91-6da61a529d35','23da3b40-e170-4850-b10f-0fb29929bf99',1,'2024-07-07 11:38:28','kas ma saan kuskilt telefoni laenata?','Kahjuks ei ole mul võimalik otse telefoni laenamist pakkuda. Soovitan küsida sõpradelt või pereliikmetelt, kas nad saaksid sulle ajutiselt telefoni laenata. Samuti võid proovida pöörduda lähedal asuvasse elektroonikapoodi või mobiilioperaatori esindusse, et küsida, kas neil on saadaval telefoni laenutamise võimalus.','GPT3.5'),('9b79dfdd-67c2-4bf7-9200-fd700af22bf9','23da3b40-e170-4850-b10f-0fb29929bf99',1,'2024-07-07 11:39:01','aga kas sa saad ise pästja kutsuda?','Ma saan sind juhendada ja nõustada, kuid kui sa vajad kiiret abi või hädaolukorras abi, siis palun helista hädaabinumbrile 112 või vastava valdkonna õigetele abistajatele. Kuidas ma saan sind veel aidata?','GPT3.5'),('a9c9ef55-471e-48d3-a118-518a2a705e20','90b985c0-3f34-44f7-b481-e5af5977bb47',1,'2024-07-07 16:11:52','tere','Tere! Kuidas ma saan sind aidata?','GPT3.5'),('ac7f97a8-57c1-423e-9fbb-4643beaabbfe','23da3b40-e170-4850-b10f-0fb29929bf99',1,'2024-07-07 11:37:43','mida teha kui häda on käes?','Kui häda on käes, on oluline jääda rahulikuks ja keskendunuks selle lahendamisele. Siin on mõned üldised sammud, mida võiksid järgida:\n\n1. Hinnake olukorda: Mõelge hoolikalt, mis on probleemi aluseks ja millised võiksid olla võimalikud lahendused.\n\n2. Võtke meetmeid: Rakendage vajalikke samme probleemi lahendamiseks ning püüdke säilitada kontroll olukorra üle.\n\n3. Otsige abi: Kui vajate abi, pöörduge lähedaste, sõprade või spetsialistide poole, et saada vajalikku tuge ja juhiseid.\n\n4. Õppige olukorrast: Hindage, mida olete kogemusest õppinud, et tulevikus sarnaseid olukordi paremini käsitleda.\n\nMuidugi sõltub see, milline hädaolukord täpsemalt on. Kui soovite, et ma täpsemalt aitan mingi konkreetse olukorra lahendamisel, andke julgelt teada.','GPT3.5'),('ac959a12-9b70-4cb7-8fd4-c377dbed6f40','99acfef9-e728-4edf-b92d-e8552d3c4646',1,'2024-07-07 11:11:01','aga kuidas on see nüüd ujumisega seotuud','Ujumise teemal on mul väga hea meel sind aidata. Kas sul on mingisuguseid küsimusi või soovid midagi konkreetsemat teada saada ujumise kohta?','GPT3.5'),('b2a60e76-1667-49ae-9a06-d2ec0b935212','12ba2fea-a102-44d8-8a28-ef817266cb76',1,'2024-07-07 15:34:01','teretere','Hello! How can I assist you today?','GPT3.5'),('bace88bd-9f9a-48b1-bc80-bd0d9d4b0b79','6ce58447-17e8-4777-b1cd-a6da037d6245',1,'2024-07-07 15:00:28','tahtsin teada, mitmes küsimus see ongi','Vabandust, ma ei saanud teie küsimusest täpselt aru. Kas saaksite palun oma küsimust täpsustada?','GPT3.5'),('d37e4cb3-bafa-4144-bedd-7ed04b1d67a6','12ba2fea-a102-44d8-8a28-ef817266cb76',1,'2024-07-07 15:33:49','tere','Tere! Kuidas ma saan sind aidata?','GPT3.5'),('dccedab0-bc86-4792-9b8a-4105e80d2301','90b985c0-3f34-44f7-b481-e5af5977bb47',1,'2024-07-07 16:10:59','tere õhtust või päevast','Tere! Kuidas ma saaksin teid aidata?','GPT3.5'),('de7b7098-c672-4a3f-89b2-093e5a4ed0a7','12ba2fea-a102-44d8-8a28-ef817266cb76',1,'2024-07-07 15:34:14','tereteretere','Hello! How can I assist you today?','GPT3.5'),('e248d1e3-82a4-441b-8627-4679f63158c1','6ce58447-17e8-4777-b1cd-a6da037d6245',1,'2024-07-07 15:00:08','mitmes küsimus see ongi?','Tere! Mida sa täpsemalt küsida soovisid? Kuidas ma saaksin sind aidata?','GPT3.5'),('f45f4b0c-7053-4077-a36f-0b5ec40e5123','23da3b40-e170-4850-b10f-0fb29929bf99',1,'2024-07-07 11:39:15','olgu, ma pean siis ise helistama, jah?','Jah, te peate ise helistama. Kui vajate selles osas abi või juhiseid, siis andke teada, kuidas ma saaksin teid aidata.','GPT3.5'),('f4b09fb7-0967-46e0-8ee9-0b523ed3ba98','28bc6890-098a-4a93-82ae-db6d8a49c733',1,'2024-07-07 15:24:40','Tere, milline päev täan tuleb?','Tere! Millal soovite teada, milline päev täna on?','GPT3.5'),('f5d22973-0cfb-484e-adef-1236d24c5b0f','0808887a-beb9-466f-9025-933962c561f5',1,'2024-07-07 15:35:47','tere','Tere! Kuidas saan sind aidata?','GPT3.5'),('f682ea4e-fb97-4e5e-8477-b07f0d9f63c5','99acfef9-e728-4edf-b92d-e8552d3c4646',1,'2024-07-07 11:11:26','kuidas jha veepiisa-efekt aita ujumisel, räägi sellest','Veepiisa-efekt on tehniline ujumise liigutus, mis aitab parandada ujuja efektiivsust ja kiirust vees. See efekt tuleneb veepiiskade eemaldamisest ujumise ajal kätest ja kätevahelisest ruumist. Ujuja liigutab käsi vees nii, et vesi voolab siledalt ja kontrollitult kätest eemale ilma tilkumata. See loob veepiisa-efekti, mis aitab vähendada vee takistust ja suurendada ujuja edasiliikumise kiirust.\n\nVeepiisa-efekti saavutamiseks on oluline, et ujuja teeks käte liigutused ilma liigse jõuta ning hoiaks käsi siledad ja ühtlased vees. Hea kehatasakaal ja õige ujumisasend aitavad samuti veepiisa-efekti tugevdada. Regulaarne treening ja teadlik praktika aitavad ujujal veepiisa-efekti paremini mõista ja rakendada, mis omakorda võib parandada tema ujumise tõhusust ja kiirust.','GPT3.5'),('f8c00a95-a952-4f5e-b8e4-cad22fa563db','99acfef9-e728-4edf-b92d-e8552d3c4646',1,'2024-07-07 11:10:03','jah, nad võiksid minna ujuma ju, aga vettt pole läheduses','Kahjuks ma ei saa ise ujuma minna, kuid võin soovitada viisi, kuidas vee läheduses värskenduse saada. Võite proovida duši all ennast jahutada või niisama veepiisa-efekti tekitada, et tunneksid end värskelt ja jahutatult.','GPT3.5'),('fbd290f0-01ac-49c8-941c-b4bf86e8bed6','d263de95-9d5a-464b-a1fb-4d3e4d8ebcd3',1,'2024-07-07 15:32:34','ikka veel tere','Tere! Kuidas ma saaksin sind aidata?','GPT3.5');
/*!40000 ALTER TABLE `interactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_profile`
--

DROP TABLE IF EXISTS `user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_profile` (
  `user_id` int NOT NULL,
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
INSERT INTO `user_profile` VALUES (1,'testuser','Test User','testuser@example.com','2024-07-07 11:09:14','Other',30,'No',85,2),(2,'testuser','Test User','testuser@example.com','2024-07-07 11:36:47','Other',30,'No',85,2),(3,'testuser','Test User','testuser@example.com','2024-07-07 11:37:21','Other',30,'No',85,2),(4,'testuser','Test User','testuser@example.com','2024-07-07 14:59:43','Other',30,'No',85,2),(5,'testuser','Test User','testuser@example.com','2024-07-07 15:24:31','Other',30,'No',85,2),(6,'testuser','Test User','testuser@example.com','2024-07-07 15:27:12','Other',30,'No',85,2),(7,'testuser','Test User','testuser@example.com','2024-07-07 15:30:33','Other',30,'No',85,2),(8,'testuser','Test User','testuser@example.com','2024-07-07 15:31:51','Other',30,'No',85,2),(9,'testuser','Test User','testuser@example.com','2024-07-07 15:33:46','Other',30,'No',85,2),(10,'testuser','Test User','testuser@example.com','2024-07-07 15:35:36','Other',30,'No',85,2),(11,'testuser','Test User','testuser@example.com','2024-07-07 15:35:44','Other',30,'No',85,2),(12,'testuser','Test User','testuser@example.com','2024-07-07 16:10:37','Other',30,'No',85,2),(13,'testuser','Test User','testuser@example.com','2024-07-18 16:03:11','Other',30,'No',85,2);
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
  `user_id` int DEFAULT NULL,
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
INSERT INTO `user_sessions` VALUES ('0808887a-beb9-466f-9025-933962c561f5',1,'2024-07-07 15:35:48','2024-07-07 15:35:49','29408845-821b-4981-8175-46d75f655da9'),('12ba2fea-a102-44d8-8a28-ef817266cb76',1,'2024-07-07 15:34:15','2024-07-07 15:34:14','9824ba38-9941-4767-acce-e8380e7fe985'),('13febed7-cae4-435c-a945-711a559a6eeb',1,'2024-07-07 11:39:29','2024-07-07 11:39:29','39f8a283-9dee-48f3-b802-906acdb08ed4'),('23da3b40-e170-4850-b10f-0fb29929bf99',1,'2024-07-07 11:39:15','2024-07-07 11:39:15','44d37105-181d-4bfc-b544-b6db8afd09f2'),('28bc6890-098a-4a93-82ae-db6d8a49c733',1,'2024-07-07 15:24:41','2024-07-07 15:26:52','18004395-af33-42e4-8600-b21c59a26b16'),('4b587070-c84d-43a3-aeff-a2b5ebf53d5f',1,'2024-07-07 15:27:26','2024-07-07 15:27:31','ae15aa1e-8eed-44a9-8b15-518c1c463c10'),('6194c823-cdf0-4edc-a37a-11f95d40852a',1,'2024-07-07 15:02:32','2024-07-07 15:02:32','f0d49924-3250-41d0-ac03-db0e997a9b8a'),('6ce58447-17e8-4777-b1cd-a6da037d6245',1,'2024-07-07 15:02:22','2024-07-07 15:02:21','b3916f0d-dd0e-4d07-b847-925c36c9c7be'),('90b985c0-3f34-44f7-b481-e5af5977bb47',1,'2024-07-07 16:12:05','2024-07-07 16:12:04','0f59886b-4611-4a95-877c-a08f54ee7dc1'),('99acfef9-e728-4edf-b92d-e8552d3c4646',1,'2024-07-07 11:13:16',NULL,'85e299f0-dc23-46e7-a6de-894726952cb5'),('9c8232af-e40f-4fc5-b799-11cb1f99f1fb',1,'2024-07-07 15:30:43','2024-07-07 15:30:48','3863cdc6-66bf-4e5a-b8de-b07a781ce252'),('b7474a1c-465c-418f-89a5-b7dc9358d508',1,'2024-07-07 15:02:35','2024-07-07 15:02:35','9fb4471b-d8fc-443e-813c-d8fb6b271071'),('d17456dc-97bd-47e7-af55-444be3414305',1,'2024-07-07 11:39:23','2024-07-07 11:39:23','49a4a01d-10af-4802-9ee9-b75819a4b162'),('d263de95-9d5a-464b-a1fb-4d3e4d8ebcd3',1,'2024-07-07 15:32:34','2024-07-07 15:32:34','fbaa3bda-c593-440b-8794-b16e7c33e41c'),('f7deaae1-f0a9-445e-a65b-931585310f39',1,'2024-07-07 15:35:35','2024-07-07 15:35:36','b1c5e0bc-90b0-4c1c-a916-e8ed7039c45a');
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

-- Dump completed on 2024-07-18 19:03:11
