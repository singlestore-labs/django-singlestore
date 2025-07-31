CREATE TABLE `m2m_multiple_article_category` (
  `article_id` BIGINT NOT NULL,
  `category_id` BIGINT NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `category_id`),
  KEY (`article_id`),
  KEY (`category_id`)
);

CREATE TABLE `m2m_multiple_article_category_second` (
  `article_id` BIGINT NOT NULL,
  `category_id` BIGINT NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `category_id`),
  KEY (`article_id`),
  KEY (`category_id`)
);