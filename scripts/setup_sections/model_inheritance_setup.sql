-- model_inheritance
CREATE TABLE `model_inheritance_supplier_restaurant` (
  `supplier_id` BIGINT NOT NULL,
  `restaurant_id` BIGINT NOT NULL,
  SHARD KEY (`supplier_id`),
  UNIQUE KEY (`supplier_id`, `restaurant_id`),
  KEY (`supplier_id`),
  KEY (`restaurant_id`)
);

CREATE TABLE `model_inheritance_base_title` (
  `base_id` BIGINT NOT NULL,
  `title_id` BIGINT NOT NULL,
  SHARD KEY (`base_id`),
  UNIQUE KEY (`base_id`, `title_id`),
  KEY (`base_id`),
  KEY (`title_id`)
);
