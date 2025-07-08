-- model_formsets
CREATE TABLE `model_formsets_authormeeting_author` (
  `authormeeting_id` BIGINT NOT NULL,
  `author_id` BIGINT NOT NULL,
  SHARD KEY (`authormeeting_id`),
  UNIQUE KEY (`authormeeting_id`, `author_id`),
  KEY (`authormeeting_id`),
  KEY (`author_id`)
);
