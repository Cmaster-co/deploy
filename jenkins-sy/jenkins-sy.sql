CREATE TABLE `jenkins`.`jenkins_cfg` (
  `appid` VARCHAR(45) NOT NULL,
  `marathon` VARCHAR(45) NOT NULL,
  `address` VARCHAR(100) NOT NULL,
  `tag` VARCHAR(45) NOT NULL,
  `branch` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NOT NULL,
  `type` VARCHAR(5) NOT NULL,
  PRIMARY KEY (`appid`, `marathon`),
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;
