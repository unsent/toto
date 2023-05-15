class UserInput:
    safest = 0
    safer = 0
    moderate = 0
    riskier = 0
    riskiest = 0

    def selectMatches(self):
        selected_matches = input("Enter the selected matches (e.g. 0,1,2): ")
        return [int(x) for x in selected_matches.split(",")]

    def distributeMatches(self):
        self.safest = int(input("How many odds do you want to select in the safest group? "))
        self.safer = int(input("How many odds do you want to select in the safer group? "))
        self.moderate = int(input("How many odds do you want to select in the moderate group? "))
        self.riskier = int(input("How many odds do you want to select in the riskier group? "))
        self.riskiest = int(input("How many odds do you want to select in the riskiest group? "))
