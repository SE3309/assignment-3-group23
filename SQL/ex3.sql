USE fantasy_league;


INSERT INTO Team (team_name, city, conference, division, record)
VALUES ('Toronto Raptors','Toronto','East','Atlantic','6-5');

INSERT INTO Team (team_name, city, conference, division, record)
VALUES ('Boston Celtics','Boston','East','Atlantic','6-7'),
       ('Los Angeles Lakers','Los Angeles','West','Pacific','8-4');
       
INSERT INTO Team (team_name, city, conference, division, record)
SELECT 'Raptors Copy', city, conference, division, record FROM Team WHERE team_name = 'Toronto Raptors';

SELECT * FROM Team;