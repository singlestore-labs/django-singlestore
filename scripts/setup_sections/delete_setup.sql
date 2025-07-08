-- delete
CREATE TABLE `delete_player_game` (
  `player_id` BIGINT NOT NULL,
  `game_id` BIGINT NOT NULL,
  SHARD KEY (`player_id`),
  UNIQUE KEY (`player_id`, `game_id`),
  KEY (`player_id`),
  KEY(`game_id`)
);
