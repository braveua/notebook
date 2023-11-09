create database if not exists notebook;
####################################
USE notebook;
####################################
CREATE TABLE IF NOT EXISTS note(
                id INT PRIMARY KEY AUTO_INCREMENT,
                parentid INT,
                subject VARCHAR(100),
                content TEXT,
                ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tag BIGINT UNSIGNED NOT NULL DEFAULT '0');
####################################
CREATE TABLE IF NOT EXISTS `tag` (
  `id` smallint unsigned NOT NULL,
  `sname` varchar(100) NOT NULL,
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `sname` (`sname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
####################################
DROP PROCEDURE IF EXISTS notebook.addnote;

DELIMITER $$
$$
CREATE DEFINER=`creator`@`%` PROCEDURE `notebook`.`addnote`(p_id INT,
							    p_parentId INT,
							    p_subject VARCHAR(255),
							    p_content TEXT
							   )
BEGIN
	INSERT into note (id, parentid, subject, content) values (p_id, p_parentId, p_subject, p_content);
END$$
DELIMITER ;
####################################
exit
