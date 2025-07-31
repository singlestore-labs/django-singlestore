CREATE TABLE `test_crmomm_stable_ponies` (
  `stable_id` BIGINT NOT NULL,
  `pony_id` BIGINT NOT NULL,
  SHARD KEY (`stable_id`),
  UNIQUE KEY (`stable_id`, `pony_id`),
  KEY (`stable_id`),
  KEY (`pony_id`)
);
