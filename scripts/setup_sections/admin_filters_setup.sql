CREATE TABLE `admin_filters_book_user` (
  `book_id` BIGINT NOT NULL,
  `user_id` BIGINT NOT NULL,
  SHARD KEY (`book_id`),
  UNIQUE KEY (`book_id`, `user_id`),
  KEY (`book_id`),
  KEY (`user_id`)
);
