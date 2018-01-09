CREATE DATABASE `studentGrade` CHARACTER SET utf8;

INSERT INTO `studentgrade_admininfo` VALUES ('00001','1234');

CREATE TABLE IF NOT EXISTS `studentgrade_studentinfo` (
  `stuID` varchar(20) NOT NULL,
  `stuName` varchar(20) NOT NULL,
  `stuSex` varchar(5) NOT NULL,
  `stuMajor` varchar(20) NOT NULL,
  `stuAge` int(11) NOT NULL,
  `stuClass_id` varchar(10) NOT NULL,
  `stuPassword` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `studentgrade_studentinfo` VALUES 
('2012211350','刘强东','男','电子商务','43','2012211305','2012211350'),
('2012211351','马云','男','电子商务','52','2012211305','2012211351'),
('2012211352','章泽天','女','电子商务','28','2012211305','2012211352'),
('2012211360','马化腾','男','计算机科学与技术','22','2012211306','2012211360'),
('2012211361','常凯申','男','计算机科学与技术','22','2012211306','2012211361'),
('2012211362','马华东','男','计算机科学与技术','22','2012211306','2012211362');




CREATE TABLE IF NOT EXISTS `studentgrade_teacherinfo` (
  `teacherID` varchar(20) NOT NULL,
  `teacherName` varchar(20) NOT NULL,
  `teacherSex` varchar(5) NOT NULL,
  `teacherAge` int(11) NOT NULL,
  `teacherPassword` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `studentgrade_teacherinfo` VALUES
('1000','杜军平','女','50','1000'),
('1001','张海平','男','50','1001'),
('1002','川端康成','男','60','1002'),
('1003','纳兰性德','男','23','1003');

INSERT INTO `studentgrade_teacherinfo` VALUES
('1004','哈哈哈','男','60','1004'),
('1005','的简欧好','男','60','1005');

CREATE TABLE IF NOT EXISTS `studentgrade_classinfo` (
  `classNo` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `studentgrade_classinfo` VALUES
('2012211304'),
('2012211305'),
('2012211306');


CREATE TABLE IF NOT EXISTS `studentgrade_courseinfo` (
  `courseID` varchar(20) NOT NULL,
  `courseName` varchar(20) NOT NULL,
  `courseTeachers_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `studentgrade_courseinfo` VALUES
('C01','数据库','1000'),
('C02','体系结构','1001'),
('C03','文学史','1002'),
('C04','诗歌','1003');

INSERT INTO `studentgrade_courseinfo` VALUES
('C07','计算机网络','1006'),
('C08','现代交换原理','1007'),
('C09','软件工程','1009'),
('C10','人工智能','1010'),
('C11','高等数学上','1011'),
('C12','高等数学下','1008'),
('C13','数学分析','1012'),
('C14','数据结构','1013'),
('C15','编译原理','1014'),
('C16','通信原理','1015'),
('C17','大学英语一','1016'),
('C18','大学英语二','1017'),
('C19','大学英语三','1018');

CREATE TABLE IF NOT EXISTS `studentgrade_studentcourse` (
`id` int(11) NOT NULL,
  `students_id` varchar(20) NOT NULL,
  `courses_id` varchar(20) NOT NULL,
  `Grade` int(10) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `studentgrade_studentcourse` VALUES
('0','2012211180','C01','98'),
('1','2012211181','C01','90'),
('2','2012211182','C01','89'),
('3','2012211183','C01','99'),
('4','2012211184','C01','97'),
('5','2012211189','C01','100'),
('6','2012211191','C04','90'),
('7','2012211194','C04','96'),
('8','2012211350','C02','88');

INSERT INTO `studentgrade_studentcourse` VALUES
('13','2012211350','C01','98'),
('14','2012211180','C01','98'),
('15','2012211181','C01','98'),
('16','3012211104','C01','98'),
('17','2012211191','C01','98'),
('18','2012211194','C01','98'),
('19','3012211100','C01','98'),
('20','3012211101','C01','98'),
('21','3012211102','C01','98'),
('22','3012211103','C01','98');

INSERT INTO `studentgrade_studentcourse` VALUES




