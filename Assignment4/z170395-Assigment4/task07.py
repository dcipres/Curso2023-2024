# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rqgdtb9_Ipyjwhy7tfm4WzdO-uamGK2t

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# TO DO

#SPARQL
# Define namespaces
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
living_thing = "http://somewhere#LivingThing"

# Definir una consulta SPARQL para listar todas las subclases de "LivingThing"
query = prepareQuery(
    f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?subclass
    WHERE {{
        ?subclass rdfs:subClassOf <{living_thing}> .
    }}
"""
)

# Execute the SPARQL query and print the results
for row in g.query(query):
    print(row["subclass"])




# Visualize the results

#for r in g.query(q1):
#  print(r)

# Obtener todas las subclases de "LivingThing" utilizando la función triples
subclasses = set()

for s, p, o in g.triples((None, rdfs.subClassOf, None)):
    if str(o) == str(living_thing):
        subclasses.add(s)
        #print(s,p,o)

# Imprimir las subclases encontradas
for subclass in subclasses:
    print(subclass)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
#SPARQL
person = Namespace("http://somewhere#Person")

# Define a SPARQL query to select all individuals of "Person" (including subclasses)
query = prepareQuery(
    f"""
    SELECT ?individual
    WHERE {{
        ?individual a/rdfs:subClassOf* <{person}> .
    }}
    """
)

# Execute the SPARQL query and print the results
for row in g.query(query):
    print(row["individual"])

# Visualize the results

rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
person = Namespace("http://somewhere#Person")

individuals = set()

# Iterar a través de todas las tripletas y encontrar instancias de "Person" y sus subclases
subclasses = set()

# Obtener todas las tripletas en el grafo donde el objeto es una subclase de "Person"
for s, p, o in g.triples((None, rdfs.subClassOf, None)):
  if str(o) == person:
    subclasses.add(s)

for s, p, o in g.triples((None, rdf.type, None)):
    #print(s,p,o)
    if str(o) == str(person) or str(o) in str(subclasses):
        individuals.add(s)

# Imprimir las instancias encontradas
for individual in individuals:
    print(individual)



"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

# TO DO
#SPARQL

person = Namespace("http://somewhere#Person")
animal = Namespace("http://somewhere#Animal")

# Definir una consulta SPARQL para seleccionar todas las instancias de "Person" sin incluir sus subclases
query = prepareQuery(
f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?individual
    WHERE {{
        {{
            ?individual rdf:type <{person}> .
        }}
        UNION
        {{
            ?individual rdf:type <{animal}> .
        }}
    }}
    """
)

# Ejecutar la consulta SPARQL e imprimir los resultados
for row in g.query(query):
    print(row["individual"])


# Visualize the results

individuals = set()
for s, p, o in g.triples((None, RDF.type, None)):
    if str(o) == person or str(o) == animal:
        individuals.add(s)
for individual in individuals:
    print(individual)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

# TO DO
knows = "http://xmlns.com/foaf/0.1/knows"
rocky = "http://somewhere#RockySmith"
fn = "http://www.w3.org/2001/vcard-rdf/3.0/FN"
individuals = set()
names = set()
for s, p, o in g.triples((None,None, None )):
  # print(s,p,o)
   if str(p) == knows and str(o) == rocky :
      #tenemos a los sujetos que conocen a rocky, obtendremos su FN
      individuals.add(s)

#por cada sujeto obtenido comprobamos si tiene propiedad FullName (FN)
for individual in individuals :
  for s,p,o in g.triples((None,None,None)):
    if s == individual and str(p)== fn:
      names.add(o)

for name in names:
  print(name)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

# TO DO
knows = "http://xmlns.com/foaf/0.1/knows"
individuals = set()
entities = set()
#Recorremos el grafo para guardar aquellas entidades con la relacion "knows"
for s, p, o in g.triples((None,None, None )):
   if str(p) == knows :
    individuals.add(s)
n = 0
#Recorremos el grafo por cada sujeto y contamos las relaciones knows si >=2 add
for individual in individuals:
  n = 0
  for s,p,o in g.triples((None,None,None)):
    if s == individual and str(p) == knows:
      #print(s)
      n = n+1
      if n>=2:
        entities.add(s)

# Visualize the results
for ent in entities:
  print(ent)