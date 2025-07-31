CREATE TABLE `model_package_article_site` (
  `article_id` BIGINT NOT NULL,
  `site_id` BIGINT NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `site_id`),
  KEY (`article_id`),
  KEY (`site_id`)
);

CREATE TABLE `model_package_article_publications` (
  `article_id` BIGINT NOT NULL,
  `publication_id` BIGINT NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `publication_id`),
  KEY (`article_id`),
  KEY (`publication_id`)
);

CREATE TABLE `model_package_advertisement_publications` (
  `advertisement_id` BIGINT NOT NULL,
  `publication_id` BIGINT NOT NULL,
  SHARD KEY (`advertisement_id`),
  UNIQUE KEY (`advertisement_id`, `publication_id`),
  KEY (`advertisement_id`),
  KEY (`publication_id`)
);
