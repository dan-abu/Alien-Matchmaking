import pandas as pd
import datetime as dt
import os.path
import sys
import random

class User:
    """User class represents user on matchmaking app"""
    def __init__(self, name: str, profession: str, eye_colour: str, gender: str, prefs: dict) -> None:
        """Creating user"""
        self.name = name
        self.gender = gender 
        self.profession = profession
        self.eye_colour = eye_colour
        self.matches = []
        self.active_status = False
        self.prefs = prefs
        self.email = self.name + "@pythonica.com"

class Platform:
    """Platform class represents the matchmaking app"""
    def __init__(self, simulated_day_count) -> None:
        """Creating platform"""
        self.users = []
        self.matches_counter = 0
        self.simulated_day_count = simulated_day_count
        self.daily_aggregation_table = pd.DataFrame(columns=['day', 'historic_users_total', 'active_users_total', 'new_matches'])
        self.eod_user_history_table = pd.DataFrame(columns=['day', 'id', 'name', 'gender', 'profession', 'eye_colour', 'matches', 'active_status', 'prefs', 'email'])
    
    def matchmake(self) -> None:
        """Match users' preferences"""
        # loops = len(self.users) - 1
        # count = 0
        # while count < loops:
        for i in range(len(self.users)):
            if self.users[i].active_status == False: #checking if user is active
                continue
            else:
                for j in range(i+1, len(self.users)):
                    if self.users[j].active_status == False: #checking if user is active
                        continue
                    else:    
                        if self.users[i].gender != self.users[j].gender and self.users[i].name not in self.users[j].matches: #for prototype, it's enough to check one of the users has the other's name in their matches list
                            if ((self.users[i].prefs['Profession'] == self.users[j].profession and self.users[j].prefs['Profession'] == self.users[i].profession)
                                or (self.users[i].prefs['Eye_colour'] == self.users[j].eye_colour and self.users[j].prefs['Eye_colour'] == self.users[i].eye_colour)):
                                self.users[i].matches.append(self.users[j])
                                self.users[j].matches.append(self.users[i])
                                print(f'We have a match between {self.users[i].name} and {self.users[j].name}. Their emails are {self.users[i].email} and {self.users[j].email}.')
                                self.matches_counter += 1
                        else:
                            continue
                        # count += 1
    
    def daily_aggregation_table_generator(self, folder) -> pd.DataFrame:
        """Generates daily aggregation dataframe to be used by the data warehouse"""
        execution_time = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.daily_aggregation_table['day'] = self.simulated_day_count
        self.daily_aggregation_table['historic_users_total'] = len(self.users)
        active_user_count = 0
        for user in self.users:
            if user.active_status == True:
                active_user_count += 1
            else:
                continue
        self.daily_aggregation_table['active_users_total'] = active_user_count
        self.daily_aggregation_table['new_matches'] = self.matches_counter

        filename = 'daily_aggregation_table' + execution_time
        filename = os.path.join(folder, filename)
        self.daily_aggregation_table.to_csv(filename)
        return self.daily_aggregation_table
    
    def eod_user_history_table_generator(self, folder) -> pd.DataFrame:
        """Generates daily end of day position of users"""
        execution_time = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.eod_user_history_table['day'] = self.simulated_day_count
        for user in self.users:
            self.eod_user_history_table['name'] = user.name
            self.eod_user_history_table['gender'] = user.gender
            self.eod_user_history_table['profession'] = user.profession
            self.eod_user_history_table['eye_colour'] = user.eye_colour
            self.eod_user_history_table['matches'] = user.matches
            self.eod_user_history_table['active_status'] = user.active_status
            self.eod_user_history_table['prefs'] = user.prefs
            self.eod_user_history_table['email'] = user.email
        
        filename = 'eod_user_history_table' + execution_time
        filename = os.path.join(folder, filename)
        self.eod_user_history_table.to_csv(filename)
        return self.eod_user_history_table
    
    def eod_cleanup(self) -> None:
        """Resetting the matches counter, daily aggregation and eod tables. Increasing day counter by 1"""
        self.matches_counter = 0
        self.simulated_day_count += 1
        self.daily_aggregation_table = pd.DataFrame(columns=self.daily_aggregation_table.columns)
        self.eod_user_history_table = pd.DataFrame(columns=self.eod_user_history_table.columns)

