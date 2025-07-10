-- update
CREATE TABLE `update_bar_m2m_foo` (
  `bar_id` BIGINT NOT NULL,
  `foo_id` BIGINT NOT NULL,
  SHARD KEY (`bar_id`),
  UNIQUE KEY (`bar_id`, `foo_id`),
  KEY (`bar_id`),
  KEY (`foo_id`)
);
