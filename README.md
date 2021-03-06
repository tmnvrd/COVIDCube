# COVIDCube

## _An RDF Data Cube for Exploring Among-Country COVID-19 Correlations_

The among-country variation in the numbers of reported COVID-19 cases and deaths per capita is not well-understood. Various hypotheses have been proposed, such as high prevalence of comorbidities, climate, pollution, health services, public policies, etc. While a number of initiatives have explored this variance, or have developed relevant datasets to better understand this variance, there remains uncertainty regarding the factors involved.

Publication:

* Tamara Novoa-Rodríguez and Aidan Hogan. "[COVIDCube: An RDF Data Cube for Exploring Among-Country COVID-19 Correlations](https://aidanhogan.com/docs/covid_rdf_cube.pdf)". In the Demo Proceedings of the 19th International Semantic Web Conference (ISWC), Online, October 24–28, 2021.

### What will you find in this repository?

There are 3 main folders:
- [RDF](https://github.com/tmnvrd/COVIDCube/tree/main/RDF) - mappings to convert from tsv to ttl files (using [Tarql](https://tarql.github.io/))
- [platform](https://github.com/tmnvrd/COVIDCube/tree/main/platform) - contains the front-end that has been developed with the framework Flask 
- [raw_data](https://github.com/tmnvrd/COVIDCube/tree/main/raw_data) - all data extracted from sources like The World Bank, WHO, Our World in Data, Wikipedia, etc..

### _Here you can see the [COVIDCube](https://c19.dcc.uchile.cl/) demo_

