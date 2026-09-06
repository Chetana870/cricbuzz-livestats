-- Expanded seed data v2 — bigger mix: more teams, players, venues, series,
-- and full batting lineups (consecutive positions) for several matches so
-- partnership-style queries (Q13) and depth-dependent queries return results.

TRUNCATE TABLE fielding_performances, bowling_performances, batting_performances,
    matches, series, players, venues, teams RESTART IDENTITY CASCADE;

INSERT INTO teams (team_name, country) VALUES
('India', 'India'),
('Australia', 'Australia'),
('England', 'England'),
('South Africa', 'South Africa'),
('New Zealand', 'New Zealand'),
('Pakistan', 'Pakistan'),
('Sri Lanka', 'Sri Lanka'),
('Bangladesh', 'Bangladesh'),
('West Indies', 'West Indies'),
('Afghanistan', 'Afghanistan');

INSERT INTO venues (venue_name, city, country, capacity) VALUES
('Wankhede Stadium', 'Mumbai', 'India', 33000),
('Melbourne Cricket Ground', 'Melbourne', 'Australia', 100000),
('Lord''s', 'London', 'England', 30000),
('Newlands', 'Cape Town', 'South Africa', 25000),
('Eden Park', 'Auckland', 'New Zealand', 42000),
('Gaddafi Stadium', 'Lahore', 'Pakistan', 27000),
('R.Premadasa Stadium', 'Colombo', 'Sri Lanka', 35000),
('Sher-e-Bangla Stadium', 'Dhaka', 'Bangladesh', 26000),
('Kensington Oval', 'Bridgetown', 'West Indies', 28000),
('Eden Gardens', 'Kolkata', 'India', 68000);

INSERT INTO players (full_name, country, playing_role, batting_style, bowling_style, team_id) VALUES
-- India
('Virat Kohli', 'India', 'Batsman', 'Right-hand bat', NULL, 1),
('Rohit Sharma', 'India', 'Batsman', 'Right-hand bat', NULL, 1),
('Shubman Gill', 'India', 'Batsman', 'Right-hand bat', NULL, 1),
('KL Rahul', 'India', 'Wicket-keeper', 'Right-hand bat', NULL, 1),
('Jasprit Bumrah', 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1),
('Ravindra Jadeja', 'India', 'All-rounder', 'Left-hand bat', 'Left-arm orthodox', 1),
('Mohammed Shami', 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1),
-- Australia
('Pat Cummins', 'Australia', 'Bowler', 'Right-hand bat', 'Right-arm fast', 2),
('Steve Smith', 'Australia', 'Batsman', 'Right-hand bat', NULL, 2),
('David Warner', 'Australia', 'Batsman', 'Left-hand bat', NULL, 2),
('Mitchell Starc', 'Australia', 'Bowler', 'Left-hand bat', 'Left-arm fast', 2),
('Travis Head', 'Australia', 'Batsman', 'Left-hand bat', NULL, 2),
('Marnus Labuschagne', 'Australia', 'Batsman', 'Right-hand bat', NULL, 2),
-- England
('Joe Root', 'England', 'Batsman', 'Right-hand bat', NULL, 3),
('Ben Stokes', 'England', 'All-rounder', 'Left-hand bat', 'Right-arm fast', 3),
('James Anderson', 'England', 'Bowler', 'Left-hand bat', 'Right-arm fast', 3),
('Harry Brook', 'England', 'Batsman', 'Right-hand bat', NULL, 3),
-- South Africa
('Quinton de Kock', 'South Africa', 'Wicket-keeper', 'Left-hand bat', NULL, 4),
('Kagiso Rabada', 'South Africa', 'Bowler', 'Right-hand bat', 'Right-arm fast', 4),
('Aiden Markram', 'South Africa', 'Batsman', 'Right-hand bat', NULL, 4),
-- New Zealand
('Kane Williamson', 'New Zealand', 'Batsman', 'Right-hand bat', NULL, 5),
('Trent Boult', 'New Zealand', 'Bowler', 'Right-hand bat', 'Left-arm fast', 5),
('Devon Conway', 'New Zealand', 'Batsman', 'Left-hand bat', NULL, 5),
-- Pakistan
('Babar Azam', 'Pakistan', 'Batsman', 'Right-hand bat', NULL, 6),
('Shaheen Afridi', 'Pakistan', 'Bowler', 'Left-hand bat', 'Left-arm fast', 6),
('Mohammad Rizwan', 'Pakistan', 'Wicket-keeper', 'Right-hand bat', NULL, 6),
-- Sri Lanka
('Kusal Mendis', 'Sri Lanka', 'Wicket-keeper', 'Right-hand bat', NULL, 7),
('Wanindu Hasaranga', 'Sri Lanka', 'All-rounder', 'Right-hand bat', 'Right-arm leg break', 7),
-- Bangladesh
('Shakib Al Hasan', 'Bangladesh', 'All-rounder', 'Left-hand bat', 'Left-arm orthodox', 8),
('Litton Das', 'Bangladesh', 'Wicket-keeper', 'Right-hand bat', NULL, 8),
-- West Indies
('Nicholas Pooran', 'West Indies', 'Wicket-keeper', 'Left-hand bat', NULL, 9),
('Jason Holder', 'West Indies', 'All-rounder', 'Right-hand bat', 'Right-arm fast-medium', 9),
-- Afghanistan
('Rashid Khan', 'Afghanistan', 'Bowler', 'Right-hand bat', 'Right-arm leg break', 10),
('Mohammad Nabi', 'Afghanistan', 'All-rounder', 'Right-hand bat', 'Right-arm off break', 10);

