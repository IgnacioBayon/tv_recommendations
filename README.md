# TV RECOMMENDATIONS

### Introduction
This code recommends TV programs based on a dataset provided by IMBd. It is an ETL

### 1. Libraries used
- 'pandas': used for managing the DataFrame, reading the dataset and
- 're': we use Regular Expressions for managing words and different patterns we might want to separate or detect.
- 'signal': to control the program's exit when pressing Ctrl+c
- 'sys': for a correct exit
- 'copy': we deepcopy the initial dataframe so we do not have to read the csv every time we want to create a new filter
- 'os': for clearing the display when starting the program and creating a new filter

### 2. ETL functions

#### 1) Extract
We simply extract the dataframe with the pandas function 'read_csv'.

#### 2) Transform
It is the most complex function. The general structure is as follows:

We distinguish between 3 cases based on the do_next variable. This variable can have three different values: 1 (Apply another Filter), 2 (New Recommendation) and 3 (Exit TV Recommendations). This variable is initialized with the value 2. 

The first thing we do is drop the columns that are not relevant to our program (Votes, Alcohol, Profanity, Nudity, Violence, Frightening). Then we drop the duplicates in case some rows are not unique. 

The first input makes you choose between movies, series or any, as it is the most general filter you might want to add. We drop every program that does not follow our filter right after each input.
Then we display the different options: Date, Genre, Duration, Certificate and Episodes. Although Name and Rate are in the Dataframe and are not dropped, we do not display them as possible filters. The films we show are always sorted by descending rate.

We then distinguish between three cases: if the previous input is either 'Genre', 'Certificate' or 'Type', either 'Duration' or 'Date or 'Episodes'. In the first case, the next input will be another election and in the second, an interval (of minutes or years, respectively and the third ascending or descending.

In the first case, we will use the function 'get_attributes', which obtains the next options from the dataframe. If the election is Genre, we have to use Regular Expressions to get all the genres (further explanation commented in 'recommendations.py' lines 19-22).

For displaying the results, we reset the indexes. if the resulting search is an empty dataframe, we calrify that there are no mathing results.

In the end of the current filter we ask what the user wants to do:
- If 1 is chosen, we apply a new filter on the one we have already. This helps if you want a very specific search. Before choosing the new filter, the applied filters are displayed on screen.
- If 2 is chosen, we repeat the process; we get a new recommendation
- If 3 is chosen we close the program. At all times, whem pressed Ctrl+c, the program shuts down correctly (handler_signal)

#### 3) Load
We expect to get instant results from this program, so we do not need to export the results to a txt or similar. Therefore, we just display the head of the filtered dataframe. 

### MAIN

Basic structure. While option 3 in 'do_next' is not chosen (exit), we run the program in loops


### END
I hope you use and enjoy the TV Recommendations program
