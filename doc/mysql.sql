CREATE DATABASE  IF NOT EXISTS `stock_data` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `stock_data`;
-- MySQL dump 10.13  Distrib 5.7.9, for Win32 (AMD64)
--
-- Host: localhost    Database: stock_data
-- ------------------------------------------------------
-- Server version	5.5.54-0ubuntu0.14.04.1

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
-- Table structure for table `index_day_historical_data`
--

DROP TABLE IF EXISTS `index_day_historical_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `index_day_historical_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(45) NOT NULL COMMENT '指数类型,暂时用代码表示。如： 000001, 399001',
  `date` date NOT NULL COMMENT '日期 如：1990/12/19',
  `week` varchar(45) DEFAULT NULL COMMENT '存中文，或者其他支付。随意存',
  `high` decimal(12,2) DEFAULT NULL COMMENT '最高价',
  `low` decimal(12,2) DEFAULT NULL COMMENT '最低价',
  `market_close` decimal(12,2) DEFAULT NULL COMMENT '收盘',
  `change_index_point` decimal(8,2) DEFAULT NULL COMMENT '涨跌..涨跌点数',
  `change_index_percentage` decimal(8,2) DEFAULT NULL COMMENT '涨幅,幅度百分比',
  `amplitude` decimal(8,2) DEFAULT NULL COMMENT '振幅%...',
  `volume` bigint(62) DEFAULT NULL COMMENT '成交量(手) 单位 万\n',
  `amount` bigint(62) DEFAULT NULL COMMENT '成交金额',
  `total_value` bigint(62) NOT NULL COMMENT '总市值,市价总值',
  `backup` text COMMENT '备份每条下载的数据，留着以后用。。具体数据结构看文档。。。',
  `update_time` int(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `type_date` (`type`,`date`)
) ENGINE=MyISAM AUTO_INCREMENT=12729 DEFAULT CHARSET=utf8 COMMENT='股市各种指数的历史数据..一天一条';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'stock_data'
--

--
-- Dumping routines for database 'stock_data'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-02-04 15:51:27
