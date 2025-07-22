CREATE TABLE `select_related_pizza_topping` (
  `pizza_id` BIGINT NOT NULL,
  `topping_id` BIGINT NOT NULL,
  SHARD KEY (`pizza_id`),
  UNIQUE KEY (`pizza_id`, `topping_id`),
  KEY (`pizza_id`),
  KEY (`topping_id`)
);
