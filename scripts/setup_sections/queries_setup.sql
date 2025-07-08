-- queries
CREATE TABLE `queries_annotation_note` (
  `annotation_id` BIGINT NOT NULL,
  `note_id` BIGINT NOT NULL,
  SHARD KEY (`annotation_id`),
  UNIQUE KEY (`annotation_id`, `note_id`),
  KEY (`annotation_id`),
  KEY (`note_id`)
);


CREATE TABLE `queries_item_tag` (
  `item_id` BIGINT NOT NULL,
  `tag_id` BIGINT NOT NULL,
  SHARD KEY (`item_id`),
  UNIQUE KEY (`item_id`, `tag_id`),
  KEY (`item_id`),
  KEY (`tag_id`)
);

CREATE TABLE `queries_valid_parent` (
  `from_valid` BIGINT NOT NULL,
  `to_valid` BIGINT NOT NULL,
  SHARD KEY (`from_valid`),
  UNIQUE KEY (`from_valid`, `to_valid`),
  KEY (`from_valid`),
  KEY (`to_valid`)
);

CREATE TABLE `queries_custompktag_custompk` (
  `custompktag_id` VARCHAR(20),
  `custompk_id` VARCHAR(10),
  SHARD KEY (`custompktag_id`),
  UNIQUE KEY (`custompktag_id`, `custompk_id`),
  KEY (`custompktag_id`),
  KEY (`custompk_id`)
);

CREATE TABLE `queries_job_responsibility` (
  `job_id` VARCHAR(20),
  `responsibility_id` VARCHAR(20),
  SHARD KEY (`job_id`),
  UNIQUE KEY (`job_id`, `responsibility_id`),
  KEY (`job_id`),
  KEY (`responsibility_id`)
);

CREATE TABLE `queries_channel_program` (
  `channel_id` BIGINT NOT NULL,
  `program_id` BIGINT NOT NULL,
  SHARD KEY (`channel_id`),
  UNIQUE KEY (`channel_id`, `program_id`),
  KEY (`channel_id`),
  KEY (`program_id`)
);


CREATE TABLE `queries_paragraph_page` (
  `paragraph_id` BIGINT NOT NULL,
  `page_id` BIGINT NOT NULL,
  SHARD KEY (`paragraph_id`),
  UNIQUE KEY (`paragraph_id`, `page_id`),
  KEY (`paragraph_id`),
  KEY (`page_id`)
);

CREATE TABLE `queries_company_person` (
  `company_id` BIGINT NOT NULL,
  `person_id` BIGINT NOT NULL,
  SHARD KEY (`company_id`),
  UNIQUE KEY (`company_id`, `person_id`),
  KEY (`company_id`),
  KEY (`person_id`)
);

CREATE TABLE `queries_classroom_student` (
  `classroom_id` BIGINT NOT NULL,
  `student_id` BIGINT NOT NULL,
  SHARD KEY (`classroom_id`),
  UNIQUE KEY (`classroom_id`, `student_id`),
  KEY (`classroom_id`),
  KEY (`student_id`)
);

CREATE TABLE `queries_teacher_school` (
  `teacher_id` BIGINT NOT NULL,
  `school_id` BIGINT NOT NULL,
  SHARD KEY (`teacher_id`),
  UNIQUE KEY (`teacher_id`, `school_id`),
  KEY (`teacher_id`),
  KEY (`school_id`)
);

CREATE TABLE `queries_teacher_friend` (
  `from_teacher_id` BIGINT NOT NULL,
  `to_teacher_id` BIGINT NOT NULL,
  SHARD KEY (`from_teacher_id`),
  UNIQUE KEY (`from_teacher_id`, `to_teacher_id`),
  KEY (`from_teacher_id`),
  KEY (`to_teacher_id`)
);