INSERT INTO series (series_name, host_country, match_type, start_date, total_matches) VALUES
('India tour of Australia 2024', 'Australia', 'Test', '2024-12-01', 4),
('England tour of India 2025', 'India', 'ODI', '2025-02-10', 3),
('Pakistan tri-series 2025', 'Pakistan', 'T20I', '2025-05-05', 5),
('South Africa vs New Zealand 2025', 'South Africa', 'Test', '2025-08-01', 2),
('Sri Lanka tour of Bangladesh 2025', 'Bangladesh', 'ODI', '2025-03-15', 3),
('West Indies vs Afghanistan 2025', 'West Indies', 'T20I', '2025-06-20', 3),
('India tour of England 2026', 'England', 'Test', '2026-06-01', 5);

INSERT INTO matches (series_id, match_description, match_format, team1_id, team2_id, venue_id, match_date,
                      toss_winner_team_id, toss_decision, winner_team_id, victory_margin, victory_type, match_status)
VALUES
(1, '1st Test', 'Test', 1, 2, 2, '2024-12-06', 1, 'bat', 2, 8, 'wickets', 'Completed'),
(1, '2nd Test', 'Test', 1, 2, 1, '2024-12-26', 2, 'bowl', 1, 5, 'wickets', 'Completed'),
(2, '1st ODI', 'ODI', 3, 1, 1, '2025-02-12', 1, 'bat', 1, 45, 'runs', 'Completed'),
(2, '2nd ODI', 'ODI', 3, 1, 1, '2025-02-15', 3, 'bowl', 3, 3, 'wickets', 'Completed'),
(3, '1st T20I', 'T20I', 6, 4, 6, '2025-05-06', 6, 'bat', 6, 20, 'runs', 'Completed'),
(3, '2nd T20I', 'T20I', 6, 5, 6, '2025-05-08', 5, 'bat', 6, 6, 'wickets', 'Completed'),
(4, '1st Test', 'Test', 4, 5, 4, '2025-08-02', 5, 'bat', 4, 88, 'runs', 'Completed'),
(5, '1st ODI', 'ODI', 7, 8, 7, '2025-03-16', 7, 'bat', 7, 35, 'runs', 'Completed'),
(5, '2nd ODI', 'ODI', 7, 8, 8, '2025-03-19', 8, 'bowl', 8, 4, 'wickets', 'Completed'),
(6, '1st T20I', 'T20I', 9, 10, 9, '2025-06-21', 9, 'bat', 9, 15, 'runs', 'Completed'),
(6, '2nd T20I', 'T20I', 9, 10, 9, '2025-06-23', 10, 'bat', 10, 7, 'wickets', 'Completed'),
(7, '1st Test', 'Test', 1, 3, 3, '2026-06-05', 3, 'bat', 1, 6, 'wickets', 'Completed');

