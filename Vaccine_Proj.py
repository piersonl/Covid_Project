"""
Lon Pierson
2/26/2022
Laney Strange
DS2500
"Project 1: How vaccination status affects Covid-19 vulnerability"
"""

# import needed extensions
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import random

# set the number of trials and experiments you want
TRIALS = 10000
EXPERIMENTS = 1000

#define function to find the probability given the column
def get_prob(ds, column_name):
    '''
    PARAMETERS:
        ds : Data Set we are using to find the probibility
        column_name : the name of the column in the data set we want to 
        find the probibility of 
    RETURNS:
        a float greater than 0 and less than 1
    '''
    # return the probability
    return((sum(ds[column_name])/64)/100000)

# create function to simulate a person and test if they're positive
# for whatever attribute we're looking for (covid, hosp, death)
def sim_person_positive(vacc_status):
    '''
    PARAMETER: 
        vacc_status : the probility of testing positive given the vaccination
        status of the person
    Return: 
        True or False statement on if the person tests positive or not
    '''
    # create a random number between 0 and 1
    ran = random.random()
    
    # if the random number is less than the chance of being "positive"
    # then it returns 1 or 0 based on if they test "positive" or not
    if ran <= vacc_status:
        return(1)
    else:
        return(0)
# create function that simulates the number of cases in one day
def sim_day(trials, vacc_status):
    '''
    PARAMETERS: 
        trials : (integer) how many people we want to see if are positive
        vacc_status : (float) the probability of the person
        testing true for whatever data we're looking at given their vaccination
        status
    RETURNS:
       the average number of positive cases for the day (a float)
    '''
    # create an empty list of outcomes
    outcomes = []
    
    # create for loop that runs the amount of trials 
    #(number of people being checked per day)
    for i in range(trials):
        # add the outcomes to the outcome list
        outcomes.append(sim_person_positive(vacc_status))
        
    # find the mean of the outcome list to get the average number
    # of positive cases per the number of trials 
    outcome_mean = sum(outcomes)/len(outcomes)
    
    # return the average 
    return outcome_mean

# create a function to graph how frequently the averages of a bunch of
# different days (EXPERIMENTS number of days) appeared
def graph_days(experiments, trials, vacc_status, want_col, bin_wid):
    '''
    PARAMETERS:
        experiments: (integer) number of how many day trials we want to perform
        trials: (integer) number of how many trials we want to perform per experiment
        vacc_status: (float) the probability of the person testing true for whatever
        data we're looking at given their vaccination status
        want_col: (string) name of the color we want the graph to be
        bin_wid: (float) size we want the width of the bins to be
    '''
    # create an empty list to add the means of each day to
    outcome_mean = []
    
    # make a for loop to run through the number of wanted days (experiments)
    for i in range(experiments):
        # add each average to the outcome_mean list
        outcome_mean.append(sim_day(trials, vacc_status))
        
    # graph a histogram of the outcome_mean list with custom color and bin width
    sb.histplot(outcome_mean, color=want_col, alpha = .5, binwidth=bin_wid)
    
    # label the y axis and legend (these are the same for all graphs)
    plt.ylabel("Number of days out of 10 Thousand")
    plt.legend(["Red = Unvaccinated", "Blue = Vaccinated", "Green = Boosted"])
    
