USE fantasy_league;

CREATE VIEW Player_Team_View AS 
SELECT 
	   P.player_id,
       P.player_name,
       P.position,
       P.nba_team,
       T.team_name,
       T.city,
       T.conference,
       T.division
FROM Player AS P
INNER JOIN Team AS T ON P.team_id = T.team_id;

SELECT
	player_name,
    position,
    team_name,
    city,
    conference
FROM Player_Team_View;

INSERT INTO Player_Team_View (
	player_id,
    player_name,
    position,
    nba_team,
    team_name,
    city,
    conference,
    division
)
VALUES (
	9999,
    'Test View Player',
    'SG',
    'Test NBA Team',
    'Test Joined Team',
    'Test City',
    'East',
    'Atlantic'
);

CREATE VIEW East_Teams AS
SELECT 
	team_id,
    team_name,
    city,
    conference,
    division,
    record
FROM Team
WHERE conference = 'East';

SELECT
	team_id,
    team_name,
    city,
    conference,
    division,
    record
FROM East_Teams;

INSERT INTO East_Teams (
	team_name,
    city,
    conference,
    division,
    record
)

VALUES (
	'View Inserted East Team',
    'View City',
    'East',
    'Atlantic',
    '0-0'
);

SELECT * FROM Team;
SELECT * FROM East_Teams;