-- Match 1: India vs Australia, 1st Test — full batting lineup, innings 1 (India) and 2 (Australia)
INSERT INTO batting_performances (match_id, player_id, team_id, innings_number, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, dismissal_type) VALUES
(1, 2, 1, 1, 1, 45, 90, 5, 0, 50.00, TRUE, 'bowled'),
(1, 3, 1, 1, 2, 32, 70, 3, 0, 45.71, TRUE, 'caught'),
(1, 1, 1, 1, 3, 76, 140, 8, 1, 54.28, TRUE, 'caught'),
(1, 4, 1, 1, 4, 28, 55, 2, 0, 50.90, TRUE, 'lbw'),
(1, 6, 1, 1, 5, 22, 40, 1, 0, 55.00, FALSE, NULL),
(1, 9, 2, 2, 1, 40, 88, 4, 0, 45.45, TRUE, 'bowled'),
(1, 10, 2, 2, 2, 58, 100, 6, 1, 58.00, TRUE, 'caught'),
(1, 12, 2, 2, 3, 92, 180, 10, 0, 51.11, TRUE, 'bowled'),
(1, 13, 2, 2, 4, 35, 70, 3, 0, 50.00, TRUE, 'caught');

INSERT INTO bowling_performances (match_id, player_id, team_id, innings_number, overs_bowled, runs_conceded, wickets_taken, economy_rate) VALUES
(1, 5, 1, 2, 22.0, 64, 4, 2.90),
(1, 7, 1, 2, 18.0, 50, 2, 2.78),
(1, 8, 2, 1, 18.4, 55, 3, 2.94),
(1, 11, 2, 1, 20.0, 60, 2, 3.00);

INSERT INTO fielding_performances (match_id, player_id, catches, stumpings, run_outs) VALUES
(1, 10, 2, 0, 0),
(1, 4, 1, 0, 1);

-- Match 2: India vs Australia, 2nd Test
INSERT INTO batting_performances (match_id, player_id, team_id, innings_number, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, dismissal_type) VALUES
(2, 2, 1, 1, 1, 30, 60, 3, 0, 50.00, TRUE, 'caught'),
(2, 1, 1, 1, 3, 103, 190, 12, 1, 54.21, TRUE, 'lbw'),
(2, 6, 1, 1, 5, 38, 70, 4, 0, 54.28, FALSE, NULL),
(2, 9, 2, 2, 1, 41, 88, 3, 0, 46.59, TRUE, 'caught'),
(2, 12, 2, 2, 3, 25, 60, 2, 0, 41.66, TRUE, 'bowled');

INSERT INTO bowling_performances (match_id, player_id, team_id, innings_number, overs_bowled, runs_conceded, wickets_taken, economy_rate) VALUES
(2, 5, 1, 2, 20.1, 48, 5, 2.38),
(2, 11, 2, 1, 24.0, 70, 2, 2.91);

-- Match 3: England vs India, 1st ODI
INSERT INTO batting_performances (match_id, player_id, team_id, innings_number, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, dismissal_type) VALUES
(3, 14, 3, 1, 3, 67, 74, 7, 1, 90.54, TRUE, 'caught'),
(3, 15, 3, 1, 4, 40, 35, 3, 2, 114.28, TRUE, 'bowled'),
(3, 1, 1, 2, 4, 88, 92, 9, 2, 95.65, TRUE, 'run out'),
(3, 2, 1, 2, 1, 30, 40, 2, 0, 75.00, TRUE, 'caught');

