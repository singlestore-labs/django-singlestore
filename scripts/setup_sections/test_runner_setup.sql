-- test_runner
CREATE TABLE `test_runner_person_friend` (
  `from_person_id` BIGINT NOT NULL,
  `to_person_id` BIGINT NOT NULL,
  SHARD KEY (`from_person_id`),
  UNIQUE KEY (`from_person_id`, `to_person_id`),
  KEY (`from_person_id`),
  KEY (`to_person_id`)
);
