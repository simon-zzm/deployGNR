/*
Navicat MySQL Data Transfer

Source Server         : 192.168.1.113-root
Source Server Version : 50623
Source Host           : 192.168.1.113:3306
Source Database       : deployGNR

Target Server Type    : MYSQL
Target Server Version : 50623
File Encoding         : 65001

Date: 2018-04-01 09:09:39
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `d_column`
-- ----------------------------
DROP TABLE IF EXISTS `d_column`;
CREATE TABLE `d_column` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `code` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `sort_no` int(11) DEFAULT NULL,
  `tree_path` varchar(300) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `i_parent_id` (`parent_id`),
  KEY `i_sort_no` (`sort_no`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of d_column
-- ----------------------------
INSERT INTO `d_column` VALUES ('1', '部署管理', 'deployMan', '0', '1', null);
INSERT INTO `d_column` VALUES ('2', '部署上线', 'deployOnline', '1', '1', null);
INSERT INTO `d_column` VALUES ('3', 'git管理', 'gitManage', '0', '1', null);
INSERT INTO `d_column` VALUES ('4', 'git项目管理', 'gitProjectMan', '3', '1', null);
INSERT INTO `d_column` VALUES ('5', 'git用户管理', 'gitUserMan', '3', '2', null);
INSERT INTO `d_column` VALUES ('6', 'git权限管理', 'gitAuthMan', '3', '3', null);
INSERT INTO `d_column` VALUES ('7', '系统管理', 'sysMan', '0', '1', null);
INSERT INTO `d_column` VALUES ('8', '用户管理', 'userMan', '7', '1', null);
INSERT INTO `d_column` VALUES ('10', '用户组管理', 'groupMan', '7', '2', null);
INSERT INTO `d_column` VALUES ('11', '用户信息', 'userSelf', '7', '4', null);
INSERT INTO `d_column` VALUES ('12', '修改个人密码', 'userEditPass', '7', '5', null);
INSERT INTO `d_column` VALUES ('13', 'git本地服务', 'gitLocalCon', '3', '4', null);
INSERT INTO `d_column` VALUES ('14', '部署权限', 'deployAuth', '1', '3', null);
INSERT INTO `d_column` VALUES ('15', '部署配置', 'deployConfig', '1', '4', null);
INSERT INTO `d_column` VALUES ('16', '部署日志', 'deployLog', '1', '2', null);

-- ----------------------------
-- Table structure for `d_deploy_history`
-- ----------------------------
DROP TABLE IF EXISTS `d_deploy_history`;
CREATE TABLE `d_deploy_history` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `projectId` int(50) DEFAULT NULL,
  `strTime` varchar(15) DEFAULT NULL,
  `userId` int(1) DEFAULT NULL,
  `gitSrcId` varchar(128) DEFAULT NULL,
  `gitConfId` varchar(128) DEFAULT 'new' COMMENT 'new为默认使用最新库',
  `gitBanrch` varchar(100) DEFAULT NULL,
  `deployStatus` varchar(10) NOT NULL DEFAULT '' COMMENT '部署结果',
  PRIMARY KEY (`id`),
  UNIQUE KEY `i_gitSrcId` (`gitSrcId`),
  KEY `i_projectId` (`projectId`),
  KEY `i_userId` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of d_deploy_history
-- ----------------------------

-- ----------------------------
-- Table structure for `d_deploy_project`
-- ----------------------------
DROP TABLE IF EXISTS `d_deploy_project`;
CREATE TABLE `d_deploy_project` (
  `id` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `deployName` varchar(100) DEFAULT NULL COMMENT '要部署的项目名',
  `deployRsyncScheme` int(1) DEFAULT '0' COMMENT '同步方案：0为rsync 工具，1为ansible',
  `deployRsyncIP` varchar(2000) DEFAULT NULL COMMENT '同步工具IP列表。格式为[ip2:port,ip1:port]',
  `deployRsyncUser` varchar(30) DEFAULT NULL COMMENT '同步用户名',
  `deployRsyncProjectName` varchar(100) DEFAULT NULL COMMENT '同步项目名',
  `deployRsyncPasswd` varchar(100) DEFAULT NULL COMMENT '同步密码',
  `deployRsyncKey` varchar(150) DEFAULT NULL COMMENT '同步key，存储位置和名称',
  `deployRsyncExclude` varchar(500) DEFAULT NULL COMMENT '同步中排除的文件或目录。格式：123.txt|123/|.git',
  `deployGitSrcUrl` varchar(300) DEFAULT NULL,
  `deployGitConfUrl` varchar(300) DEFAULT NULL,
  `deployRsyncForntComm` varchar(100) DEFAULT NULL COMMENT '同步代码前本地执行的脚本（bashshell）。存储为unixtime+6位数字随机序号文件。',
  `deployRsyncBackComm` varchar(100) DEFAULT NULL COMMENT '同步代码后远程执行的脚本（bashshell）存储为unixtime+6位数字随机序号文件。',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of d_deploy_project
-- ----------------------------

-- ----------------------------
-- Table structure for `d_git_project`
-- ----------------------------
DROP TABLE IF EXISTS `d_git_project`;
CREATE TABLE `d_git_project` (
  `id` int(13) unsigned NOT NULL AUTO_INCREMENT,
  `gitProjectName` varchar(50) DEFAULT NULL COMMENT 'git项目名称',
  `gitUrl` varchar(100) DEFAULT NULL COMMENT '以git开头的连接',
  `gitStatus` int(1) DEFAULT '0' COMMENT 'git库在本状态：0本地未创建，1本地以创建，2本地删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of d_git_project
-- ----------------------------
INSERT INTO `d_git_project` VALUES ('1', 'gittest1', '', '0');
INSERT INTO `d_git_project` VALUES ('2', 'gittest2', '', '0');

-- ----------------------------
-- Table structure for `d_git_project_user`
-- ----------------------------
DROP TABLE IF EXISTS `d_git_project_user`;
CREATE TABLE `d_git_project_user` (
  `id` int(13) unsigned NOT NULL AUTO_INCREMENT,
  `gitUserId` int(13) DEFAULT NULL,
  `gitProjectId` int(13) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `i_gitUserId_gitProjectId` (`gitUserId`,`gitProjectId`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of d_git_project_user
-- ----------------------------
INSERT INTO `d_git_project_user` VALUES ('1', '1', '1');
INSERT INTO `d_git_project_user` VALUES ('2', '2', '1');
INSERT INTO `d_git_project_user` VALUES ('3', '2', '2');

-- ----------------------------
-- Table structure for `d_git_user`
-- ----------------------------
DROP TABLE IF EXISTS `d_git_user`;
CREATE TABLE `d_git_user` (
  `id` int(13) NOT NULL AUTO_INCREMENT,
  `gitUser` varchar(50) DEFAULT NULL COMMENT 'git用户名',
  `keyFile` varchar(200) DEFAULT NULL COMMENT 'git用户秘钥文件位置',
  `passwd` varchar(200) DEFAULT NULL,
  `status` int(1) DEFAULT '0' COMMENT '0为使用中，1为 禁用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of d_git_user
-- ----------------------------
INSERT INTO `d_git_user` VALUES ('1', 'simon1', 'simon1.pub', null, '0');
INSERT INTO `d_git_user` VALUES ('2', 'simon2', 'simon2.pub', null, '0');

-- ----------------------------
-- Table structure for `d_group`
-- ----------------------------
DROP TABLE IF EXISTS `d_group`;
CREATE TABLE `d_group` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `group_name` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `group_code` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `mark` varchar(50) COLLATE utf8_bin DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of d_group
-- ----------------------------
INSERT INTO `d_group` VALUES ('1', '超级管理员', 'superman', null);
INSERT INTO `d_group` VALUES ('2', 'git管理', 'gitman', null);
INSERT INTO `d_group` VALUES ('3', '部署组', 'deployman', null);

-- ----------------------------
-- Table structure for `d_group_column`
-- ----------------------------
DROP TABLE IF EXISTS `d_group_column`;
CREATE TABLE `d_group_column` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) DEFAULT NULL,
  `column_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_column_ation` (`column_id`,`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of d_group_column
-- ----------------------------
INSERT INTO `d_group_column` VALUES ('1', '1', '1');
INSERT INTO `d_group_column` VALUES ('2', '1', '2');
INSERT INTO `d_group_column` VALUES ('3', '1', '3');
INSERT INTO `d_group_column` VALUES ('4', '1', '4');
INSERT INTO `d_group_column` VALUES ('5', '1', '5');
INSERT INTO `d_group_column` VALUES ('6', '1', '6');
INSERT INTO `d_group_column` VALUES ('7', '1', '7');
INSERT INTO `d_group_column` VALUES ('8', '1', '8');
INSERT INTO `d_group_column` VALUES ('10', '1', '10');
INSERT INTO `d_group_column` VALUES ('11', '1', '11');
INSERT INTO `d_group_column` VALUES ('12', '1', '12');
INSERT INTO `d_group_column` VALUES ('19', '1', '13');
INSERT INTO `d_group_column` VALUES ('25', '1', '14');
INSERT INTO `d_group_column` VALUES ('26', '1', '15');
INSERT INTO `d_group_column` VALUES ('27', '1', '16');

-- ----------------------------
-- Table structure for `d_group_submit`
-- ----------------------------
DROP TABLE IF EXISTS `d_group_submit`;
CREATE TABLE `d_group_submit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) DEFAULT NULL,
  `submit_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_column_ation` (`submit_id`,`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of d_group_submit
-- ----------------------------
INSERT INTO `d_group_submit` VALUES ('7', '1', '100');
INSERT INTO `d_group_submit` VALUES ('8', '1', '101');
INSERT INTO `d_group_submit` VALUES ('9', '1', '102');
INSERT INTO `d_group_submit` VALUES ('10', '1', '103');
INSERT INTO `d_group_submit` VALUES ('11', '1', '104');
INSERT INTO `d_group_submit` VALUES ('12', '1', '105');
INSERT INTO `d_group_submit` VALUES ('13', '1', '106');
INSERT INTO `d_group_submit` VALUES ('14', '1', '107');
INSERT INTO `d_group_submit` VALUES ('15', '1', '108');
INSERT INTO `d_group_submit` VALUES ('16', '1', '109');
INSERT INTO `d_group_submit` VALUES ('17', '1', '110');
INSERT INTO `d_group_submit` VALUES ('18', '1', '111');
INSERT INTO `d_group_submit` VALUES ('19', '1', '112');
INSERT INTO `d_group_submit` VALUES ('20', '1', '113');
INSERT INTO `d_group_submit` VALUES ('23', '1', '114');
INSERT INTO `d_group_submit` VALUES ('24', '1', '115');

-- ----------------------------
-- Table structure for `d_group_user`
-- ----------------------------
DROP TABLE IF EXISTS `d_group_user`;
CREATE TABLE `d_group_user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `group_id` varchar(45) COLLATE utf8_bin NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_group_index` (`user_id`,`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of d_group_user
-- ----------------------------
INSERT INTO `d_group_user` VALUES ('3', '1', '1');

-- ----------------------------
-- Table structure for `d_submit`
-- ----------------------------
DROP TABLE IF EXISTS `d_submit`;
CREATE TABLE `d_submit` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `submit_id` int(11) NOT NULL COMMENT ' 权限编号',
  `mark` varchar(20) DEFAULT NULL COMMENT '功能说明',
  `submit_local` varchar(50) DEFAULT NULL COMMENT '权限位置',
  PRIMARY KEY (`id`),
  UNIQUE KEY `i_submit_id` (`submit_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COMMENT='单个提交功能列表';

-- ----------------------------
-- Records of d_submit
-- ----------------------------
INSERT INTO `d_submit` VALUES ('1', '100', '用户个人信息查询、修改', '系统管理->修改个人密码 ');
INSERT INTO `d_submit` VALUES ('2', '101', '用户信息增加、减少、修改密码', '系统管理->用户管理（查看）');
INSERT INTO `d_submit` VALUES ('3', '102', '用户信息增加、减少、修改密码', '系统管理->用户管理（修改）');
INSERT INTO `d_submit` VALUES ('4', '103', '用户组管理', '系统管理->用户组管理（查看）');
INSERT INTO `d_submit` VALUES ('5', '104', '用户组管理', '系统管理->用户组管理（修改）');
INSERT INTO `d_submit` VALUES ('6', '105', 'git项目管理', 'git管理->git项目管理（查看）');
INSERT INTO `d_submit` VALUES ('7', '106', 'git项目管理', 'git管理->git项目管理（修改）');
INSERT INTO `d_submit` VALUES ('8', '107', 'git用户管理', 'git管理->git用户管理（查看）');
INSERT INTO `d_submit` VALUES ('9', '108', 'git用户管理', 'git管理->git用户管理（修改）');
INSERT INTO `d_submit` VALUES ('10', '109', 'git用户权限管理', 'git管理->git权限管理（项目添加用户）');
INSERT INTO `d_submit` VALUES ('11', '110', 'git用户权限管理', 'git管理->git权限管理（用户添加项目）');
INSERT INTO `d_submit` VALUES ('12', '111', 'git本地配置生成', 'git管理->git本地服务（配置生成）');
INSERT INTO `d_submit` VALUES ('13', '112', 'git本地库创建', 'git管理->git本地服务（新建库）');
INSERT INTO `d_submit` VALUES ('14', '113', '部署配置', '部署管理->部署配置（查看）');
INSERT INTO `d_submit` VALUES ('15', '114', '部署配置', '部署管理->部署配置（修改）');
INSERT INTO `d_submit` VALUES ('16', '115', '部署配置提交', '部署管理->部署配置（添加）');

-- ----------------------------
-- Table structure for `d_user`
-- ----------------------------
DROP TABLE IF EXISTS `d_user`;
CREATE TABLE `d_user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) COLLATE utf8_bin NOT NULL,
  `nick_name` varchar(10) COLLATE utf8_bin NOT NULL COMMENT '昵称',
  `passwd` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `email` varchar(30) COLLATE utf8_bin DEFAULT NULL,
  `phone_num` int(13) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ----------------------------
-- Records of d_user
-- ----------------------------
INSERT INTO `d_user` VALUES ('1', 'admin', 'admin', 'pbkdf2:sha256:150000$ySHb4MxP$27f5f2fecd3bcd0121d95061689eff5036611d36f8aa3f96936d71c2f957bb58', '', '123');
