#Drew Childs, 12/2/2019, Program 7
import random
import math


class Bacteria:
    def __init__(self, resistance, health = 10, life_span = 15, birth_counter = 3):     #Initializes stats for bacteria
        self.resistance = resistance + random.randint(-1, 1)
        self.health = health
        self.life_span = life_span
        self.birth_counter = birth_counter
        if self.resistance < 1:             #makes sure resistance is between 1 and 10
            self.resistance = 1
        if self.resistance > 10:
            self.resistance = 10

    def __str__(self):      #returns stats for bacteria in form of string
        return ("H(%0.1f)    R(%d)    LS(%d)    BC(%d)" % (self.health, self.resistance, self.life_span, self.birth_counter))

    def is_alive(self):     #Determines if bacteria is still living
        if self.health > 0 and self.life_span > 0:
            return True
        else:
            return False

    def tick(self):     #Tick function for bacteria life span and birth counter
        self.birth_counter -= 1
        self.life_span -= 1

    def dose(self, dosage):     #applies dosage to bacteria health
        self.health -= dosage * (1/self.resistance)

    def reproduce(self):        #Ensures bacteria can reproduce
        if self.is_alive() == True and self.birth_counter <= 0:
            self.birth_counter = 3
            return Bacteria(self.resistance)


class Host(Bacteria):
    def __init__(self, bacteria_count):
        super().__init__(resistance = 3)        #inherits bacteria attributes
        self.bacteria_stats = []
        for each in range(bacteria_count):          #Creates new bacteria instance for desired amount of bacteria.
            self.bacteria_stats.append(Bacteria(3)) #adds them to list so attributes for individual bacteria can be called upon later

    def __str__(self):
        avg_health = 0
        avg_resistance = 0
        for each in self.bacteria_stats:        #calculating average health and resistance for bacteria group
            avg_health += each.health
            avg_resistance += each.resistance
        try:
            avg_health /= len(self.bacteria_stats)
            avg_resistance /= len(self.bacteria_stats)
        except:
            avg_health = math.nan       #only executes if there are no bacteria
            avg_resistance = math.nan
        return ("Count: %d\nAverage Health: %0.1f\nAverage Resistance: %0.1f" % (len(self.bacteria_stats), avg_health, avg_resistance))     #returns string containing bacteria stats

    def tick_host(self, with_dose = False):
        if with_dose == True:                       #I placed this if statement outside the loop instead of having one for loop so this redundant
            for bacteria in self.bacteria_stats:    #if statement wouldn't run thousands of times for no reason
                bacteria.dose(25)
                bacteria.tick()     #I have this function dose, tick, then reproduce
                new_bacteria = bacteria.reproduce()
                if bacteria.is_alive() == False:        #removes any dead bacteria
                    self.bacteria_stats.remove(bacteria)
                if new_bacteria != None:
                    self.bacteria_stats.append(new_bacteria)
        else:
            for bacteria in self.bacteria_stats:        #Same as above, just doesn't apply dosage
                bacteria.tick()
                new_bacteria = bacteria.reproduce()
                if bacteria.is_alive() == False:
                    self.bacteria_stats.remove(bacteria)
                if new_bacteria != None:
                    self.bacteria_stats.append(new_bacteria)


No_Dosage = Host(1)     #creates initial objects
Full_Dosage = Host(1)
Half_Dosage = Host(1)

for cycle in range(30):     #runs first 30 ticks for starting point for all
    No_Dosage.tick_host()
    Full_Dosage.tick_host()
    Half_Dosage.tick_host()

for dosage in range(15):        #Applies appropriate dosage to objects
    No_Dosage.tick_host()
    Full_Dosage.tick_host(True)
    if dosage % 2 == 0:
        Half_Dosage.tick_host()
    else:
        Half_Dosage.tick_host(True)

print("No Dosage:\n%s\n\nFull Dosage:\n%s\n\nHalf Dosed:\n%s" % (No_Dosage, Full_Dosage, Half_Dosage))  #prints what dosage was applied, then calls __str__ function in host to print stats
