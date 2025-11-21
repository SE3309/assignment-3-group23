import random
from datetime import date, timedelta

from faker import Faker
import mysql.connector

fake = Faker()

# ========== CONFIG ==========

DB_NAME = "fantasy_league"

MYSQL_CONFIG = {
     "host": "127.0.0.1",        # Localhost → SSH tunnel. You are NOT connecting to EC2 directly.
    "user": "appuser",           # MySQL username created on EC2 MySQL instance
    "password": "mypassword",    # Password for appuser
    "database": "fantasy_league",
    "port": 3307                 # MUST match the SSH tunnel port. If this is wrong → connection fails.
}

def connect():
    """
    Opens and returns a MySQL connection.
    Keeping this in a function means it's easy to modify connection logic later.
    """
    return mysql.connector.connect(**MYSQL_CONFIG)


# ========== GENERATORS ==========

def generate_users(cur, num_users=120):
    """
    Generate fake users (admin, owner, player roles).
    This function MUST run first because many tables depend on User.user_id.
    """
    print(f"Generating {num_users} users...")
    roles = ["Owner", "Player", "Admin"]  # categories of users in your fantasy app

    for i in range(num_users):

        # Basic fake profile creation
        username = f"user_{i + 1}"          # predictable, reproducible usernames
        email = f"{username}@example.com"   # matches username
        password = "password123"            # static for seeded data
        role = random.choices(
            roles,
            weights=[0.2, 0.7, 0.1]         # 70% players, 20% owners, 10% admins
        )[0]
        name = fake.name()

        # INSERT statement
        cur.execute(
            """
            INSERT INTO User (username, email, password, role, name)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (username, email, password, role, name)
        )


def generate_leagues(cur, num_leagues=5):
    """
    Create a small number of fantasy leagues, each owned by a random user.
    Requires that the User table is already populated.
    """
    print(f"Generating {num_leagues} leagues...")

    # Fetch user IDs to assign as league creators.
    cur.execute("SELECT user_id FROM User;")
    user_ids = [row[0] for row in cur.fetchall()]

    point_systems = ["standard", "ppr", "half_ppr"]  # league rule variations

    for i in range(num_leagues):
        league_name = f"League {i + 1}"
        season_year = "2024/2025"                   # static but could be randomized
        creator_user_id = random.choice(user_ids)   # assign any user as creator
        point_system = random.choice(point_systems)

        # Insert league row
        cur.execute(
            """
            INSERT INTO League (league_name, season_year, creator_user_id, point_system)
            VALUES (%s, %s, %s, %s)
            """,
            (league_name, season_year, creator_user_id, point_system)
        )


def generate_teams(cur, num_teams=30):
    """
    Insert real-world NBA teams (fictionalized), used by Player as a parent FK.
    """
    print(f"Generating {num_teams} teams...")

    conferences = ["East", "West"]                   # NBA-like
    divisions = ["North", "South", "Atlantic", "Central", "Pacific"]

    for i in range(num_teams):
        team_name = f"Team {i + 1}"                  # simple naming style
        city = fake.city()                           # random city for flavor
        conference = random.choice(conferences)
        division = random.choice(divisions)
        record = f"{random.randint(20, 60)}-{random.randint(10, 40)}"
        # Example: "47-29"

        # Insert row
        cur.execute(
            """
            INSERT INTO Team (team_name, city, conference, division, record)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (team_name, city, conference, division, record)
        )


def generate_players(cur, num_players=350):
    """
    Create hundreds of fake basketball players.
    Each player belongs to a team (FK dependency).
    """
    print(f"Generating {num_players} players...")

    # Fetch list of all valid teams
    cur.execute("SELECT team_id, team_name FROM Team;")
    teams = cur.fetchall()                           # list of (team_id, team_name)
    team_ids = [t[0] for t in teams]                 # extract only IDs

    positions = ["PG", "SG", "SF", "PF", "C"]        # NBA positions

    for _ in range(num_players):
        player_name = fake.name()
        position = random.choice(positions)
        team_id = random.choice(team_ids)            # assign player to random team

        # Find team_name from team_id (inefficient but functional)
        nba_team = teams[[t[0] for t in teams].index(team_id)][1]

        # Insert into Player table
        cur.execute(
            """
            INSERT INTO Player (player_name, position, nba_team, team_id)
            VALUES (%s, %s, %s, %s)
            """,
            (player_name, position, nba_team, team_id)
        )


