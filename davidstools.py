import pandas as pd

def extract_state_data(state, dataframe):

    df = dataframe[dataframe['State'] == state]

    return df

def select_dates(dataframe, start, end):

    columnlist = ['countyFIPS', 'County Name', 'State', 'StateFIPS']

    df = dataframe.copy()
    pruned_frame = df.drop(columns=columnlist, axis=1, inplace=False)
    pruned_frame = pruned_frame.T
    pruned_frame.index = pd.to_datetime(pruned_frame.index)

    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)

    pruned_frame = pruned_frame.T
    pruned_frame = pruned_frame[[col for col in pruned_frame.columns if start_date <= col <= end_date]]

    pruned_frame = pruned_frame.T
    pruned_frame.index = pruned_frame.index.strftime('%Y-%m-%d')
    pruned_frame = pruned_frame.T

    df = df.iloc[:, :4]
    df = pd.concat([df, pruned_frame], axis=1)

    return df

def correct_numbers(dataframe):
    df = dataframe.copy()
    columnlist = ['countyFIPS', 'County Name', 'State', 'StateFIPS']
    dates = df.drop(columns=columnlist, inplace=False)
    datelist = dates.T.index.to_list()

    previous = 0
    for date in datelist:
        if date == datelist[0]:
            previous = df[date]
            continue
        holder = df[date]
        df[date] = df[date] - previous
        previous = holder

    df[datelist[0]] = 0

    return df

def top_5(dataframe):

    df = dataframe.copy()

    df = df.sort_values(by='2021-01-03', ascending=False)

    return df.head(5)