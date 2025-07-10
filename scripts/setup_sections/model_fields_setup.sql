-- model_fields
CREATE TABLE `model_fields_manytomany_manytomany` (
  `from_manytomany_id` BIGINT NOT NULL,
  `to_manytomany_id` BIGINT NOT NULL,
  SHARD KEY (`from_manytomany_id`),
  UNIQUE KEY (`from_manytomany_id`, `to_manytomany_id`),
  KEY (`from_manytomany_id`),
  KEY (`to_manytomany_id`)
);

CREATE TABLE `model_fields_allfieldsmodel_allfieldsmodel` (
  `from_allfieldsmodel_id` BIGINT NOT NULL,
  `to_allfieldsmodel_id` BIGINT NOT NULL,
  SHARD KEY (`from_allfieldsmodel_id`),
  UNIQUE KEY (`from_allfieldsmodel_id`, `to_allfieldsmodel_id`),
  KEY (`from_allfieldsmodel_id`),
  KEY (`to_allfieldsmodel_id`)
);
