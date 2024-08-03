CREATE TABLE `personalwebsite`.`articles` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`title` VARCHAR(45) NOT NULL,
	`subtitle` VARCHAR(120) NOT NULL,
	`thumbnail` VARCHAR(255) NOT NULL,
	`date_published` DATE NOT NULL,
	`endpoint` VARCHAR(30) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE INDEX `endpoint_UNIQUE` (`endpoint` ASC)
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

