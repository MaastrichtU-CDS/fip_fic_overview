from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import tabulate

sparql = SPARQLWrapper("http://130.60.24.146:7883/sparql")

query ="""
prefix fip: <https://w3id.org/fair/fip/terms/>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

select distinct 
?FIC 
?FIP
?FIPquestion 
?resource 
?label

where {
  ?nanopub rdf:type <http://www.nanopub.org/nschema#Nanopublication>;
    <http://purl.org/nanopub/admin/hasSubIri> ?decl;
    <http://www.w3.org/ns/prov#wasDerivedFrom> ?FIP.
  
  ?decl a fip:FIP-Declaration ;
    fip:refers-to-question ?question ;
    fip:declared-by ?communityNanoPub ;
    ?rel ?resource .
  values ?rel { fip:declares-current-use-of fip:declares-planned-use-of }
  optional { ?communityNanoPub a ?communityType . }
  optional { ?resource rdfs:label ?resourcelabel . }
  optional { ?communityNanoPub rdfs:label ?communityLabel . }
  optional {
    values ?resourcetype { fip:Available-FAIR-Enabling-Resource fip:FAIR-Enabling-Resource-to-be-Developed }
    ?resource a ?resourcetype
  }

  bind (replace(str(?communityNanoPub), ".*#", "") as ?c)
  bind (replace(str(?question), "^.*-([^-MD]+(-[MD]+)?)$", "$1") as ?FIPquestion)
  bind (concat(replace(?FIPquestion, "F|M", "0"), "x") as ?sort)
  bind (replace(str(?rel), "^.*/declares-(.*)-use-of$", "$1") as ?r)
  bind (replace(str(?resourcetype), "^.*/([^/-]*)-?FAIR-Enabling-Resource-?([^/]*)$", "$1$2") as ?rt)
  bind (replace(replace(replace(concat(?r, "/", ?rt), "^.*/to-be-Developed$", "1"), "^planned/.*$", "2"), "^current/.*$", "3") as ?value)
  bind (replace(str(?resource), "^.*?(#|/)([^/#]*/?[^/#]*)/?$", "$2") as ?res)
  bind (str(?resourcelabel) as ?reslabel)
  bind (coalesce(?reslabel, ?res) as ?resourcelabel2)
  bind (replace(?resourcelabel2, "\\\|", "-", "i") as ?label) 
  bind (coalesce(?communityLabel, ?c) as ?community)
  bind (replace(?community, "\\\|", "-", "i") as ?FIC) 
  #filter (?value = "3") #insert value 1,2,3 for either "to be developed", "planned" or "current" use of resources.   
  filter (strstarts(?FIPquestion, "I2-D") || strstarts(?FIPquestion, "I3-MD")) 
} 
order by ?FIC ?FIPquestion
"""

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
    for column in ['FIC', 'FIP', 'FIPquestion', 'resource', 'label']:
        result[column] = row[column]['value']
    results.append(result)

# Create a DataFrame
df = pd.DataFrame(results)

# How many unique communities are there?
num_distinct_communities = df['FIC'].nunique()
num_distinct_fip = df['FIP'].nunique()
print(f'Currently there are {num_distinct_communities} distinct FAIR implementation communities that have created {num_distinct_fip} FAIR implementation profiles together:')
print("""<style>
table {
  width: 100%;
}

table td {
  font-size: 10px;
}
.container-lg {
  max-width: none !important;
}
</style>
""" )

if query is not None:
    print(tabulate.tabulate(df, headers='keys', showindex=False, tablefmt="github"))
