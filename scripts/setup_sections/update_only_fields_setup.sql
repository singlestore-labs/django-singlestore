-- update_only_fields
CREATE TABLE `update_only_fields_employee_account` (
  `employee_id` BIGINT NOT NULL,
  `account_id` BIGINT NOT NULL,
  SHARD KEY (`employee_id`),
  UNIQUE KEY (`employee_id`, `account_id`),
  KEY (`employee_id`),
  KEY (`account_id`)
);
