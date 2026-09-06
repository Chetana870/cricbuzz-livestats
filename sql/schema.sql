-- Cricbuzz LiveStats — PostgreSQL Schema
-- Run this against the cricbuzz_livestats database

CREATE TABLE teams (
    team_id     SERIAL PRIMARY KEY,
    team_name   VARCHAR(100) NOT NULL UNIQUE,
    country     VARCHAR(100) NOT NULL
);

CREATE TABLE players (
    player_id      SERIAL PRIMARY KEY,
    full_name      VARCHAR(150) NOT NULL,
    country        VARCHAR(100) NOT NULL,
    playing_role   VARCHAR(50)  NOT NULL,   -- Batsman/Bowler/All-rounder/Wicket-keeper
    batting_style  VARCHAR(50),
    bowling_style  VARCHAR(50),
    team_id        INTEGER REFERENCES teams(team_id)
);
CREATE INDEX idx_players_country ON players(country);
CREATE INDEX idx_players_role ON players(playing_role);

CREATE TABLE venues (
    venue_id    SERIAL PRIMARY KEY,
    venue_name  VARCHAR(150) NOT NULL,
    city        VARCHAR(100) NOT NULL,
    country     VARCHAR(100) NOT NULL,
    capacity    INTEGER CHECK (capacity >= 0)
);
CREATE INDEX idx_venues_capacity ON venues(capacity);

CREATE TABLE series (
    series_id       SERIAL PRIMARY KEY,
    series_name     VARCHAR(150) NOT NULL,
    host_country    VARCHAR(100),
    match_type      VARCHAR(20),   -- Test/ODI/T20I
    start_date      DATE NOT NULL,
    total_matches   INTEGER CHECK (total_matches >= 0)
);
CREATE INDEX idx_series_start_date ON series(start_date);

CREATE TABLE matches (
    match_id             SERIAL PRIMARY KEY,
    series_id            INTEGER REFERENCES series(series_id),
    match_description    VARCHAR(200),
    match_format         VARCHAR(10) NOT NULL CHECK (match_format IN ('Test','ODI','T20I')),
    team1_id             INTEGER NOT NULL REFERENCES teams(team_id),
    team2_id             INTEGER NOT NULL REFERENCES teams(team_id),
    venue_id             INTEGER REFERENCES venues(venue_id),
    match_date           DATE NOT NULL,
    toss_winner_team_id  INTEGER REFERENCES teams(team_id),
    toss_decision        VARCHAR(10) CHECK (toss_decision IN ('bat','bowl')),
    winner_team_id       INTEGER REFERENCES teams(team_id),
    victory_margin       INTEGER,
    victory_type         VARCHAR(10) CHECK (victory_type IN ('runs','wickets')),
    match_status         VARCHAR(20)
);
CREATE INDEX idx_matches_date ON matches(match_date);
CREATE INDEX idx_matches_format ON matches(match_format);

CREATE TABLE batting_performances (
    performance_id   SERIAL PRIMARY KEY,
    match_id         INTEGER NOT NULL REFERENCES matches(match_id),
    player_id        INTEGER NOT NULL REFERENCES players(player_id),
    team_id          INTEGER NOT NULL REFERENCES teams(team_id),
    innings_number   INTEGER NOT NULL,
    batting_position INTEGER,
    runs_scored      INTEGER DEFAULT 0 CHECK (runs_scored >= 0),
    balls_faced      INTEGER DEFAULT 0 CHECK (balls_faced >= 0),
    fours            INTEGER DEFAULT 0,
    sixes            INTEGER DEFAULT 0,
    strike_rate      DECIMAL(6,2),
    is_out           BOOLEAN DEFAULT TRUE,
    dismissal_type   VARCHAR(30),
    UNIQUE (match_id, player_id, innings_number)
);
CREATE INDEX idx_batting_player ON batting_performances(player_id);
CREATE INDEX idx_batting_position ON batting_performances(batting_position);

CREATE TABLE bowling_performances (
    performance_id   SERIAL PRIMARY KEY,
    match_id         INTEGER NOT NULL REFERENCES matches(match_id),
    player_id        INTEGER NOT NULL REFERENCES players(player_id),
    team_id          INTEGER NOT NULL REFERENCES teams(team_id),
    innings_number   INTEGER NOT NULL,
    overs_bowled     DECIMAL(4,1) CHECK (overs_bowled >= 0),
    runs_conceded    INTEGER CHECK (runs_conceded >= 0),
    wickets_taken    INTEGER DEFAULT 0 CHECK (wickets_taken >= 0),
    economy_rate     DECIMAL(5,2),
    UNIQUE (match_id, player_id, innings_number)
);
CREATE INDEX idx_bowling_player ON bowling_performances(player_id);

CREATE TABLE fielding_performances (
    performance_id SERIAL PRIMARY KEY,
    match_id       INTEGER NOT NULL REFERENCES matches(match_id),
    player_id      INTEGER NOT NULL REFERENCES players(player_id),
    catches        INTEGER DEFAULT 0,
    stumpings      INTEGER DEFAULT 0,
    run_outs       INTEGER DEFAULT 0,
    UNIQUE (match_id, player_id)
);
CREATE INDEX idx_fielding_player ON fielding_performances(player_id);
