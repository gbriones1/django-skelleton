-- MariaDB dump 10.17  Distrib 10.4.6-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: modb
-- ------------------------------------------------------
-- Server version	10.4.6-MariaDB

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=169 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cache_table`
--

DROP TABLE IF EXISTS `cache_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cache_table` (
  `cache_key` varchar(255) NOT NULL,
  `value` longtext NOT NULL,
  `expires` datetime(6) NOT NULL,
  PRIMARY KEY (`cache_key`),
  KEY `cache_table_expires` (`expires`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_appliance`
--

DROP TABLE IF EXISTS `database_appliance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_appliance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_brand`
--

DROP TABLE IF EXISTS `database_brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_brand` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_collection`
--

DROP TABLE IF EXISTS `database_collection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_collection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `amount` decimal(9,2) NOT NULL,
  `sell_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `database_collection_sell_id_f2f7dacc_fk_database_sell_id` (`sell_id`),
  CONSTRAINT `database_collection_sell_id_f2f7dacc_fk_database_sell_id` FOREIGN KEY (`sell_id`) REFERENCES `database_sell` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_configuration`
--

DROP TABLE IF EXISTS `database_configuration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_configuration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_email` varchar(254) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL,
  `receiver_email` varchar(254) DEFAULT NULL,
  `mailOnPriceChange` tinyint(1) NOT NULL,
  `mailOnNegativeValues` tinyint(1) NOT NULL,
  `quotations_email` varchar(254) DEFAULT NULL,
  `quotations_password` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_customer`
--

DROP TABLE IF EXISTS `database_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_customer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `database_customer_name_51de86ce_uniq` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=983 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_customer_contact`
--

DROP TABLE IF EXISTS `database_customer_contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_customer_contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `for_quotation` tinyint(1) NOT NULL,
  `for_invoice` tinyint(1) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `database_customer_co_customer_id_b82d84e5_fk_database_` (`customer_id`),
  CONSTRAINT `database_customer_co_customer_id_b82d84e5_fk_database_` FOREIGN KEY (`customer_id`) REFERENCES `database_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_employee`
--

DROP TABLE IF EXISTS `database_employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_employee` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=277 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_employee_work`
--

DROP TABLE IF EXISTS `database_employee_work`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_employee_work` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `earning` decimal(9,2) NOT NULL,
  `employee_id` int(11) NOT NULL,
  `work_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `database_employee_work_work_id_employee_id_bdebc284_uniq` (`work_id`,`employee_id`),
  KEY `database_employee_wo_employee_id_9fada81d_fk_database_` (`employee_id`),
  CONSTRAINT `database_employee_wo_employee_id_9fada81d_fk_database_` FOREIGN KEY (`employee_id`) REFERENCES `database_employee` (`id`),
  CONSTRAINT `database_employee_work_work_id_40563437_fk_database_work_id` FOREIGN KEY (`work_id`) REFERENCES `database_work` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_input`
--

