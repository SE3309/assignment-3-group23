USE fantasy_league;

-- Exercise 5, Query 1
SELECT player_name, position, nba_team FROM Player WHERE position = 'SF';

-- Exercise 5, Query 2
SELECT P.player_name, P.position, T.team_name, T.city FROM Player P INNER JOIN Team T ON P.team_id = T.team_id;

-- Exercise 5, Query 3
SELECT player_id, points FROM Player_Game_Stats ORDER BY points DESC;

-- Exercise 5, Query 4
SELECT player_id, AVG(points) AS avg_points, AVG(assists) AS avg_assists, AVG(rebounds) AS avg_rebounds
FROM Player_Game_Stats
GROUP BY player_id;

-- Exercise 5, Query 5
SELECT player_id,
	   COUNT(*) AS games_played,
       SUM(points) AS total_points FROM Player_Game_Stats 
       GROUP BY player_id
       HAVING SUM(points) > 200;
       
-- Exercise 5, Query 6
SELECT player_name FROM Player WHERE player_id IN (
	SELECT player_id
    FROM Player_Game_Stats
    WHERE points > 30
    );
    
-- Exercise 5, Query 7
SELECT U.name AS user_name, R.roster_name, L.league_name, T.team_name, P.player_name
FROM Roster AS R
INNER JOIN User AS U ON U.user_id = R.user_id
INNER JOIN League AS L ON L.league_id = R.league_id
INNER JOIN Team AS T ON T.team_id = 1
INNER JOIN Player AS P ON P.team_id = T.team_id;
