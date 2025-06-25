-- initial_setup
CREATE DATABASE test_django_db;
USE test_django_db;

-- get_or_create
CREATE TABLE `get_or_create_thing_tag` (
  `thing_id` BIGINT NOT NULL,
  `tag_id` BIGINT NOT NULL,
  SHARD KEY (`thing_id`),
  UNIQUE KEY (`thing_id`, `tag_id`),
  KEY (`thing_id`),
  KEY (`tag_id`)
);


CREATE TABLE `get_or_create_book_author` (
  `book_id` BIGINT NOT NULL,
  `author_id` BIGINT NOT NULL,
  SHARD KEY (`book_id`),
  UNIQUE KEY (`book_id`, `author_id`),
  KEY (`book_id`),
  KEY (`author_id`)
);

-- aggregation
CREATE TABLE `aggregation_book_author` (
  `book_id` BIGINT NOT NULL,
  `author_id` BIGINT NOT NULL,
  SHARD KEY (`book_id`),
  UNIQUE KEY (`book_id`,`author_id`),
  KEY (`book_id`),
  KEY (`author_id`)
);


CREATE TABLE `aggregation_author_friend` (
  `from_author_id` BIGINT NOT NULL,
  `to_author_id` BIGINT NOT NULL,
  SHARD KEY (`from_author_id`),
  UNIQUE KEY (`from_author_id`,`to_author_id`),
  KEY (`from_author_id`),
  KEY (`to_author_id`)
);


CREATE TABLE `aggregation_store_book` (
  `store_id` BIGINT NOT NULL,
  `book_id` BIGINT NOT NULL,
  SHARD KEY (`store_id`),
  UNIQUE KEY (`store_id`,`book_id`),
  KEY (`store_id`),
  KEY (`book_id`)
);


-- lookup
CREATE TABLE `lookup_tag_article` (
  `tag_id` BIGINT NOT NULL,
  `article_id` BIGINT NOT NULL,
  SHARD KEY (`tag_id`),
  UNIQUE KEY (`tag_id`, `article_id`),
  KEY (`tag_id`),
  KEY(`article_id`)
);


CREATE TABLE `lookup_player_game` (
  `player_id` BIGINT NOT NULL,
  `game_id` BIGINT NOT NULL,
  SHARD KEY (`player_id`),
  UNIQUE KEY (`player_id`, `game_id`),
  KEY (`player_id`),
  KEY(`game_id`)
);


-- raw_query
CREATE TABLE `raw_query_reviewer_book` (
    `reviewer_id` BIGINT NOT NULL,
    `book_id` BIGINT NOT NULL,
    SHARD KEY (`reviewer_id`),
    UNIQUE KEY(`reviewer_id`, `book_id`),
    KEY (`reviewer_id`),
    KEY(`book_id`)
);

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


-- model_inheritance
CREATE TABLE `model_inheritance_supplier_restaurant` (
  `supplier_id` BIGINT NOT NULL,
  `restaurant_id` BIGINT NOT NULL,
  SHARD KEY (`supplier_id`),
  UNIQUE KEY (`supplier_id`, `restaurant_id`),
  KEY (`supplier_id`),
  KEY (`restaurant_id`)
);

CREATE TABLE `model_inheritance_base_title` (
  `base_id` BIGINT NOT NULL,
  `title_id` BIGINT NOT NULL,
  SHARD KEY (`base_id`),
  UNIQUE KEY (`base_id`, `title_id`),
  KEY (`base_id`),
  KEY (`title_id`)
);

-- annotations
CREATE TABLE `annotations_author_friend` (
  `from_author_id` BIGINT NOT NULL,
  `to_author_id` BIGINT NOT NULL,
  SHARD KEY (`from_author_id`),
  UNIQUE KEY (`from_author_id`, `to_author_id`),
  KEY (`from_author_id`),
  KEY (`to_author_id`)
);

CREATE TABLE `annotations_book_author` (
  `book_id` BIGINT NOT NULL,
  `author_id` BIGINT NOT NULL,
  SHARD KEY (`book_id`),
  UNIQUE KEY (`book_id`, `author_id`),
  KEY (`book_id`),
  KEY (`author_id`)
);

