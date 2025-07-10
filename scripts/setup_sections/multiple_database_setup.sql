-- multiple_database
CREATE TABLE `multiple_database_book_person` (
  `book_id` BIGINT NOT NULL,
  `person_id` VARCHAR(100) NOT NULL,
  SHARD KEY (`book_id`),
  UNIQUE KEY (`book_id`, `person_id`),
  KEY (`book_id`),
  KEY (`person_id`)
);
