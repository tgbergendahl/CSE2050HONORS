import random

class Contestant:
    def __init__(self, name):
        self.name = name
        self.pair = None
        self.probabilities = {}
        
    def add_pair(self, pair):
        self.pair = pair
        
    def check_pair(self, pair):
        return self.pair == pair
        
    def find_partner2(self, remaining):
        for potential_pair in remaining:
            if self.probabilities[potential_pair] != 0:
                return potential_pair
        
# worst-case scenario - only remaining potential partners 
# to pick from have already been guaranteed incompatible - just deal with it
        
        return remaining[0]
        
    def find_partner3(self, remaining):
    #pick contestant with highest "probability"
        new_dict = {contestant: self.probabilities[contestant] for contestant in remaining}
        
        return max(new_dict, key=new_dict.get)
        
    def find_partner4(self, remaining):
        first = None
        second = None
        third = None
        x = (len(remaining) / 1.5)
        for contestant in remaining:
            if contestant in self.probabilities:
                if self.probabilities[contestant] > x:
                    first = contestant
                else:
                    third = contestant
            else:
                second = contestant
        
        if first:
            return first
            
        elif second:
            return second
        
        else:
            return third
        
    def initialize_probabilities(self, contestants):
        contestants.remove(self)
        for contestant in contestants:
            self.probabilities[contestant] = 1
    
    def update_probability2(self, contestant, num_pairs):
        if num_pairs == 0:
            self.probabilities[contestant] = 0
        
    def update_probability3(self, contestant, num_pairs):
    #if a probability ever hits zero it should stay at zero - this means that this pair is guaranteed not to work
        if self.probabilities[contestant] == 0:
            return
        if num_pairs == 0:
            self.probabilities[contestant] = 0
        else:
            self.probabilities[contestant] = (self.probabilities[contestant] + num_pairs) / 2
    
    def update_probability4(self, contestant, num_pairs):
        if contestant in self.probabilities:
            if self.probabilities[contestant] == 0:
                return
            else:
                self.probabilities[contestant] = ((self.probabilities[contestant] + num_pairs) / 2)
        else:
            self.probabilities[contestant] = num_pairs
        
    def __repr__(self):
        return self.name
        
class Game:
    def __init__(self, contestants):
        self.contestants = []
        self.status = False
        for contestant in contestants:
            self.contestants.append(Contestant(contestant))
            
        self.rounds = 0
    
    def round(self):
        raise NotImplementedError("Round not implemented!")
        
    def game_over(self):
        self.status = True
  
    def run_game(self):
        #make perfect pairs
        temp_list = [(contestant) for contestant in self.contestants]
        random.shuffle(temp_list)
        
        for contestant in self.contestants:
            temp_list2 = [(c2) for c2 in self.contestants]
            contestant.initialize_probabilities(temp_list2)
        
        while len(temp_list) > 0:
            a = temp_list.pop()
            b = temp_list.pop()
            a.add_pair(b)
            b.add_pair(a)
            
        while self.status == False:
            self.round()
        # print("Game over! This week's game was completed in {} rounds!".format(self.rounds))

class Game1(Game):
    def __init__(self, contestants):
        super().__init__(contestants)

    def round(self):
        temp_list = [(contestant) for contestant in self.contestants]
        pairs = []
        random.shuffle(temp_list)
        
        #making pairs
        while len(temp_list) > 0:
            a = temp_list.pop()
            b = temp_list.pop()
            pairs.append((a, b))
        successful_pairs = 0
        
        #checking all pairs - game ends if all are found
        for pair in pairs:
            if pair[0].check_pair(pair[1]):
                successful_pairs += 1
        if successful_pairs == len(pairs):
            self.game_over()

        #truth booth

        booth = pairs[0]
        if booth[0].check_pair(booth[1]):
            self.contestants.remove(booth[0])
            self.contestants.remove(booth[1])
        
        self.rounds += 1

class Game2(Game):
    def __init__(self, contestants):
        super().__init__(contestants)

    def round(self):
        temp_list = [(contestant) for contestant in self.contestants]
        pairs = []
        random.shuffle(temp_list)
        
        while len(temp_list) > 0:
            a = temp_list.pop()
            b = a.find_partner2(temp_list)
            temp_list.remove(b)
            pairs.append((a, b))
        
        successful_pairs = 0
        for pair in pairs:
            if pair[0].check_pair(pair[1]):
                successful_pairs += 1
        if successful_pairs == len(pairs):
            self.game_over()
        
        if successful_pairs == 0:
            for pair in pairs:
                pair[0].update_probability2(pair[1], 0)
                pair[1].update_probability2(pair[0], 0)
        
        #truth booth
        
        booth = pairs[0]
        if booth[0].check_pair(booth[1]):
            self.contestants.remove(booth[0])
            self.contestants.remove(booth[1])
        else:
            booth[0].update_probability2(booth[1], 0)
            booth[1].update_probability2(booth[0], 0)
        
        self.rounds += 1
        
