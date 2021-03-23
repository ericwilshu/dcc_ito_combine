"""
This module provide code for creating a Dungeon Crawl Classics RPG 0 level character.

Classes:
    dccZeroLevelChar:

Dependencies:
    Modules:
        pprint
        random
        import_data
    Files:
        Table1_1_Ability_Score_Modifiers.csv
        Table1_2_Luck_Score.txt
        Human_Occupations.csv
        Dwarf_Occupations.csv
        Elf_Occupations.csv
        Halfling_Occupations.csv
        Table1_3a_Farmer_Type.txt
        Table1_3b_Animal_Type.txt
        Table1_3c_Whats_In_The_Cart.txt
        Table3_4_Equipment.txt
        AppendixL.csv
"""
#from pprint import pprint
from random import randint



class dccZeroLevelChar:
    """
    dccZeroLevelChar class is used to encapsulate all the data needed to fill out a
    character sheet for a Dungeon Crawl Classics RPG 0 level character, and the methods used
    to derive them. The tables from the rulebook must be imported by the import_data module.

    Properties:
        testSuitability -> boolean  If True, character will only be used if attribute modifiers sum to 0 or greater.
        noHuman -> boolean          If True, no human characters will be created.
        noDwarf -> boolean          If True, no dwarf characters will be created.
        noElf -> boolean            If True, no elf characters will be created.
        noHalfling -> boolean       If True, no halfling characters will be created.
        suitable -> boolean         True, if attribute modifiers total 0 or greater.

        strengthScore -> int
        agilityScore -> int
        staminaScore -> int
        intelligenceScore -> int
        personalityScore -> int
        luckScore -> int
        strengthModifier -> int
        agilityModifier -> int
        staminaModifier -> int
        intelligenceModifier -> int
        personalityModifier -> int
        luckModifier -> int
        luckySign -> string
        reflexSavingThrow -> int
        fortitudeSavingThrow -> int
        willpowerSavingThrow -> int
        race -> string
        racialTraits -> string
        occupation -> string
        trainedWeapon -> string
        tradeGoods -> string
        languages -> list
        money -> dictionary
        trainedWeaponDamage -> string
        trainedWeaponRange -> string
        equipment -> list
        speed -> string
        initiative -> int
        hitPoints -> int
        armorClass -> int

    Methods:
        __init__(self, dataDict, testSuitability=True, noHuman=False, noDwarf=False, noElf=False, noHalfling=False) -> dccZeroLevelChar
        diceRoll(self, numOfSides=6, numOfDice=1) -> int
        rollAbilityScores(self) -> None
        getAbilityScoreModifiers(self, data) -> None
        charIsSuitable(self) -> boolean
        getLuckySign(self, data) -> string
        getSavingThrows(self) -> tuple
        getRace(self) -> string
        getRacialTraits(self) -> list
        getOccupation(self, occupations, animals, farmers, whatsInCart) -> tuple
        getLanguages(self, languageList) -> list
        getStartingFunds(self) -> dictionary
        getWeaponDamage(self) -> tuple
        getEquipment(self, data) -> list
        getSpeed(self) -> string
        getInitiative(self) -> int
        getHitPoints(self) -> int
        getArmorClass(self) -> int
        __str__(self) -> string
    """


    def __init__(self, dataDict, testSuitability=True, noHuman=False, noDwarf=False, noElf=False, noHalfling=False):
        """
        Initialize a new dccZeroLevelChar.

        Args:
            dataDict: a dictinary containing all the table data from the character
                creation section of the Dungeon Crawl Classics RPG rulebook.
            testSuitability: a boolean telling whether we want to check the suitability
                of the attribute rolls.
            noHuman: Make sure the dccZeroLevelChar is not a human.
            noDwarf: Make sure the dccZeroLevelChar is not a dwarf.
            noElf: Make sure the dccZeroLevelChar is not an elf.
            noHalfling: Make sure the dccZeroLevelChar is not a halfling.
        """

        #At least one character race must be allowed.
        #If all the noRace args are set to True, we ignore them and set them all to False.
        if noHuman and noDwarf and noElf and noHalfling:
            noHuman = noDwarf = noElf = noHalfling = False

        self.dataDict = dataDict
        self.testSuitability = testSuitability
        self.noHuman = noHuman
        self.noDwarf = noDwarf
        self.noElf = noElf
        self.noHalfling = noHalfling

        self.rollAbilityScores()
        self.getAbilityScoreModifiers(dataDict["Ability Score Modifiers"])

        #If we are testing for suitability, we may have to reroll a few times.
        if self.testSuitability:
            self.suitable = self.charIsSuitable()
            while not self.suitable:
                self.rollAbilityScores()
                self.getAbilityScoreModifiers(dataDict["Ability Score Modifiers"])
                self.suitable = self.charIsSuitable()


        self.luckySign = self.getLuckySign(dataDict["Luck Scores"])
        self.reflexSavingThrow, self.fortitudeSavingThrow, self.willpowerSavingThrow = self.getSavingThrows()
        self.race = self.getRace()
        self.racialTraits = self.getRacialTraits()
        self.occupation, self.trainedWeapon, self.tradeGoods = self.getOccupation(dataDict[self.race + " Occupation"], dataDict["Animal Type"], dataDict["Farmer Type"], dataDict["What's In The Cart"])
        self.languages = self.getLanguages(dataDict["Languages"])
        self.money = self.getStartingFunds()
        self.trainedWeaponDamage, self.trainedWeaponRange = self.getWeaponDamage()
        self.equipment = self.getEquipment(dataDict["Equipment"])
        self.speed = self.getSpeed()
        self.initiative = self.getInitiative()
        self.hitPoints = self.getHitPoints()
        self.armorClass = self.getArmorClass()


    def diceRoll(self, numOfSides=6, numOfDice=1):
        """
        Return the result of a simulated a dice roll.

        Args:
            numOfSides: The number of sides on the dice to be used.
            numOfDice: The number of dice to roll and add up the results of.
        """
        sum = 0
        for i in range(numOfDice):
            sum += randint(1, numOfSides)
        return sum


    def rollAbilityScores(self):
        """Set the attribute scores of the dccZeroLevelChar."""
        self.strengthScore = self.diceRoll(6, 3)
        self.agilityScore = self.diceRoll(6, 3)
        self.staminaScore = self.diceRoll(6, 3)
        self.intelligenceScore = self.diceRoll(6, 3)
        self.personalityScore = self.diceRoll(6, 3)
        self.luckScore = self.diceRoll(6, 3)


    def getAbilityScoreModifiers(self, data):
        """
        Set the attribute modifiers of the dccZeroLevelChar.

        Args:
            data: Dictionary containing Table1_1_Ability_Score_Modifiers data
                from the Dungeon Crawl Classics RPG rulebook.
        """
        self.strengthModifier = data[self.strengthScore]["Modifier"]
        self.agilityModifier = data[self.agilityScore]["Modifier"]
        self.staminaModifier = data[self.staminaScore]["Modifier"]
        self.intelligenceModifier = data[self.intelligenceScore]["Modifier"]
        self.personalityModifier = data[self.personalityScore]["Modifier"]
        self.luckModifier = data[self.luckScore]["Modifier"]
        #self.wizardSpellsKnown = data[self.intelligenceScore]["Wizard Spells Known"]
        #self.maxSpellLevel = data[self.intelligenceScore]["Max Spell Level"]


    def charIsSuitable(self):
        """
        Add up all attribute modifiers of the dccZeroLevelChar.
        Return True if they add up to at least 0, False otherwise.
        """
        suitability = 0
        suitability += self.strengthModifier
        suitability += self.agilityModifier
        suitability += self.staminaModifier
        suitability += self.intelligenceModifier
        suitability += self.personalityModifier
        suitability += self.luckModifier
        return suitability >= 0


    def getLuckySign(self, data):
        """
        Return the lucky sign of the dccZeroLevelChar.

        Args:
            data: List containing Table1_2_Luck_Score data from the Dungeon
                Crawl Classics RPG rulebook.
        """
        return data[self.diceRoll(30, 1)-1]


    def getSavingThrows(self):
        """Return the saving throw modifiers of the dccZeroLevelChar as a tuple."""
        reflex = self.agilityModifier
        fortitude = self.staminaModifier
        willpower = self.personalityModifier
        if "Lucky sign: Saving throws" in self.luckySign:
            reflex += self.luckModifier
            fortitude += self.luckModifier
            willpower += self.luckModifier
        if "Struck by lightning" in self.luckySign:
            reflex += self.luckModifier
        if "Lived through famine" in self.luckySign:
            fortitude += self.luckModifier
        if "Resisted temptation" in self.luckySign:
            willpower += self.luckModifier
        return (reflex, fortitude, willpower)


    def getRace(self):
        """Return the dccZeroLevelChar race, based on args passed to the __init__ method."""
        race_okay = False
        while not race_okay:
            race_roll = self.diceRoll(10, 1)
            if race_roll == 1 and not self.noDwarf:
                race = "Dwarf"
                race_okay = True
            elif race_roll == 2 and not self.noElf:
                race = "Elf"
                race_okay = True
            elif race_roll == 3 and not self.noHalfling:
                race = "Halfling"
                race_okay = True
            elif not self.noHuman:
                race = "Human"
                race_okay = True

        return race


    def getRacialTraits(self):
        """Return a list of the dccZeroLevelChar racial traits."""
        if self.race == "Human":
            return []
        elif self.race == "Dwarf":
            return ["Infravision", "Underground skills"]
        elif self.race == "Elf":
            return ["Infravision",
                    "Immune to magic sleep/paralysis",
                    "Heightened senses",
                    "Iron vulnerability"]
        else:
            return ["Infravision", "Small size"]


    def getOccupation(self, occupations, animals, farmers, whatsInCart):
        """
        Return the occupation, starting weapon, and trade good of the dccZeroLevelChar.

        Args:
            occupations: Dictionary containing Table1_3_Occupation2 data from
                the  Dungeon Crawl Classics RPG rulebook.
            animals: List containing possible animals owned as trade goods.
            farmers: List containing types of farmers.
            whatsInCart: List containing things that might fill a cart owned as
                a trade good.
        """
        if self.race == "Human":
            occupation_range = 70
        else:
            occupation_range = 10

        occ_roll = self.diceRoll(occupation_range, 1)
        for occupation in occupations:
            if occ_roll <= int(occupation):
                job = occupations[occupation]["Occupation"]
                weapon = occupations[occupation]["Trained Weapon"]
                goods = occupations[occupation]["Trade Goods"]
                break

        #Occupations that get ranged weapons start with a little ammo.
        if weapon == "Shortbow" or weapon == "Sling":
            weapon = weapon + " + " + str(self.diceRoll()) + " ammo"

        #For occupations that deal with animal ownership, roll what animal is owned.
        if job == "Dwarven herder" or job == "Herder" or job == "Farmer":
            dieRoll = self.diceRoll(20, 1)
            if dieRoll > 14:
                goods = animals[dieRoll - 14]

        #For farmers, roll what kind of farming they know.
        if job == "Farmer":
            job = farmers[self.diceRoll(8, 1)-1] + " farmer"

        #For a wainwright, roll what their cart is full of.
        if job == "Wainwright":
            goods = "Pushcart full of " + whatsInCart[self.diceRoll()-1]

        return (job, weapon, goods)


    def getLanguages(self, languageList):
        """
        Return a list of languages known by the dccZeroLevelChar.

        Args:
            languageList: Dictionary containing language data from AppendixL in
                the Dungeon Crawl Classics RPG rulebook."""


        #This little sub-method returns one random language from the list of languages
        #for the character's race.
        def getOneLanguage(languageList):
            roll = self.diceRoll(100, 1)
            for lang in languageList:
                if languageList[lang][self.race] == '-':
                    continue
                elif roll <= int(languageList[lang][self.race]):
                    return lang


        #Everybody knows common.
        languages = ["Common"]
        #Low intelligence characters are illiterate.
        if self.intelligenceScore <= 5:
            languages.append("Illiterate")
            return languages
        if self.intelligenceScore <= 7:
            return languages
        #Demi-humans may know their own language!
        if self.race in ["Dwarf", "Elf", "Halfling"] and self.intelligenceScore >= 8:
            languages.append(self.race)

        #Use intelligence (and possibly luck) modifier, to find how many more
        #languages the character knows.
        bonusLangs = int(self.intelligenceModifier)

        if "Birdsong" in self.luckySign:
            bonusLangs += int(self.luckModifier)

        #Roll for each bonus language known, rerolling in the case of doubles.
        #Use the getOneLanguage method from above.
        if bonusLangs > 0:
            while bonusLangs > 0:
                newLang = getOneLanguage(languageList)
                while newLang in languages:
                    newLang = getOneLanguage(languageList)
                languages.append(newLang)
                bonusLangs -= 1

        return languages


    def getStartingFunds(self):
        """
        Return the starting money of the dccZeroLevelChar in a dictionary.

        GP = 'gold pieces',
        SP = 'silver pieces',
        CP = 'copper pieces'
        """
        #Most character start with 5d12 coppers.
        money = {"GP":0, "SP":0, "CP":0}
        money["CP"] += self.diceRoll(12, 5)

        #Some occupations start richer.
        if self.occupation == "Halfling trader":
            money["SP"] += 20
        elif self.occupation == "Halfling moneylender":
            money["GP"] += 5
            money["SP"] += 10
            money["CP"] += 200
        elif self.occupation == "Merchant":
            money["GP"] += 4
            money["SP"] += 14
            money["CP"] += 27
        elif self.occupation == "Tax collector":
            money["CP"] += 100

        return money


    def getWeaponDamage(self):
        """Return the damage and range of the dccZeroLevelChar starting weapon,"""
        weapon = self.trainedWeapon.lower()

        if "dagger" in weapon:
            damage = "1d4"
            range = "0/0/0"
        elif "spear" in weapon:
            damage = "1d8"
            range = "0/0/0"
        elif "staff" in weapon:
            damage = "1d4"
            range = "0/0/0"
        elif "club" in weapon:
            damage = "1d4"
            range = "0/0/0"
        elif "axe" in weapon:
            damage = "1d6"
            range = "10/20/30*"
        elif "short sword" in weapon:
            damage = "1d6"
            range = "0/0/0"
        elif "dart" in weapon:
            damage = "1d4"
            range = "20/40/60*"
        elif "shortbow" in weapon:
            damage = "1d6"
            range = "50/100/150"
        elif "sling" in weapon:
            damage = "1d4"
            range = "40/80/160*"
        elif "longsword" in weapon:
            damage = "1d8"
            range = "0/0/0"
        elif "mace" in weapon:
            damage = "1d6"
            range = "0/0/0"
        else:
            damage = "1d3 subdual"
            range = "0/0/0"

        return (damage, range)


    def getEquipment(self, data):
        """
        Return the dccZeroLevelChar starting equipment as a list.

        Args:
            data: List containing Table3_4_Equipment data from the Dungeon
                Crawl Classics RPG rulebook.
        """
        equipment = []
        #Include damage and range with weapon in equipment list.
        weapon = self.trainedWeapon + " " + self.trainedWeaponDamage + " " + self.trainedWeaponRange
        equipment.append(weapon)
        if self.tradeGoods != '':
            equipment.append(self.tradeGoods)
        #Pick a random bonus possession!
        equipment.append(data[self.diceRoll(24, 1)-1])

        return equipment


    def getSpeed(self):
        """Return the dccZeroLevelChar starting speed in feet per round."""
        speed = 30
        if self.race in ["Dwarf", "Halfling"]:
            speed = 20

        if "Wild child" in self.luckySign:
            speed += self.luckModifier * 5

        #Add an apostrophe to the number to indicate feet per round.
        speed = str(speed) + "'"

        return speed


    def getInitiative(self):
        """Return the dccZeroLevelChar initiative modifier."""
        initiative = self.agilityModifier

        if "Speed of the cobra" in self.luckySign:
            initiative += self.luckModifier

        return initiative


    def getHitPoints(self):
        """Return the dccZeroLevelChar starting hit points."""
        hitPoints = self.diceRoll(4, 1) + self.staminaModifier

        if "Bountiful harvest" in self.luckySign:
            hitPoints += self.luckModifier
        #Need to have at least 1 hit point.
        if hitPoints < 1:
            hitPoints = 1

        return hitPoints


    def getArmorClass(self):
        """Return the dccZeroLevelChar starting armor class."""
        armorClass = 10 + self.agilityModifier
        if self.tradeGoods == "Leather armor":
            armorClass += 2
        elif self.tradeGoods == "Hide armor":
            armorClass += 3
        elif self.tradeGoods == "Shield":
            armorClass += 1

        if "Charmed house" in self.luckySign:
            armorClass += self.luckModifier

        return armorClass


    def __str__(self):
        """Return a string with all properties of this dccZeroLevelChar, with descriptive labels."""
        printList = [   "Strength score: " + str(self.strengthScore),
                        "Strength modifier: " + str(self.strengthModifier),
                        "Agility score: " + str(self.agilityScore),
                        "Agility modifier: " + str(self.agilityModifier),
                        "Stamina score: " + str(self.staminaScore),
                        "Stamina modifier: " + str(self.staminaModifier),
                        "Intelligence score: " + str(self.intelligenceScore),
                        "Intelligence modifier: " + str(self.intelligenceModifier),
                        "Personality score: " + str(self.personalityScore),
                        "Personality modifier: " + str(self.personalityModifier),
                        "Luck score: " + str(self.luckScore),
                        "Luck modifier: " + str(self.luckModifier),
                        #"Wizard spells known: " + str(self.wizardSpellsKnown),
                        #"Max spell level: " + str(self.maxSpellLevel),
                        "Luck sign: " + str(self.luckySign),
                        "Reflex saving throw: " + str(self.reflexSavingThrow),
                        "Fortitude saving throw: " + str(self.fortitudeSavingThrow),
                        "Willpower saving throw: " + str(self.willpowerSavingThrow),
                        "Race: " + str(self.race),
                        "Racial traits: " + str(self.racialTraits),
                        "Occupation: " + str(self.occupation),
                        "Trained weapon: " + str(self.trainedWeapon),
                        "Trade goods: " + str(self.tradeGoods),
                        "Languages: " + str(self.languages),
                        "Money: " + str(self.money),
                        "Equipment: " + str(self.equipment),
                        "Speed: " + str(self.speed),
                        "Initiative: " + str(self.initiative),
                        "Hit points: " + str(self.hitPoints),
                        "Armor class: " + str(self.armorClass)
                    ]

        return '\n'.join(printList)
