-- backends
CREATE TABLE `backends_verylongmodelnamezzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz_person` (
  `verylongmodelnamezzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz_id` BIGINT NOT NULL,
  `person_id` BIGINT NOT NULL,
  SHARD KEY (`verylongmodelnamezzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz_id`),
  UNIQUE KEY (`verylongmodelnamezzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz_id`, `person_id`),
  KEY (`verylongmodelnamezzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz_id`),
  KEY (`person_id`)
);

CREATE TABLE `backends_object_object` (
  `from_object_id` BIGINT NOT NULL,
  `to_object_id` BIGINT NOT NULL,
  SHARD KEY (`from_object_id`),
  UNIQUE KEY (`from_object_id`, `to_object_id`),
  KEY (`from_object_id`),
  KEY (`to_object_id`)
);