class DataWarehouse:
    """Represents a simplified form of the data warehoue that the platform writes to"""
    def __init__(self, daily_agg_cols: list) -> None:
        """Creating data warehouse"""
        self.daily_aggregation_table = pd.DataFrame(columns=daily_agg_cols)
        self.landing_table = pd.DataFrame(columns=['name', 'gender', 'profession', 'eye_colour', 'matches', 'active_status', 'prefs', 'email'])
    
    def update_aggregation_table(self, aggregation_table) -> list:
        """Update aggregation table"""
        if self.daily_aggregation_table.empty:
            for column in aggregation_table:
                self.daily_aggregation_table[column] = aggregation_table[column]
        else:
            self.daily_aggregation_table = pd.concat([self.daily_aggregation_table, aggregation_table]).drop_duplicates(keep=False)
        return self.daily_aggregation_table
    
    def update_landing_table(self, raw_table) -> pd.DataFrame:
        """Checking to see if any changes need to be made to the landing table in the data warehosue"""
        new_table_cols = raw_table.cols[1:]
        new_table = raw_table[new_table_cols]
        if self.landing_table.empty:
            for column in new_table:
                self.landing_table[column] = new_table[column]
        else:
            self.landing_table = pd.concat([self.landing_table, new_table]).drop_duplicates(keep=False)
        return self.landing_table

def input_list_converter(filepath: str) -> list:
    """Converts .txt inputs into list"""
    with open(filepath, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        return lines
    
if __name__ == "__main__":
    print('Welcome to AMA, the alien matchmaking app. Prepare to watch love unfold!')

    male_names = input_list_converter('/Users/dan/Desktop/Daniel/Work/Coding/Muzz/Alien Matchmaking/data/inputs/male_names.txt')
    female_names = input_list_converter('/Users/dan/Desktop/Daniel/Work/Coding/Muzz/Alien Matchmaking/data/inputs/female_names.txt')

    eye_colours = input_list_converter('/Users/dan/Desktop/Daniel/Work/Coding/Muzz/Alien Matchmaking/data/inputs/eye_colours.txt')

    professions = input_list_converter('/Users/dan/Desktop/Daniel/Work/Coding/Muzz/Alien Matchmaking/data/inputs/professions.txt')

    ama = Platform(1)

    num_men = int(sys.argv[1])
    num_women = int(sys.argv[2])

    for i in range(num_men):
        ama.users.append(User(name=random.choice(male_names),
                        profession=random.choice(professions),
                        eye_colour=random.choice(eye_colours),
                        gender='Male',
                        prefs={'Profession': random.choice(professions), 'Eye_colour': random.choice(eye_colours)}
                        ))
    for i in range(num_women):
        ama.users.append(User(name=random.choice(female_names),
                        profession=random.choice(professions),
                        eye_colour=random.choice(eye_colours),
                        gender='Female',
                        prefs={'Profession': random.choice(professions), 'Eye_colour': random.choice(eye_colours)}
                        ))
    
    ama.matchmake()
    ama.daily_aggregation_table_generator('/Users/dan/Desktop/Daniel/Work/Coding/Muzz/Alien Matchmaking/data/daily_aggregation')
    ama.eod_user_history_table_generator('/Users/dan/Desktop/Daniel/Work/Coding/Muzz/Alien Matchmaking/data/eod_user_history')

    ama_dwh = DataWarehouse(ama.daily_aggregation_table.columns)
    ama_dwh.update_aggregation_table(ama.daily_aggregation_table)
    ama_dwh.update_landing_table(ama.eod_user_history_table)
    ama.eod_cleanup()

    print('Matchmaking complete for the day.')

        
        
