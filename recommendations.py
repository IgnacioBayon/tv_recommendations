import pandas as pd
import re
import signal
import sys
import copy
import os

# Ignacio Bayón Jiménez Ugarte


def handler_signal(signal, frame):
    print("\n\nExit TV Recomendations\n")
    sys.exit(1)


def get_attributes(df: pd.DataFrame, election1: str):
    """In filters that need more than one selection, we
    obtain all the atributtes using this function"""
    # As there may be more than one genre in a single film's genre,
    # for obtaining the different genres we have to divide each film's
    # genres into lists and check individually if each of them is already
    # added to the list
    section = df[election1].sort_values().unique().tolist()
    space_re = re.compile(r'\s')
    comma_re = re.compile(r'\,')
    if election1 == "Genre":
        genres = []
        for genre_iter in section:
            genre_iter = space_re.sub('', genre_iter)
            genres_particular = comma_re.split(genre_iter)
            for genre_particular in genres_particular:
                if genre_particular not in genres:
                    genres.append(genre_particular)
        section_filtered = genres

    if election1 in ["Type", "Certificate"]:
        section_filtered = section

    return section_filtered


def extract():
    df = pd.read_csv('imdb.csv', sep=',', encoding='latin1')
    return df


def transform(df: pd.DataFrame, do_next: str, ap_filters: dict[str:str]):
    # We drop the 'Votes' and 'Frightening' columns for being too specific.
    # We drop the others due to being included in'Certificate' column

    if do_next == '2':

        # try:
        drop = [
            'Votes', 'Alcohol', 'Profanity',
            'Nudity', 'Violence', 'Frightening'
            ]
        df.drop(drop, axis=1, inplace=True)
        # except:
        #     pass
        # In case there are some duplicated lines
        df.drop_duplicates(inplace=True)

        # The first filter we have to go through is Film / Series
        print("\n\tWelcome to TV Recomendations\nFirst, filter by:",
              "\n\t - Film\n\t - Series\n\t - Any")
        election0 = input("\t > ")
        # Control over correct input
        while election0 not in ['Film', 'Series', 'Any']:
            print("Please, introduce a correct entry: ")
            election0 = input("\t > ")
        ap_filters['Type'] = election0

        # We filter based on the type of program
        if election0 == "Film":
            # We drop the 'Episodes' Column
            df.drop('Episodes', axis=1, inplace=True)

        if election0 != 'Any':
            drop_lst = []
            for i in df.index:
                if df['Type'][i] != election0:
                    drop_lst.append(i)
            df.drop(drop_lst, inplace=True)

    if ap_filters != {}:
        print(f"\nMENU\nApplied Filters: {ap_filters}",
              "\nOn what aspect would you like to be recommended?")
    else:
        print("\nMENU\nOn what aspect would you like to be recommended?")

    categories = []

    for category in df:
        # We want to keep the names but not filter based on the name
        if category not in ['Name', 'Rate'] and category not in ap_filters:
            categories.append(category)
            print(f'\t - {category}')

    election1 = input("\t>> ")
    while election1 not in categories:  # Control over correct input
        print("Please, introduce a correct entry: ")
        for category in categories:
            print(f'\t - {category}')
        election1 = input("\t>> ")

    # First, we are going to sort the dataframe based on the rate, as we are
    # always going to recommend first the higher rated movies within the filter
    df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce')
    df.dropna(inplace=True)
    df = df.sort_values(by='Rate', ascending=False)

    # Once we select the category we would like to be recommended on, we
    # choose the aspect within the category (eg. Genre -> Adventure)
    if election1 in ['Genre', 'Certificate', 'Type']:
        election1_lst = get_attributes(df, election1)
        print(re.sub(r'\'', '', str(election1_lst)[1:-1]))
        election12 = input(f"\nChoose '{election1}'\n\t > ")
        while election12 not in election1_lst:  # Control over correct input
            print("Please, introduce a correct entry")
            election12 = input(f"Choose '{election1}'\n\t > ")

        if election1 == 'Genre':
            # First, we get rid of those who don't contain the chosen genre
            # within its own genres.
            genre_re = re.compile(election12)
            drop_lst = []
            for i in df.index:
                search = genre_re.search(df['Genre'][i])
                if search is None:
                    drop_lst.append(i)
            df.drop(drop_lst, inplace=True)

    if election1 in ['Duration', 'Date']:
        # Tenemos que conseguir hacerlo por un intervalo
        df[election1] = pd.to_numeric(df[election1], errors='coerce')
        # If we want to filter based on the Date, the films which do not
        # have an associated date must not be considered
        df.dropna(inplace=True)
        date_re = re.compile(r'[0-9]+-[0-9]')

        election12 = input("Choose interval (a1-a2)\n       >>> ")
        while date_re.search(election12) is None:
            print("Please, introduce a correct entry")
            election12 = input("Choose date interval (year1-year2)\n       >>> ")
        interval = re.split(r'\-', election12)
        for i in range(len(interval)):
            interval[i] = int(interval[i])
        interval[1] += 1  # To include the higher date
        drop_lst_date = []
        for i in df.index:
            if df[election1][i] not in range(interval[0], interval[1]):
                drop_lst_date.append(i)

        df.sort_values(by=['Rate', election1],
                       ascending=[False, True], inplace=True)
        df.drop(drop_lst_date, inplace=True)

    if election1 in ['Episodes']:
        df[election1] = pd.to_numeric(df[election1], errors='coerce')
        # If we want to filter based on the Date, the films which do not
        # have an associated date must not be considered
        df.dropna(inplace=True)
        election12 = input("Choose:\n\t- Ascending \n\t- Descending\n       >>> ")
        # Control over correct input
        while election12 not in ['Ascending', 'Descending']:
            print("Please, introduce a correct entry")
            election12 = input("Choose:\n\t - Ascending \n\t - Descending\n       >>> ")
        if election12 == 'Ascending':
            df.sort_values(by=[election1, 'Rate'],
                           ascending=[True, False], inplace=True)
        else:
            df.sort_values(by=[election1, 'Rate'],
                           ascending=[False, False], inplace=True)

    ap_filters[election1] = election12

    # We reset the Indexes
    df_show = df.reset_index(drop=True)
    if not df_show.empty:  # if the dataframe is not empty
        load(df_show)
    else:
        print(f"No matches found with the following filter:\n{ap_filters}")

    print("\nWhat would you like to do?\n\t 1. Apply another filter",
          "\n\t 2. New Recommendation\n\t 3. Exit TV Recommendations")
    do_next = input("\t > ")
    while do_next not in ['1', '2', '3']:
        print("Please, introduce a correct entry")
        do_next = input("\t > ")

    return df, do_next, ap_filters


def load(df_show: pd.DataFrame):
    print(df_show.head())


if __name__ == "__main__":

    signal.signal(signal.SIGINT, handler_signal)

    # We set the 'do_next' variable to 1, as it is associated
    # with the ation 'apply new filter'
    do_next = '2'

    df_0 = pd.read_csv('imdb.csv')

    while do_next != '3':
        if do_next == '1':
            df, do_next, ap_filters = transform(df, do_next, ap_filters)
        elif do_next == '2':
            os.system('cls')
            df = copy.deepcopy(df_0)
            df, do_next, ap_filters = transform(df, do_next, {})

    print("\n\nExit TV Recomendations\n")
    sys.exit(1)
