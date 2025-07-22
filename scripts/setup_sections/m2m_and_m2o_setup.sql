CREATE TABLE `m2m_and_m2o_issue_user` (
  `issue_id` BIGINT NOT NULL,
  `user_id` BIGINT NOT NULL,
  SHARD KEY (`issue_id`),
  UNIQUE KEY (`issue_id`, `user_id`),
  KEY (`issue_id`),
  KEY (`user_id`)
);

CREATE TABLE `m2m_and_m2o_stringreferencemodel_stringreferencemodel` (
  `from_stringreferencemodel_id` BIGINT NOT NULL,
  `to_stringreferencemodel_id` BIGINT NOT NULL,
  SHARD KEY (`from_stringreferencemodel_id`),
  UNIQUE KEY (`from_stringreferencemodel_id`, `to_stringreferencemodel_id`),
  KEY (`from_stringreferencemodel_id`),
  KEY (`to_stringreferencemodel_id`)
);