CREATE TABLE `annotations_store_book` (
  `store_id` BIGINT NOT NULL,
  `book_id` BIGINT NOT NULL,
  SHARD KEY (`store_id`),
  UNIQUE KEY (`store_id`, `book_id`),
  KEY (`store_id`),
  KEY (`book_id`)
);


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


-- many_to_many
CREATE TABLE `many_to_many_article_publication` (
  `article_id` BIGINT NOT NULL,
  `publication_id` BIGINT NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `publication_id`),
  KEY (`article_id`),
  KEY (`publication_id`)
);

CREATE TABLE `many_to_many_article_tag` (
  `article_id` BIGINT NOT NULL,
  `tag_id` BIGINT NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `tag_id`),
  KEY (`article_id`),
  KEY (`tag_id`)
);

CREATE TABLE `many_to_many_user_article` (
  `article_id` BIGINT NOT NULL,
  `user_id` VARCHAR(20) NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `user_id`),
  KEY (`article_id`),
  KEY (`user_id`)
);


-- model_forms
CREATE TABLE `model_forms_colourfulitem_colour` (
  `colourfulitem_id` BIGINT NOT NULL,
  `colour_id` BIGINT NOT NULL,
  SHARD KEY (`colourfulitem_id`),
  UNIQUE KEY (`colourfulitem_id`, `colour_id`),
  KEY (`colourfulitem_id`),
  KEY (`colour_id`)
);

CREATE TABLE `model_forms_stumpjoke_character` (
  `stumpjoke_id` BIGINT NOT NULL,
  `character_id` BIGINT NOT NULL,
  SHARD KEY (`stumpjoke_id`),
  UNIQUE KEY (`stumpjoke_id`, `character_id`),
  KEY (`stumpjoke_id`),
  KEY (`character_id`)
);

CREATE TABLE `model_forms_dice_number` (
  `dice_id` BIGINT NOT NULL,
  `number_id` BIGINT NOT NULL,
  SHARD KEY (`dice_id`),
  UNIQUE KEY (`dice_id`, `number_id`),
  KEY (`dice_id`),
  KEY (`number_id`)
);

CREATE TABLE `model_forms_article_category` (
  `article_id` BIGINT NOT NULL,
  `category_id` BIGINT NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `category_id`),
  KEY (`article_id`),
  KEY (`category_id`)
);

-- update
CREATE TABLE `update_bar_m2m_foo` (
  `bar_id` BIGINT NOT NULL,
  `foo_id` BIGINT NOT NULL,
  SHARD KEY (`bar_id`),
  UNIQUE KEY (`bar_id`, `foo_id`),
  KEY (`bar_id`),
  KEY (`foo_id`)
);

-- model_formsets
CREATE TABLE `model_formsets_authormeeting_author` (
  `authormeeting_id` BIGINT NOT NULL,
  `author_id` BIGINT NOT NULL,
  SHARD KEY (`authormeeting_id`),
  UNIQUE KEY (`authormeeting_id`, `author_id`),
  KEY (`authormeeting_id`),
  KEY (`author_id`)
);

-- serializers
CREATE TABLE `serializers_article_category` (
  `article_id` BIGINT NOT NULL,
  `category_id` BIGINT NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `category_id`),
  KEY (`article_id`),
  KEY (`category_id`)
);

CREATE TABLE `serializers_article_categorymetadata` (
  `article_id` BIGINT NOT NULL,
  `categorymetadata_id` BIGINT NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `categorymetadata_id`),
  KEY (`article_id`),
  KEY (`categorymetadata_id`)
);

CREATE TABLE `serializers_article_topic` (
  `article_id` BIGINT NOT NULL,
  `topic_id` BIGINT NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `topic_id`),
  KEY (`article_id`),
  KEY (`topic_id`)
);

CREATE TABLE `serializers_m2mdata_anchor` (
  `m2mdata_id` BIGINT NOT NULL,
  `anchor_id` BIGINT NOT NULL,
  SHARD KEY (`m2mdata_id`),
  UNIQUE KEY (`m2mdata_id`, `anchor_id`),
  KEY (`m2mdata_id`),
  KEY (`anchor_id`)
);

CREATE TABLE `serializers_parent_parent` (
  `from_parent_id` BIGINT NOT NULL,
  `to_parent_id` BIGINT NOT NULL,
  SHARD KEY (`from_parent_id`),
  UNIQUE KEY (`from_parent_id`, `to_parent_id`),
  KEY (`from_parent_id`),
  KEY (`to_parent_id`)
);

