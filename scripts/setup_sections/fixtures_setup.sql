-- fixtures
CREATE TABLE `fixtures_blog_article` (
  `blog_id` BIGINT NOT NULL,
  `article_id` BIGINT NOT NULL,
  SHARD KEY (`blog_id`),
  UNIQUE KEY (`blog_id`, `article_id`),
  KEY (`blog_id`),
  KEY (`article_id`)
);

CREATE TABLE `fixtures_visa_permission` (
  `visa_id` BIGINT NOT NULL,
  `permission_id` BIGINT NOT NULL,
  SHARD KEY (`visa_id`),
  UNIQUE KEY (`visa_id`, `permission_id`),
  KEY (`visa_id`),
  KEY (`permission_id`)
);

CREATE TABLE `fixtures_book_person` (
  `book_id` BIGINT NOT NULL,
  `person_id` TEXT NOT NULL,
  SHARD KEY (`book_id`),
  UNIQUE KEY (`book_id`, `person_id`),
  KEY (`book_id`),
  KEY (`person_id`)
);

CREATE TABLE `fixtures_naturalkeything_naturalkeything` (
  `from_naturalkeything_id` TEXT NOT NULL,
  `to_naturalkeything_id` TEXT NOT NULL,
  SHARD KEY (`from_naturalkeything_id`),
  UNIQUE KEY (`from_naturalkeything_id`, `to_naturalkeything_id`),
  KEY (`from_naturalkeything_id`),
  KEY (`to_naturalkeything_id`)
);
