DROP TABLE  IF EXISTS `nibbles`;
CREATE TABLE IF NOT EXISTS `nibbles` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `job_key` char(16) NOT NULL,
  `phase` MEDIUMINT UNSIGNED NOT NULL DEFAULT 1,
  `token` varchar(256),
  `status` enum('AVAILABLE', 'LEASED', 'ERROR', 'COMPLETE') NOT NULL DEFAULT 'AVAILABLE',
  `status_time` DATETIME
) ENGINE=INNODB;