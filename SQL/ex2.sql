CREATE DATABASE fantasy_league;
USE fantasy_league;

CREATE TABLE User (
	user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('Owner','Player','Admin') NOT NULL DEFAULT 'Player',
    date_created DATE DEFAULT (CURRENT_DATE),
    name VARCHAR(100)
    );
    
CREATE TABLE League (
	league_id INT AUTO_INCREMENT PRIMARY KEY,
    league_name VARCHAR(100) NOT NULL,
    season_year VARCHAR(9),
    date_created DATE DEFAULT (CURRENT_DATE),
    creator_user_id INT,
    point_system VARCHAR(10),
    FOREIGN KEY (creator_user_id) REFERENCES User(user_id)
    );
    
CREATE TABLE Roster (
	roster_id INT AUTO_INCREMENT PRIMARY KEY,
    roster_name VARCHAR(100) NOT NULL,
    user_id INT,
    league_id INT,
    wins INT DEFAULT 0,
    losses INT DEFAULT 0,
    total_fantasy_points INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (league_id) REFERENCES League(league_id)
    );

CREATE TABLE Team (
	team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    conference VARCHAR(50),
    division VARCHAR(50),
    record VARCHAR(10)
    );
    
CREATE TABLE Player (
	player_id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(100) NOT NULL,
    position VARCHAR(20),
    nba_team VARCHAR(100),
    team_id INT,
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
    );

CREATE TABLE Player_Game_Stats (
	stat_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    game_number INT,
    games_played INT,
    points INT,
    assists INT,
    rebounds INT,
    steals INT,
    blocks INT,
    turnovers INT,
    field_goal_percentage DECIMAL(5,2),
    three_point_percentage DECIMAL(5,2),
    free_throw_percentage DECIMAL(5.2),
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
    );

CREATE TABLE Total_Game_Stats (
	game_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT,
    player_id INT,
    game_number INT,
    game_points INT,
    game_assists INT,
    game_rebounds INT,
    game_steals INT,
    game_blocks INT,
    game_turnovers INT,
    game_3pm INT,
    game_fgm INT,
    game_ftm INT,
    FOREIGN KEY (team_id) REFERENCES Team(team_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
    );

CREATE TABLE Player_Averages (
	player_id INT PRIMARY KEY,
    average_points DECIMAL(5,2),
    average_rebounds DECIMAL(5,2),
    average_steals DECIMAL(5,2),
    average_assists DECIMAL(5,2),
    average_blocks DECIMAL(5,2),
    average_turnovers DECIMAL(5,2),
    average_field_goal_percentage DECIMAL(5,2),
    average_three_point_percentage DECIMAL(5,2),
    average_free_throw_percentage DECIMAL(5,2),
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
    );
    
    
