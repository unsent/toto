import requests


class ApiIntegration(object):

    soccer_leagues = ["soccer_turkey_super_league"]
    #   , "soccer_germany_bundesliga", "soccer_france_ligue_one", "soccer_epl", "soccer_netherlands_eredivisie", "soccer_spain_la_liga", "soccer_italy_serie_a", "soccer_uefa_champs_league"]
    bookmaker = "betsson"
    markets = "h2h"
    regions = "eu"
    odds_format = "decimal"
    api_key = "9100fa1b92182d18118f3b0b36f74065"

    # Create an empty list to store all the matches and odds
    def fetchMatchesWithOdds(self):
        all_matches = []

        for soccer_league in self.soccer_leagues:
            # Call the API to get odds for the given league and bookmaker
            response = requests.get(self.fetchDataByLeague(soccer_league)).json()

            # Loop over each match in the API response and filter by bookmaker
            for match in response:
                bookmaker_odds = []
                for bookmaker_data in match["bookmakers"]:
                    if bookmaker_data["key"] == self.bookmaker: bookmaker_odds = bookmaker_data["markets"][0]["outcomes"]
                    # print(bookmaker_odds)

                # Add the match and odds to the list of all matches
                all_matches.append(
                    {"id": match['id'], "description": f"{match['home_team']} vs {match['away_team']}",
                     "odds": bookmaker_odds}
                )
        return all_matches

    def fetchDataByLeague(self, soccer_league):
        url = f"https://api.the-odds-api.com/v4/sports/{soccer_league}/odds/?" \
              f"apiKey={self.api_key}" \
              f"&regions={self.regions}" \
              f"&markets={self.markets}" \
              f"&oddsFormat={self.odds_format}"
        return url
