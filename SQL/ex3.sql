USE fantasy_league;

INSERT INTO Team (team_name, city, conference, division, record)
VALUES ('Toronto Raptors','Toronto','East','Atlantic','6-5'),
       ('Boston Celtics','Boston','East','Atlantic','6-7'),
       ('Los Angeles Lakers','Los Angeles','West','Pacific','8-4'),
       ('Raptors Copy','Toronto','East','Atlantic','6-5');

SELECT * FROM Team

SELECT conference, COUNT(*) AS team_count
FROM Team
GROUP BY conference

SELECT t1.team_name as team1, t2.team_name as team2, t1.conference
FROM Team t1
JOIN Team t2
    ON t1.conference=t2.conference
    AND t1.team_name<t2.team_name
