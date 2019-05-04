/*
 Navicat Premium Data Transfer

 Source Server         : passowrd-chenkangliu
 Source Server Type    : MySQL
 Source Server Version : 80011
 Source Host           : localhost:3306
 Source Schema         : shares

 Target Server Type    : MySQL
 Target Server Version : 80011
 File Encoding         : 65001

 Date: 04/05/2019 12:09:15
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for shares_trades
-- ----------------------------
DROP TABLE IF EXISTS `shares_trades`;
CREATE TABLE `shares_trades`  (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `shares_code` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '编码',
  `shares_name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `data_date` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '日期',
  `start_price` decimal(20, 2) NULL DEFAULT NULL COMMENT '开盘价',
  `top_price` decimal(20, 2) NULL DEFAULT NULL COMMENT '最高价',
  `low_price` decimal(20, 2) NULL DEFAULT NULL COMMENT '最低价',
  `end_price` decimal(20, 2) NULL DEFAULT NULL COMMENT '收盘价',
  `range_amount` decimal(20, 2) NULL DEFAULT NULL COMMENT '涨跌额',
  `range_percent` decimal(10, 3) NULL DEFAULT NULL COMMENT '涨跌幅',
  `volume_number` int(20) NULL DEFAULT NULL COMMENT '成交量（手）',
  `volume_amount` int(20) NULL DEFAULT NULL COMMENT '成交额（万元）',
  `amplitude_percent` decimal(10, 3) NULL DEFAULT NULL COMMENT '振幅(%)',
  `switch_percent` decimal(10, 3) NULL DEFAULT NULL COMMENT '换手率(%)',
  `create_time` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0),
  `update_time` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uix_date_code`(`data_date`, `shares_code`) USING BTREE,
  INDEX `idx_trades_code`(`shares_code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