DROP TABLE IF EXISTS `database_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_input` (
  `invoice_id` int(11) DEFAULT NULL,
  `movement_ptr_id` int(11) NOT NULL,
  PRIMARY KEY (`movement_ptr_id`),
  KEY `database_input_invoice_id_08593029_fk_database_invoice_id` (`invoice_id`),
  CONSTRAINT `database_input_invoice_id_08593029_fk_database_invoice_id` FOREIGN KEY (`invoice_id`) REFERENCES `database_invoice` (`id`),
  CONSTRAINT `database_input_movement_ptr_id_115b3554_fk_database_movement_id` FOREIGN KEY (`movement_ptr_id`) REFERENCES `database_movement` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_invoice`
--

DROP TABLE IF EXISTS `database_invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_invoice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number` varchar(30) NOT NULL,
  `date` date NOT NULL,
  `due` date DEFAULT NULL,
  `price` decimal(9,2) NOT NULL,
  `credit` decimal(9,2) DEFAULT NULL,
  `discount` decimal(9,2) DEFAULT NULL,
  `paid` tinyint(1) NOT NULL,
  `provider_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `database_invoice_number_date_2c4d9900_uniq` (`number`,`date`),
  KEY `database_invoice_provider_id_b21afe00_fk_database_provider_id` (`provider_id`),
  CONSTRAINT `database_invoice_provider_id_b21afe00_fk_database_provider_id` FOREIGN KEY (`provider_id`) REFERENCES `database_provider` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8151 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_lending`
--

DROP TABLE IF EXISTS `database_lending`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_lending` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `employee_id` int(11) DEFAULT NULL,
  `returned` tinyint(1) NOT NULL,
  `returned_date` datetime(6) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `date` datetime(6) NOT NULL,
  `organization_storage_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `database_lending_employee_id_b5edaa0a` (`employee_id`),
  KEY `database_lending_customer_id_d484bc09_fk_database_customer_id` (`customer_id`),
  KEY `database_lending_organization_storage_e6d8893b_fk_database_` (`organization_storage_id`),
  CONSTRAINT `database_lending_customer_id_d484bc09_fk_database_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `database_customer` (`id`),
  CONSTRAINT `database_lending_employee_id_b5edaa0a_fk_database_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `database_employee` (`id`),
  CONSTRAINT `database_lending_organization_storage_e6d8893b_fk_database_` FOREIGN KEY (`organization_storage_id`) REFERENCES `database_organization_storage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_lending_product`
--

DROP TABLE IF EXISTS `database_lending_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_lending_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` int(11) NOT NULL,
  `returned_amount` int(11) NOT NULL,
  `lending_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `database_lending_pro_lending_id_29198a01_fk_database_` (`lending_id`),
  KEY `database_lending_pro_product_id_1dea9989_fk_database_` (`product_id`),
  CONSTRAINT `database_lending_pro_lending_id_29198a01_fk_database_` FOREIGN KEY (`lending_id`) REFERENCES `database_lending` (`id`),
  CONSTRAINT `database_lending_pro_product_id_1dea9989_fk_database_` FOREIGN KEY (`product_id`) REFERENCES `database_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_lending_tool`
--

DROP TABLE IF EXISTS `database_lending_tool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_lending_tool` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` int(11) NOT NULL,
  `returned_amount` int(11) NOT NULL,
  `lending_id` int(11) NOT NULL,
  `tool_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `database_lending_tool_lending_id_66644151_fk_database_lending_id` (`lending_id`),
  KEY `database_lending_tool_tool_id_63195d84_fk_database_tool_id` (`tool_id`),
  CONSTRAINT `database_lending_tool_lending_id_66644151_fk_database_lending_id` FOREIGN KEY (`lending_id`) REFERENCES `database_lending` (`id`),
  CONSTRAINT `database_lending_tool_tool_id_63195d84_fk_database_tool_id` FOREIGN KEY (`tool_id`) REFERENCES `database_tool` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_movement`
--

DROP TABLE IF EXISTS `database_movement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_movement` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime(6) NOT NULL,
  `organization_storage_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `database_movement_organization_storage_4b2dfa09_fk_database_` (`organization_storage_id`),
  CONSTRAINT `database_movement_organization_storage_4b2dfa09_fk_database_` FOREIGN KEY (`organization_storage_id`) REFERENCES `database_organization_storage` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30594 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_movement_product`
--

DROP TABLE IF EXISTS `database_movement_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_movement_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` int(11) NOT NULL,
  `price` decimal(9,2) NOT NULL,
  `movement_id` int(11) DEFAULT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `database_movement_pr_product_id_daa43a10_fk_database_` (`product_id`),
  KEY `database_movement_pr_movement_id_cac1721b_fk_database_` (`movement_id`),
  CONSTRAINT `database_movement_pr_movement_id_cac1721b_fk_database_` FOREIGN KEY (`movement_id`) REFERENCES `database_movement` (`id`),
  CONSTRAINT `database_movement_pr_product_id_daa43a10_fk_database_` FOREIGN KEY (`product_id`) REFERENCES `database_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=111318 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_order`
--

DROP TABLE IF EXISTS `database_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime(6) NOT NULL,
  `claimant_id` int(11) DEFAULT NULL,
  `provider_id` int(11) NOT NULL,
  `organization_storage_id` int(11) NOT NULL,
  `received_date` datetime(6) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  `replacer_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `database_order_provider_id_2102e8aa_fk_database_provider_id` (`provider_id`),
  KEY `database_order_claimant_id_2d941dc4` (`claimant_id`),
  KEY `database_order_organization_storage_c992742f_fk_database_` (`organization_storage_id`),
  KEY `database_order_e11d6795` (`replacer_id`),
  CONSTRAINT `database_order_claimant_id_2d941dc4_fk_database_employee_id` FOREIGN KEY (`claimant_id`) REFERENCES `database_employee` (`id`),
  CONSTRAINT `database_order_organization_storage_c992742f_fk_database_` FOREIGN KEY (`organization_storage_id`) REFERENCES `database_organization_storage` (`id`),
  CONSTRAINT `database_order_provider_id_2102e8aa_fk_database_provider_id` FOREIGN KEY (`provider_id`) REFERENCES `database_provider` (`id`),
  CONSTRAINT `database_order_replacer_id_c3563faf_fk_database_organization_id` FOREIGN KEY (`replacer_id`) REFERENCES `database_organization` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6377 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_order_product`
--

DROP TABLE IF EXISTS `database_order_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_order_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `product_id` int(11) NOT NULL,
  `amount_received` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `database_order_product_order_id_f15fa77a_fk_database_order_id` (`order_id`),
  KEY `database_order_produ_product_id_49f3319c_fk_database_` (`product_id`),
  CONSTRAINT `database_order_produ_product_id_49f3319c_fk_database_` FOREIGN KEY (`product_id`) REFERENCES `database_product` (`id`),
  CONSTRAINT `database_order_product_order_id_f15fa77a_fk_database_order_id` FOREIGN KEY (`order_id`) REFERENCES `database_order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34511 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_organization`
--

DROP TABLE IF EXISTS `database_organization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_organization` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_organization_storage`
--

DROP TABLE IF EXISTS `database_organization_storage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_organization_storage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `organization_id` int(11) NOT NULL,
  `storage_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `database_organizatio_organization_id_b3350820_fk_database_` (`organization_id`),
  KEY `database_organizatio_storage_type_id_320d4a73_fk_database_` (`storage_type_id`),
  CONSTRAINT `database_organizatio_organization_id_b3350820_fk_database_` FOREIGN KEY (`organization_id`) REFERENCES `database_organization` (`id`),
  CONSTRAINT `database_organizatio_storage_type_id_320d4a73_fk_database_` FOREIGN KEY (`storage_type_id`) REFERENCES `database_storagetype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_output`
--

DROP TABLE IF EXISTS `database_output`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_output` (
  `employee_id` int(11) DEFAULT NULL,
  `destination_id` int(11) DEFAULT NULL,
  `replacer_id` int(11) DEFAULT NULL,
  `movement_ptr_id` int(11) NOT NULL,
  PRIMARY KEY (`movement_ptr_id`),
  KEY `database_output_replacer_id_e7e2a2aa_fk_database_organization_id` (`replacer_id`),
  KEY `database_output_employee_id_07d382ef` (`employee_id`),
  KEY `database_output_destination_id_80dad6e9` (`destination_id`),
  CONSTRAINT `database_output_destination_id_80dad6e9_fk_database_customer_id` FOREIGN KEY (`destination_id`) REFERENCES `database_customer` (`id`),
  CONSTRAINT `database_output_employee_id_07d382ef_fk_database_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `database_employee` (`id`),
  CONSTRAINT `database_output_movement_ptr_id_e9a248b7_fk_database_movement_id` FOREIGN KEY (`movement_ptr_id`) REFERENCES `database_movement` (`id`),
  CONSTRAINT `database_output_replacer_id_e7e2a2aa_fk_database_organization_id` FOREIGN KEY (`replacer_id`) REFERENCES `database_organization` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_payment`
--

DROP TABLE IF EXISTS `database_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_payment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `amount` decimal(9,2) NOT NULL,
  `invoice_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `database_payment_invoice_id_cd6514fa_fk_database_invoice_id` (`invoice_id`),
  CONSTRAINT `database_payment_invoice_id_cd6514fa_fk_database_invoice_id` FOREIGN KEY (`invoice_id`) REFERENCES `database_invoice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_percentage`
--

DROP TABLE IF EXISTS `database_percentage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_percentage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `max_price_limit` decimal(9,2) NOT NULL,
  `sale_percentage_1` decimal(9,2) NOT NULL,
  `sale_percentage_2` decimal(9,2) NOT NULL,
  `sale_percentage_3` decimal(9,2) NOT NULL,
  `service_percentage_1` decimal(9,2) NOT NULL,
  `service_percentage_2` decimal(9,2) NOT NULL,
  `service_percentage_3` decimal(9,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_pricelist`
--

DROP TABLE IF EXISTS `database_pricelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_pricelist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customer_id` (`customer_id`),
  CONSTRAINT `database_pricelist_customer_id_f189b0b9_fk_database_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `database_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_pricelist_product`
--

DROP TABLE IF EXISTS `database_pricelist_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_pricelist_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alt_code` varchar(30) DEFAULT NULL,
  `price` decimal(9,2) NOT NULL,
  `pricelist_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `database_pricelist_p_pricelist_id_37031f45_fk_database_` (`pricelist_id`),
  KEY `database_pricelist_p_product_id_8392824b_fk_database_` (`product_id`),
  CONSTRAINT `database_pricelist_p_pricelist_id_37031f45_fk_database_` FOREIGN KEY (`pricelist_id`) REFERENCES `database_pricelist` (`id`),
  CONSTRAINT `database_pricelist_p_product_id_8392824b_fk_database_` FOREIGN KEY (`product_id`) REFERENCES `database_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_product`
--

DROP TABLE IF EXISTS `database_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(30) NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `price` decimal(9,2) NOT NULL,
  `discount` decimal(9,2) NOT NULL,
  `appliance_id` int(11) DEFAULT NULL,
  `brand_id` int(11) DEFAULT NULL,
  `provider_id` int(11) DEFAULT NULL,
  `picture` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `database_product_appliance_id_6fa4860b_fk_database_appliance_id` (`appliance_id`),
  KEY `database_product_brand_id_f22b830a_fk_database_brand_id` (`brand_id`),
  KEY `database_product_provider_id_3007d844_fk_database_provider_id` (`provider_id`),
  CONSTRAINT `database_product_appliance_id_6fa4860b_fk_database_appliance_id` FOREIGN KEY (`appliance_id`) REFERENCES `database_appliance` (`id`),
  CONSTRAINT `database_product_brand_id_f22b830a_fk_database_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `database_brand` (`id`),
  CONSTRAINT `database_product_provider_id_3007d844_fk_database_provider_id` FOREIGN KEY (`provider_id`) REFERENCES `database_provider` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1805 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_provider`
--

DROP TABLE IF EXISTS `database_provider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_provider` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `database_provider_name_091c51b5_uniq` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_provider_contact`
--

DROP TABLE IF EXISTS `database_provider_contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_provider_contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `for_orders` tinyint(1) NOT NULL,
  `provider_id` int(11) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `database_provider_co_provider_id_a253b3a8_fk_database_` (`provider_id`),
  CONSTRAINT `database_provider_co_provider_id_a253b3a8_fk_database_` FOREIGN KEY (`provider_id`) REFERENCES `database_provider` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_quotation`
--

DROP TABLE IF EXISTS `database_quotation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_quotation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `authorized` tinyint(1) NOT NULL,
  `service` decimal(9,2) NOT NULL,
  `discount` decimal(9,2) NOT NULL,
  `date` datetime(6) NOT NULL,
  `plates` varchar(30) DEFAULT NULL,
  `unit` varchar(30) DEFAULT NULL,
  `pricelist_id` int(11) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `work_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `database_quotation_pricelist_id_88187099_fk_database_` (`pricelist_id`),
  KEY `database_quotation_customer_id_d5204f87_fk_database_customer_id` (`customer_id`),
  KEY `database_quotation_work_id_08ade9ba_fk_database_work_id` (`work_id`),
  CONSTRAINT `database_quotation_customer_id_d5204f87_fk_database_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `database_customer` (`id`),
  CONSTRAINT `database_quotation_pricelist_id_88187099_fk_database_` FOREIGN KEY (`pricelist_id`) REFERENCES `database_pricelist` (`id`),
  CONSTRAINT `database_quotation_work_id_08ade9ba_fk_database_work_id` FOREIGN KEY (`work_id`) REFERENCES `database_work` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_quotation_others`
--

DROP TABLE IF EXISTS `database_quotation_others`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_quotation_others` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(60) NOT NULL,
  `amount` int(11) NOT NULL,
  `price` decimal(9,2) NOT NULL,
  `quotation_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `database_quotation_o_quotation_id_a523942e_fk_database_` (`quotation_id`),
  CONSTRAINT `database_quotation_o_quotation_id_a523942e_fk_database_` FOREIGN KEY (`quotation_id`) REFERENCES `database_quotation` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_quotation_product`
--

DROP TABLE IF EXISTS `database_quotation_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_quotation_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` int(11) NOT NULL,
  `price` decimal(9,2) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quotation_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `database_quotation_p_product_id_e7ffe3f2_fk_database_` (`product_id`),
  KEY `database_quotation_p_quotation_id_8d435181_fk_database_` (`quotation_id`),
  CONSTRAINT `database_quotation_p_product_id_e7ffe3f2_fk_database_` FOREIGN KEY (`product_id`) REFERENCES `database_product` (`id`),
  CONSTRAINT `database_quotation_p_quotation_id_8d435181_fk_database_` FOREIGN KEY (`quotation_id`) REFERENCES `database_quotation` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_sell`
--

DROP TABLE IF EXISTS `database_sell`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_sell` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number` varchar(30) NOT NULL,
  `date` date NOT NULL,
  `due` date DEFAULT NULL,
  `price` decimal(9,2) NOT NULL,
  `credit` decimal(9,2) DEFAULT NULL,
  `discount` decimal(9,2) DEFAULT NULL,
  `paid` tinyint(1) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `database_sell_number_date_7a9a3f19_uniq` (`number`,`date`),
  KEY `database_sell_customer_id_84538a27_fk_database_customer_id` (`customer_id`),
  CONSTRAINT `database_sell_customer_id_84538a27_fk_database_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `database_customer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_storage_product`
--

DROP TABLE IF EXISTS `database_storage_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_storage_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` int(11) NOT NULL,
  `organization_storage_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `must_have` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `database_storage_pro_organization_storage_0545b0de_fk_database_` (`organization_storage_id`),
  KEY `database_storage_pro_product_id_cfbcd9d8_fk_database_` (`product_id`),
  CONSTRAINT `database_storage_pro_organization_storage_0545b0de_fk_database_` FOREIGN KEY (`organization_storage_id`) REFERENCES `database_organization_storage` (`id`),
  CONSTRAINT `database_storage_pro_product_id_cfbcd9d8_fk_database_` FOREIGN KEY (`product_id`) REFERENCES `database_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5148 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_storage_tool`
--

DROP TABLE IF EXISTS `database_storage_tool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_storage_tool` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` int(11) NOT NULL,
  `organization_storage_id` int(11) NOT NULL,
  `tool_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `database_storage_too_organization_storage_0ccd4a9b_fk_database_` (`organization_storage_id`),
  KEY `database_storage_tool_tool_id_33715d14_fk_database_tool_id` (`tool_id`),
  CONSTRAINT `database_storage_too_organization_storage_0ccd4a9b_fk_database_` FOREIGN KEY (`organization_storage_id`) REFERENCES `database_organization_storage` (`id`),
  CONSTRAINT `database_storage_tool_tool_id_33715d14_fk_database_tool_id` FOREIGN KEY (`tool_id`) REFERENCES `database_tool` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_storagetype`
--

DROP TABLE IF EXISTS `database_storagetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_storagetype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_tool`
--

DROP TABLE IF EXISTS `database_tool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_tool` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(30) NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `condition` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `database_work`
--

DROP TABLE IF EXISTS `database_work`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `database_work` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `end_time` time(6) DEFAULT NULL,
  `start_time` time(6) DEFAULT NULL,
  `unit_section` varchar(30) DEFAULT NULL,
  `number` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `number` (`number`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-01-29  9:25:33
