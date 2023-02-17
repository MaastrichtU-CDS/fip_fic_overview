from datasources import triples as sparql
import pandas as pd
import tabulate

rdfEndpoint = sparql.SPARQLTripleStore("http://130.60.24.146:7883/sparql")

query = None
with open('fic_i2_i3.sparql') as f:
    query = f.read()

def get_sparql_dataframe(json_result_sparql):
    """
    Helper function to convert SPARQL results into a Pandas data frame.
    """
    cols = json_result_sparql['head']['vars']

    out = []
    for row in json_result_sparql['results']['bindings']:
        item = []
        for c in cols:
            item.append(row.get(c, {}).get('value'))
        out.append(item)

    df = pd.DataFrame(out, columns=cols)

    if len(json_result_sparql['results']['bindings']) > 0:
        firstRow = json_result_sparql['results']['bindings'][0]
        for c in cols:
            varType = firstRow.get(c,{}).get("type")
            if varType == "uri":
                df[c] = df[c].astype("category")
            if varType == "literal" or varType == "typed-literal":
                dataType = firstRow.get(c,{}).get("datatype")
                if dataType=="http://www.w3.org/2001/XMLSchema#int":
                    df[c] = pd.to_numeric(df[c], errors='coerce')
                if dataType=="http://www.w3.org/2001/XMLSchema#integer":
                    df[c] = pd.to_numeric(df[c], errors='coerce')
                if dataType=="http://www.w3.org/2001/XMLSchema#double":
                    df[c] = pd.to_numeric(df[c], errors='coerce')
                if dataType=="http://www.w3.org/2001/XMLSchema#string":
                    df[c] = df[c].astype("category")
    
    return df

if query is not None:
    df = get_sparql_dataframe(rdfEndpoint.sparql_get(query, getMetadata=True))
    print(tabulate.tabulate(df, headers='keys', showindex=False, tablefmt="github"))