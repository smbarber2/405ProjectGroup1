import pandas as pd

DEATHS = pd.read_csv('covid_deaths_usafacts.csv')
CASES = pd.read_csv('covid_confirmed_usafacts.csv')
POPULATION = pd.read_csv('covid_county_population_usafacts.csv')

META_COLUMNS = ['countyFIPS', 'County Name', 'State', 'StateFIPS']

# This function converts CASES or DEATHS into a DataFrame containing totals on a given date
def national_data(frame):
    national_data = frame.drop(columns=META_COLUMNS, axis=1).sum()

    d = {'United States': national_data}

    df = pd.DataFrame(data=d).T

    return df

# This function converts CASES or DEATHS into a DataFrame organized by year with NaN values for values not included.
def national_yearly_data(frame):
    national_data = frame.drop(columns=META_COLUMNS, axis=1).sum()

    d = {'United States': national_data}

    df = pd.DataFrame(data=d).reset_index(names='Date')
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')

    dates = ['2020-01-22','2020-12-31','2021-01-01','2021-12-31','2022-01-01','2022-12-31','2023-01-01','2023-07-23']

    years = ['2020', '2021', '2022', '2023']

    i = 0
    arrays = []
    for year in years:
        data = df.loc[dates[i] : dates[i+1]].reset_index()
        data['Yearless'] = data['Date'].astype(str).str.slice(5)
        data.drop(columns=['Date'], inplace=True)
        data.rename(columns={'United States':year, 'Yearless':'Date'}, inplace=True)
        arrays.append(data)
        i+=2
    
    dff = arrays[0].drop(columns='2020', axis=1)
    for array in arrays:
        dff = dff.merge(array, how='outer', on='Date')

    return dff

# This function takes in a state abr and the frame in question and produces
# data in the same format as national_yearly_data but for a single state.
def state_data(state, frame):
    state = frame[frame['State'] == state]
    return national_data(state)