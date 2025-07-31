CREATE TABLE `signals_book_author` (
  `book_id` BIGINT NOT NULL,
  `author_id` BIGINT NOT NULL,
  SHARD KEY (`book_id`),
  UNIQUE KEY (`book_id`, `author_id`),
  KEY (`book_id`),
  KEY (`author_id`)
);
