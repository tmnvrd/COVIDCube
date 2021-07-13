#%% Imports
import sparql
import pandas as pd
import numpy as np
from flask import Flask, redirect, url_for, render_template, json
from scipy.stats import pearsonr 
import unicodedata


#%% Useful functions

# Read an sparql query file, connect to https://c19.dcc.uchile.cl/db and return a dataframe with data
def sparql_to_df(filename):
    path_query = '/home/tamara/Documents/U/Memoria/memoria/Script/platform/query/'
    db = 'https://c19.dcc.uchile.cl/db/ds'
    # sparql query
    with open(path_query + filename, 'r') as file:
        _query_ = file.read()
    # get data:
    _sparql_ = sparql.query(db, _query_)
    # unpack data and transform to dataframe
    data = []
    for row in _sparql_:
        values = sparql.unpack_row(row)
        data.append(values)
    df = pd.DataFrame(data, columns = ['Country', 'Measure']) 
    return df
#%%

def query_to_df(_query_):
    db = 'https://c19.dcc.uchile.cl/db/ds'
    # get data:
    _sparql_ = sparql.query(db, _query_)
    # unpack data and transform to dataframe
    data = []
    for row in _sparql_:
        values = sparql.unpack_row(row)
        data.append(values)
    df = pd.DataFrame(data, columns = ['Country', 'Measure']) 
    return df


def dataset_to_df():
    q = """PREFIX qb: <http://purl.org/linked-data/cube#>
        PREFIX dct: <http://purl.org/dc/terms/>
        SELECT distinct ?dataset ?title ?measure
        FROM <urn:x-arq:UnionGraph>
        WHERE {
        ?dataset qb:structure  ?structure ;
                dct:title ?title .
        ?structure a qb:DataStructureDefinition;
                    qb:component [ qb:measure ?measure]
        }"""
    db = 'https://c19.dcc.uchile.cl/db/ds'
    # get data:
    _sparql_ = sparql.query(db, q)
    # unpack data and transform to dataframe
    data = []
    for row in _sparql_:
        values = sparql.unpack_row(row)
        data.append(values)
    df = pd.DataFrame(data, columns = ['dataset', 'title', 'measure']) 
    df['dataset'] = df['dataset'].map(lambda x: x.replace('http://example.org/ns#', ''))
    df['title'] = df['title']
    df['measure'] = df['measure'].map(lambda x: x.replace('http://example.org/measure#', ''))
    return df

#%%
def to_covid_corr(df_nonrelated, name_nonrelated, df_CSSEConfirmedGlobal, df_CSSEDeathsGlobal, df_CSSERecoveredGlobal):
    df_CSSEconfirmed = pd.merge(df_nonrelated, df_CSSEConfirmedGlobal, on = "Country", how = "inner")
    df_CSSEdeaths = pd.merge(df_nonrelated, df_CSSEDeathsGlobal, on = "Country", how = "inner")
    df_CSSErecovered = pd.merge(df_nonrelated, df_CSSERecoveredGlobal, on = "Country", how = "inner")
    corr_CSSEconfirmed, _ = pearsonr(df_CSSEconfirmed['Measure_x'].astype('float'), df_CSSEconfirmed['Measure_y'].astype('float'))
    corr_CSSEdeaths, _ = pearsonr(df_CSSEdeaths['Measure_x'].astype('float'), df_CSSEdeaths['Measure_y'].astype('float')) 
    corr_CSSErecovered, _ = pearsonr(df_CSSErecovered['Measure_x'].astype('float'), df_CSSErecovered['Measure_y'].astype('float'))

    #data = [
    #    [name_nonrelated, corr_CSSEconfirmed], 
    #    [name_nonrelated, corr_CSSEdeaths],
    #    [name_nonrelated, corr_CSSErecovered]
    #]
    #df = pd.DataFrame(data, columns = ['variable', 'corr']) 
    var_cov = {'name': name_nonrelated,
            'data':[corr_CSSEconfirmed,
                    corr_CSSEdeaths,
                    corr_CSSErecovered
                    ]
            }
    return var_cov


