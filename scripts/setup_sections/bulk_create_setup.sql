-- bulk_create
CREATE TABLE `bulk_create_relatedmodel_bigautofieldmodel` (
  `relatedmodel_id` BIGINT NOT NULL,
  `bigautofieldmodel_id` BIGINT NOT NULL,
  SHARD KEY (`relatedmodel_id`),
  UNIQUE KEY (`relatedmodel_id`, `bigautofieldmodel_id`),
  KEY (`relatedmodel_id`),
  KEY (`bigautofieldmodel_id`)
);