INSERT INTO bowling_performances (match_id, player_id, team_id, innings_number, overs_bowled, runs_conceded, wickets_taken, economy_rate) VALUES
(3, 5, 1, 1, 10.0, 42, 3, 4.20),
(3, 16, 3, 2, 10.0, 55, 1, 5.50);

-- Match 4: England vs India, 2nd ODI
INSERT INTO batting_performances (match_id, player_id, team_id, innings_number, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, dismissal_type) VALUES
(4, 15, 3, 1, 5, 71, 65, 6, 3, 109.23, FALSE, NULL),
(4, 17, 3, 1, 6, 22, 20, 2, 1, 110.00, TRUE, 'caught'),
(4, 2, 1, 2, 1, 55, 60, 7, 1, 91.66, TRUE, 'bowled'),
(4, 3, 1, 2, 2, 33, 38, 3, 1, 86.84, TRUE, 'caught');

INSERT INTO bowling_performances (match_id, player_id, team_id, innings_number, overs_bowled, runs_conceded, wickets_taken, economy_rate) VALUES
(4, 5, 1, 1, 10.0, 38, 2, 3.80);

-- Match 5: Pakistan vs South Africa, 1st T20I
INSERT INTO batting_performances (match_id, player_id, team_id, innings_number, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, dismissal_type) VALUES
(5, 24, 6, 1, 1, 62, 44, 6, 3, 140.90, TRUE, 'caught'),
(5, 26, 6, 1, 2, 30, 22, 3, 1, 136.36, TRUE, 'bowled'),
(5, 18, 4, 2, 2, 39, 30, 4, 1, 130.00, TRUE, 'bowled'),
(5, 20, 4, 2, 3, 28, 24, 2, 1, 116.66, TRUE, 'caught');

INSERT INTO bowling_performances (match_id, player_id, team_id, innings_number, overs_bowled, runs_conceded, wickets_taken, economy_rate) VALUES
(5, 25, 6, 2, 4.0, 28, 3, 7.00),
(5, 19, 4, 1, 4.0, 35, 1, 8.75);

-- Match 6: Pakistan vs New Zealand, 2nd T20I
INSERT INTO batting_performances (match_id, player_id, team_id, innings_number, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, dismissal_type) VALUES
(6, 24, 6, 1, 1, 45, 33, 5, 2, 136.36, TRUE, 'caught'),
(6, 21, 5, 2, 3, 51, 40, 4, 2, 127.50, FALSE, NULL),
(6, 23, 5, 2, 4, 20, 18, 1, 1, 111.11, TRUE, 'bowled');

INSERT INTO bowling_performances (match_id, player_id, team_id, innings_number, overs_bowled, runs_conceded, wickets_taken, economy_rate) VALUES
(6, 25, 6, 2, 4.0, 30, 2, 7.50),
(6, 22, 5, 1, 4.0, 25, 2, 6.25);

-- Match 7: South Africa vs New Zealand, 1st Test
INSERT INTO batting_performances (match_id, player_id, team_id, innings_number, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, dismissal_type) VALUES
(7, 18, 4, 1, 2, 84, 160, 9, 0, 52.50, TRUE, 'caught'),
(7, 20, 4, 1, 3, 46, 90, 4, 0, 51.11, TRUE, 'bowled'),
(7, 21, 5, 2, 3, 96, 200, 8, 0, 48.00, TRUE, 'lbw'),
(7, 23, 5, 2, 4, 30, 60, 2, 0, 50.00, FALSE, NULL);

INSERT INTO bowling_performances (match_id, player_id, team_id, innings_number, overs_bowled, runs_conceded, wickets_taken, economy_rate) VALUES
(7, 19, 4, 2, 26.0, 78, 4, 3.00),
(7, 22, 5, 1, 22.0, 66, 3, 3.00);

INSERT INTO fielding_performances (match_id, player_id, catches, stumpings, run_outs) VALUES
(7, 18, 3, 1, 0);

