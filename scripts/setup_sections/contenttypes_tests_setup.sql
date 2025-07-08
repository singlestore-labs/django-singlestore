-- contenttypes_tests
CREATE TABLE `contenttypes_tests_modelwithm2mtosite_site` (
  `modelwithm2mtosite_id` BIGINT NOT NULL,
  `site_id` BIGINT NOT NULL,
  SHARD KEY (`modelwithm2mtosite_id`),
  UNIQUE KEY (`modelwithm2mtosite_id`, `site_id`),
  KEY (`modelwithm2mtosite_id`),
  KEY (`site_id`)
);
