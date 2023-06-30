
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import tabulate

sparql = SPARQLWrapper("http://130.60.24.146:7883/sparql")

query = None
with open('fic_i2_i3.sparql') as f:
    query = f.read()


# Insert SPARQL query, return results
sparql.setQuery(query)

sparql.setReturnFormat(JSON)
results = sparql.query().convert()


# The results are returned as a dictionary.  We're interested in the 'results' -> 'bindings' path
results_raw = results['results']['bindings']

# Transform raw results into a list of results
results = []
for row in results_raw:
    result = {}
    for column in ['FAIR_Implementation_Community','community', 'fip', 'FIPquestion', 'resource', 'resourcelabel2']:
        result[column] = row[column]['value']
    results.append(result)

# Create a DataFrame
df = pd.DataFrame(results)

# How many unique communities are there?
num_distinct_communities = df['community'].nunique()
num_distinct_fip = df['fip'].nunique()
print(f'Currently there are {num_distinct_communities} distinct FAIR implementation communities that have created {num_distinct_fip} FAIR implementation profiles together.')

if query is not None:
    print(tabulate.tabulate(df, headers='keys', showindex=False, tablefmt="github"))