def main():
    # ask the user what information they want to see visualized
    data_wanted = input("Do you want info on cases, hospitalizations, or deaths? ")
    data_wanted = data_wanted.lower()
    
    # read in the file as a data set using pandas
    cds = pd.read_csv("covid19postvaxstatewidestats.csv")
    
    # create an index value starting at 0
    idx = 0
    
    # read through each date and if the date is not from december 2021
    # or january 2022 drop the row using the index value
    '''
    I am dropping every month aside from december and january since they're 
    the most recent months and have the most up to date information on what 
    percentage of the population is vaccinated vs unvaccinated vs boosted.
    There was also a pretty large spike in Covid-19 cases during these 
    months so the percentages will be more accurate since there were more
    cases overall
    '''
    for date in cds["date"]:
        if "2021-12" not in date:
            if "2022-01" not in date:
                cds = cds.drop(idx, axis = 0)
        idx += 1
        
    # drop all the columns with information that we aren't using
    cds = cds.drop(["date", "area", "area_type", "unvaccinated_cases",\
                   "vaccinated_cases", "boosted_cases", "unvaccinated_hosp",\
                    "vaccinated_hosp", "boosted_hosp", "unvaccinated_deaths",\
                    "vaccinated_deaths", "boosted_deaths","population_vaccinated",\
                    "population_unvaccinated", "population_boosted"], axis=1)
        
    # find the probability of testing positive given the 3 possible vaccination
    # statuses and save them to variables
    unvaccinated_case_prob = get_prob(cds, "unvaccinated_cases_per_100k")
    vaccinated_case_prob = get_prob(cds, "vaccinated_cases_per_100k")
    boosted_case_prob = get_prob(cds, "boosted_cases_per_100k")
    
    # find the probability of being hospitalized given the 3 possible vaccination
    # statuses and the average number of positive cases for each status
    # and save to a variable 
    unvaccinated_hosp_prob = get_prob(cds, "unvaccinated_hosp_per_100k")*\
        (sum(cds["unvaccinated_cases_per_100k"])/64)
    vaccinated_hosp_prob = get_prob(cds, "vaccinated_hosp_per_100k")*\
        (sum(cds["vaccinated_cases_per_100k"])/64)
    boosted_hosp_prob = get_prob(cds, "boosted_hosp_per_100k")*\
        (sum(cds["boosted_cases_per_100k"])/64)
        
    # find the probability of dying given the 3 possible vaccination
    # statuses and the average number of positive cases for each status
    # and save to a variable 
    unvaccinated_death_prob = get_prob(cds, "unvaccinated_deaths_per_100k")*\
        (sum(cds["unvaccinated_cases_per_100k"])/64)
    vaccinated_death_prob = get_prob(cds, "vaccinated_deaths_per_100k")*\
        (sum(cds["vaccinated_cases_per_100k"])/64)
    boosted_death_prob = get_prob(cds, "boosted_deaths_per_100k")*\
        (sum(cds["boosted_cases_per_100k"])/64)
        
    # if the user asked for information on the probability of positive cases
    # graph the average chance of testing positive given vaccination status
    if data_wanted == "cases":
        graph_days(EXPERIMENTS, TRIALS, unvaccinated_case_prob, "red", .0001)
        graph_days(EXPERIMENTS, TRIALS, vaccinated_case_prob, "blue", .0001)
        graph_days(EXPERIMENTS, TRIALS, boosted_case_prob, "green", .0001)
        plt.title("Average chance of testing positive for Covid-19 given vaccination status")
        plt.xlabel("Chance of Testing Positive for Covid-19")
        
    # if the user asked for information on the probability of hospitalizations
    # graph the average chance of being hospitalized given vaccination status 
    # and the number of positive cases
    if data_wanted == "hospitalizations":
       graph_days(EXPERIMENTS, TRIALS, unvaccinated_hosp_prob, "red", .001)
       graph_days(EXPERIMENTS, TRIALS,  vaccinated_hosp_prob, "blue", .001)
       graph_days(EXPERIMENTS, TRIALS, boosted_hosp_prob, "green", .001) 
       plt.title("Average chance of being hospitalized for Covid-19 given vaccination status")
       plt.xlabel("Chance of Being Hospitalized for Covid-19")
       
    # if the user asked for information on the probability of dying
    # graph the average chance of dying given vaccination status 
    # and the number of positive cases
    if data_wanted == "deaths":
       graph_days(EXPERIMENTS, TRIALS, unvaccinated_death_prob, "red", .0001)
       graph_days(EXPERIMENTS, TRIALS, vaccinated_death_prob, "blue", .0001)
       graph_days(EXPERIMENTS, TRIALS, boosted_death_prob, "green", .0001) 
       plt.title("Average chance of dying for Covid-19 given vaccination status")
       plt.xlabel("Chance of dying for Covid-19") 
       
    # add an else statement in case the user types something aside
    # from the options
    else:
        print("We don't have information on that topic!")
       
if __name__ == "__main__":
    main()