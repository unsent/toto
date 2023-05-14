import requests
import random
from operator import attrgetter
import  itertools 
from math import pow


soccer_leagues = ["soccer_turkey_super_league"]
                #   , "soccer_germany_bundesliga", "soccer_france_ligue_one", "soccer_epl", "soccer_netherlands_eredivisie", "soccer_spain_la_liga", "soccer_italy_serie_a", "soccer_uefa_champs_league"]
bookmaker = "betsson"
markets = "h2h"
regions = "eu"
odds_format = "decimal"
api_key = "9100fa1b92182d18118f3b0b36f74065"

# Create an empty list to store all the matches and odds
all_matches = []

# Loop over each soccer league
for soccer_league in soccer_leagues:
    # Call the API to get odds for the given league and bookmaker
    url = f"https://api.the-odds-api.com/v4/sports/{soccer_league}/odds/?apiKey={api_key}&regions={regions}&markets={markets}&oddsFormat={odds_format}"
    response = requests.get(url).json()

    # Loop over each match in the API response and filter by bookmaker
    for match in response:
        bookmaker_odds = []
        for bookmaker_data in match["bookmakers"]:
            if bookmaker_data["key"] == bookmaker:
                bookmaker_odds = bookmaker_data["markets"][0]["outcomes"]
                # print(bookmaker_odds)

        # Add the match and odds to the list of all matches
        all_matches.append(
            {"id" : match['id'], "description": f"{match['home_team']} vs {match['away_team']}", "odds": bookmaker_odds}
        )

# Print all the match descriptions numbered 01 to n
for i, match in enumerate(all_matches):
    print(f"{i+1:02d}. {match['description']}")

# Ask user for selected matches
selected_matches = input("Enter the selected matches (e.g. 01,02,03): ")
selected_matches = [int(x.strip()) - 1 for x in selected_matches.split(",")]

# Check all odds of selected matches and divide them into 5 groups: safest to riskiest
selected_odds = []
for match_index in selected_matches:
    for outcome in all_matches[match_index]["odds"]:
        outcome['index'] = match_index
        outcome['id'] = all_matches[match_index]["id"]
        selected_odds.append(outcome)
        # print(outcome)

# The options for each index
options = [['1', '0', '2'] for _ in range(3)]

# Generate all possible combinations
combinations = list(itertools.product(*selected_odds))

# Print the combinations
for i, c in enumerate(combinations):
    print(f"{i+1}: {', '.join([f'index: {j} : {c[j]}' for j in range(len(c))])}")

num_odds = len(selected_odds)
group_size = num_odds // 5
selected_odds.sort(key=lambda x: x["price"])

# Ask user's desired amount of selection in 5 groups: safest to riskiest
num_safest = int(input("How many odds do you want to select in the safest group? "))

num_safer = int(input("How many odds do you want to select in the safer group? "))

num_moderate = int(input("How many odds do you want to select in the moderate group? "))

num_riskier = int(input("How many odds do you want to select in the riskier group? "))

num_riskiest = int(input("How many odds do you want to select in the riskiest group? "))

# Check if the input values are valid
if num_safest + num_safer + num_moderate + num_riskier + num_riskiest> len(selected_odds):
    print("Error: The sum of matches in risk groups cannot be greater than the number of selected odds.")
    exit()

if num_safest + num_safer + num_moderate + num_riskier + num_riskiest< len(selected_matches):
    print("Error: The sum of matches in risk groups cannot be smaller than the number of selected matches.")
    exit()

# Ask user for number of selected matches with 2 and 3 odds
num_2_odds = int(input("How many matches would you like to select with 2 odds? "))

num_3_odds = int(input("How many matches would you like to select with 3 odds? "))

# Check if the input values are valid
if num_2_odds + num_3_odds*2 + len(selected_matches) > len(selected_odds):
    print("Error: The sum of desired odds cannot be greater than the number of selected odds.")
    exit()

if num_2_odds + num_3_odds*2 + len(selected_matches) != num_safest + num_safer + num_moderate + num_riskier + num_riskiest:
    print("Error: The sum of desired odds needs to be equal to desired number of selected odds in risk groups.")
    exit()

# Check if the input values are valid
if num_2_odds + num_3_odds > len(selected_matches):
    print("Error: The sum of matches with 2 odds and 3 odds cannot be greater than the number of selected matches.")
    exit()