-- Match 8: Sri Lanka vs Bangladesh, 1st ODI
INSERT INTO batting_performances (match_id, player_id, team_id, innings_number, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, dismissal_type) VALUES
(8, 27, 7, 1, 1, 58, 65, 6, 1, 89.23, TRUE, 'caught'),
(8, 28, 7, 1, 2, 44, 50, 4, 0, 88.00, TRUE, 'bowled'),
(8, 29, 8, 2, 3, 39, 48, 3, 0, 81.25, TRUE, 'run out'),
(8, 30, 8, 2, 4, 20, 25, 1, 0, 80.00, TRUE, 'caught');

INSERT INTO bowling_performances (match_id, player_id, team_id, innings_number, overs_bowled, runs_conceded, wickets_taken, economy_rate) VALUES
(8, 29, 8, 1, 8.0, 40, 2, 5.00);

-- Match 9: Sri Lanka vs Bangladesh, 2nd ODI
INSERT INTO batting_performances (match_id, player_id, team_id, innings_number, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, dismissal_type) VALUES
(9, 27, 7, 1, 1, 33, 40, 3, 0, 82.50, TRUE, 'bowled'),
(9, 29, 8, 2, 3, 61, 70, 6, 1, 87.14, FALSE, NULL);

INSERT INTO bowling_performances (match_id, player_id, team_id, innings_number, overs_bowled, runs_conceded, wickets_taken, economy_rate) VALUES
(9, 28, 7, 2, 10.0, 45, 1, 4.50);

-- Match 10: West Indies vs Afghanistan, 1st T20I
INSERT INTO batting_performances (match_id, player_id, team_id, innings_number, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, dismissal_type) VALUES
(10, 31, 9, 1, 1, 55, 38, 5, 3, 144.73, TRUE, 'caught'),
(10, 32, 9, 1, 2, 28, 22, 2, 1, 127.27, TRUE, 'bowled'),
(10, 34, 10, 2, 2, 34, 30, 3, 1, 113.33, TRUE, 'lbw');

INSERT INTO bowling_performances (match_id, player_id, team_id, innings_number, overs_bowled, runs_conceded, wickets_taken, economy_rate) VALUES
(10, 33, 10, 2, 4.0, 25, 3, 6.25);

-- Match 11: West Indies vs Afghanistan, 2nd T20I
INSERT INTO batting_performances (match_id, player_id, team_id, innings_number, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, dismissal_type) VALUES
(11, 31, 9, 1, 1, 40, 30, 4, 1, 133.33, TRUE, 'bowled'),
(11, 34, 10, 2, 2, 47, 35, 4, 2, 134.28, FALSE, NULL);

INSERT INTO bowling_performances (match_id, player_id, team_id, innings_number, overs_bowled, runs_conceded, wickets_taken, economy_rate) VALUES
(11, 33, 10, 2, 4.0, 22, 2, 5.50);

-- Match 12: India vs England, 1st Test (2026)
INSERT INTO batting_performances (match_id, player_id, team_id, innings_number, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, is_out, dismissal_type) VALUES
(12, 2, 1, 1, 1, 62, 110, 6, 0, 56.36, TRUE, 'caught'),
(12, 1, 1, 1, 3, 118, 210, 14, 1, 56.19, TRUE, 'bowled'),
(12, 3, 1, 1, 4, 40, 80, 4, 0, 50.00, TRUE, 'lbw'),
(12, 14, 3, 2, 1, 45, 90, 4, 0, 50.00, TRUE, 'caught'),
(12, 15, 3, 2, 2, 71, 130, 7, 1, 54.61, TRUE, 'bowled');

INSERT INTO bowling_performances (match_id, player_id, team_id, innings_number, overs_bowled, runs_conceded, wickets_taken, economy_rate) VALUES
(12, 5, 1, 2, 24.0, 66, 4, 2.75),
(12, 16, 3, 1, 20.0, 58, 3, 2.90);

INSERT INTO fielding_performances (match_id, player_id, catches, stumpings, run_outs) VALUES
(12, 4, 2, 1, 0);