class Game3(Game):
    def __init__(self, contestants):
        super().__init__(contestants)

    def round(self):
        temp_list = [(contestant) for contestant in self.contestants]
        pairs = []
        random.shuffle(temp_list)
        
        while len(temp_list) > 0:
            a = temp_list.pop()
            b = a.find_partner3(temp_list)
            temp_list.remove(b)
            pairs.append((a, b))
        
        successful_pairs = 0
        for pair in pairs:
            if pair[0].check_pair(pair[1]):
                successful_pairs += 1
        if successful_pairs == len(pairs):
            self.game_over()
        
        for pair in pairs:
            pair[0].update_probability3(pair[1], successful_pairs)
            pair[1].update_probability3(pair[0], successful_pairs)
        
        #truth booth
        
        booth = pairs[0]
        if booth[0].check_pair(booth[1]):
            self.contestants.remove(booth[0])
            self.contestants.remove(booth[1])
        else:
            booth[0].update_probability3(booth[1], 0)
            booth[1].update_probability3(booth[0], 0)
        
        self.rounds += 1

class Game4(Game):
    def __init__(self, contestants):
        super().__init__(contestants)
        self.hot_seat = None
    
    def run_game(self):
        temp_list = [(contestant) for contestant in self.contestants]
        random.shuffle(temp_list)
    
        while len(temp_list) > 0:
                a = temp_list.pop()
                b = temp_list.pop()
                a.add_pair(b)
                b.add_pair(a)
                
        while self.status == False:
            self.hot_seat = self.contestants.pop()
            while self.hot_seat:
                self.round(self.hot_seat)
        
    def round(self, hot_seat):
        temp_list = [(contestant) for contestant in self.contestants]
        random.shuffle(temp_list)
        
        pairs = []
        b = hot_seat.find_partner4(temp_list)
        temp_list.remove(b)
        pairs.append((hot_seat, b))
        
        while len(temp_list) > 0:
            a = temp_list.pop()
            b = a.find_partner4(temp_list)
            temp_list.remove(b)
            pairs.append((a, b))
        
        
        successful_pairs = 0
        for pair in pairs:
            if pair[0].check_pair(pair[1]):
                successful_pairs += 1
        if successful_pairs == len(pairs):
            self.game_over()
        
        for pair in pairs:
            pair[0].update_probability4(pair[1], successful_pairs)
            pair[1].update_probability4(pair[0], successful_pairs)
        
        #truth booth
        
        booth = pairs[0]
        if booth[0].check_pair(booth[1]):
            self.contestants.remove(booth[1])
            self.hot_seat = None
            if len(self.contestants) == 0:
                self.status = True
        else:
            booth[0].update_probability4(booth[1], 0)
            booth[1].update_probability4(booth[0], 0)
        
        self.rounds += 1
        
def run_avg1(n):
    results1 = []
    for i in range(n):
        contestants = [str(i) for i in range(16)]
        g = Game1(contestants)
        g.run_game()
        results1.append(g.rounds)
    sum1 = 0
    for n in results1:
        sum1 += n
    avg1 = sum1 / len(results1)
    
    print("Average of {} rounds for Algorithm 1".format(avg1))
    return(avg1, results1)

def run_avg2(n):
    results2 = []
    for i in range(n):
        contestants = [str(i) for i in range(16)]
        g = Game2(contestants)
        g.run_game()
        results2.append(g.rounds)
    sum2 = 0
    for n in results2:
        sum2 += n
    avg2 = sum2 / len(results2)
    
    print("Average of {} rounds for Algorithm 2".format(avg2))
    
    return (avg2, results2)

def run_avg3(n):
    results3 = []
    for i in range(n):
        contestants = [str(i) for i in range(16)]
        g = Game3(contestants)
        g.run_game()
        results3.append(g.rounds)
    sum3 = 0
    for n in results3:
        sum3 += n
    avg3 = sum3 / len(results3)
    
    print("Average of {} rounds for Algorithm 3".format(avg3))
    
    return (avg3, results3)

def run_avg4(n):
    results4 = []
    for i in range(n):
        contestants = [str(i) for i in range(16)]
        g = Game4(contestants)
        g.run_game()
        results4.append(g.rounds)
    sum4 = 0
    for n in results4:
        sum4 += n
    avg4 = sum4 / len(results4)
    
    print("Average of {} rounds for Algorithm 4".format(avg4))
    
    return (avg4, results4)
     
if __name__ == "__main__":
    n = 1000
    run_avg1(n)
    run_avg2(n)
    run_avg3(n)
    run_avg4(n)