def generate_rosters(cur, rosters_per_league=10, players_per_roster=12):
    """
    Create rosters.
    NOTE: This creates the roster *itself* but does NOT map players to rosters
          because there is no Roster_Player join table yet.
    """
    print("Generating rosters...")

    # Load all FK options
    cur.execute("SELECT league_id FROM League;")
    league_ids = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT user_id FROM User;")
    user_ids = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT player_id FROM Player;")
    player_ids = [row[0] for row in cur.fetchall()]

    roster_ids = []          # will collect new roster primary keys

    # Create several rosters per league
    for league_id in league_ids:
        for i in range(rosters_per_league):
            user_id = random.choice(user_ids)        # roster owner
            roster_name = f"Roster_{league_id}_{i + 1}"
            wins = random.randint(0, 20)
            losses = random.randint(0, 20)
            total_fantasy_points = random.randint(500, 5000)

            # Insert roster
            cur.execute(
                """
                INSERT INTO Roster (roster_name, user_id, league_id, wins, losses, total_fantasy_points)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (roster_name, user_id, league_id, wins, losses, total_fantasy_points)
            )

            roster_ids.append(cur.lastrowid)  # capture auto-increment ID for future player assignment


def generate_player_game_stats(cur, num_games_per_player=40):
    """
    Create granular per-game stats for each player.
    This table is large: (num_players * num_games_per_player).
    It must exist BEFORE generating Total_Game_Stats.
    """
    print("Generating player game stats...")

    # Get all player IDs (so every player gets 40 games)
    cur.execute("SELECT player_id FROM Player;")
    player_ids = [row[0] for row in cur.fetchall()]

    for player_id in player_ids:

        # Each loop generates a full season for this player
        for game_number in range(1, num_games_per_player + 1):

            # Fake basic stats
            points = random.randint(0, 50)
            assists = random.randint(0, 15)
            rebounds = random.randint(0, 20)
            steals = random.randint(0, 5)
            blocks = random.randint(0, 5)
            turnovers = random.randint(0, 7)

            # Shooting percentages (not linked to makes)
            fg_pct = round(random.uniform(30, 70), 2)
            tp_pct = round(random.uniform(25, 60), 2)
            ft_pct = round(random.uniform(60, 95), 2)

            # Insert into Player_Game_Stats
            cur.execute(
                """
                INSERT INTO Player_Game_Stats
                    (player_id, game_number, games_played, points, assists, rebounds,
                     steals, blocks, turnovers,
                     field_goal_percentage, three_point_percentage, free_throw_percentage)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    player_id,
                    game_number,
                    num_games_per_player,     # means "season length", not "games played to date"
                    points,
                    assists,
                    rebounds,
                    steals,
                    blocks,
                    turnovers,
                    fg_pct,
                    tp_pct,
                    ft_pct
                )
            )


def generate_total_game_stats(cur):
    """
    Creates another layer of stats (team + player per game).
    Uses Player_Game_Stats as the source.
    Ensures certain basketball constraints (e.g., FGM >= 3PM).
    """
    print("Generating total game stats...")

    # Perform a JOIN to get combined player/team data per game
    cur.execute("""
        SELECT p.player_id, p.team_id, s.game_number,
               s.points, s.assists, s.rebounds,
               s.steals, s.blocks, s.turnovers
        FROM Player p
        JOIN Player_Game_Stats s ON p.player_id = s.player_id;
    """)

    rows = cur.fetchall()          # could be ~14k rows

    for (
        player_id, team_id, game_number,
        points, assists, rebounds, steals, blocks, turnovers
    ) in rows:

        # Reuse stats directly
        game_points = points
        game_assists = assists
        game_rebounds = rebounds
        game_steals = steals
        game_blocks = blocks
        game_turnovers = turnovers

        # Generate 3-pointers made
        game_3pm = random.randint(0, 8)

        # Make sure FGM cannot be less than 3PM (logical constraint)
        min_fgm = game_3pm
        max_fgm = max(min_fgm, game_points // 2 + 5)

        game_fgm = random.randint(min_fgm, max_fgm)

        # Generate free throws made
        game_ftm = random.randint(0, 10)

        # Insert row
        cur.execute(
            """
            INSERT INTO Total_Game_Stats
                (team_id, player_id, game_number,
                 game_points, game_assists, game_rebounds,
                 game_steals, game_blocks, game_turnovers,
                 game_3pm, game_fgm, game_ftm)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                team_id,
                player_id,
                game_number,
                game_points,
                game_assists,
                game_rebounds,
                game_steals,
                game_blocks,
                game_turnovers,
                game_3pm,
                game_fgm,
                game_ftm
            )
        )


def generate_player_averages(cur):
    """
    Recomputes the Player_Averages table based on Player_Game_Stats.
    This ensures averages are always in sync with raw stats.
    """
    print("Generating player averages from stats...")

    # Remove all rows (easier than UPDATE since averages change each run)
    cur.execute("DELETE FROM Player_Averages;")

    # Compute averages using pure SQL (faster, cleaner than Python loops)
    cur.execute(
        """
        INSERT INTO Player_Averages (
            player_id,
            average_points,
            average_rebounds,
            average_steals,
            average_assists,
            average_blocks,
            average_turnovers,
            average_field_goal_percentage,
            average_three_point_percentage,
            average_free_throw_percentage
        )
        SELECT
            player_id,
            AVG(points),
            AVG(rebounds),
            AVG(steals),
            AVG(assists),
            AVG(blocks),
            AVG(turnovers),
            AVG(field_goal_percentage),
            AVG(three_point_percentage),
            AVG(free_throw_percentage)
        FROM Player_Game_Stats
        GROUP BY player_id;
        """
    )


def main():
    """
    Main execution sequence.
    Order of function calls MUST respect foreign key dependencies.
    """
    conn = connect()
    cur = conn.cursor()

    # === GENERATION ORDER===
    # User → League → Team → Player → Roster → Game Stats → Totals → Averages
    generate_users(cur, num_users=120)
    generate_leagues(cur, num_leagues=5)
    generate_teams(cur, num_teams=30)
    generate_players(cur, num_players=350)
    generate_rosters(cur, rosters_per_league=10, players_per_roster=12)
    generate_player_game_stats(cur, num_games_per_player=40)
    generate_total_game_stats(cur)
    generate_player_averages(cur)

    # Commit all inserts to SQL
    conn.commit()

    # Cleanup
    cur.close()
    conn.close()
    print("Done!")


if __name__ == "__main__":
    main()
