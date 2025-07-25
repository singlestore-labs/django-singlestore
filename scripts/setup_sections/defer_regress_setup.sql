CREATE TABLE `defer_regress_request_item` (
  `request_id` BIGINT NOT NULL,
  `item_id` BIGINT NOT NULL,
  SHARD KEY (`request_id`),
  UNIQUE KEY (`request_id`, `item_id`),
  KEY (`request_id`),
  KEY (`item_id`)
);