def to_covid_corr2(df_nonrelated, name_nonrelated, df_CSSEConfirmedGlobal, df_CSSEDeathsGlobal, df_CSSERecoveredGlobal):
    df_CSSEconfirmed = pd.merge(df_nonrelated, df_CSSEConfirmedGlobal, on = "Country", how = "inner")
    df_CSSEdeaths = pd.merge(df_nonrelated, df_CSSEDeathsGlobal, on = "Country", how = "inner")
    df_CSSErecovered = pd.merge(df_nonrelated, df_CSSERecoveredGlobal, on = "Country", how = "inner")
    corr_CSSEconfirmed, _ = pearsonr(df_CSSEconfirmed['Measure_x'].astype('float'), df_CSSEconfirmed['Measure_y'].astype('float'))
    corr_CSSEdeaths, _ = pearsonr(df_CSSEdeaths['Measure_x'].astype('float'), df_CSSEdeaths['Measure_y'].astype('float')) 
    corr_CSSErecovered, _ = pearsonr(df_CSSErecovered['Measure_x'].astype('float'), df_CSSErecovered['Measure_y'].astype('float'))

    #data = [
    #    [name_nonrelated, corr_CSSEconfirmed], 
    #    [name_nonrelated, corr_CSSEdeaths],
    #    [name_nonrelated, corr_CSSErecovered]
    #]
    #df = pd.DataFrame(data, columns = ['variable', 'corr']) 
    var_cov = [name_nonrelated,
            [corr_CSSEconfirmed, corr_CSSEdeaths, corr_CSSErecovered
                    ]]
    return var_cov

def get_corr():
    #SPARQL QUERIES
    df_CSSEConfirmedGlobal = sparql_to_df('CSSEConfirmedGlobal.sparql')
    df_CSSEDeathsGlobal = sparql_to_df('CSSEDeathsGlobal.sparql')
    df_CSSERecoveredGlobal = sparql_to_df('CSSERecoveredGlobal.sparql')
    df_under_five_mortality_rate = sparql_to_df('under-five_mortality_rate.sparql')
    df_accessElectricity = sparql_to_df('accessElectricity.sparql')
    df_accountOwnership = sparql_to_df('accountOwnership.sparql')
    df_adjustedNetSavings = sparql_to_df('adjustedNetSavings.sparql')
    df_carbonDioxideEmissions = sparql_to_df('carbonDioxideEmissions.sparql')
    df_contributingFamilyWorkers = sparql_to_df('contributingFamilyWorkers.sparql')
    df_peopleUsingDrinkingWaterServices = sparql_to_df('peopleUsingDrinkingWaterServices.sparql')
    df_gdpOnResearchDevelopment = sparql_to_df('gdpOnResearchDevelopment.sparql')
    df_grossDomesticProductGrowthRate = sparql_to_df('grossDomesticProductGrowthRate.sparql')

    #correlations
    under5 = to_covid_corr(df_under_five_mortality_rate, "Under five mortality rate", df_CSSEConfirmedGlobal, df_CSSEDeathsGlobal, df_CSSERecoveredGlobal)
    accessElectricity = to_covid_corr(df_accessElectricity, "Access to electricity", df_CSSEConfirmedGlobal, df_CSSEDeathsGlobal, df_CSSERecoveredGlobal)
    accountOwnership = to_covid_corr(df_accountOwnership, "Account ownership at a financial institution", df_CSSEConfirmedGlobal, df_CSSEDeathsGlobal, df_CSSERecoveredGlobal)
    adjustedNetSavings = to_covid_corr(df_adjustedNetSavings, "Adjusted net savings", df_CSSEConfirmedGlobal, df_CSSEDeathsGlobal, df_CSSERecoveredGlobal)
    carbonDioxideEmissions = to_covid_corr(df_carbonDioxideEmissions, "Carbon dioxide emissions", df_CSSEConfirmedGlobal, df_CSSEDeathsGlobal, df_CSSERecoveredGlobal)
    contributingFamilyWorkers = to_covid_corr(df_contributingFamilyWorkers, "Contributing family workers", df_CSSEConfirmedGlobal, df_CSSEDeathsGlobal, df_CSSERecoveredGlobal)
    peopleUsingDrinkingWaterServices = to_covid_corr(df_peopleUsingDrinkingWaterServices, "People using safely managed drinking water services", df_CSSEConfirmedGlobal, df_CSSEDeathsGlobal, df_CSSERecoveredGlobal)
    gdpOnResearchDevelopment = to_covid_corr(df_gdpOnResearchDevelopment, "Gross domestic expenditures on research and development", df_CSSEConfirmedGlobal, df_CSSEDeathsGlobal, df_CSSERecoveredGlobal)
    grossDomesticProductGrowthRate = to_covid_corr(df_grossDomesticProductGrowthRate, "Gross domestic product growth rate", df_CSSEConfirmedGlobal, df_CSSEDeathsGlobal, df_CSSERecoveredGlobal)
    
    data_dict = {}
    data_dict['under_five_mortality_rate'] = under5
    data_dict['accessElectricity'] = accessElectricity
    data_dict['accountOwnership'] = accountOwnership
    data_dict['adjustedNetSavings'] = adjustedNetSavings
    data_dict['carbonDioxideEmissions'] = carbonDioxideEmissions
    data_dict['contributingFamilyWorkers'] = contributingFamilyWorkers
    data_dict['peopleUsingDrinkingWaterServices'] = peopleUsingDrinkingWaterServices
    data_dict['gdpOnResearchDevelopment'] = gdpOnResearchDevelopment
    data_dict['grossDomesticProductGrowthRate'] = grossDomesticProductGrowthRate
    return data_dict


