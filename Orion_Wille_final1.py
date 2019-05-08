# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 11:17:40 2019

@author: white
"""

'''
    Orion Wille
    4/28/19
    Python 1 - DAT-119 - Spring 2019
'''

import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#get spreadsheets as dataframes
player_key_location = r"name key.csv"
player_key = pd.read_csv(player_key_location, index_col=0)

batting_stats_location = r"batting.csv"
batting_stats = pd.read_csv(batting_stats_location)

def main():
    
    menu()


def menu():
    #welcome message
    print("\nWelcome to the Baseball Database!")
    print("This program allows you to easily locate stats for players and teams from 1871 to 2018.")
    user_input = input("Press 1 on your keyboard to search the database by player, 2 to search by team, or 3 to exit the program: ")
    #menu options
    while user_input != "3":
        if user_input == "1":
            player_search()
            break
        elif user_input == "2":
            team_search()
            break
        else:
            print("\nInvalid input, please enter either 1, 2 or 3")
            user_input = input("Press 1 on your keyboard to search the database, 2 to search by team, or 3 to exit the program: ")
    else:
        print("\nExiting Program")

        
def player_search():
    
    #get player name input
    get_name_last = input("Enter the player's LAST name, or continue on to year search to find stats for all players in a given year: ")
    #set input to lower case
    get_name_last = get_name_last.lower()
    #input validation
    str_flag = False
    while str_flag == False:
        if all(letter.isalpha() for letter in get_name_last):
            str_flag = True
        else:
            get_name_last = input("Please enter valid LAST name: ")
            get_name_last = get_name_last.lower()
            str_flag = False

    #check to see if a name has been entered
    if get_name_last != "":
        
        #locate player in database
        player_name = player_key.loc[player_key["nameLast"] == get_name_last]
        #check to see if found in database
        while player_name.empty:
            get_name_last = input("Player not found in database, please review entered data and try again, or press ENTER to return to the menu: ")
            #check to see if back to menu
            if get_name_last == "":
                menu()
                return
            else:
                player_name = player_key.loc[player_key["nameLast"] == get_name_last] 
        #once last name is found, find players first name as well and add both to lists
        player_first = player_name["nameFirst"].values.tolist()
        player_last = player_name["nameLast"].values.tolist()
        #combing first and last name list
        player_full = []
        for item in range(len(player_first)):
            player_full.append(player_first[item])
            player_full.append(player_last[item])
        #make player id into a list
        player_id = player_name.index.values.tolist()
        #if there is more than one player with same last name
        if len(player_id) > 1:
            #specify by first name
            get_name_first = input("Multiple people found with that last name, please enter FIRST name to specify, or press ENTER to view all players with this last name: ")
            get_name_first = get_name_first.lower()
            #input validation
            str_flag = False
            while str_flag == False:
                if all(letter.isalpha() or letter.isspace() for letter in get_name_first):
                    str_flag = True
                else:
                    get_name_first = input("Invalid input, please enter a valid name: ")
                    get_name_first = get_name_first.lower()
                player_first = player_key.loc[(player_key["nameLast"] == get_name_last) & (player_key["nameFirst"] == get_name_first)]
                if get_name_first == "":
                    str_flag = True
                else:
                    if player_first.empty:
                        get_name_first = input("Player not found. Please review data and enter a valid name, or press ENTER to view all players with this name: ") 
                        get_name_first = get_name_first.lower()
                        str_flag = False

                          

            print()
            #give option to view all players with same last name
            if get_name_first == "":
                #print names 
                for item in player_full:
                    if item == player_last[0]:
                        print(item)                        
                    else:
                        print(item, end=" ")
                #search by first and last name        
                print("\nWhich of these players would you like to search for?")
                name_search = input("Enter the FULL name of the player you want to search, or press ENTER to return to menu: ")
                name_search = name_search.lower()
                #input validation
                str_flag = False                
                while str_flag == False:
                    #return to menu if user pressed ENTER
                    if name_search == "":
                        menu()
                        return
                    if name_search.isspace():
                        name_search = input("Please correct spaces and enter a valid input: ")
                        str_flag = False
                    else:                
                        if all(letter.isalpha() or letter.isspace() for letter in name_search) and " " in name_search:
                            str_flag = True  
                        else:
                            name_search = input("Invalid input, please enter a valid FULL name: ")
                            name_search = name_search.lower()                        
                            str_flag = False
                #input validation        
                empty_flag = False                
                while empty_flag == False:       
                    #process name list
                    name_search_list = name_search.split()
                    name_search_last = name_search_list[1:]                        
                    name_search_first = name_search_list[0]
                    name_search_last = "".join(name_search_last)
                    name_search_first = "".join(name_search_first)
                    #locate in database
                    player_first = player_key.loc[(player_key["nameLast"] == name_search_last) & (player_key["nameFirst"] == name_search_first)]                    
                    #check to see if name was found in database
                    if player_first.empty:
                        name_search = input("Player not found. Please review data and enter a valid name: ") 
                        name_search = name_search.lower()
                        empty_flag = False
                        #more input validation
                        str_flag = False                
                        while str_flag == False:                
                            if all(letter.isalpha() or letter.isspace() for letter in name_search) and " " in name_search:
                                str_flag = True                            
                            else:
                                name_search = input("Invalid input, please enter a valid FULL name: ")
                                name_search = name_search.lower()
                                str_flag = False
                        
                    else:
                        empty_flag = True
            

                #make full name into a list a process
                player_first_index = player_first.index.values.tolist()
                player_first_index = "".join(player_first_index)
                player_name_full = player_first.values.tolist()
                string_name = player_name_full[0]
                string_name = string_name[0:]
                string_name = " ".join(string_name)
                #if there were players with same last name, get player id    
                player_batting = batting_stats.loc[batting_stats["playerID"] == player_first_index]
                #assign results to batting output for later use
                batting_output = player_batting[['name', 'year',  'team', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI']]
                
                
            else:
                #locate first name
                player_first = player_key.loc[(player_key["nameLast"] == get_name_last) & (player_key["nameFirst"] == get_name_first)]
                
                #check to make sure it's in database
                if player_first.empty:
                    print("Invalid input")
                else:
                    #turn full name into list and process
                    player_first_index = player_first.index.values.tolist()
                    player_first_index = "".join(player_first_index)
                    player_name_full = player_first.values.tolist()
                    string_name = player_name_full[0]
                    string_name = string_name[0:]
                    string_name = " ".join(string_name)
                    #find player ID
                    player_batting = batting_stats.loc[batting_stats["playerID"] == player_first_index]
                    #assign results to batting output for later use
                    batting_output = player_batting[['name', 'year', 'team', 'G', 'AB', 'R', 'H', '2B','3B', 'HR', 'RBI']]
                
        #player has unique name
        else:
            player_first_index = "\n".join(player_id)
            player_batting = batting_stats.loc[batting_stats["playerID"] == player_first_index]
            #assign results to batting output for later use
            batting_output = player_batting[['name', 'year', 'team', 'G', 'AB','R', 'H', '2B', '3B', 'HR', 'RBI']]
            
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #year input       
    print("\nEnter a year between 1871 and 2018 to find the stats for this player when they played in a particular year (Optional), or press ENTER to display stats for all years")
    user_year = input("Enter a year: ")
    #input validation
    digit_flag = False
    while digit_flag == False:        
        if user_year.isdigit() or user_year == "":
            digit_flag = True
        else:
            user_year = input("Invalid input, please enter a correct year, or press ENTER to view all years results: ")
        
    #check to see if user entered a year
    if user_year != "":
        #check to see if a name was entered in the player search, if not displays stats for all players in given year
        if get_name_last == "":    
            user_year = int(user_year)
            #locate year in database
            player_year = batting_stats.loc[batting_stats["year"] == user_year]
            #assign resluts to batting output for later use
            batting_output = player_year[['name', 'year', 'team', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI']]
            #if no results found, ask for new input
            while player_year.empty:
                user_year = input("No results found in database, please enter a year between 1871 and 2018, or press ENTER to return to menu: ")                
                #input validation
                digit_flag = False
                while digit_flag == False:        
                    if user_year.isdigit():
                        user_year = int(user_year)
                        digit_flag = True
                    #return to menu option
                    elif user_year =="":
                        menu()
                        return
                    else:
                        user_year = input("Invalid input, please enter a correct year, or press ENTER to return to menu: ")
                       
                    player_year = batting_stats.loc[batting_stats["year"] == user_year]
                    batting_output = player_year[['name', 'year', 'team', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI']]
            
            #print result
            print(batting_output.to_string(index = False))
        #display stats for particular player in particular year
        else:
            user_year = int(user_year)
            #locate player name and year in database
            player_and_year = batting_stats.loc[(batting_stats["playerID"] == player_first_index) & (batting_stats["year"] == user_year)]
            #assign resluts to batting output for later use
            batting_output = player_and_year[['name', 'year', 'team', 'G', 'AB', 'R', 'H', '2B','3B', 'HR',	'RBI']]
            #if no results found ask for new input
            while player_and_year.empty:
                user_year = input("No results found in database, player did not player in the entered year, please enter another year or press ENTER to return to menu: ")                
                #input validation
                digit_flag = False
                while digit_flag == False:        
                    if user_year.isdigit():
                        user_year = int(user_year)
                        digit_flag = True
                    #return to menu option
                    elif user_year =="":
                        menu()
                        return
                    else:
                        user_year = input("Invalid input, please enter a correct year, or press ENTER to return to menu: ")
                        
                    player_and_year = batting_stats.loc[(batting_stats["playerID"] == player_first_index) & (batting_stats["year"] == user_year)]
                    batting_output = player_and_year[['name', 'year', 'team', 'G', 'AB', 'R', 'H', '2B','3B', 'HR',	'RBI']]
            #print result
            print(batting_output.to_string(index = False))
    #if no player input or year input return to menu
    elif user_year == "" and get_name_last == "":
        print("\nNo valid input entered, returning to menu")  
        
    #if no year entered, display all stats for player    
    else:
        print(batting_output.to_string(index = False))   
    #back to menu
    menu()
    
def team_search():
    #get user team input
    user_team = input("What team would you like to search for?: ")
    user_team = user_team.lower()
    #check to see if user entered a year
    if user_team != "":
        #locate team in database
        team_name = batting_stats.loc[batting_stats["team"] == user_team]
        #if no results found, ask for new input
        while team_name.empty:
            user_team = input("Team not found in database, please review entered data and try again, or press ENTER to return to the menu: ")
            team_name = batting_stats.loc[batting_stats["team"] == user_team]
            #if user pressed ENTER, return to menu
            if user_team == "":
                menu()
                return
            
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #year input
    print("\nEnter a year to find the stats for this team when they played in a particular year (Optional), or press ENTER to display stats for all years")
    user_year = input("Enter a year: ")
    #input validation
    digit_flag = False
    while digit_flag == False:        
        if user_year.isdigit() or user_year == "":
            digit_flag = True
        else:
            user_year = input("Invalid input, please enter a correct year, or press ENTER to view all years for this team: ")

    #check to see if user entered a year
    if user_year != "":
        #check to see if user entered a team
        if user_team == "":            
            user_year = int(user_year)  
            #locate year in database
            team_year = batting_stats.loc[batting_stats["year"] == user_year]
            #assign resluts to batting output for later use
            batting_output = team_year[['name', 'year', 'team', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI']]
            #if no results found, ask for new input
            while team_year.empty:
                user_year = input("No results found in database, please enter a year between 1871 and 2018, or press ENTER to return to menu: ")                
                #input validation
                digit_flag = False
                while digit_flag == False:        
                    if user_year.isdigit():
                        user_year = int(user_year)
                        digit_flag = True
                    #return to menu option
                    elif user_year =="":
                        menu()
                        return
                    else:
                        user_year = input("Invalid input, please enter a correct year, or press ENTER to return to menu: ")
                       
                    team_year = batting_stats.loc[batting_stats["year"] == user_year]
                    batting_output = team_year[['name', 'year', 'team', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI']]
            #print result
            print(batting_output.to_string(index = False))
        #user did enter a team
        else:
            user_year = int(user_year)
            #locate team and year in database
            team_and_year = batting_stats.loc[(batting_stats["year"] == user_year)&(batting_stats["team"] == user_team)]
            #assign resluts to batting output for later use
            batting_output = team_and_year[['name', 'year', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI']]
            #if no results found, ask for new input
            while team_and_year.empty:
                user_year = input("No results found in database, team was not active during the entered year, please enter another year or press ENTER to return to menu: ")                
                #input validation
                digit_flag = False
                while digit_flag == False:        
                    if user_year.isdigit():
                        user_year = int(user_year)
                        digit_flag = True
                    #return to menu option
                    elif user_year =="":
                        menu()
                        return
                    else:
                        user_year = input("Invalid input, please enter a correct year, or press ENTER to return to menu: ")
                       
                    team_and_year = batting_stats.loc[batting_stats["year"] == user_year]
                    batting_output = team_and_year[['name', 'year', 'team', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI']]
            #print results
            print(batting_output.to_string(index = False))
    #if no player input or year input return to menu
    elif user_year == "" and user_team == "":
        print("\nNo valid input entered, returning to menu") 
    #if no year entered, display all stats for team 
    else:
        batting_output = team_name[['name', 'year', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI']]
        print(batting_output.to_string(index = False))
    #back to menu
    menu()
    
            
main()
    
    
