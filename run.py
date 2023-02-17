from datasources import triples as sparql

rdfEndpoint = sparql.SPARQLTripleStore("http://130.60.24.146:7883/sparql")

query = None
with open('fic_i2_i3.sparql') as f:
    query = f.read()

if query is not None:
    print(rdfEndpoint.sparql_get(query))