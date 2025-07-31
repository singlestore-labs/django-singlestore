CREATE TABLE `admin_docs_person_group` (
  `person_id` BIGINT NOT NULL,
  `group_id` BIGINT NOT NULL,
  SHARD KEY (`person_id`),
  UNIQUE KEY (`person_id`, `group_id`),
  KEY (`person_id`),
  KEY (`group_id`)
);
