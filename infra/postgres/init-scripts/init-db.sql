CREATE TABLE IF NOT EXISTS match_info (
    matchId SERIAL PRIMARY KEY,
    playerScore0 INT,
    playerScore1 INT,
    baronKills INT
);

-- inserting non matchId data since it is SERIAL
INSERT INTO match_info(playerScore0, playerScore1, baronKills) VALUES
    (-1, -1, -1),
    (5235, 121231, 12312312)
;