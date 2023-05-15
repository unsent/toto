import random

import ApiIntegration as integ
import UserInput as userinp

NUMBER_OF_ODDS_PER_MATCH = 3

api = integ.ApiIntegration()
userInput = userinp.UserInput()

print(api.fetchMatchesWithOdds())
all_matches = api.fetchMatchesWithOdds()

selectedMatches = userInput.selectMatches()
userInput.distributeMatches()

# Check all odds of selected matches and divide them into 5 groups: safest to riskiest
selectedMatchesOdds = []
for match_index in selectedMatches:
    for outcome in all_matches[match_index]["odds"]:
        outcome['id'] = all_matches[match_index]["id"]
        selectedMatchesOdds.append(outcome)

selectedMatchesOdds.sort(key=lambda x: x["price"])
print(selectedMatchesOdds)

window = len(selectedMatchesOdds) // 5
safestOdds = selectedMatchesOdds[:window]
saferOdds = selectedMatchesOdds[window:window * 2]
moderateOdds = selectedMatchesOdds[window * 2:window * 3]
riskierOdds = selectedMatchesOdds[window * 3:window * 4]
riskiestOdds = selectedMatchesOdds[window * 4:]


def allMatchesPlayed(playedMatchList):
    playedMatchIds = []
    for x in playedMatchList:
        if playedMatchIds.__contains__(x["id"]):
            continue
        playedMatchIds.append(x["id"])
    return len(playedMatchIds) == len(selectedMatches)


def selectOdds(noOfSafest, safestOdds, noOfSafer, saferOdds, noOfModerate, moderateOdds, noOfRiskier, riskierOdds,
               noOfRiskiest, riskiestOdds, playedMatchList):
    if noOfSafest == 0 and noOfSafer == 0 and noOfModerate == 0 and noOfRiskier == 0 and noOfRiskiest == 0 and not allMatchesPlayed(
            playedMatchList):
        return
    elif noOfSafest == 0 and noOfSafer == 0 and noOfModerate == 0 and noOfRiskier == 0 and noOfRiskiest == 0 and allMatchesPlayed(
                playedMatchList):
        return playedMatchList

    if noOfSafest != 0:
        index = random.randint(0, len(safestOdds) - 1)
        playedMatchList.append(safestOdds[index])
        safestOdds.__delitem__(index)
        return selectOdds(noOfSafest - 1, safestOdds, noOfSafer, saferOdds, noOfModerate, moderateOdds, noOfRiskier,
                          riskierOdds, noOfRiskiest, riskiestOdds, playedMatchList)
    elif noOfSafer != 0:
        index = random.randint(0, len(saferOdds) - 1)
        playedMatchList.append(saferOdds[index])
        saferOdds.__delitem__(index)
        return selectOdds(noOfSafest, safestOdds, noOfSafer - 1, saferOdds, noOfModerate, moderateOdds, noOfRiskier,
                          riskierOdds, noOfRiskiest, riskiestOdds, playedMatchList)
    elif noOfModerate != 0:
        index = random.randint(0, len(moderateOdds) - 1)
        playedMatchList.append(moderateOdds[index])
        moderateOdds.__delitem__(index)
        return selectOdds(noOfSafest, safestOdds, noOfSafer, saferOdds, noOfModerate - 1, moderateOdds, noOfRiskier,
                          riskierOdds, noOfRiskiest, riskiestOdds, playedMatchList)
    elif noOfRiskier != 0:
        index = random.randint(0, len(riskierOdds) - 1)
        playedMatchList.append(riskierOdds[index])
        riskierOdds.__delitem__(index)
        return selectOdds(noOfSafest, safestOdds, noOfSafer, saferOdds, noOfModerate, moderateOdds, noOfRiskier - 1,
                          riskierOdds, noOfRiskiest, riskiestOdds, playedMatchList)
    else:
        index = random.randint(0, len(riskiestOdds) - 1)
        playedMatchList.append(riskiestOdds[index])
        riskiestOdds.__delitem__(index)
        return selectOdds(noOfSafest, safestOdds, noOfSafer, saferOdds, noOfModerate, moderateOdds, noOfRiskier,
                          riskierOdds, noOfRiskiest - 1, riskiestOdds, playedMatchList)


print(selectOdds(userInput.safest, safestOdds,
                 userInput.safer, saferOdds,
                 userInput.moderate, moderateOdds,
                 userInput.riskier, riskierOdds,
                 userInput.riskiest, riskiestOdds,
                 []))
