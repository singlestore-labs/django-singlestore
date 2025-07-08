-- get_or_create
CREATE TABLE `get_or_create_thing_tag` (
  `thing_id` BIGINT NOT NULL,
  `tag_id` BIGINT NOT NULL,
  SHARD KEY (`thing_id`),
  UNIQUE KEY (`thing_id`, `tag_id`),
  KEY (`thing_id`),
  KEY (`tag_id`)
);


CREATE TABLE `get_or_create_book_author` (
  `book_id` BIGINT NOT NULL,
  `author_id` BIGINT NOT NULL,
  SHARD KEY (`book_id`),
  UNIQUE KEY (`book_id`, `author_id`),
  KEY (`book_id`),
  KEY (`author_id`)
);
