CREATE TABLE `filtered_relation_author_book` (
  `author_id` BIGINT NOT NULL,
  `book_id` BIGINT NOT NULL,
  SHARD KEY (`author_id`),
  UNIQUE KEY (`author_id`, `book_id`),
  KEY (`author_id`),
  KEY (`book_id`)
);