#%%
def get_data():
    df = dataset_to_df()
    data_dict = {}
    names = []
    #covid variables
    df_CSSEConfirmedGlobal = sparql_to_df('CSSEConfirmedGlobal.sparql')
    df_CSSEDeathsGlobal = sparql_to_df('CSSEDeathsGlobal.sparql')
    df_CSSERecoveredGlobal = sparql_to_df('CSSERecoveredGlobal.sparql')
    #non-relates variables
    for i in range(df.shape[0]):
        if not ('dataset-CSSE' in df['dataset'][i]) and not ('PScore' in df['dataset'][i]) and not ('ecdc' in df['dataset'][i]):
            #create query
            row  = df.iloc[i]
            dataset = row[0]
            title = row[1]
            measure = row[2]
            prefix = """PREFIX c19:  <http://example.org/ns#>
                PREFIX c19-measure:  <http://example.org/measure#>
                PREFIX c19-dimension:  <http://example.org/dimension#>
                PREFIX c19-interval: <http://example.org/interval#>
                PREFIX wd:  <http://www.wikidata.org/entity/>
                PREFIX qb: <http://purl.org/linked-data/cube#>"""
            select = """SELECT ?country ?num_non 
                FROM <urn:x-arq:UnionGraph>"""
            where = """WHERE {
                ?obs qb:dataSet c19:""" + dataset + """;
                c19-dimension:refArea ?country;
                c19-measure:""" + measure + """ ?num_non .
                }"""
            _query_ = prefix + select + where
            #data to dataframe
            df_query = query_to_df(_query_)
            #correlations
            if (df_query.shape[0] != 0):
                correlation = to_covid_corr2(df_query, title, df_CSSEConfirmedGlobal, df_CSSEDeathsGlobal, df_CSSERecoveredGlobal)
                name = dataset.replace('dataset-', '')
                names.append(name)
                data_dict[name] = correlation
    return data_dict, names


# %%

# %%
