create database if not exists notebook;
####################################
use notebook;
####################################
CREATE TABLE IF NOT EXISTS note(
                id INT PRIMARY KEY AUTO_INCREMENT,
                parentid INT,
                subject VARCHAR(100),
                content TEXT,
                ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
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
