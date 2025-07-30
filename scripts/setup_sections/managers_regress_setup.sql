CREATE TABLE `managers_regress_relationmodel_relatedmodel` (
  `relationmodel_id` BIGINT NOT NULL,
  `relatedmodel_id` BIGINT NOT NULL,
  SHARD KEY (`relationmodel_id`),
  UNIQUE KEY (`relationmodel_id`, `relatedmodel_id`),
  KEY (`relationmodel_id`),
  KEY (`relatedmodel_id`)
);