CREATE ROWSTORE REFERENCE TABLE `serializers_naturalkeything_other_things` (
  `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `from_naturalkeything_id` bigint NOT NULL,
  `to_naturalkeything_id` bigint NOT NULL,
  UNIQUE KEY(`from_naturalkeything_id`,`to_naturalkeything_id`)
);


CREATE TABLE `serializers_m2mselfdata_m2mselfdata` (
  `from_m2mselfdata_id` BIGINT NOT NULL,
  `to_m2mselfdata_id` BIGINT NOT NULL,
  SHARD KEY (`from_m2mselfdata_id`),
  UNIQUE KEY (`from_m2mselfdata_id`, `to_m2mselfdata_id`),
  KEY (`from_m2mselfdata_id`),
  KEY (`to_m2mselfdata_id`)
);

CREATE TABLE `serializers_m2mintermediatedata_anchor` (
  `m2mintermediatedata_id` BIGINT NOT NULL,
  `anchor_id` BIGINT NOT NULL,
  SHARD KEY (`m2mintermediatedata_id`),
  UNIQUE KEY (`m2mintermediatedata_id`, `anchor_id`),
  KEY (`m2mintermediatedata_id`),
  KEY (`anchor_id`)
);

-- update_only_fields
CREATE TABLE `update_only_fields_employee_account` (
  `employee_id` BIGINT NOT NULL,
  `account_id` BIGINT NOT NULL,
  SHARD KEY (`employee_id`),
  UNIQUE KEY (`employee_id`, `account_id`),
  KEY (`employee_id`),
  KEY (`account_id`)
);

-- contenttypes_tests
CREATE TABLE `contenttypes_tests_modelwithm2mtosite_site` (
  `modelwithm2mtosite_id` BIGINT NOT NULL,
  `site_id` BIGINT NOT NULL,
  SHARD KEY (`modelwithm2mtosite_id`),
  UNIQUE KEY (`modelwithm2mtosite_id`, `site_id`),
  KEY (`modelwithm2mtosite_id`),
  KEY (`site_id`)
);

-- test_runner
CREATE TABLE `test_runner_person_friend` (
  `from_person_id` BIGINT NOT NULL,
  `to_person_id` BIGINT NOT NULL,
  SHARD KEY (`from_person_id`),
  UNIQUE KEY (`from_person_id`, `to_person_id`),
  KEY (`from_person_id`),
  KEY (`to_person_id`)
);

-- model_fields
CREATE TABLE `model_fields_manytomany_manytomany` (
  `from_manytomany_id` BIGINT NOT NULL,
  `to_manytomany_id` BIGINT NOT NULL,
  SHARD KEY (`from_manytomany_id`),
  UNIQUE KEY (`from_manytomany_id`, `to_manytomany_id`),
  KEY (`from_manytomany_id`),
  KEY (`to_manytomany_id`)
);

CREATE TABLE `model_fields_allfieldsmodel_allfieldsmodel` (
  `from_allfieldsmodel_id` BIGINT NOT NULL,
  `to_allfieldsmodel_id` BIGINT NOT NULL,
  SHARD KEY (`from_allfieldsmodel_id`),
  UNIQUE KEY (`from_allfieldsmodel_id`, `to_allfieldsmodel_id`),
  KEY (`from_allfieldsmodel_id`),
  KEY (`to_allfieldsmodel_id`)
);

-- multiple_database
CREATE TABLE `multiple_database_book_person` (
  `book_id` BIGINT NOT NULL,
  `person_id` VARCHAR(100) NOT NULL,
  SHARD KEY (`book_id`),
  UNIQUE KEY (`book_id`, `person_id`),
  KEY (`book_id`),
  KEY (`person_id`)
);

-- aggregation_regress
CREATE TABLE `aggregation_regress_author_friend` (
  `from_author_id` BIGINT NOT NULL,
  `to_author_id` BIGINT NOT NULL,
  SHARD KEY (`from_author_id`),
  UNIQUE KEY (`from_author_id`, `to_author_id`),
  KEY (`from_author_id`),
  KEY (`to_author_id`)
);

CREATE TABLE `aggregation_regress_book_author` (
  `book_id` BIGINT NOT NULL,
  `author_id` BIGINT NOT NULL,
  SHARD KEY (`book_id`),
  UNIQUE KEY (`book_id`,`author_id`),
  KEY (`book_id`),
  KEY (`author_id`)
);

CREATE TABLE `aggregation_regress_store_book` (
  `store_id` BIGINT NOT NULL,
  `book_id` BIGINT NOT NULL,
  SHARD KEY (`store_id`),
  UNIQUE KEY (`store_id`,`book_id`),
  KEY (`store_id`),
  KEY (`book_id`)
);

CREATE TABLE `aggregation_regress_recipe_authorproxy` (
  `recipe_id` BIGINT NOT NULL,
  `authorproxy_id` BIGINT NOT NULL,
  SHARD KEY (`recipe_id`),
  UNIQUE KEY (`recipe_id`, `authorproxy_id`),
  KEY (`recipe_id`),
  KEY (`authorproxy_id`)
);

-- generic_relations_regress
CREATE TABLE `generic_relations_regress_organization_contact` (
  `organization_id` BIGINT NOT NULL,
  `contact_id` BIGINT NOT NULL,
  SHARD KEY (`organization_id`),
  UNIQUE KEY (`organization_id`, `contact_id`),
  KEY (`organization_id`),
  KEY (`contact_id`)
);

-- fixtures
CREATE TABLE `fixtures_blog_article` (
  `blog_id` BIGINT NOT NULL,
  `article_id` BIGINT NOT NULL,
  SHARD KEY (`blog_id`),
  UNIQUE KEY (`blog_id`, `article_id`),
  KEY (`blog_id`),
  KEY (`article_id`)
);

CREATE TABLE `fixtures_visa_permission` (
  `visa_id` BIGINT NOT NULL,
  `permission_id` BIGINT NOT NULL,
  SHARD KEY (`visa_id`),
  UNIQUE KEY (`visa_id`, `permission_id`),
  KEY (`visa_id`),
  KEY (`permission_id`)
);

CREATE TABLE `fixtures_book_person` (
  `book_id` BIGINT NOT NULL,
  `person_id` TEXT NOT NULL,
  SHARD KEY (`book_id`),
  UNIQUE KEY (`book_id`, `person_id`),
  KEY (`book_id`),
  KEY (`person_id`)
);

CREATE TABLE `fixtures_naturalkeything_naturalkeything` (
  `from_naturalkeything_id` TEXT NOT NULL,
  `to_naturalkeything_id` TEXT NOT NULL,
  SHARD KEY (`from_naturalkeything_id`),
  UNIQUE KEY (`from_naturalkeything_id`, `to_naturalkeything_id`),
  KEY (`from_naturalkeything_id`),
  KEY (`to_naturalkeything_id`)
);

-- one_to_one
CREATE TABLE `one_to_one_favorites_restaurant` (
  `favorites_id` BIGINT NOT NULL,
  `restaurant_id` BIGINT NOT NULL,
  SHARD KEY (`favorites_id`),
  UNIQUE KEY (`favorites_id`, `restaurant_id`),
  KEY (`favorites_id`),
  KEY (`restaurant_id`)
);

-- bulk_create
CREATE TABLE `bulk_create_relatedmodel_bigautofieldmodel` (
  `relatedmodel_id` BIGINT NOT NULL,
  `bigautofieldmodel_id` BIGINT NOT NULL,
  SHARD KEY (`relatedmodel_id`),
  UNIQUE KEY (`relatedmodel_id`, `bigautofieldmodel_id`),
  KEY (`relatedmodel_id`),
  KEY (`bigautofieldmodel_id`)
);

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

-- delete
CREATE TABLE `delete_player_game` (
  `player_id` BIGINT NOT NULL,
  `game_id` BIGINT NOT NULL,
  SHARD KEY (`player_id`),
  UNIQUE KEY (`player_id`, `game_id`),
  KEY (`player_id`),
  KEY(`game_id`)
);

-- db_functions
CREATE TABLE `db_functions_article_author` (
  `article_id` BIGINT NOT NULL,
  `author_id` BIGINT NOT NULL,
  SHARD KEY (`article_id`),
  UNIQUE KEY (`article_id`, `author_id`),
  KEY (`article_id`),
  KEY (`author_id`)
);
