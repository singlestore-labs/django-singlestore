-- raw_query
CREATE TABLE `raw_query_reviewer_book` (
    `reviewer_id` BIGINT NOT NULL,
    `book_id` BIGINT NOT NULL,
    SHARD KEY (`reviewer_id`),
    UNIQUE KEY(`reviewer_id`, `book_id`),
    KEY (`reviewer_id`),
    KEY(`book_id`)
);
