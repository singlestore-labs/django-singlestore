-- one_to_one
CREATE TABLE `one_to_one_favorites_restaurant` (
  `favorites_id` BIGINT NOT NULL,
  `restaurant_id` BIGINT NOT NULL,
  SHARD KEY (`favorites_id`),
  UNIQUE KEY (`favorites_id`, `restaurant_id`),
  KEY (`favorites_id`),
  KEY (`restaurant_id`)
);
