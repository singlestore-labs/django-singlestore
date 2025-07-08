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
