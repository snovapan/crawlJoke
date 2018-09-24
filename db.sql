CREATE TABLE `t_joke` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `classify` varchar(100) DEFAULT NULL COMMENT '分类',
  `title` varchar(100) DEFAULT NULL COMMENT '标题',
  `content` mediumtext COMMENT '内容',
  `pubtime` datetime DEFAULT NULL COMMENT '发布时间',
  `jokelink` varchar(100) DEFAULT NULL COMMENT '来源',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

