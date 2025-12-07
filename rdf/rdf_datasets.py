from rdflib import Graph, Literal, Namespace, URIRef, BNode
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS as DCT, PROV
import os

# Namespaces
DCAT = Namespace("http://www.w3.org/ns/dcat#")
DCAT3 = Namespace("http://www.w3.org/ns/dcat3#")
DCATAPIT = Namespace("http://dati.gov.it/onto/dcatapit/")
ADMS = Namespace("http://www.w3.org/ns/adms#")
CC = Namespace("http://creativecommons.org/ns#")
XSD_NS = Namespace("http://www.w3.org/2001/XMLSchema#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
FOAF_NS = Namespace("https://hexdocs.pm/foaf/FOAF.NS.FOAF.html#summary")

# Base namespace the project datasets
OLD = Namespace("https://github.com/eugeniavd/retired_places/")

g = Graph()

# Prefixes
g.bind("dcat", DCAT)
g.bind("dcat3", DCAT3)
g.bind("dcatapit", DCATAPIT)
g.bind("dct", DCT)
g.bind("adms", ADMS)
g.bind("xsd", XSD_NS)
g.bind("cc", CC)
g.bind("skos", SKOS)
g.bind("old", OLD)
g.bind("prov", PROV)


# Data: List of dataset dictionaries
datasets_list = [
    {
        # D1 – Italy Population 2025
        "id": "D1_population_regions",
        "uri": OLD["D1_population_regions"],

        "title": "D1 – Italy Population 2025",
        "description": (
            "Resident population by age, sex and marital status on January 1st. "
            "It is a process that, starting from Population Census data, calculates "
            "the municipal resident population by sex, year of birth and marital "
            "status as of December 31 of each year and is released as of January 1 "
            "of the following year. Resident population consists of the people "
            "having habitual residence in the national territory even if temporarily "
            "absent, both Italian and foreign citizenship."
        ),

        "publisher_uri": "https://www.istat.it/",
        "publisher_name": "Istituto nazionale di statistica (ISTAT)",
        "creator_uri": "https://www.istat.it/",
        "creator_name": "Italian National Institute of Statistics",

        "language": "it",
        "production_year": "2025",

        "spatial_coverage_uri": "https://viaf.org/viaf/152361066",

        "distribution": [
            {
                "access_url": (
                    "https://github.com/eugeniavd/retired_places/blob/main/"
                    "data/raw/D1_population_regions.csv"
                ),
                "media_type": "text/csv",
                "format": "CSV",
                "access_rights_uri": (
                    "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                ),
            }
        ],

        "source_url": "https://demo.istat.it/app/?i=POS&l=it",

        "license_uri": "https://creativecommons.org/licenses/by/4.0/",
        "keywords": ["regione", "età", "popolazione"],

        "theme": {
            "uri": "http://publications.europa.eu/resource/authority/data-theme/SOCI",
            "label": "Population and society",
        },
    },

    {
        # D2 – Italy Housing Data 2021
        "id": "D2_housing_it",
        "uri": OLD["D2_housing_it"],

        "title": "D2 – Italy Housing Data 2021",
        "description": (
            "Housing census data on dwellings and occupied housing units in Italy. "
            "The dataset provides information on the stock of dwellings by type, "
            "occupancy status and other housing characteristics at territorial level."
        ),

        "publisher_uri": "https://www.istat.it/",
        "publisher_name": "Istituto nazionale di statistica (ISTAT)",
        "creator_uri": "https://www.istat.it/",
        "creator_name": "Italian National Institute of Statistics",

        "language": "it",
        "production_year": "2021",

        "spatial_coverage_uri": "https://viaf.org/viaf/152361066",

        "distribution": [
            
            {

                "access_url": (
                    "https://github.com/eugeniavd/retired_places/blob/main/"
                    "data/raw/D2_housing_it.xlsx"
                ),
                "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "format": "XLSX",
                "access_rights_uri": (
                    "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                ),
            },
        ],

        "source_url": (
            "https://esploradati.istat.it/databrowser/#/it/censpop/"
            "categories/DCSS_ABITAZIONI_TV/IT1,DF_DCSS_ABITAZIONI_TV_1,1.0"
        ),

        "license_uri": "https://creativecommons.org/licenses/by/4.0/",
        "keywords": ["abitazioni", "censimento", "alloggi"],

        "theme": {
            "uri": "http://publications.europa.eu/resource/authority/data-theme/REGI",
            "label": "Regions and cities",
        },
    },

    {
        # GD1 – Italy Regions Boundaries
        "id": "GD1_regions_it",
        "uri": OLD["GD1_regions_it"],

        "title": "GD1 – Italy Regions Boundaries",
        "description": (
            "Geospatial dataset of Italian administrative regions (NUTS 2 level) "
            "used for statistical purposes. The dataset provides polygon geometries "
            "for regional boundaries in 2025."
        ),

        "publisher_uri": "https://www.istat.it/",
        "publisher_name": "Istituto nazionale di statistica (ISTAT)",
        "creator_uri": "https://www.istat.it/",
        "creator_name": "Italian National Institute of Statistics",

        "language": "it",
        "production_year": "2025",

        "spatial_coverage_uri": "https://viaf.org/viaf/152361066",

        "distribution": [
            {
                "access_url": (
                    "https://github.com/eugeniavd/retired_places/tree/main/"
                    "data/raw/GD1_regions_it"
                ),
                "media_type": "application/x-shapefile",
                "format": "SHP",
                "access_rights_uri": (
                    "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                ),
            }
        ],

        "source_url": (
            "https://www.istat.it/notizia/"
            "confini-delle-unita-amministrative-a-fini-statistici-al-1-gennaio-2018-2/"
        ),

        "license_uri": "https://creativecommons.org/licenses/by/4.0/",
        "keywords": ["confini", "regioni", "geometrie"],

        "theme": {
            "uri": "http://publications.europa.eu/resource/authority/data-theme/REGI",
            "label": "Regions and cities",
        },
    },

    {
        # GD2 – Settlements Location Center
        "id": "GD2_places_center",
        "uri": OLD["GD2_places_center"],

        "title": "GD2 – Settlements Location Center",
        "description": (
            "Geospatial dataset of settlement locations in Central Italy, "
            "derived from OpenStreetMap via Geofabrik. Used to identify and map "
            "settlements in the Centre macro-region."
        ),

        "publisher_uri": "https://www.geofabrik.de/",
        "publisher_name": "Geofabrik GmbH",
        "creator_uri": "https://www.openstreetmap.org/",
        "creator_name": "OpenStreetMap Contributors",

        "language": "en",
        "production_year": "2025",

        "spatial_coverage_uri": "https://viaf.org/viaf/152361066",

        "distribution": [
            {
                "access_url": (
                    "https://github.com/eugeniavd/retired_places/tree/main/"
                    "data/raw/GD2_places_center"
                ),
                "media_type": "application/x-shapefile",
                "format": "SHP",
                "access_rights_uri": (
                    "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                ),
            }
        ],

        "source_url": "https://download.geofabrik.de/europe/italy.html",

        "license_uri": "https://opendatacommons.org/licenses/odbl/1-0/",
        "keywords": ["OpenStreetMap", "geometry", "center", "Italy"],

        "theme": {
            "uri": "http://publications.europa.eu/resource/authority/data-theme/REGI",
            "label": "Regions and cities",
        },
    },

    {
        # GD3 – Settlements Location Islands
        "id": "GD3_places_islands",
        "uri": OLD["GD3_places_islands"],

        "title": "GD3 – Settlements Location Islands",
        "description": (
            "Geospatial dataset of settlement locations (populated places) in the "
            "Italian islands (Sicilia, Sardegna), derived from OpenStreetMap via "
            "Geofabrik. Used to map settlements in the Islands macro-region."
        ),

        "publisher_uri": "https://www.geofabrik.de/",
        "publisher_name": "Geofabrik GmbH",
        "creator_uri": "https://www.openstreetmap.org/",
        "creator_name": "OpenStreetMap Contributors",

        "language": "en",
        "production_year": "2025",

        "spatial_coverage_uri": "https://viaf.org/viaf/152361066",

        "distribution": [
            {
                "access_url": (
                    "https://github.com/eugeniavd/retired_places/tree/main/"
                    "data/raw/GD3_places_islands"
                ),
                "media_type": "application/x-shapefile",
                "format": "SHP",
                "access_rights_uri": (
                    "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                ),
            }
        ],

        "source_url": "https://download.geofabrik.de/europe/italy.html",

        "license_uri": "https://opendatacommons.org/licenses/odbl/1-0/",
        "keywords": ["OpenStreetMap", "geometry", "sicily", "islands", "Italy"],

        "theme": {
            "uri": "http://publications.europa.eu/resource/authority/data-theme/REGI",
            "label": "Regions and cities",
        },
    },

    {
        # GD4 – Settlements Location North-East
        "id": "GD4_places_north_east",
        "uri": OLD["GD4_places_north_east"],

        "title": "GD4 – Settlements Location North-East",
        "description": (
            "Geospatial dataset of settlement locations (populated places) in "
            "North-Eastern Italy, derived from OpenStreetMap via Geofabrik."
        ),

        "publisher_uri": "https://www.geofabrik.de/",
        "publisher_name": "Geofabrik GmbH",
        "creator_uri": "https://www.openstreetmap.org/",
        "creator_name": "OpenStreetMap Contributors",

        "language": "en",
        "production_year": "2025",

        "spatial_coverage_uri": "https://viaf.org/viaf/152361066",

        "distribution": [
            {
                "access_url": (
                    "https://github.com/eugeniavd/retired_places/tree/main/"
                    "data/raw/GD4_places_north_east"
                ),
                "media_type": "application/x-shapefile",
                "format": "SHP",
                "access_rights_uri": (
                    "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                ),
            }
        ],

        "source_url": "https://download.geofabrik.de/europe/italy.html",

        "license_uri": "https://opendatacommons.org/licenses/odbl/1-0/",
        "keywords": ["OpenStreetMap", "geometry", "Nord-Est", "Italy"],

        "theme": {
            "uri": "http://publications.europa.eu/resource/authority/data-theme/REGI",
            "label": "Regions and cities",
        },
    },

    {
        # GD5 – Settlements Location North-West
        "id": "GD5_places_north_west",
        "uri": OLD["GD5_places_north_west"],

        "title": "GD5 – Settlements Location North-West",
        "description": (
            "Geospatial dataset of settlement locations (populated places) in "
            "North-Western Italy, derived from OpenStreetMap via Geofabrik."
        ),

        "publisher_uri": "https://www.geofabrik.de/",
        "publisher_name": "Geofabrik GmbH",
        "creator_uri": "https://www.openstreetmap.org/",
        "creator_name": "OpenStreetMap Contributors",

        "language": "en",
        "production_year": "2025",

        "spatial_coverage_uri": "https://viaf.org/viaf/152361066",

        "distribution": [
            {
                "access_url": (
                    "https://github.com/eugeniavd/retired_places/tree/main/"
                    "data/raw/GD5_places_north_west"
                ),
                "media_type": "application/x-shapefile",
                "format": "SHP",
                "access_rights_uri": (
                    "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                ),
            }
        ],

        "source_url": "https://download.geofabrik.de/europe/italy.html",

        "license_uri": "https://opendatacommons.org/licenses/odbl/1-0/",
        "keywords": ["OpenStreetMap", "geometry", "Nord-Ovest", "Italy"],

        "theme": {
            "uri": "http://publications.europa.eu/resource/authority/data-theme/REGI",
            "label": "Regions and cities",
        },
    },

    {
        # GD6 – Settlements Location South
        "id": "GD6_places_south",
        "uri": OLD["GD6_places_south"],

        "title": "GD6 – Settlements Location South",
        "description": (
            "Geospatial dataset of settlement locations (populated places) in "
            "Southern Italy, derived from OpenStreetMap via Geofabrik."
        ),

        "publisher_uri": "https://www.geofabrik.de/",
        "publisher_name": "Geofabrik GmbH",
        "creator_uri": "https://www.openstreetmap.org/",
        "creator_name": "OpenStreetMap Contributors",

        "language": "en",
        "production_year": "2025",

        "spatial_coverage_uri": "https://viaf.org/viaf/152361066",

        "distribution": [
            {
                "access_url": (
                    "https://github.com/eugeniavd/retired_places/tree/main/"
                    "data/raw/GD6_places_south"
                ),
                "media_type": "application/x-shapefile",
                "format": "SHP",
                "access_rights_uri": (
                    "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                ),
            }
        ],

        "source_url": "https://download.geofabrik.de/europe/italy.html",

        "license_uri": "https://opendatacommons.org/licenses/odbl/1-0/",
        "keywords": ["OpenStreetMap", "geometrie", "south", "Italy"],

        "theme": {
            "uri": "http://publications.europa.eu/resource/authority/data-theme/REGI",
            "label": "Regions and cities",
        },
    },

    # MASHED DATASETS
    {
        # MD1 – Share Houses Occupation
        "id": "MD1_share_houses_occupation",
        "uri": OLD["MD1_share_houses_occupation"],

        "title": "MD1 – Share of Occupied and Unoccupied Houses by Region",
        "description": (
            "Derived dataset providing housing occupation indicators by Italian region. "
            "For each region, it reports the number of occupied houses, unoccupied houses "
            "and total housing units, along with the share of unoccupied houses "
            "(share_unoccupied). The table also includes a normalized region name "
            "(region_norm) and a region code (region_code) to support consistent "
            "joining and visualizations."
        ),

        "publisher_uri": "https://github.com/eugeniavd/retired_places",
        "publisher_name": "Retired Places Project",
        "creator_uri": "https://github.com/eugeniavd",
        "creator_name": "Evgeniia Vdovichenko",

        "language": "en",
        "production_year": "2025",

        "spatial_coverage_uri": "https://viaf.org/viaf/152361066",

        "distribution": [
            {
                "access_url": (
                    "https://github.com/eugeniavd/retired_places/blob/main/"
                    "data/processed/MD1_share_houses_occupation.csv"
                ),
                "media_type": "text/csv",
                "format": "CSV",
                "access_rights_uri": (
                    "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                ),
            }
        ],

        "license_uri": "https://creativecommons.org/licenses/by/4.0/",
        "keywords": [
            "housing", "occupied houses", "unoccupied houses",
            "regions"
        ],

        "theme": {
            "uri": "http://publications.europa.eu/resource/authority/data-theme/SOCI",
            "label": "Population and society",
        },
    },

    {
        # MD2 – Share 65 plus
        "id": "MD2_share_65_plus",
        "uri": OLD["MD2_share_65_plus"],

        "title": "MD2 – Share of Population Aged 65+ by Region",
        "description": (
            "Derived dataset providing the share of population aged 65 and over by Italian region. "
            "For each region, it reports the total number of residents aged 65+ (pop_65plus), "
            "total population (tot_pop) and the resulting percentage of older residents "
            "(share_65plus). The table also includes the region name (region) and a numeric "
            "region code (region_code) to support aggregation, joining and visualization."
        ),

        "publisher_uri": "https://github.com/eugeniavd/retired_places",
        "publisher_name": "Retired Places Project",
        "creator_uri": "https://github.com/eugeniavd",
        "creator_name": "Evgeniia Vdovichenko",

        "language": "en",
        "production_year": "2025",

        "spatial_coverage_uri": "https://viaf.org/viaf/152361066",

        "distribution": [
            {
                "access_url": (
                    "https://github.com/eugeniavd/retired_places/blob/main/"
                    "data/processed/MD2_share_65_plus.csv"
                ),
                "media_type": "text/csv",
                "format": "CSV",
                "access_rights_uri": (
                    "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                ),
            }
        ],

        "license_uri": "https://creativecommons.org/licenses/by/4.0/",
        "keywords": [
            "ageing", "65 plus", "older population",
            "regions", "demography"
        ],

        "theme": {
            "uri": "http://publications.europa.eu/resource/authority/data-theme/SOCI",
            "label": "Population and society",
        },
    },

    {
        # MD3 – Settlements per Region
        "id": "MD3_settlements_count",
        "uri": OLD["MD3_settlements_count"],

        "title": "MD3 – Number of Settlements per Region",
        "description": (
            "Derived dataset reporting the number of settlements per Italian region. "
            "For each region, it provides the total count of small settlements "
            "(villages and hamlets), together with the region name (region) and a numeric "
            "region code (region_code). This table is used to quantify and compare how "
            "densely the territory is fragmented into individual settlements across regions."
        ),

        "publisher_uri": "https://github.com/eugeniavd/retired_places",
        "publisher_name": "Retired Places Project",
        "creator_uri": "https://github.com/eugeniavd",
        "creator_name": "Evgeniia Vdovichenko",

        "language": "en",
        "production_year": "2025",

        "spatial_coverage_uri": "https://viaf.org/viaf/152361066",

        "distribution": [
            {
                "access_url": (
                    "https://github.com/eugeniavd/retired_places/blob/main/"
                    "data/processed/MD3_settlements_count.csv"
                ),
                "media_type": "text/csv",
                "format": "CSV",
                "access_rights_uri": (
                    "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                ),
            }
        ],

        "license_uri": "https://opendatacommons.org/licenses/odbl/1-0/",
        "keywords": [
            "settlements", "places",
            "regions", "geospatial"
        ],

        "theme": {
            "uri": "http://publications.europa.eu/resource/authority/data-theme/REGI",
            "label": "Regions and cities",
        },
    },

    {
        # MD4 – Dispersed Settlements Index
        "id": "MD4_dispertion_places",
        "uri": OLD["MD4_dispertion_places"],

        "title": "MD4 – Dispersed Settlements Index by Region",
        "description": (
            "Derived index capturing the dispersion of settlements across Italian "
            "regions. The dataset combines the number of small settlements with regional "
            "population or area to approximate how dispersed or concentrated "
            "settlement patterns are in each region."
        ),

        "publisher_uri": "https://github.com/eugeniavd/retired_places",
        "publisher_name": "Retired Places Project",
        "creator_uri": "https://github.com/eugeniavd",
        "creator_name": "Evgeniia Vdovichenko",

        "language": "en",
        "production_year": "2025",

        "spatial_coverage_uri": "https://viaf.org/viaf/152361066",

        "distribution": [
            {
                "access_url": (
                    "https://github.com/eugeniavd/retired_places/blob/main/"
                    "data/processed/MD4_dispertion_places.csv"
                ),
                "media_type": "text/csv",
                "format": "CSV",
                "access_rights_uri": (
                    "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                ),
            }
        ],

        "license_uri": "https://opendatacommons.org/licenses/odbl/1-0/",
        "keywords": [
            "settlements dispersion", "dispersed places",
            "regional index"
        ],

        "theme": {
            "uri": "http://publications.europa.eu/resource/authority/data-theme/REGI",
            "label": "Regions and cities",
        },
    },

    {
        # MD5 – Age vs Houses Occupation
        "id": "MD5_age_houses_occupation",
        "uri": OLD["MD5_age_houses_occupation"],

        "title": "MD5 – Ageing vs Housing Occupation by Region",
        "description": (
            "Derived dataset combining ageing indicators and housing occupation metrics "
            "for each Italian region. For every region, it reports the size and share of "
            "the 65+ population (pop_65plus, tot_pop, share_65plus) together with housing "
            "occupation figures (homes_occupied, homes_unoccupied, homes_total) and the "
            "share of unoccupied houses (share_unoccupied). The table also includes the "
            "normalized region name (region_norm), a region code (region_code) and a "
            "macro-region label (macro_region). To support typology and ranking, it adds "
            "boolean flags for high ageing and high vacancy (high_65, high_vac), a 2×2 "
            "category label (category_2x2) and regional ranks for ageing and vacancy "
            "indicators (rank_65, rank_vac, rank_diff)."
        ),

        "publisher_uri": "https://github.com/eugeniavd/retired_places",
        "publisher_name": "Retired Places Project",
        "creator_uri": "https://github.com/eugeniavd",
        "creator_name": "Evgeniia Vdovichenko",

        "language": "en",
        "production_year": "2025",

        "spatial_coverage_uri": "https://viaf.org/viaf/152361066",

        "distribution": [
            {
                "access_url": (
                    "https://github.com/eugeniavd/retired_places/blob/main/"
                    "data/processed/MD5_age_houses_occupation.csv"
                ),
                "media_type": "text/csv",
                "format": "CSV",
                "access_rights_uri": (
                    "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                ),
            }
        ],

        "license_uri": "https://creativecommons.org/licenses/by/4.0/",
        "keywords": [
            "ageing", "housing", "65 plus",
            "occupied houses", "regional indicators"
        ],

        "theme": {
            "uri": "http://publications.europa.eu/resource/authority/data-theme/SOCI",
            "label": "Population and society",
        },
    },

    {
        # MED1 – Settlements Italy (merged geospatial dataset)
        "id": "MED1_settlements_italy",
        "uri": OLD["MED1_settlements_italy"],

        "title": "MED1 – Settlements Italy (Merged Geospatial Layer)",
        "description": (
            "Merged geospatial dataset of settlement locations (populated places) "
            "for the whole of Italy. It combines the regional settlement extracts "
            "used in the project (Center, Islands, North-East, North-West, South) "
            "into a single national layer stored as a GeoPackage (GPKG). The dataset "
            "is derived from OpenStreetMap data and is used as the core geospatial "
            "layer for the analysis of settlement patterns across Italian regions."
        ),

        "publisher_uri": "https://github.com/eugeniavd/retired_places",
        "publisher_name": "Retired Places Project",
        "creator_uri": "https://github.com/eugeniavd",
        "creator_name": "Evgeniia Vdovichenko",

        "language": "en",
        "production_year": "2025",

        "spatial_coverage_uri": "https://viaf.org/viaf/152361066",

        "distribution": [
            {
                "access_url": (
                    "https://github.com/eugeniavd/retired_places/blob/main/"
                    "data/processed/MED1_settlements_italy.gpkg"
                ),
                "media_type": "application/geopackage+sqlite3",
                "format": "GPKG",
                "access_rights_uri": (
                    "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                ),
            }
        ],

        "license_uri": "https://opendatacommons.org/licenses/odbl/1-0/",

        "keywords": [
            "settlements", "GeoPackage",
            "OpenStreetMap", "Italy"
        ],

        "theme": {
            "uri": "http://publications.europa.eu/resource/authority/data-theme/REGI",
            "label": "Regions and cities",
        },
    },
]


for data in datasets_list:
    # --- URI ---
    dataset_uri = data["uri"]                 
    catalog_uri = OLD["catalog"]             

    # Catalog and dataset connnection
    g.add((catalog_uri, DCAT.dataset, dataset_uri))

    # type
    g.add((dataset_uri, RDF.type, DCAT.Dataset))

    # --- Language ---
    content_lang = data.get("language")

    # --- Title ---
    title = data.get("title")
    if title:
        if content_lang:
            g.add((dataset_uri, DCT.title, Literal(title, lang=content_lang)))
        else:
            g.add((dataset_uri, DCT.title, Literal(title)))

    # --- Description ---
    description = data.get("description")
    if description:
        if content_lang:
            g.add((dataset_uri, DCT.description, Literal(description, lang=content_lang)))
        else:
            g.add((dataset_uri, DCT.description, Literal(description)))

    # --- Publisher ---
    publisher_uris = data.get("publisher_uri")
    publisher_names = data.get("publisher_name")

    if publisher_uris:
        if not isinstance(publisher_uris, list):
            publisher_uris = [publisher_uris]

        for i, uri in enumerate(publisher_uris):
            publisher_uri = URIRef(uri)
            g.add((dataset_uri, DCT.publisher, publisher_uri))
            g.add((publisher_uri, RDF.type, FOAF_NS.Agent))

            if publisher_names:
                if isinstance(publisher_names, list):
                    if i < len(publisher_names):
                        g.add((publisher_uri, FOAF_NS.name, Literal(publisher_names[i])))
                else:
                    g.add((publisher_uri, FOAF_NS.name, Literal(publisher_names)))

    # --- Creator ---
    if data.get("creator_uri"):
        creator_uri = URIRef(data["creator_uri"])
        g.add((dataset_uri, DCT.creator, creator_uri))
        g.add((creator_uri, RDF.type, FOAF_NS.Agent))
        if data.get("creator_name"):
            g.add((creator_uri, FOAF_NS.name, Literal(data["creator_name"])))

    if content_lang:
        g.add(
            (dataset_uri,
             DCT.language,
             URIRef(f"http://lexvo.org/id/iso639-1/{content_lang}"))
        )

    # --- production_year ---
    if data.get("production_year"):
        g.add(
            (dataset_uri,
             DCT.issued,
             Literal(data["production_year"], datatype=XSD_NS.gYear))
        )

    # --- Spatial coverage ---
    if data.get("spatial_coverage_uri"):
        g.add((dataset_uri, DCT.spatial, URIRef(data["spatial_coverage_uri"])))

    # --- Source ---
    if data.get("source_url"):
        src = URIRef(data["source_url"])
        g.add((dataset_uri, DCT.source, src))
        g.add((dataset_uri, PROV.wasDerivedFrom, src))

    # --- Distribution ---
    if "distribution" in data:
        dist_list = data["distribution"]
        
        if isinstance(dist_list, dict):
            dist_list = [dist_list]

        for dist_data in dist_list:
            dist_bnode = BNode()
            g.add((dataset_uri, DCAT.distribution, dist_bnode))
            g.add((dist_bnode, RDF.type, DCAT.Distribution))

            access_url = dist_data.get("access_url")
            if access_url:
                g.add((dist_bnode, DCAT.accessURL, URIRef(access_url)))

            media_type = dist_data.get("media_type")
            if media_type:
                g.add((dist_bnode, DCAT.mediaType, Literal(media_type)))

            file_format = dist_data.get("format")
            if file_format:
                g.add((dist_bnode, DCT["format"], Literal(file_format)))

            byte_size = dist_data.get("byte_size")
            if byte_size is not None:
                g.add(
                    (dist_bnode,
                     DCAT.byteSize,
                     Literal(byte_size, datatype=XSD_NS.integer))
                )

            access_rights = dist_data.get("access_rights_uri")
            if access_rights:
                g.add(
                    (dist_bnode,
                     DCT.accessRights,
                     URIRef(access_rights))
                )

    # --- License ---
    if data.get("license_uri"):
        g.add((dataset_uri, DCT.license, URIRef(data["license_uri"])))

    # --- Keywords ---
    if "keywords" in data:
        for keyword in data["keywords"]:
            if content_lang:
                g.add((dataset_uri, DCAT.keyword, Literal(keyword, lang=content_lang)))
            else:
                g.add((dataset_uri, DCAT.keyword, Literal(keyword)))

    # --- Theme ---
    if data.get("theme"):
        theme_uri = URIRef(data["theme"]["uri"])

        g.add((dataset_uri, DCAT.theme, theme_uri))

        g.add((theme_uri, RDF.type, SKOS.Concept))
        g.add((
            theme_uri,
            SKOS.prefLabel,
            Literal(data["theme"]["label"], lang="en"),
        ))

# Saving the RDF
output_dir = os.path.join("rdf", "rdf_serialization")
os.makedirs(output_dir, exist_ok=True)

datasets_file = os.path.join(output_dir, "serialization_datasets.ttl")

with open(datasets_file, "w", encoding="utf-8") as f:
    f.write(g.serialize(format="turtle"))

print("Serialization complete!")