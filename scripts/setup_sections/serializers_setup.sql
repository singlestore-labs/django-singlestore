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
