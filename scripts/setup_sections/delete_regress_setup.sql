-- delete_regress
CREATE TABLE `delete_regress_played_with` (
  `child_id` BIGINT NOT NULL,
  `toy_id` BIGINT NOT NULL,
  `date_col` TIMESTAMP,
  SHARD KEY (`child_id`),
  UNIQUE KEY (`child_id`, `toy_id`),
  KEY (`child_id`),
  KEY (`toy_id`)
);

CREATE TABLE `delete_regress_researcher_contact` (
  `researcher_id` BIGINT NOT NULL,
  `contact_id` BIGINT NOT NULL,
  SHARD KEY (`researcher_id`),
  UNIQUE KEY (`researcher_id`, `contact_id`),
  KEY (`researcher_id`),
  KEY (`contact_id`)
);
