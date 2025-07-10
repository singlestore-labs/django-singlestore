-- many_to_many
CREATE TABLE `many_to_many_article_publication` (
  `article_id` BIGINT NOT NULL,
  `publication_id` BIGINT NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `publication_id`),
  KEY (`article_id`),
  KEY (`publication_id`)
);

CREATE TABLE `many_to_many_article_tag` (
  `article_id` BIGINT NOT NULL,
  `tag_id` BIGINT NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `tag_id`),
  KEY (`article_id`),
  KEY (`tag_id`)
);

CREATE TABLE `many_to_many_user_article` (
  `article_id` BIGINT NOT NULL,
  `user_id` VARCHAR(20) NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `user_id`),
  KEY (`article_id`),
  KEY (`user_id`)
);
