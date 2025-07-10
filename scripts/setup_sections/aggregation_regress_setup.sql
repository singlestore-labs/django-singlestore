-- aggregation_regress
CREATE TABLE `aggregation_regress_author_friend` (
  `from_author_id` BIGINT NOT NULL,
  `to_author_id` BIGINT NOT NULL,
  SHARD KEY (`from_author_id`),
  UNIQUE KEY (`from_author_id`, `to_author_id`),
  KEY (`from_author_id`),
  KEY (`to_author_id`)
);

CREATE TABLE `aggregation_regress_book_author` (
  `book_id` BIGINT NOT NULL,
  `author_id` BIGINT NOT NULL,
  SHARD KEY (`book_id`),
  UNIQUE KEY (`book_id`,`author_id`),
  KEY (`book_id`),
  KEY (`author_id`)
);

CREATE TABLE `aggregation_regress_store_book` (
  `store_id` BIGINT NOT NULL,
  `book_id` BIGINT NOT NULL,
  SHARD KEY (`store_id`),
  UNIQUE KEY (`store_id`,`book_id`),
  KEY (`store_id`),
  KEY (`book_id`)
);

CREATE TABLE `aggregation_regress_recipe_authorproxy` (
  `recipe_id` BIGINT NOT NULL,
  `authorproxy_id` BIGINT NOT NULL,
  SHARD KEY (`recipe_id`),
  UNIQUE KEY (`recipe_id`, `authorproxy_id`),
  KEY (`recipe_id`),
  KEY (`authorproxy_id`)
);
