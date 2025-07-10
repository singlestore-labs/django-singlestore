-- generic_relations_regress
CREATE TABLE `generic_relations_regress_organization_contact` (
  `organization_id` BIGINT NOT NULL,
  `contact_id` BIGINT NOT NULL,
  SHARD KEY (`organization_id`),
  UNIQUE KEY (`organization_id`, `contact_id`),
  KEY (`organization_id`),
  KEY (`contact_id`)
);
