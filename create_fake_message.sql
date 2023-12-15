INSERT INTO Message (SenderID, ReceiverID, Message, Timestamp, isRead)
SELECT
    FLOOR(RAND() * 18) + 1 AS SenderID,
    FLOOR(RAND() * 18) + 1 AS ReceiverID,
    CONCAT('Test message ', FLOOR(RAND() * 100) + 1) AS Message,
    NOW() - INTERVAL FLOOR(RAND() * 30) DAY AS Timestamp,
    RAND() > 0.5 AS isRead
FROM
    information_schema.tables
LIMIT 100;
