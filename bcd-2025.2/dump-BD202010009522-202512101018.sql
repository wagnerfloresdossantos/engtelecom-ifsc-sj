/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.13-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: bd.sj.ifsc.edu.br    Database: BD202010009522
-- ------------------------------------------------------
-- Server version	10.5.22-MariaDB

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
-- Table structure for table `Aluno`
--

DROP TABLE IF EXISTS `Aluno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Aluno` (
  `matricula` varchar(12) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `dataInicio` varchar(100) NOT NULL,
  PRIMARY KEY (`matricula`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Aluno`
--

LOCK TABLES `Aluno` WRITE;
/*!40000 ALTER TABLE `Aluno` DISABLE KEYS */;
INSERT INTO `Aluno` VALUES
('202010002403','IGOR BUDAG DE OLIVEIRA','CURSANDO','2020.1'),
('202010009522','WAGNER FLORES DOS SANTOS\n\n','CURSANDO','2020.1'),
('202020901307','LUCAS COSTA FONTES','CURSANDO','2021.1'),
('202020901580','JAMILLY DA SILVA PINHEIRO','CURSANDO','2022.1'),
('202110811052','BEATRIZ PAPST DE ABREU','CURSANDO','2022.2'),
('202210503217','BEATRIZ PAZ FARIA','CURSANDO','2023.1'),
('202210508199','JÚLIA ESPÍNDOLA STEINBACH','CURSANDO','2022.2');
/*!40000 ALTER TABLE `Aluno` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Aluno_Disciplina`
--

DROP TABLE IF EXISTS `Aluno_Disciplina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Aluno_Disciplina` (
  `nota` int(11) NOT NULL,
  `matricula` varchar(12) NOT NULL,
  `codDisciplina` varchar(10) NOT NULL,
  `ano` varchar(10) NOT NULL,
  `semestre` varchar(6) NOT NULL,
  PRIMARY KEY (`matricula`,`codDisciplina`,`semestre`,`ano`),
  KEY `Aluno_Disciplina_Disciplina_FK` (`codDisciplina`),
  CONSTRAINT `Aluno_Disciplina_Aluno_FK` FOREIGN KEY (`matricula`) REFERENCES `Aluno` (`matricula`),
  CONSTRAINT `Aluno_Disciplina_Disciplina_FK` FOREIGN KEY (`codDisciplina`) REFERENCES `Disciplina` (`codDisciplina`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Aluno_Disciplina`
--

LOCK TABLES `Aluno_Disciplina` WRITE;
/*!40000 ALTER TABLE `Aluno_Disciplina` DISABLE KEYS */;
INSERT INTO `Aluno_Disciplina` VALUES
(10,'202010002403','BCD029008','2025','2'),
(9,'202010002403','COM029008','2025','2'),
(10,'202010009522','BCD029008','2025','2'),
(5,'202010009522','COM029008','2025','2'),
(6,'202010009522','PJI129006','2025','2'),
(9,'202010009522','STD129006','2025','2'),
(5,'202020901307','BCD029008','2025','2'),
(10,'202020901580','COM029008','2025','2'),
(9,'202210503217','STD129006','2025','2');
/*!40000 ALTER TABLE `Aluno_Disciplina` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Curso`
--

DROP TABLE IF EXISTS `Curso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Curso` (
  `codCurso` varchar(10) NOT NULL,
  `descricao` varchar(100) NOT NULL,
  `credMin` int(10) unsigned NOT NULL,
  `nome` varchar(100) NOT NULL,
  PRIMARY KEY (`codCurso`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Curso`
--

LOCK TABLES `Curso` WRITE;
/*!40000 ALTER TABLE `Curso` DISABLE KEYS */;
INSERT INTO `Curso` VALUES
('290','BACHARELADO',3996,'ENGENHARIA DE TELECOMUNICAÇÕES'),
('7862','TECNOLÓGICO',2000,'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS');
/*!40000 ALTER TABLE `Curso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Curso_Disciplina`
--

DROP TABLE IF EXISTS `Curso_Disciplina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Curso_Disciplina` (
  `codCurso` varchar(10) NOT NULL,
  `codDisciplina` varchar(10) NOT NULL,
  `anoSemestre` varchar(10) NOT NULL,
  PRIMARY KEY (`codCurso`,`codDisciplina`,`anoSemestre`),
  KEY `Curso_Disciplina_Disciplina_FK` (`codDisciplina`),
  CONSTRAINT `Curso_Disciplina_Curso_FK` FOREIGN KEY (`codCurso`) REFERENCES `Curso` (`codCurso`),
  CONSTRAINT `Curso_Disciplina_Disciplina_FK` FOREIGN KEY (`codDisciplina`) REFERENCES `Disciplina` (`codDisciplina`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Curso_Disciplina`
--

LOCK TABLES `Curso_Disciplina` WRITE;
/*!40000 ALTER TABLE `Curso_Disciplina` DISABLE KEYS */;
INSERT INTO `Curso_Disciplina` VALUES
('290','BCD029008','2025'),
('290','COM029008','2025'),
('290','PJI129006','2025'),
('290','STD129006','2025'),
('7862','BCD029008','2025');
/*!40000 ALTER TABLE `Curso_Disciplina` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Disciplina`
--

DROP TABLE IF EXISTS `Disciplina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Disciplina` (
  `nome` varchar(100) NOT NULL,
  `codDisciplina` varchar(10) NOT NULL,
  `credFixos` int(10) unsigned NOT NULL,
  `descricao` varchar(50) NOT NULL,
  PRIMARY KEY (`codDisciplina`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Disciplina`
--

LOCK TABLES `Disciplina` WRITE;
/*!40000 ALTER TABLE `Disciplina` DISABLE KEYS */;
INSERT INTO `Disciplina` VALUES
('BANCOS DE DADOS','BCD029008',3,'BCD029008 - BANCOS DE DADOS'),
('SISTEMAS DE COMUNICAÇÃO II','COM029008',4,'COM029008 - SISTEMAS DE COMUNICAÇÃO II\n'),
('PROJETO INTEGRADOR II','PJI129006',4,'PJI129006 - PROJETO INTEGRADOR II'),
('SISTEMAS DISTRIBUÍDOS','STD129006',4,'STD129006 - SISTEMAS DISTRIBUÍDOS');
/*!40000 ALTER TABLE `Disciplina` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Disciplina_Professor`
--

DROP TABLE IF EXISTS `Disciplina_Professor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Disciplina_Professor` (
  `codDisciplina` varchar(10) NOT NULL,
  `codProfessor` int(10) unsigned NOT NULL,
  `ano` int(10) unsigned NOT NULL,
  `semetre` int(10) unsigned NOT NULL,
  PRIMARY KEY (`ano`,`semetre`,`codDisciplina`,`codProfessor`),
  KEY `Disciplina_Professor_Disciplina_FK` (`codDisciplina`),
  KEY `Disciplina_Professor_Professor_FK` (`codProfessor`),
  CONSTRAINT `Disciplina_Professor_Disciplina_FK` FOREIGN KEY (`codDisciplina`) REFERENCES `Disciplina` (`codDisciplina`),
  CONSTRAINT `Disciplina_Professor_Professor_FK` FOREIGN KEY (`codProfessor`) REFERENCES `Professor` (`codProfessor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Disciplina_Professor`
--

LOCK TABLES `Disciplina_Professor` WRITE;
/*!40000 ALTER TABLE `Disciplina_Professor` DISABLE KEYS */;
INSERT INTO `Disciplina_Professor` VALUES
('BCD029008',1,2025,2),
('BCD029008',2,2025,2),
('COM029008',4,2025,2),
('COM029008',5,2025,2),
('PJI129006',3,2025,2),
('STD129006',6,2025,2);
/*!40000 ALTER TABLE `Disciplina_Professor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Professor`
--

DROP TABLE IF EXISTS `Professor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Professor` (
  `nome` varchar(100) NOT NULL,
  `codProfessor` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`codProfessor`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Professor`
--

LOCK TABLES `Professor` WRITE;
/*!40000 ALTER TABLE `Professor` DISABLE KEYS */;
INSERT INTO `Professor` VALUES
('RAMON HUGO DE SOUZA',1),
('ANA LUIZA SCHARF',2),
('ADILSON JAIR CARDOSO',3),
('MARCIO HENRIQUE DONIAK',4),
('ROBERTO WANDERLEY DA NOBREGA',5),
('EMERSON RIBEIRO DE MELLO',6);
/*!40000 ALTER TABLE `Professor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'BD202010009522'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-10 10:18:20
