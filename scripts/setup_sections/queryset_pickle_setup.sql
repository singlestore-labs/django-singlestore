CREATE TABLE `queryset_pickle_m2mmodel_group` (
  `m2mmodel_id` BIGINT NOT NULL,
  `group_id` BIGINT NOT NULL,
  SHARD KEY (`m2mmodel_id`),
  UNIQUE KEY (`m2mmodel_id`, `group_id`),
  KEY (`m2mmodel_id`),
  KEY (`group_id`)
);
