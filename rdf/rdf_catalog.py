from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS as DCT, PROV, FOAF
import os

# Namespaces
DCAT = Namespace("http://www.w3.org/ns/dcat#")
DCAT3 = Namespace("http://www.w3.org/ns/dcat3#")
DCATAPIT = Namespace("http://dati.gov.it/onto/dcatapit/")
ADMS = Namespace("http://www.w3.org/ns/adms#")
CC = Namespace("http://creativecommons.org/ns#")
XSD_NS = Namespace("http://www.w3.org/2001/XMLSchema#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

# Base namespace the project datasets
OLD = Namespace("https://github.com/eugeniavd/retired_places/")

catalog_g = Graph()

# Prefixes
catalog_g.bind("dcat", DCAT)
catalog_g.bind("dcat3", DCAT3)
catalog_g.bind("dcatapit", DCATAPIT)
catalog_g.bind("dct", DCT)
catalog_g.bind("adms", ADMS)
catalog_g.bind("xsd", XSD_NS)
catalog_g.bind("cc", CC)
catalog_g.bind("skos", SKOS)
catalog_g.bind("old", OLD)
catalog_g.bind("prov", PROV)
catalog_g.bind("foaf", FOAF)

# Catalog URI and metadata
catalog_uri = URIRef("https://github.com/eugeniavd/retired_places/tree/main/data/")
catalog_g.add((catalog_uri, RDF.type, DCAT.Catalog))
catalog_g.add((catalog_uri, DCT.title, Literal("Retired Places Datasets Catalog", lang="en")))
catalog_g.add((catalog_uri, DCT.description, Literal(
    "Catalog containing the source, merged and mashup datasets for the Retired Places project.",
    lang="en"
)))

# Publisher information
publisher_uri = URIRef("https://github.com/eugeniavd/retired_places/")
catalog_g.add((catalog_uri, DCT.publisher, publisher_uri))
catalog_g.add((publisher_uri, RDF.type, FOAF.Organization))
catalog_g.add((publisher_uri, FOAF.name, Literal("Open Access – Retired Places Project", lang="en")))

# Dates 
catalog_g.add((catalog_uri, DCT.issued, Literal("2025-11-13", datatype=XSD.date)))
catalog_g.add((catalog_uri, DCT.modified, Literal("2025-12-07", datatype=XSD.date)))

# DCAT.language
catalog_g.add((catalog_uri, DCAT.language, URIRef("http://www.lexvo.org/page/iso639-3/eng")))
catalog_g.add((catalog_uri, DCAT.language, URIRef("http://www.lexvo.org/page/iso639-3/ita")))

# ADMS.identifier
catalog_g.add((catalog_uri, ADMS.identifier, Literal("OLD_catalog", datatype=XSD.string)))

# Theme taxonomy used by the catalog
theme_taxonomy_uri = URIRef("http://publications.europa.eu/resource/authority/data-theme")
catalog_g.add((catalog_uri, DCAT.themeTaxonomy, theme_taxonomy_uri))
catalog_g.add((theme_taxonomy_uri, RDF.type, SKOS.ConceptScheme))
catalog_g.add((theme_taxonomy_uri, DCT.title, Literal(
    "Publications Office of the European Union Data Themes", lang="en"
)))
catalog_g.add((theme_taxonomy_uri, DCT.description, Literal(
    "Controlled vocabulary of data themes used for dataset classification in DCAT-AP.",
    lang="en"
)))

# Conformance to DCAT 3
dcat_ap_uri = URIRef("https://www.w3.org/TR/vocab-dcat-3/")
catalog_g.add((catalog_uri, DCT.conformsTo, dcat_ap_uri))

# License – ODbL 1.0
license_uri = URIRef("https://creativecommons.org/publicdomain/zero/1.0/")
catalog_g.add((catalog_uri, DCT.license, license_uri))

# Details about the license
catalog_g.add((license_uri, RDF.type, CC.License))
catalog_g.add((license_uri, CC.legalcode, URIRef(
    "https://creativecommons.org/publicdomain/zero/1.0/"
)))
catalog_g.add((license_uri, RDFS.label, Literal("Creative Commons CC0 1.0 Universal (Public Domain Dedication)", lang="en")))

# Provenance
catalog_g.add((catalog_uri, PROV.wasAttributedTo, publisher_uri))

# List of dataset IDs 
dataset_ids = [
    "D1_population_regions",
    "D2_housing_it",
    "GD1_regions_it",
    "GD2_places_center",
    "GD3_places_islands",
    "GD4_places_north_east",
    "GD5_places_north_west",
    "GD6_places_south",
    "MD1_share_houses_occupation",
    "MD2_share_65_plus",
    "MD3_settlements_count",
    "MD4_dispertion_places",
    "MD5_age_houses_occupation",
    "MED1_settlements_italy",
]

# Add each dataset as a proper DCAT Dataset resource
for dataset_id in dataset_ids:
    dataset_uri = OLD[dataset_id] 
    catalog_g.add((catalog_uri, DCAT3.dataset, dataset_uri))
    catalog_g.add((dataset_uri, RDF.type, DCAT.Dataset))
    catalog_g.add((dataset_uri, DCT.identifier, Literal(dataset_id)))
    

# Saving the RDF
output_dir = os.path.join("rdf", "rdf_serialization")
os.makedirs(output_dir, exist_ok=True)

catalog_file = os.path.join(output_dir, "serialization_catalog.ttl")

with open(catalog_file, "w", encoding="utf-8") as f:
    f.write(catalog_g.serialize(format="turtle"))

print("Serialization complete!")
