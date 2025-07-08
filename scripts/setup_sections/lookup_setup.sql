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
