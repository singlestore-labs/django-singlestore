CREATE TABLE `async_manytomanymodel_simplemodel` (
  `manytomanymodel_id` BIGINT NOT NULL,
  `simplemodel_id` BIGINT NOT NULL,
  SHARD KEY (`manytomanymodel_id`),
  UNIQUE KEY (`manytomanymodel_id`, `simplemodel_id`),
  KEY (`manytomanymodel_id`),
  KEY (`simplemodel_id`)
);
