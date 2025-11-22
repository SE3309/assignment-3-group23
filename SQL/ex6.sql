USE fantasy_league;

-- Exercise 6, Query 1
UPDATE Team
SET record = '0-0'
WHERE conference = 'East';

-- Exercise 6, Query 2
DELETE FROM Player 
WHERE team_id = (
	SELECT team_id FROM Team WHERE team_name = 'Boston Celtics'
    );
    
-- Exercise 6, Query 3
INSERT INTO Roster (roster_name, user_id, league_id)
SELECT 
	CONCAT(U.username, '_GeneratedRoster'),
    U.user_id,
    L.league_id
FROM User AS U
INNER JOIN League AS L on L.creator_user_id = U.user_id;


    