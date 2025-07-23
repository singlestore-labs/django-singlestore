CREATE TABLE `get_object_or_404_article_author` (
  `article_id` BIGINT NOT NULL,
  `author_id` BIGINT NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `author_id`),
  KEY (`article_id`),
  KEY (`author_id`)
);