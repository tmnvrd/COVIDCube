#%%
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from math import isnan
import csv
import sparql
from flask import Flask, redirect, url_for, render_template, json
from scipy.stats import pearsonr 
import sparql_corr as scorr





# APP
app = Flask(__name__)

mortality = []

@app.route("/query")
def query():
    q = ("""PREFIX c19:  <http://example.org/ns#>
    PREFIX c19-measure:  <http://example.org/measure#>
    PREFIX c19-dimension:  <http://example.org/dimension#> 
    PREFIX wd:  <http://www.wikidata.org/entity/> 
    PREFIX qb: <http://purl.org/linked-data/cube#>

    SELECT *
    FROM <urn:x-arq:UnionGraph>
    WHERE {
    ?obs qb:dataSet c19:dataset-under-five_mortality_rate .
    ?obs c19-measure:mortalityRate ?num .
    }""")

    #result = sparql.query('http://localhost:3030/ds', q)
    result = sparql.query('https://c19.dcc.uchile.cl/db/ds', q)
    print(result.fetchone())
    print('----------------------', result.variables)
    #print(sparql.unpack_row(result.fetchone()))
    #print(sparql.unpack_row(result))
    
    for row in result:
        print('FOOOOOOOOOOOOOOOOOOOOOOOOOOOR')
        print('row:', row)
        values = sparql.unpack_row(row)
        print(values[0], "-", values[1], "orbits")
        mortality.append(float(values[1]))
    print('------------------')
    print('------------------')
    print('------------------')
    print(type(values[1]))
    print('------------------')
    print('------------------')
    print('------------------')
    print(mortality)
    print('------------------')
    print('------------------')
    print('------------------')
    mort = np.array(mortality)
    
    return render_template("index.html", values=values)

@app.route("/test")
def test():
    return render_template("layout.html")

@app.route("/")
def home():
    #data_dict = scorr.get_corr()
    data_dict, names = scorr.get_data()
    return render_template("heatmatrix.html", data=json.dumps(data_dict), names=json.dumps(names))

#@app.route("/<name>")
#def user(name):
#    return f"Hello {name}!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
#    app.run(debug=True)
    