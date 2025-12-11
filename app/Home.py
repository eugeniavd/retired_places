import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Retired Places",
    layout="wide"
)
import pandas as pd
import json
import plotly.express as px
from pathlib import Path
import numpy as np
import plotly.graph_objects as go



# ---------- DATA LOADING ----------

@st.cache_data
def load_data():
    """
    Load regional metrics and the GeoJSON with regional boundaries.

    We join the metrics table to the GeoJSON using the region code. 
    This is more robust than matching on labels.
    """
    base_path = Path(__file__).resolve().parent.parent
    data_path = base_path / "data" / "app_ready"

    df = pd.read_csv(data_path / "MD5_age_houses_occupation.csv")
    df["COD_REG"] = df["region_code"].astype(int)

    df_disp = pd.read_csv(data_path / "MD4_dispertion_places.csv")

    with open(data_path / "italy_regions.geojson", "r", encoding="utf-8") as f:
        geojson = json.load(f)

    return df, geojson, df_disp

df_regions, regions_geojson, df_disp = load_data()



# ---------- SIDEBAR NAVIGATION ----------
NAV_ITEMS = [
    ("About", "#about-section"),
    ("Key Findings", "#results-section"),
    ("Scenario", "#scenario-section"),
    ("Datasets", "#datasets-section"),
    ("Analysis", "#docs-section"),
    ("Sustainability", "#sustainability-section"),
    ("Visualisations", "#graphs-section"),
    ("RDF Assertion", "#rdf-section"),
    ("Licenses & Credits", "#licenses-section"),
]

with st.sidebar:
    st.title("Jump to section")
    for label, anchor in NAV_ITEMS:
        st.markdown(f"- [{label}]({anchor})")


# ---------- SESSION STATE ----------
if "show_all_charts" not in st.session_state:
    st.session_state["show_all_charts"] = False


# ---------- PAGE CSS ----------
button_css = """
<style>
.button,
.button:link,
.button:visited,
.button:hover,
.button:active {
    display: inline-block;
    padding: 0.4rem 1.2rem;
    border-radius: 4px;            
    background-color: #f97316;      
    color: #ffffff !important;
    text-decoration: none !important;
    font-weight: 600;
    font-size: 0.9rem;
    border: none;
    cursor: pointer;
    transition: background-color 0.15s ease, transform 0.15s ease,
                box-shadow 0.15s ease;
}

.button:hover {
    background-color: #ea580c;    
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    transform: translateY(-1px);
}
</style>
"""
st.markdown(button_css, unsafe_allow_html=True)

# ontology tiles
ontology_css = """
<style>
#ontology-tiles div[data-testid="stExpander"] {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    background-color: #ffffff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    margin-bottom: 0.8rem;
    transition: border-color 0.15s ease, box-shadow 0.15s ease,
                transform 0.15s ease, background-color 0.15s ease;
}

#ontology-tiles div[data-testid="stExpander"]:hover {
    background-color: #fff7f0; 
    box-shadow: 0 3px 8px rgba(0,0,0,0.1);
    transform: translateY(-2px);
}

#ontology-tiles div[data-testid="stExpander"] summary {
    padding: 0.55rem 0.9rem;
    font-weight: 600;
    font-size: 0.9rem;
}
</style>
"""
st.markdown(ontology_css, unsafe_allow_html=True)

# dataset cards
card_css = """
<style>
.dataset-card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    background-color: #ffffff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    margin-bottom: 1.5rem;
    height: 100%;
    transition: background-color 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease;
}

.dataset-card:hover {
    background-color: #fff7f0; 
    box-shadow: 0 3px 8px rgba(0,0,0,0.1);
    transform: translateY(-2px);
}

.dataset-card-title {
    font-weight: 700;
    margin-bottom: 0.1rem;
}

.dataset-card-subtitle {
    font-size: 0.9rem;
    color: #555555;
    margin-bottom: 0.35rem;
}

.dataset-card-divider {
    border-top: 1px solid #e0e0e0;
    margin: 0.35rem 0 0.6rem 0;
}

.dataset-card-uri {
    font-family: monospace;
    font-size: 0.9rem;
}
</style>
"""
st.markdown(card_css, unsafe_allow_html=True)


# ---------- HERO BLOCK ----------
with st.container():
    st.markdown("<div id='top'></div>", unsafe_allow_html=True)
    st.title('"Retired" Places')
    st.markdown(
    "##### *To what extent do municipalities with a high share of residents aged 65+ "
    "also show signs of settlement abandonment, and where do “retired people” and "
    "“retired places” diverge in Italy?*"
)
    
st.write("") 

st.markdown(
        """
          <a class="button"
             href="#results-section">
             FIND OUT
          </a>
        </div>
        """,
        unsafe_allow_html=True,
    )    

st.write("---")


# ---------- ABOUT ----------
st.markdown("<div id='about-section'></div>", unsafe_allow_html=True)
st.header("About the Project")

 
st.write(
    """
    **“Retired” Places** is a data-driven exploration of how population ageing, housing vacancy, and settlement structure intersect across Italian regions. The project asks where “retired people” 
    (older residents) and “retired places” (territories marked by abandonment and dispersion) overlap — 
    and where they diverge.

Building on official open data from [**ISTAT**](https://www.istat.it/) and volunteered geographic 
information from [**OpenStreetMap**](https://download.geofabrik.de/europe/italy.html), 
the project combines statistics on the share of residents aged 65+, housing occupancy, and the density of 
small settlements into a single analytical framework. By tracing these indicators together, it becomes 
possible to identify territories that are simultaneously older and emptier, as well as regions that are 
ageing but still densely lived-in.

The project provides interactive maps, ranked charts, and quadrants that allow users to explore 
territorial patterns behind familiar narratives about “ghost villages”, inner areas, and regional divides 
in Italy. Rather than treating ageing or depopulation as isolated “problems”, the project foregrounds 
structural conditions — from housing markets to dispersed settlement patterns — and supports more informed 
debate on territorial cohesion and the geography of later life.

This prototype focuses on three complementary dimensions:

- **Ageing and demography** – share of residents aged 65+ across regions.  
- **Housing and vacancy** – proportion of unoccupied dwellings as a proxy for “retired” places.  
- **Settlement structure** – counts and dispersion of small settlements, highlighting territories where 
people are thinly spread.

    """
)
st.write("---")


# ---------- Key Findings ----------
st.markdown("<div id='results-section'></div>", unsafe_allow_html=True)
st.header("Key Findings")
st.markdown("*This section highlights the main quantitative signals from the project.*")

tab_map, tab_summary = st.tabs(["Map", "Summary"])

with tab_map:
    st.subheader("Who Still Lives Here?")

    # ---- filters based on the metrics DataFrame ----
    macro_list = sorted(df_regions["macro_region"].dropna().unique())
    selected_macro = st.multiselect(
        "Filter by macro-region",
        options=macro_list,
        default=macro_list,
    )

    show_ageing = st.checkbox("Show the share of 65+", value=True)
    show_vacancy = st.checkbox("Show the share of abandoned homes", value=False)

    # Filter metrics by selected macro-regions
    df_map = df_regions[df_regions["macro_region"].isin(selected_macro)]

    if not show_ageing and not show_vacancy:
        st.info("Select at least one layer to display the map.")

    elif show_ageing and not show_vacancy:
        # only ageing layer

        fig_age = px.choropleth(
            df_map,
            geojson=regions_geojson,
            locations="COD_REG",
            featureidkey="properties.COD_REG",
            color="share_65plus",
            hover_name="region_norm",
            projection="mercator",
            hover_data={
                "share_65plus": ":.2f",  
                "region_code": False,        
            },
        )

        fig_age.update_geos(fitbounds="locations", visible=False)
        fig_age.update_layout(
            height=700,
            margin={"r": 40, "t": 20, "l": 20, "b": 20},
            coloraxis_colorbar_title="Share of 65+ (%)",
        )

        st.plotly_chart(fig_age, use_container_width=True)

    elif show_vacancy and not show_ageing:
        # only vacancy layer

        fig_vac = px.choropleth(
            df_map,
            geojson=regions_geojson,
            locations="COD_REG",
            featureidkey="properties.COD_REG",
            color="share_unoccupied",
            hover_name="region_norm",
            projection="mercator",
            hover_data={
                "share_unoccupied": ":.2f",
                "region_code": False,
            },
        )
    
        fig_vac.update_geos(fitbounds="locations", visible=False)
        fig_vac.update_layout(
            height=700,
            margin={"r": 40, "t": 20, "l": 20, "b": 20},
            coloraxis_colorbar_title="Share of unoccupied homes (%)",
        )
        st.plotly_chart(fig_vac, use_container_width=True)

    else:
        # both layers → two maps side by side
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Ageing layer (share_65plus)**")
            fig_age = px.choropleth(
                df_map,
                geojson=regions_geojson,
                locations="COD_REG",
                featureidkey="properties.COD_REG",
                color="share_65plus",
                hover_name="region",
                projection="mercator",
            )
            fig_age.update_geos(fitbounds="locations", visible=False)
            fig_age.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                coloraxis_colorbar_title="Share of 65+ (%)",
            )
            st.plotly_chart(fig_age, use_container_width=True)

        with col2:
            st.markdown("**Vacancy layer (share_unoccupied)**")
            fig_vac = px.choropleth(
                df_map,
                geojson=regions_geojson,
                locations="COD_REG",
                featureidkey="properties.COD_REG",
                color="share_unoccupied",
                hover_name="region",
                projection="mercator",
            )
            fig_vac.update_geos(fitbounds="locations", visible=False)
            fig_vac.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                coloraxis_colorbar_title="Share of unoccupied homes (%)",
            )
            st.plotly_chart(fig_vac, use_container_width=True)

with tab_summary:
    st.subheader("Research Summary")
    st.write(
        "This tab highlights a few key quantitative signals from the analysis of "
        "ageing, housing vacancy and settlement patterns across Italian regions."
    )

    # --- Local CSS for the KPI-style cards ---
    results_css = """
    <style>
    .results-row {
        display: flex;
        flex-wrap: wrap;
        gap: 2.5rem;
        margin-top: 1.8rem;
        margin-bottom: 2.2rem;
    }
    .result-card {
        flex: 1 1 260px;
        display: flex;
        align-items: flex-start;
        gap: 0.9rem;
    }
    .result-icon {
        font-size: 2.3rem;
        line-height: 1;
    }
    .result-main {
    font-size: 3rem;   
    font-weight: 700;
    margin: 0;
}
    .result-label {
        font-size: 0.95rem;
        margin: 0.15rem 0 0 0;
    }
    </style>
    """
    st.markdown(results_css, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="results-row">
          <div class="result-card">
            <div class="result-icon">📊</div>
            <div>
              <p class="result-main">8</p>
              <p class="result-label">
                <strong>Datasets</strong>, including source and mashup tables, underpin the analysis of
                ageing, vacancy and settlement structure across Italy.
              </p>
            </div>
          </div>

          <div class="result-card">
            <div class="result-icon">👵</div>
            <div>
              <p class="result-main">24.73%</p>
              <p class="result-label">
                <strong>National share of residents aged 65+</strong> in 2025, used as a benchmark for
                comparing regional ageing patterns.
              </p>
            </div>
          </div>
        </div>

        <div class="results-row">
          <div class="result-card">
            <div class="result-icon">🏚️</div>
            <div>
              <p class="result-main">5</p>
              <p class="result-label">
                <strong>Regions in the “Old & Empty” quadrant</strong> – combining above-median ageing and
                housing vacancy.
              </p>
            </div>
          </div>

          <div class="result-card">
            <div class="result-icon">🗺️</div>
            <div>
              <p class="result-main">Valle d'Aosta</p>
              <p class="result-label">
                The <strong>most dispersed region</strong> has a Dispersed Settlements Index over ten times
                higher than the national average, signalling very fragmented settlement patterns.
              </p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("---")


# ---------- SCENARIO ----------
st.markdown("<div id='scenario-section'></div>", unsafe_allow_html=True)
st.header("Scenario")
st.markdown("*This section outlines the narrative scenario behind the project – "
    "who the analysis is for, and how the "
    "data-driven story of ageing and “retired places” in Italy is meant to "
    "be explored through the dashboard.*")
st.markdown(
    "##### *What happens to a country when its people grow older and its homes quietly empty out?*"
)
st.write(
    """
    We used official 
    statistics to trace how ageing, housing vacancy, and settlement patterns play out across Italy’s regions.
      By combining ISTAT data on residents aged 65+, housing stock and unoccupied dwellings with 
      OpenStreetMap information on small settlements, the project asks where “retired people” 
      and “retired places” overlap – and where they do not. 

Through interactive maps and charts, readers can explore regions that are both older and emptier, 
territories that are ageing but still densely lived-in, and areas where services and settlements are 
thinly spread across many tiny places. By turning dispersed indicators into a coherent narrative, the 
project aims to inform public debate on territorial cohesion, service provision for older residents, 
and the future of Italy’s inner and rural areas – highlighting where policy, planning, and community 
initiatives are most urgently needed to keep places liveable as the population ages.

    """
)

st.write("---")


# ---------- DATASETS ----------
st.markdown("<div id='datasets-section'></div>", unsafe_allow_html=True)
st.header("Datasets")
st.markdown("*This section documents the selection and use of datasets in the project. The project makes " \
"use of 14 distinct datasets, comprising both primary (source) and derived (mashup) data.*"
)


def render_dataset_card(ds: dict):
    
    license_url = ds.get("license_url")
    if license_url:
        license_html = f'<a href="{license_url}" target="_blank">{ds["license"]}</a>'
    else:
        license_html = ds["license"]

    uri_label = ds.get("uri_label", ds["uri"])
    uri_html = f'<a href="{ds["uri"]}" target="_blank">{uri_label}</a>'

    st.markdown(
        f"""
        <div class="dataset-card">
          <div class="dataset-card-title">{ds['title']}</div>
          <div class="dataset-card-subtitle">ID: {ds['id']}</div>
          <div class="dataset-card-divider"></div>
          <p>
            <strong>Publisher:</strong> {ds['publisher']}<br>
            <strong>Format:</strong> {ds['format']}<br>
            <strong>Metadata:</strong> {ds['metadata']}<br>
            <strong>URI:</strong> <span class="dataset-card-uri">{uri_html}</span><br>
            <strong>License:</strong> {license_html}
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


source_datasets = [
    {
        "id": "D1_population_regions",
        "title": "D1 – Italy Population 2025",
        "publisher": "Istat",
        "format": "CSV",
        "metadata": "Provided",
        "uri": "https://demo.istat.it/app/?i=POS&l=it",
        "uri_label": "Popolazione residente",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
    },
    {
        "id": "D2_housing_it",
        "title": "D2 – Italy Housing Data 2021",
        "publisher": "IstatData",
        "format": "CSV, XLXS",
        "metadata": "Provided",
        "uri": "https://esploradati.istat.it/databrowser/#/it/censpop/categories/DCSS_ABITAZIONI_TV/IT1,DF_DCSS_ABITAZIONI_TV_1,1.0",
        "uri_label": "Censimento delle abitazioni",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
    },
    {
        "id": "GD1_regions_it",
        "title": "GD1 – Italy Regions Boundaries",
        "publisher": "Istat",
        "format": "SHP",
        "metadata": "Provided",
        "uri": "https://www.istat.it/notizia/confini-delle-unita-amministrative-a-fini-statistici-al-1-gennaio-2018-2/",
        "uri_label": "Confini amministrativi",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
    },
    {
        "id": "GD2_places_center",
        "title": "GD2 – Settlements Location Center",
        "publisher": "Geofabric",
        "format": "SHP",
        "metadata": "Provided",
        "uri": "https://download.geofabrik.de/europe/italy.html",
        "uri_label": "OpenStreetMap data Italy",
        "license": "ODbL 1.0",
        "license_url": "https://opendatacommons.org/licenses/odbl/1-0/",
    },
    {
        "id": "GD3_places_islands",
        "title": "GD3 – Settlements Location Islands",
        "publisher": "Geofabric",
        "format": "SHP",
        "metadata": "Provided",
        "uri": "https://download.geofabrik.de/europe/italy.html",
        "uri_label": "OpenStreetMap data Italy",
        "license": "ODbL 1.0",
        "license_url": "https://opendatacommons.org/licenses/odbl/1-0/",
    },
    {
        "id": "GD4_ places_north_east",
        "title": "GD4 – Settlements Location North-East",
        "publisher": "Geofabric",
        "format": "SHP",
        "metadata": "Provided",
        "uri": "https://download.geofabrik.de/europe/italy.html",
        "uri_label": "OpenStreetMap data Italy",
        "license": "ODbL 1.0",
        "license_url": "https://opendatacommons.org/licenses/odbl/1-0/",
    },
    {
        "id": "GD5_ places_north_west",
        "title": "GD5 – Settlements Location North-West",
        "publisher": "Geofabric",
        "format": "SHP",
        "metadata": "Provided",
        "uri": "https://download.geofabrik.de/europe/italy.html",
        "uri_label": "OpenStreetMap data Italy",
        "license": "ODbL 1.0",
        "license_url": "https://opendatacommons.org/licenses/odbl/1-0/",
    },
    {
        "id": "GD6_ places_south",
        "title": "GD6 – Settlements Location South",
        "publisher": "Geofabric",
        "format": "SHP",
        "metadata": "Provided",
        "uri": "https://download.geofabrik.de/europe/italy.html",
        "uri_label": "OpenStreetMap data Italy",
        "license": "ODbL 1.0",
        "license_url": "https://opendatacommons.org/licenses/odbl/1-0/",
    },

]

mashup_datasets = [
    {
        "id": "MD1_share_houses_occupation",
        "title": "MD1 – Share Houses Occupation",
        "publisher": "Retired Places Project",
        "format": "CSV",
        "metadata": "Provided",
        "uri": "https://github.com/eugeniavd/retired_places/blob/main/data/processed/MD1_share_houses_occupation.csv",
        "uri_label": "MD1_share_houses_occupation",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
    },
    {
        "id": "MD2_share_65_plus",
        "title": "MD2 – Share 65 Plus",
        "publisher": "Retired Places Project",
        "format": "CSV",
        "metadata": "Provided",
        "uri": "https://github.com/eugeniavd/retired_places/blob/main/data/processed/MD2_share_65_plus.csv",
        "uri_label": "MD2_share_65_plus",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
    },
    {
        "id": "MD3_settlements_count",
        "title": "MD3 – Settlements per Region",
        "publisher": "Retired Places Project",
        "format": "CSV",
        "metadata": "Provided",
        "uri": "https://github.com/eugeniavd/retired_places/blob/main/data/processed/MD3_settlements_count.csv",
        "uri_label": "MD3_settlements_count",
        "license": "ODbL 1.0",
        "license_url": "https://opendatacommons.org/licenses/odbl/1-0/"
    },
    {
        "id": "MD4_dispertion_places",
        "title": "MD4 - Dispersed Settlements Index",
        "publisher": "Retired Places Project",
        "format": "CSV",
        "metadata": "Provided",
        "uri": "https://github.com/eugeniavd/retired_places/blob/main/data/processed/MD4_dispertion_places.csv",
        "uri_label": "MD4_dispertion_places",
        "license": "ODbL 1.0",
        "license_url": "https://opendatacommons.org/licenses/odbl/1-0/"
    },
    {
        "id": "MD5_age_houses_occupation",
        "title": "MD5 – Age vs Houses Occupation",
        "publisher": "Retired Places Project",
        "format": "CSV",
        "metadata": "Provided",
        "uri": "https://github.com/eugeniavd/retired_places/blob/main/data/processed/MD5_age_houses_occupation.csv",
        "uri_label": "MD5_age_houses_occupation",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
    },
]

merged_datasets = [
    {
        "id": "MED1_settlements_italy",
        "title": "MED1 – Settlements Italy",
        "publisher": "Retired Places Project",
        "format": "GPKG",
        "metadata": "Provided",
        "uri": "https://github.com/eugeniavd/retired_places/blob/main/data/processed/MED1_settlements_italy.gpkg ",
        "uri_label": "MED1_settlements_italy",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
    },
   
]

tab_source, tab_mashup, tab_merged, tab_preproc = st.tabs(
    ["Source datasets", "Mashup datasets", "Merged datasets", "Preprocessing pipeline"]
)

cols_per_row = 3  

with tab_source:
    st.markdown(
        """
Eight source datasets were selected and downloaded from:

- **I.Stat**, the official data warehouse of ISTAT (Italian National Institute of Statistics),  
  which organises statistical information by theme in multidimensional tables and provides
  a wide range of standardised metadata; and
- The **OpenStreetMap (OSM)** project, which offers volunteered geographic information on
  settlements and places in Italy.

These source datasets were chosen on the basis of:

- their provenance from authoritative or well-documented providers (ISTAT and OSM),
- their typology (demographic, housing, and geospatial data),
- their formats (machine-readable tabular data such as CSV/Excel and vector geodata such as shapefiles),
- the richness and standardisation of their metadata (in particular, adherence to ISTAT’s metadata model and,
  where applicable, DCAT-AP_IT), and
- their open licensing conditions (e.g. **CC BY 4.0** for ISTAT, **ODbL 1.0** for OSM), which enable lawful
  reuse and publication of derived products.
        """
    )

    n = len(source_datasets)
    for i in range(0, n, cols_per_row):
        row_items = source_datasets[i : i + cols_per_row]
        cols = st.columns(cols_per_row)

        start_idx = 0

        for ds, col in zip(row_items, cols[start_idx : start_idx + len(row_items)]):
            with col:
                render_dataset_card(ds)

with tab_mashup:
    st.markdown(
        """
On the basis of the sources, we constructed 5 mashup and 1 merged dataset in which the original tables and geodata 
were cleaned, integrated, and harmonised into a coherent analytical framework. These mashup datasets 
combine demographic indicators, housing indicators, and settlement structure measures at the regional 
level, and were explicitly tailored to address the project’s research questions. In doing so, we preserved 
explicit references to the provenance, typology, formats, metadata, and licenses of the underlying sources, 
ensuring that the resulting integrated datasets are both analytically robust and compliant with open-data 
reuse requirements.
        """
    )
    n = len(mashup_datasets)
    for i in range(0, n, cols_per_row):
        row_items = mashup_datasets[i : i + cols_per_row]
        cols = st.columns(cols_per_row)

        if len(row_items) == 2 and i + cols_per_row >= n:
            start_idx = 0  
        else:
            start_idx = 0

        for ds, col in zip(row_items, cols[start_idx : start_idx + len(row_items)]):
            with col:
                render_dataset_card(ds)

with tab_merged:
    n = len(merged_datasets)
    for i in range(0, n, cols_per_row):
        row_items = merged_datasets[i : i + cols_per_row]
        cols = st.columns(cols_per_row)

        if len(row_items) == 2 and i + cols_per_row >= n:
            start_idx = 0  
        else:
            start_idx = 0

        for ds, col in zip(row_items, cols[start_idx : start_idx + len(row_items)]):
            with col:
                render_dataset_card(ds)


with tab_preproc:
    st.markdown(
        """
### Data Cleaning and Preprocessing

We define “older people” as those aged **65 years and over**, following Eurostat’s demographic convention. 
For example, the report *Ageing Europe – statistics on population developments* describes “older people” 
as the population “aged 65 years or more” when analysing ageing trends and regional age structures in the EU.

The source datasets then underwent a cleaning and preprocessing phase. The workflow includes:

- **Ingestion of raw sources** (ISTAT CSV/SDMX tables and ISTAT/OSM geodata).  
- **Cleaning and harmonisation of region identifiers**, including alignment of region codes and names across 
  all tables, as well as checks for missing values and duplicate records.  
- **Computation of indicators**, such as `share_65plus`, `share_unoccupied`, `settlements_count`, the 2×2 
  typology `category_2x2`, and the divergence measure `rank_diff`, together with settlement counts and the 
  *Dispersed Settlements Index*.  
- **Joining** the indicators to regional geometries to create map-ready geospatial layers.  
- **Export** of app-ready tables (MD1–MD5, MED1) and GeoJSON layers used in the visualisations.

All transformation steps are implemented in reproducible Jupyter notebooks stored in the
project repository.
    """
    )

    st.write("") 

    st.markdown(
        """
        <div style="text-align: center; margin-top: 0.5rem;">
          <span style="margin-right: 0.75rem; font-weight: 500;">
            Look at preprocessing notebooks (GitHub)
          </span>
          <a class="button"
             href="https://github.com/eugeniavd/retired_places/tree/main/data_preparation/notebooks"
             target="_blank">
             GO
          </a>
        </div>
        """,
        unsafe_allow_html=True,
    )    

st.write("---")


# ---------- ANALYSIS ----------
st.markdown("<div id='docs-section'></div>", unsafe_allow_html=True)
st.header("Analysis")

st.markdown("*This section summarises the data quality, legal, ethical and technical assessments carried " \
"out for the main datasets and derived indicators, highlighting key limitations and clarifying the " \
"conditions under which the data can be safely interpreted and reused.*")


DATASET_TITLES = {
    "d1": "D1 – Italy Population 2025",
    "d2": "D2 – Italy Housing Data 2021",
    "gd1": "GD1 – Italy Regions Boundaries",
    "gd2_gd6": "GD2–GD6 – Settlements Location",
}

DATASET_KEYS = ["d1", "d2", "gd1", "gd2_gd6"]

technical_datasets = {
    "d1": "D1 – Italy Population 2025",
    "d2": "D2 – Italy Housing Data 2021",
    "gd1": "GD1 – Italy Regions Boundaries",
    "gd2_gd6": "GD2–GD6 – Settlements Location",
    "md1": "MD1 – Share Houses Occupation",
    "md2": "MD2 – Share 65 Plus",
    "md3": "MD3 – Settlements per Region",
    "md4": "MD4 – Dispersed Settlements Index",
    "md5": "MD5 – Age vs Houses Occupation",
}

QUALITY_TEXTS = {
    "d1": """
**Data quality – D1: Italy Population 2025**

*Accuracy – High*

The dataset is structurally clean: numeric fields ("Totale maschi", "Totale femmine", etc) are consistently 
parsed as numbers, and region codes/names follow the expected Italian regional structure.

*Coherence – High*

Region names and region codes are internally consistent (20 regions present, with no obvious duplicates or conflicting labels).
Age values run from 0 to 100 plus a 999 “overall” aggregate, which is coherent with standard demographic tables (single-year ages + residual category). Within the table, totals by sex and combined totals are coherent, with no contradictory values detected.

*Completeness – High*

The dataset covers all 20 Italian regions and age classes 0–100 + 999, with a full matrix of region × age × sex totals. There are no missing values in the actual data rows; only the final note row contains missing values and should be filtered out. For regional-level analysis of population structure in 2025, the dataset can be considered complete.

*Timeliness – High*

The dataset refers to 1 January 2025 (provisional data), which is very recent relative to the current year. For an analysis focused on recent demographic structure, this timing is appropriate and aligned with current conditions, even if final (non-provisional) revisions may appear later.

""",
    
    "d2": """
**Data quality – D2: Italy Housing Data 2021**

*Accuracy – High*

For each record, the relationship occupied dwellings + unoccupied dwellings = total dwellings
holds exactly, which indicates internal numerical consistency. The territorial units are labelled with standard Italian regional and autonomous province names. Taken together, these elements support a High rating for syntactic and semantic accuracy.

*Coherence – High*

The list of territorial units covers all Italian regions and autonomous provinces, without duplicates or conflicting labels. The indicators (e.g. abitazioni occupate, non occupate, al 31 dicembre) are logically consistent with one another and adhere to their documented definitions. There are no internal contradictions such as totals smaller than their components.
Consequently, the dataset exhibits High coherence within its administrative and statistical context.

*Completeness – High*

The dataset includes all Italian regions (20 regions plus 2 autonomous provinces), thus providing full coverage at the regional level. For each territorial unit, values are available for all three indicators, and there are no missing observations in the core data fields. For analyses of the structure of the housing stock at regional scale, the dataset can therefore be regarded as exhaustive. On this basis, Completeness is assessed as High.

*Timeliness – Medium*

The reference year for the data is 2021, with an annual reporting frequency. For the purpose of examining medium- to long-term trends in the housing stock, this temporal resolution is generally adequate, as housing characteristics tend to change relatively slowly. However, in the context of climate disasters occurring in 2023–2025, the 2021 snapshot is somewhat outdated, and more recent vintages (e.g. 2022–2023) would be preferable. Accordingly, Timeliness is rated as Medium: sufficiently recent for structural analysis, but subject to a non-negligible temporal lag.

""",
    
    "gd1": """
**Data quality – GD1: Italy Regions Boundaries**

*Accuracy – High*

Attribute fields (e.g. regional identifiers and names) are expected to follow the national administrative nomenclature, 
allowing unambiguous linkage with tabular datasets such as population and housing statistics. While minor geometric 
tolerances are inherent to any vector representation, the level of positional accuracy is appropriate for regional-scale analysis. Taken together, these characteristics support a High rating for syntactic and semantic accuracy.

*Coherence – High*

The shapefile encodes a single, coherent layer of Italian regional units, with non-overlapping polygons and a shared boundary topology. Its structure is consistent with the regional aggregation used in the accompanying statistical datasets (e.g. population and housing by region), which enables straightforward spatial joins without internal contradictions. No additional or obsolete territorial units are expected at this level, and the geometry is aligned with the current administrative configuration. For these reasons, the dataset is assessed as exhibiting High coherence within the administrative and geospatial context.

*Completeness – High*

The layer is designed to cover the entirety of the Italian national territory at the regional level and therefore includes all regions. No gaps are expected in the spatial coverage, and each region is represented by at least one polygon with a corresponding attribute record. For the purposes of regional-scale mapping and linkage to regional indicators, the dataset can thus be considered complete. Accordingly, Completeness is rated as High.

*Timeliness – High*

The reference date indicated by the file name is 1 January 2025, which reflects the most recent territorial configuration at the time of analysis. Therefore, Timeliness is assessed as High.

""",
    
    "gd2_gd6": """
**Data quality – GD2–GD6: Settlements Location**

*Accuracy – Medium*

The dataset is structurally valid: all records are correctly encoded as point geometries in 
[**WGS84**](https://www.wikidata.org/wiki/Q11902211?uselang=it), and attribute fields (osm_id, code, fclass) 
are syntactically consistent across 23,355 features. However, as a volunteered geographic information 
source, OpenStreetMap exhibits variability in semantic accuracy: settlement classifications ("fclass" such 
as city, town, village, hamlet, locality) and population values are derived from community contributions 
and are not systematically validated against official statistics. Approximately 30% of features have non-zero population values, which are often approximate or missing for smaller settlements.
For these reasons, Accuracy is assessed as Medium: adequate for contextual and exploratory spatial analysis, 
but not suitable as a primary authoritative source for population counts.

*Coherence – High*

Internally, the dataset is coherent: each feature has a single settlement classification, and there are no geometric inconsistencies such as invalid point geometries or duplicated coordinates within the same identifier. The spatial extent corresponds to a contiguous portion of central Italy, and the settlement hierarchy (from city to hamlet and locality) follows the standard OSM tagging schema. This internal logic is consistent and can be reliably interpreted in conjunction with regional boundary datasets. Consequently, Coherence is rated as High.

*Completeness – Medium*

OpenStreetMap coverage is known to be heterogeneous, with large cities and towns almost universally present, but smaller villages, hamlets, farms and localities subject to local mapping activity. In this dataset, the presence of multiple settlement classes suggests good coverage, yet it cannot be guaranteed that all real-world settlements are represented, especially in rural or sparsely mapped areas. Furthermore, the population field is missing (zero) for the majority of small places, limiting completeness for demographic use. Accordingly, Completeness is assessed as Medium: satisfactory for mapping settlement patterns and relative density, but incomplete for exhaustive enumeration of all inhabited places and their populations.

*Timeliness – Medium*

The shapefile does not include explicit metadata on the extraction date or version, although OpenStreetMap itself is updated continuously. In the absence of a clearly documented timestamp, the dataset must be treated as a static snapshot of OSM at an unknown date, which introduces uncertainty when analysing recent dynamics (e.g. very new urban developments or recently renamed places). For medium-term structural analyses of settlement distribution, this limitation is acceptable but should be acknowledged. For these reasons, Timeliness is rated as Medium.
""",
}

LEGAL_TEXTS = {
    "d1": """
**Legal analysis – D1: Italy Population 2025**

*Privacy Issues*

The dataset contains only aggregated demographic counts by age, sex, and region. No names, addresses, 
identification numbers, or other direct or indirect identifiers are included. Under the [**GDPR**](https://gdpr-text.com/) and the 
Italian Personal Data Protection Code ([**Italian Legislative Decree No. 196/2003**](https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2003-06-30;196), as amended by 
[**Legislative Decree No. 101/2018**](https://www.gazzettaufficiale.it/eli/id/2018/09/04/18G00129/sg)), such regional aggregates are classified as non-personal data, as they do 
not enable the identification of natural persons, even when combined with other reasonably available 
information. The risk of re-identification is negligible, given the high level of spatial aggregation 
and the absence of small-cell disclosure.

*Intellectual Property Rights* 

ISTAT, as the Italian National Statistical Institute, is the rights holder for this dataset. According to 
its legal notice, ISTAT content is, unless otherwise specified, released under the 
Creative Commons Attribution 4.0 International ([**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en)) license. This grants broad rights of reuse, 
subject only to proper attribution.

*Licensing and Reuse*

Under [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en), users are free to copy, redistribute, transform, and build upon the data for any purpose, including commercial, provided that:
- ISTAT is clearly acknowledged as the source.
- Any modifications or derived indicators are indicated as such.
- A link to the license is provided where feasible. 

There is no share-alike or non-commercial restriction. Derived regional indicators (e.g. ageing indices) 
can therefore be published under a compatible open license, such as [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en).

*Access Limitations*

The dataset is distributed as open data via ISTAT’s open-data infrastructure and/or geo-statistical services, without registration or access control. There are no diplomatic, security, or classification constraints; the content concerns standard official statistics.

*Economic Conditions*

Access to the dataset is free of charge, in line with the [**EU Open Data Directive**](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv:OJ.L_.2019.172.01.0056.01.ENG) and Italian rules on 
the reuse of public-sector information, which promote non-discriminatory, low- or zero-cost access to PSI.  
No licensing or resale fees apply.

*Temporal Aspects*

The data refer to 1 January 2025 and follow ISTAT’s regular demographic update cycle. While later revisions may occur, the temporal coverage and update schedule are clearly documented, allowing users to interpret indicators in a time-consistent manner.

*Final Note on Publication*

Reusing D1 in this project is fully compatible with European and Italian open-data frameworks. Attribution to ISTAT and documentation of all processing steps (e.g. aggregation, indicator construction, joins with other datasets) are sufficient to ensure legally compliant and transparent reuse.

""",
    "d2": """
**Legal analysis – D2: Italy Housing Data 2021**

*Privacy Issues*

D2 provides regional-level counts of occupied and unoccupied dwellings. It contains no microdata, household identifiers, addresses, or other information that could 
single out individuals or specific properties. Accordingly, under [**GDPR**](https://gdpr-text.com/) and the Italian data-protection framework, D2 qualifies as non-personal, aggregate data, with no 
ealistic risk of re-identification.

*Intellectual Property Rights*

ISTAT is the producer and rights holder. As with other ISTAT open data, these housing statistics fall under the CC BY 4.0 regime unless otherwise stated. 

*Licensing and Reuse*

The CC BY 4.0 license permits free reuse, adaptation, and redistribution of the dataset, provided that:
- ISTAT is credited as the source of the original housing statistics.
- Any derived variables (e.g. vacancy rates, ratios of unoccupied dwellings) are clearly flagged as products of the present project.

This allows inclusion of D2 in an integrated, openly licensed analytical dataset (e.g. [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en)) alongside other ISTAT aggregates.

*Access Limitations*

The dataset is made available as open data via ISTAT’s portal with no authentication, contractual, or territorial restrictions. 

*Economic Conditions*

D2 is freely accessible, with no per-use charges, in line with the principles of open data and the reuse of public-sector information in Italy and the EU. 

*Temporal Aspects*

The reference year is 2021. While not perfectly aligned with the 2025 population snapshot, the temporal lag is explicitly documented, allowing appropriate interpretation 
(e.g. structural housing conditions rather than real-time housing dynamics).

*Final Note on Publication*

The reuse of D2 within this project is legally straightforward. With proper attribution and methodological transparency, derived indicators of housing vacancy and exposure 
can be shared as open data without additional legal constraints.

""",
    "gd1": """
**Legal analysis – GD1: Italy Regions Boundaries**

*Privacy Issues*

D3 consists exclusively of geometric boundaries and associated regional identifiers/names. It contains no personal or household-level attributes. 

*Intellectual Property Rights*

The boundary dataset is part of ISTAT’s suite of “confini delle unità amministrative a fini statistici”, which ISTAT releases as open geodata. Under ISTAT’s general 
legal notice, such content is licensed under [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en). 

*Licensing and Reuse*

[**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en) permits:

- Use of the geometries for mapping, spatial analysis, and integration with other datasets.
- Creation and publication of derived works (e.g. choropleth maps, derived grid overlays, enriched regional databases), with proper attribution to ISTAT.

There is no share alike requirement; the combined analytical dataset may be released under [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en) or 
another open data license chosen by the authors.

*Access Limitations*

The boundaries are downloadable as shapefiles and other GIS formats directly from ISTAT and related geodata portal and can be accessed without registration or specific 
authorization.

*Economic Conditions*

The geospatial data are provided free of charge, consistent with Italian and EU open-data policies for public-sector geoinformation. 

*Temporal Aspects*

D3 is explicitly referenced to 1 January 2025, with a clearly documented annual update process in which ISTAT revises administrative boundaries and disseminates 
harmonised layers for all years. This clarity on temporal validity is crucial for aligning regional indicators to the correct territorial configuration.

*Final Note on Publication*
Using D3 as the spatial framework for regional analyses is fully compatible with both national open-data rules and INSPIRE-aligned geospatial standards adopted in the 
European Union. Its inclusion in openly licensed maps and datasets is legally unproblematic, provided ISTAT is credited.

""",
    "gd2_gd6": """
**Legal analysis – GD2–GD6: Settlements Location**

*Privacy Issues*

GD2 – GD6 contain named places and settlement points (e.g. cities, towns, villages, hamlets, localities), encoded as coordinates with attributes such as "name", "fclass", and 
occasionally "population". These features describe geographic entities, not natural persons. No personal identifiers, user accounts, or contributor details are included in 
the exported shapefiles. As such, the dataset qualifies as non-personal data under the [**GDPR**](https://gdpr-text.com/): it does not relate to an identified or identifiable individual, and there is 
no realistic path to re-identification from the attributes present.

*Intellectual Property Rights*

The underlying geodata originate from the [**OpenStreetMap  project**](https://www.openstreetmap.org/#map=6/42.09/12.56), whose database is owned and stewarded by the OpenStreetMap Foundation (OSMF) and its contributors. OSM 
data are licensed under the Open Database License ([**ODbL 1.0**](https://opendatacommons.org/licenses/odbl/1-0/)). 

*Licensing and Reuse*

Under the [**ODbL 1.0**](https://opendatacommons.org/licenses/odbl/1-0/), users may:

- Share, adapt, and build upon the [**OSM**](https://www.openstreetmap.org/#map=6/42.09/12.56) database,
- Under the conditions of attribution, share-alike for derivative databases, and keeping the database open. 

Therefore, if D4 is only used as a basemap / contextual layer and the main analytical dataset remains at the regional level (ISTAT aggregates), the integrated analytical 
dataset may be licensed under CC BY 4.0, while maps of settlements continue to acknowledge OSM under [**ODbL 1.0**](https://opendatacommons.org/licenses/odbl/1-0/). 

*Access Limitations*

[**OSM**](https://www.openstreetmap.org/#map=6/42.09/12.56) data are openly downloadable from multiple sources ([**OpenStreetMap  project**](https://www.openstreetmap.org/#map=6/42.09/12.56), [**Geofabrik**](https://www.geofabrik.de/) and other mirrors) without registration or access control, in accordance with the 
project’s open-data ethos. 

*Economic Conditions*

The data were obtained free of charge, in line with the [**OSM**](https://www.openstreetmap.org/#map=6/42.09/12.56) community’s commitment to open mapping. No license fees or royalties are due, although the attribution and 
share-alike obligations under [**ODbL 1.0**](https://opendatacommons.org/licenses/odbl/1-0/) must be observed.

*Temporal Aspects*

OpenStreetMap is continuously edited, but each shapefile export represents a snapshot at a specific point in time. The extracts used in this project do not embed a formal 
version identifier in the file itself, so the download date should be documented in project metadata to make the temporal provenance explicit. From a legal standpoint, 
this temporal aspect does not affect licensing, but it is important for transparency and reproducibility.

*Final Note on Publication*

Incorporating D4 into the project is legally acceptable provided that:

- OSM is explicitly acknowledged ([**“© OpenStreetMap contributors”**](https://www.openstreetmap.org/#map=6/42.09/12.56) and reference to [**ODbL 1.0**](https://opendatacommons.org/licenses/odbl/1-0/)). 
- Any publicly shared derived databases at the settlement level that rely directly on OSM geometries or attributes comply with the [**ODbL**](https://opendatacommons.org/licenses/odbl/1-0/) share-alike requirement.
- Regional-level analytical datasets derived exclusively from ISTAT aggregates can remain under [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en), with OSM confined to cartographic visualisations.

""",
}

TECH_TEXTS = {
    "d1": """
#### Technical analysis – D1: Italy Population 2025

##### Metadata Quality ([**AgID model**](https://www.agid.gov.it/sites/default/files/repository_files/lg_infrastruttura_interoperabilita_pdnd.pdf))

- **Syntactic quality – High**  
  The dataset is disseminated through ISTAT’s open-data infrastructure in machine-readable formats (CSV, SDMX) with structurally valid fields and well-formed headers.

- **Semantic quality – High**  
  Variables such as age, sex, and territorial unit rely on official ISTAT classifications and geographic codes, ensuring unambiguous interpretation and alignment with 
  other official statistics.

- **Completeness – High**  
  Mandatory metadata elements (publisher, license, update frequency, temporal reference) and most recommended elements (methodological notes, data quality statements) 
  are present, enabling informed reuse.

- **Consistency – High**  
  The dataset is consistent with the broader ISTAT statistical system: region codes and labels match those used in other demographic and territorial datasets, and 
  temporal references are aligned with ISTAT’s annual demographic series.

##### FAIR principles

- **Findable – High**  
  The dataset is indexed in ISTAT’s open-data catalogue and on dati.gov.it, with stable identifiers and [**DCAT-AP_IT**](https://docs.italia.it/italia/daf/linee-guida-cataloghi-dati-dcat-ap-it/it/stabile/dcat-ap_it.html)-compliant metadata, making it straightforward to 
  retrieve through catalog search.

- **Accessible – High**  
  Data and metadata are retrievable over open HTTP(S) using non-proprietary formats (CSV, SDMX). No authentication is required.

- **Interoperable – High**  
  Use of official geographic codes, standard statistical classifications, and well-documented structures facilitates integration with other ISTAT and EU datasets.

- **Reusable – High**  
  The dataset is released under [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en), with clear provenance and methodological documentation, enabling broad reuse.
""",
     "d2": """
#### Technical analysis – D2: Italy Housing Data 2021

##### Metadata Quality (AgID model)

- **Syntactic quality – High**  
  D2 is provided in tabular formats compatible with standard statistical tools. Metadata records follow the same [**DCAT-AP_IT**](https://docs.italia.it/italia/daf/linee-guida-cataloghi-dati-dcat-ap-it/it/stabile/dcat-ap_it.html) structure as other ISTAT open data, and field types (counts, territorial codes) are correctly defined.

- **Semantic quality – High**  
  Definitions ensure semantic clarity across publications.

- **Completeness – High**  
  Descriptive metadata specify territorial coverage (all Italian regions), reference year (2021), frequency (annual), and methodological context (housing statistics series). No critical metadata elements are missing.

- **Consistency – High**  
  Territorial identifiers and naming conventions are consistent with D1 and D3, allowing coherent joins. Time stamps and series labels correspond to the official ISTAT housing-statistics programme.

##### FAIR principles

- **Findable – High**  
  The dataset is indexed in ISTAT’s catalogue and can be discovered by theme or by territorial level. Persistent URLs and dataset identifiers support stable referencing.

- **Accessible – High**  
  Openly downloadable without barriers, in machine-readable formats suitable for automated processing.

- **Interoperable – High**  
  Use of standard tabular structures enables straightforward integration with demographic, economic, or environmental datasets at the same territorial level.

- **Reusable – High**  
  Licensed under [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en) with adequate methodological notes, enabling recombination, transformation, and publication of derived indicators under compatible open licenses.
""",
    "gd1": """
#### Technical analysis – GD1: Italy Regions Boundaries

##### Metadata Quality (AgID model)

- **Syntactic quality – High**  
  The shapefile was originally provided in a projected coordinate reference system, WGS 84 / UTM zone 32N (EPSG:32632), i.e. with eastings and northings in metres 
  rather than geographic latitude/longitude coordinates. Although this CRS is based on the [**WGS84**](https://www.wikidata.org/wiki/Q11902211?uselang=it) datum, it is not equivalent to the commonly used geographic 
  CRS WGS 84 (EPSG:4326). For compatibility with web mapping tools and other GeoJSON-based workflows, the dataset was reprojected to EPSG:4326.
  Metadata follow national and INSPIRE/INSPIRE-aligned profiles, describing projection, scale, 
  lineage, and update cycle.

- **Semantic quality – High**  
  Each polygon is associated with official ISTAT regional codes and names, reflecting the legally valid statistical-administrative configuration.

- **Completeness – High**  
  Metadata specify spatial coverage (national), hierarchical levels, reference date (1 January 2025), and data lineage, providing all essential elements for geospatial reuse.

- **Consistency – High**  
  The dataset is internally coherent (no gaps or overlaps at the regional level) and consistent with ISTAT’s time-series work on historical boundaries, which 
  documents changes over time.

##### FAIR principles

- **Findable – High**  
  D3 is registered on the ISTAT website, making it easily findable as the authoritative boundary dataset.

- **Accessible – High**  
  Boundaries are downloadable in standard GIS formats via open services. No technical or legal barriers hinder access.

- **Interoperable – High**  
  Use of [**WGS84**](https://www.wikidata.org/wiki/Q11902211?uselang=it), standard shapefile formats, and ISTAT territorial codes ensures high interoperability with 
  other spatial and statistical layers.

- **Reusable – High**  
  Released as ISTAT open data under [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en), allowing reuse for mapping, modelling, and integration into 
  derivative spatial databases.
""",
    "gd2_gd6": """
#### Technical analysis – GD2–GD6: Settlements Location

##### Metadata Quality (AgID model)

- **Syntactic quality – Medium**  
  At the file level, the shapefiles are structurally valid, with correctly defined point geometries in [**WGS84**](https://www.wikidata.org/wiki/Q11902211?uselang=it) and a stable attribute schema 
  (`osm_id`, `name`, `fclass`, `population`, etc.). However, dataset-level metadata are relatively sparse compared to [**DCAT-AP_IT**](https://docs.italia.it/italia/daf/linee-guida-cataloghi-dati-dcat-ap-it/it/stabile/dcat-ap_it.html) practice: information such as extraction 
  date, lineage, and intended use must be inferred from external documentation rather than embedded in the files themselves.

- **Semantic quality – Medium**  
  Attribute semantics follow the OpenStreetMap tagging conventions (e.g. `place=city/town/village/hamlet/locality`), which are well documented within the OSM community 
  but not formally aligned with Italian official territorial classifications. This limits semantic interoperability with ISTAT typologies, although the tags are 
  consistent inside the OSM ecosystem.

- **Completeness – Medium**  
  Basic descriptive metadata (title, geographic extent, coordinate reference system) are either implicit in the download source or present in minimal form. Richer 
  elements—such as quality statements, coverage assessments, and detailed provenance—are not part of the shapefile metadata and must be reconstructed by the user.

- **Consistency – Medium/High**  
  Within each extract, the attribute structure is consistent across features, and OSM’s global tagging model provides internal coherence. However, local inconsistencies 
  and heterogeneous mapping practices across regions introduce some variability, particularly for classes and population tags.

##### FAIR principles

- **Findable – Medium**  
  OSM data are globally findable through the main OpenStreetMap portal, but the specific Italian settlement extracts used here are not listed in the national [**DCAT-AP_IT**](https://docs.italia.it/italia/daf/linee-guida-cataloghi-dati-dcat-ap-it/it/stabile/dcat-ap_it.html)
  catalogues. Searchability therefore depends more on community infrastructures than on governmental catalogues.

- **Accessible – High**  
  Data are freely downloadable over open protocols in widely supported formats (PBF, shapefile, etc.), with no access restrictions.

- **Interoperable – Medium**  
  Use of [**WGS84**](https://www.wikidata.org/wiki/Q11902211?uselang=it) and open formats supports technical interoperability. At the semantic level, however, OSM’s community-driven taxonomies are not fully harmonised 
  with national administrative codes or official settlement classifications, requiring additional mapping work for integration with ISTAT datasets.

- **Reusable – Medium**  
  OSM data are licensed under the Оpen Database License ([**ODbL 1.0**](https://opendatacommons.org/licenses/odbl/1-0/)), which permits free reuse with attribution and share-alike obligations on derived databases. 
  Provenance is clear at the project level (“© OpenStreetMap contributors”) but less explicit at the feature level; documentation on coverage and quality is available 
  via community channels rather than formal metadata. These factors support substantial reuse but require careful legal and methodological handling when combining OSM 
  with other open datasets.
""",
# ---------- MD1 ----------
    "md1": """
#### Technical analysis – MD1: Share Houses Occupation

##### Metadata Quality (AgID model)

- **Syntactic quality – High**  
  MD1 is stored as a machine-readable CSV with a small number of fields (e.g. `region_code`, `region_name`, `total_dwellings`, `unoccupied_dwellings`, `share_unoccupied`). 
  Column types are simple and consistently generated via scripts, which reduces the risk of ad-hoc errors.

- **Semantic quality – High**  
  The indicator definition (“share of unoccupied dwellings” = `unoccupied / total`) is transparent and directly traceable to ISTAT’s official housing counts. Territorial 
  identifiers reuse ISTAT regional codes and names, maintaining semantic alignment with the source.

- **Completeness – High**  
  All 20 Italian regions are included, and the minimal set of variables needed to interpret the indicator (absolute values + share) is present. There are no structural 
  missing values at regional level.

- **Consistency – High**  
  MD1 is derived by a single, documented transformation from D2. The same code is applied uniformly to all 
  regions; regional codes and names are consistent with other project tables (MD2, MD5).

##### FAIR principles

- **Findable – Medium**  
  Within the project, MD1 is clearly named, versioned, and referenced in notebooks and documentation. However, it is not (yet) registered in a national DCAT or 
  institutional catalogue, so its findability is limited to the project repository.

- **Accessible – High**  
  MD1 is provided as an open CSV in the project repo, retrievable via standard HTTP/HTTPS and usable without any proprietary software.

- **Interoperable – High**  
  Use of ISTAT regional codes and simple tabular structure makes it easy to join with other statistical and geospatial datasets at regional level.

- **Reusable – High**  
  Provenance (derived from ISTAT D2) and formulae for constructing the share are documented in the code. 
  If the project as a whole is released under CC BY 4.0, MD1 will be straightforward to reuse and extend 
  by third parties.
""",
    # ---------- MD2 ----------
    "md2": """
#### Technical analysis – MD2: Share 65 Plus

##### Metadata Quality (AgID model)

- **Syntactic quality – High**  
  MD2 follows the same simple, regular CSV structure (`region_code`, `region_name`, `population_65plus`, `total_population`, `share_65plus`). Data types are numeric and 
  consistently generated.

- **Semantic quality – High**  
  The definition of “65+” and “total population” is inherited from ISTAT demographic statistics. The resulting share is semantically clear and unambiguous, and 
  territorial units are aligned with official regional classifications.

- **Completeness – High**  
  All regions are present, and the dataset contains both absolute counts and relative shares, enabling multiple forms of analysis without additional inputs.

- **Consistency – High**  
  MD2 is produced via a uniform aggregation and division procedure from D1; identical territorial codes are used across MD1, MD2, MD5, which preserves cross-dataset 
  consistency.

##### FAIR principles

- **Findable – Medium**  
  As with MD1, MD2 is well referenced inside the project (filenames, notebooks, plots) but is not yet indexed in external catalogues. It is “locally” findable rather 
  than globally.

- **Accessible – High**  
  Distributed as CSV under open access in the repository; no technical barriers prevent reuse.

- **Interoperable – High**  
  Regional codes and the minimal, well-named column schema support easy integration with other regional indicators and GIS layers.

- **Reusable – High**  
  Documentation of the aggregation level (region), reference year, and derivation from ISTAT D1 makes the indicator reusable in other comparative studies of 
  ageing, provided the project’s open license (e.g. CC BY 4.0) is applied.
""",
    # ---------- MD3 ----------
    "md3": """
#### Technical analysis – MD3: Settlements per Region

##### Metadata Quality (AgID model)

- **Syntactic quality – High**  
  MD3 collapses complex OSM point data into regional (or macro-regional) counts by settlement type (e.g. villages, hamlets, localities). The resulting CSV has a 
  regular structure with one row per territory and numerically typed count columns.

- **Semantic quality – Medium/High**  
  The semantics of “city”, “town”, “village” etc. follow OpenStreetMap tagging rather than ISTAT classifications. The methodology explicitly states that these are 
  OSM settlement classes, not official administrative categories. Within that framing, the indicators are meaningful, but they are not directly equivalent to 
  official *comune* or *località* typologies.

- **Completeness – Medium**  
  At the regional aggregation level, MD3 includes counts for all regions, but completeness is limited by underlying OSM coverage (under-mapping in some rural areas). 

- **Consistency – High (within project scope)**  
  The same extraction pipelines and filters are applied to all OSM tiles, and then the same aggregation logic is used for all regions. This yields internally 
  consistent indicators, even if OSM source completeness varies geographically.

##### FAIR principles

- **Findable – Medium**  
  MD3 is discoverable inside your repository as a clearly named derived product but is not yet catalogued externally.

- **Accessible – High**  
  Provided as CSV in the repo, readable with standard tools.

- **Interoperable – Medium**  
  Technically, interoperability is good (WGS84-based joins to regions and standard CSV). Semantically, interoperability is constrained by the need to understand 
  OSM tagging conventions; crosswalks to official categories are not 1:1.

- **Reusable – High**  
  Reuse is facilitated by clear attribution to “© OpenStreetMap contributors, ODbL 1.0” at the data source level and by documentation of aggregation methods. 
  Because MD3 is a derived database from OSM, publishing it publicly would require an ODbL-compatible license; within that constraint, reuse potential is high.
""",
    # ---------- MD4 ----------
    "md4": """
#### Technical analysis – MD4: Dispersed Settlements Index

##### Metadata Quality (AgID model)

- **Syntactic quality – High**  
  MD4 encodes indicators such as density of places per area, or proxies for spatial dispersion, again as a tidy CSV at regional level. Numeric formats are 
  coherent, and there is a clear one-row-per-region structure.

- **Semantic quality – Medium/High**  
  The indicators represent analytical constructs (e.g. “dispersion index”), which are well defined in the notebooks. Provided that formulas and units are 
  documented, the semantics are robust. However, they still inherit the OSM-based limitations of what counts as a “settlement point”.

- **Completeness – Medium**  
  All regions possess values, but their robustness depends on OSM coverage (missing or misclassified small settlements = potential bias). MD4 is therefore interpreted 
  as indicative of relative spatial structure, not as an exact settlement inventory.

- **Consistency – High**  
  The same geospatial pipeline and statistics are used for all regions, ensuring methodological consistency.

##### FAIR principles

- **Findable – Medium**  
  As an internal analytical layer, MD4 is well labelled in the project but not yet present in external catalogues.

- **Accessible – High**  
  Openly accessible CSV via the repository.

- **Interoperable – Medium**  
  Outputs are numeric indicators with ISTAT regional codes, which makes them easy to merge. Interpreting them correctly, however, requires access to methodological 
  notes (e.g. which settlement classes were included).

- **Reusable – High**  
  Reuse is feasible for others who wants a proxy for settlement dispersion. Licensing follows the same pattern as MD3 (ODbL-compatible if shared as a database), 
  which is a legal — not technical — constraint.
""",
    # ---------- MD5 ----------
    "md5": """
#### Technical analysis – MD5: Age vs Houses Occupation

##### Metadata Quality (AgID model)

- **Syntactic quality – High**  
  MD5 brings together core indicators from MD1 and MD2 (and possibly other variables) into a single regional-level dataset. Column names and types are regular, 
  and the table is fully machine-readable.

- **Semantic quality – High**  
  Each variable is either a direct reproduction (e.g. `share_65plus`, `share_unoccupied`) or a transparent derivative (e.g. typology categories such as 
  “high ageing / high vacancy”). When typologies or clusters are used, their thresholds and logic are documented, which preserves semantic clarity.

- **Completeness – High**  
  All Italian regions have complete rows for the included indicators. The dataset is explicitly positioned as a “master table” for the project’s regional analysis.

- **Consistency – High**  
  MD5 provides a consistent key (`region_code`) that matches D1–D3, and all included indicators are generated from earlier, checked datasets (MD1–MD4), 
  which greatly reduces the risk of inconsistencies across indicators.

##### FAIR principles

- **Findable – Medium**  
  Within the project, MD5 is the central analytical dataset and is referenced in figures, notebooks, and the report. As such, it is easy to locate inside the 
  repository. 

- **Accessible – High**  
  Distributed as a tidy CSV (and possibly GeoPackage when joined with D3) via open protocols, with no access barriers.

- **Interoperable – High**  
  MD5 uses standard regional codes and clearly defined indicators, making it straightforward to interoperate with other regional datasets 
  (e.g. climate indicators, socio-economic statistics). 

- **Reusable – High**  
  MD5 concentrates the most policy-relevant indicators (ageing, housing vacancy, settlement structure proxies) into one place with clear provenance. 
  Under an open license (e.g. CC BY 4.0 for the ISTAT-derived parts, plus proper acknowledgement of any OSM-derived components), it provides a high-value, 
  reusable resource for researchers, journalists, and public authorities interested in “retired people / retired places” typologies.
""",
}

tab_quality, tab_legal, tab_ethics, tab_technical = st.tabs(
    ["Data Quality", "Legal", "Ethical", "Technical"]
)

# =============== QUALITY TAB ===============
with tab_quality:
    st.markdown("### Data Quality Analysis")
    st.info("Accuracy, coherence and reliability of datasets.")
    st.markdown(
    """
In accordance with the [**National Guidelines for the Enhancement of the Public Information Asset**](https://docs.italia.it/italia/daf/lg-patrimonio-pubblico/it/stabile/aspettiorg.html#qualita-dei-dati),
developed within the Data & Analytics Framework project by AgID and the Digital Transformation Team,
we carried out a comprehensive quality assessment of all datasets employed in this study. This assessment
was designed to ensure that our analysis of population ageing and housing occupation in Italy is based
on data that are reliable and fit for the intended analytical purposes.

The evaluation followed four core dimensions of data quality:

- **Accuracy (syntactic and semantic):** the extent to which the data and their attributes correctly
  represent the real-world phenomena they are intended to describe.
- **Coherence:** the degree to which the data are internally consistent and free from contradictions
  when compared with other related datasets within the same administrative and statistical context.
- **Completeness:** the extent to which the datasets provide exhaustive values and fully cover all
  relevant entities and sources required by the underlying procedures.
- **Timeliness:** the alignment between the reference period of the data and the temporal requirements
  of the processes they support, ensuring that the information is sufficiently up to date for the
  analyses conducted.
"""
)

    cols = st.columns(2)

    for idx, key in enumerate(DATASET_KEYS):
       col = cols[idx % 2] 
       with col:
          with st.expander(DATASET_TITLES[key], expanded=False):
            st.markdown(QUALITY_TEXTS[key])

    st.markdown("The results of this analysis are summarized in a table highlighting the overall quality of " \
    "each dataset and identifying any areas requiring improvement.")

    st.markdown(
    """
| ID Dataset                       | Accuracy | Coherence | Completeness | Timeliness |
|----------------------------------|----------|-----------|--------------|------------|
| D1 – Italy Population 2025      | high     | high      | high         | high       |
| D2 – Italy Housing Data 2021    | high     | high      | high         | medium     |
| GD1 – Italy Regions Boundaries  | high     | high      | high         | high       |
| GD2–GD6 – Settlements Location  | medium   | high      | medium       | medium     |
"""
)

# =============== LEGAL TAB ===============
with tab_legal:
    st.markdown("### Legal Analysis")
    st.info("Open data laws and reuse rights.")
    st.markdown(
    """
The legal analysis of the source datasets is a crucial step in ensuring the long-term sustainability of both the data production workflow and the publication of the resulting datasets. It also serves to guarantee that the data service remains balanced, consistent with public-sector responsibilities, and respectful of individual rights.
This analysis was conducted in the following dimensions: privacy, intellectual property rights (IPR) policies, licensing conditions, limitations on public access, economic conditions, and temporal aspects related to data availability and updating.
"""
)

    cols = st.columns(2)
    for idx, key in enumerate(DATASET_KEYS):
      col = cols[idx % 2]
      with col:
        with st.expander(DATASET_TITLES[key], expanded=False):
            st.markdown(LEGAL_TEXTS[key])


    st.markdown(
    """
    #### Publication License
The table below summarizes the original licenses of the source datasets and the final publication license 
applied to the mashup datasets.
"""
    )

    st.markdown(
    """
| Dataset                         | Original licenses        | Final license |
|---------------------------------|--------------------------|---------------|
| MD1 – Share Houses Occupation   | CC BY 4.0                | CC BY 4.0     |
| MD2 – Share 65 Plus             | CC BY 4.0                | CC BY 4.0     |
| MD3 – Settlements per Region    | ODbL 1.0, CC BY 4.0      | ODbL 1.0      |
| MD4 – Dispersed Settlements Index | ODbL 1.0, CC BY 4.0    | ODbL 1.0      |
| MD5 – Age vs Houses Occupation  | CC BY 4.0                | CC BY 4.0     |
| MED1 – Settlements Italy        | CC BY 4.0                | CC BY 4.0     |
"""
)
    

# =============== ETHICS TAB ===============
with tab_ethics:
    st.markdown("### Ethical Analysis")
    st.info("Respect for privacy, equity and transparency.")

    st.markdown(
    """
The ethical assessment of our Italian open-data processing was structured using the 
[**ODI Data Ethics Canvas**](https://theodi.org/insights/tools/the-data-ethics-canvas-2021/)
and guided by data-ethics principles formulated by 
[**DataEthics.eu**](https://dataethics.eu/about/), complemented by 
[**OECD Good Practice Principles for Data Ethics in the Public Sector**](https://www.oecd.org/en/publications/oecd-good-practice-principles-for-data-ethics-in-the-public-sector_caa35b76-en.html).
The analysis concerns four main components: ISTAT regional population data (D1), ISTAT housing stock data (D2), 
ISTAT regional boundaries (D3), and OpenStreetMap settlement points (GD2–GD6).
    """
)

    col_left, col_right = st.columns(2)

    with col_left:
        with st.expander("Data Ethics Principles", expanded=False):
            st.markdown(
                """

*Human-Centric Design*

The project investigates how demographic ageing, housing vacancy, and settlement structure interact across Italian regions and inner areas. By focusing on aggregated 
indicators (e.g. share of population aged 65+, share of unoccupied dwellings, density and hierarchy of settlements), the analysis aims to support more equitable 
territorial and social policies—especially for older residents and communities facing depopulation, reduced services, or increased environmental risk.

*Fairness and Equity*  
All indicators are computed at aggregated territorial levels (regions and municipalities, occasionally broader “inner area” groupings) to avoid identifying individuals 
or very small groups. When comparing territories, we explicitly avoid simple “ranking” language (e.g. “best”/“worst” regions) and instead interpret differences through 
structural factors such as labour markets, infrastructure, geography, and historical development. Problematic terms such as “ghost towns” or “dying villages” are not used, 
or, if they appear at all, are only used with clear explanation and never as labels for residents themselves.

*Transparency*  
Data sources (ISTAT datasets for D1–D3 and OpenStreetMap for GD2–GD6) are fully open and cited throughout the project. All key processing steps—data cleaning, 
spatial joins, construction of derived indicators, typology classification—are documented in reproducible scripts and notebooks. Where choices were made (e.g. thresholds 
for “high ageing” or “high vacancy”), these are clearly motivated and recorded so that others can scrutinise or replicate the workflow.

*Accountability* 
The project aligns with Italian and EU open-data and data-protection frameworks. A versioned code repository is maintained. Reuse conditions for ISTAT and OSM data 
are respected, and any future extension to more granular or sensitive data (e.g. microdata or survey information) would be subjected to additional ethical review.

*Privacy and Respect for Affected Populations*  
All datasets used are aggregate and officially classified as non-personal data. No microdata, addresses, or directly identifiable information are processed. Nonetheless, 
we recognise that indicators such as “very old population living in highly vacant housing areas” describe vulnerable communities. Narrative interpretations are 
therefore framed to highlight needs, resilience, and policy gaps rather than to blame communities for demographic or economic trends.
                """
            )

    with col_right:
        with st.expander("Ethical Concerns and Mitigation", expanded=False):
            st.markdown(
                """
*Avoiding Stigmatisation of Territories*  
High shares of older residents, vacant dwellings, or shrinking settlements can easily be framed as “problems”. To mitigate this risk, descriptive statistics and maps are 
accompanied by contextual discussion of long-term structural drivers (e.g. industrial decline, historical migration patterns, transport accessibility). Visualisations 
avoid alarmist colour schemes and labelling; instead of “critical” or “doomed” areas, we use neutral terms.

*Geographical and Socio-Economic Sensitivity* 
Italy is characterised by well-known territorial inequalities (e.g. between North and South, coastal and inland, metropolitan and inner areas). Analyses are designed 
not to reinforce stereotypes about “backward” regions but to show how institutional, infrastructural, and environmental factors interact with demographic change. Where 
regional disparities appear, they are interpreted as signals of differentiated policy needs, not as moral judgements on local populations.

*Data Limitations and Representation*  
The project explicitly acknowledges the limitations of each dataset. ISTAT aggregates are robust but may not fully capture intra-regional heterogeneity; housing stock 
data are slightly older than the most recent demographic data; OpenStreetMap settlement points are incomplete and reflect uneven mapping activity. These constraints are 
discussed in the documentation.

*Responsibility in Interpretation*  
Correlations between high ageing, high vacancy, and settlement structure are treated as descriptive patterns, not as proof of causality. Visualisations and typologies are 
presented as heuristic tools to explore territorial configurations, accompanied by explicit caveats about confounding factors (e.g. tourism, second homes, 
commuting patterns).

*Public Engagement and Literacy*  
The project produces accessible maps and charts intended for non-specialist audiences, including local administrators, civil society organisations, and interested citizens.
 To promote data literacy, simplified explanations of indicators and methods are provided alongside technical documentation and open code repositories for experts. 
 Where metaphorical language (such as “retired places”) is used in outreach materials, it is contextualised to avoid caricaturing communities and to emphasise their 
 agency and potential.
                """
            )

    st.markdown("#### Final note")

    st.markdown(
        """
The ethical safeguards adopted in this project reflect contemporary European standards for responsible open-data use and research under [**GDPR**](https://gdpr-text.com/). By combining robust aggregate 
statistics (ISTAT) with carefully contextualised geospatial information (ISTAT boundaries and OpenStreetMap settlements), and by foregrounding fairness, transparency, 
and accountability, the project seeks to reuse public data in a manner that is both ethically and socially responsible.

Rather than treating ageing or depopulating territories as problems in themselves, the analysis aims to illuminate structural conditions and inform balanced debates on 
territorial cohesion, service provision for older residents, and sustainable regional development in Italy.
        """
    )

# =============== TECHNICAL TAB ===============
with tab_technical:
    st.markdown("### Technical Analysis")
    st.info("Metadata structure and FAIR principles compliance.")
    st.markdown(
        """
The technical assessment of the Italian datasets follows the metadata model set out by 
the Agenzia per l’Italia Digitale (AgID) in the [**Linee Guida recanti regole tecniche per l’apertura dei dati 
e il riutilizzo dell’informazione del settore pubblico**](https://www.agid.gov.it/sites/agid/files/2024-05/lg-open-data_v.1.0_1.pdf ), which adopt DCAT‑AP and the national DCAT AP_IT profile for 
metadata description. In addition, each dataset is evaluated against the 
[**FAIR principles**](https://www.go-fair.org/fair-principles/) (Findable, Accessible, Interoperable, Reusable).
        """
    )


    TECH_KEYS = ["d1", "d2", "gd1", "gd2_gd6", "md1", "md2", "md3", "md4", "md5"]
    cols = st.columns(2)

    for idx, key in enumerate(TECH_KEYS):
       col = cols[idx % 2]          
       with col:
        with st.expander(technical_datasets[key], expanded=False):
            st.markdown(TECH_TEXTS[key])

    st.markdown("### Final note: overall technical and FAIR quality")

    st.markdown(
        """
**Source datasets (D1–D3, GD1–GD2–GD6)**  

Taken together, **D1–D3** exhibit high technical and metadata quality in line with
AgID’s model and FAIR principles, reflecting mature institutional practices in
ISTAT’s open-data and geodata infrastructures.  
The settlement layers (**GD2–GD6**) provide valuable complementary information on
settlement structure but, as community-generated datasets, show medium-level metadata
and FAIR compliance, and therefore require additional documentation and harmonisation
for rigorous analytical reuse.

**Derived / mashup datasets (MD1–MD5)**  

- **MD1–MD2 (ISTAT-derived shares)** – technically and semantically very strong,
  with high FAIR compliance; ideal candidates for long-term open publication under
  **CC BY 4.0**.
- **MD3–MD4 (OSM-derived settlement and dispersion measures)** – technically well
  constructed and internally consistent, but FAIR and semantic quality are moderated
  by the inherent variability and licensing constraints of OpenStreetMap data.
- **MD5 (integrated regional master dataset)** – offers the highest analytical value
  and, with clear documentation and a concise data dictionary, can reach a very solid
  level of FAIRness as the main “public” dataset of the project.
        """
    )        

st.write("---")



# ---------- SUSTAINABILITY OF DATASET UPDATES ----------
st.markdown("<div id='sustainability-section'></div>", unsafe_allow_html=True)
st.header("Is it Sustainable?")
st.markdown(
    "*This section reflects on the long-term sustainability of the datasets and indicators used in the project – "
    "how they can be updated, documented and reused as Italy’s population and its “retired places” continue to evolve.*"
)


st.write(
    """
    
The datasets used in this project are derived from open official statistics published by the Italian 
National Institute of Statistics (ISTAT) and volunteered geographic information from OpenStreetMap (OSM). 
ISTAT manages its demographic and housing tables, 
while OSM extracts are periodically regenerated by community providers such as Geofabrik. 
As these infrastructures evolve, the exact download links and URIs referenced in this prototype may become 
outdated, even if the underlying data series continue to be maintained.

“Retired Places” is a final project for the *Open Access and Digital Ethics* course (a.y. 2024/2025) 
within the *Digital Humanities and Digital Knowledge* Master’s programme at the University of Bologna. 
It is not intended as a continuously maintained observatory. The analytical pipeline, however, 
is documented in notebooks and scripts so that future users can re-run the workflow with updated ISTAT 
and OSM releases, regenerate indicators, and adapt the visualisations if they wish to extend the project. From a sustainability perspective, the project focuses on the **lifecycle of the derived datasets** 
(MD1–MD5, MED1) and how they can remain reusable over time.

    """
)

with st.expander("Updatability of sources", expanded=False):
    st.markdown(
        """
All indicators are constructed from clearly referenced, versioned ISTAT and OSM inputs. When new
vintages of demographic, housing or geospatial data are released, the same pipeline can be applied to
produce updated regional indicators of ageing, vacancy and settlement structure.
        """
    )

with st.expander("Stable identifiers and documentation", expanded=False):
    st.markdown(
        """
The use of ISTAT regional codes as primary keys, together with a documented data dictionary and RDF
metadata, helps ensure that future users can understand and safely merge the derived datasets even if
original portals, file names or URLs change.
        """
    )

with st.expander("Reproducible preprocessing", expanded=False):
    st.markdown(
        """
Data cleaning, harmonisation and indicator computation are implemented in reproducible Jupyter notebooks
and scripts stored in the project repository. This makes it possible to re-create the mashup and merged
datasets from scratch, rather than depending on a single static snapshot.
        """
    )

with st.expander("Licensing and long-term reuse", expanded=False):
    st.markdown(
        """
Derived datasets respect the original licenses (CC BY 4.0 for ISTAT, ODbL 1.0 for OSM) and are documented
with explicit provenance. This clarifies what can be republished as open data and under which conditions,
supporting legally robust reuse in future research, journalism or policy analysis.
        """
    )

with st.expander("Graceful ageing of the dashboard", expanded=False):
    st.markdown(
        """
Even if the Streamlit interface is not maintained indefinitely, the combination of open formats
(CSV, GeoJSON), explicit metadata (DCAT, PROV), and public code means that the analytical content
can outlive the specific web application and be integrated into other platforms or updated visual layers.
        """
    )

st.write(
    """

In this way, the project treats the app not as the final product, but as a demonstrator built on top 
of datasets and metadata that are designed to remain interpretable, re-runnable and extensible over 
time as Italy’s population and its “retired places” continue to evolve.

    """
)    
    
st.write("---")


# ---------- VISUALISATIONS ----------
st.markdown("<div id='graphs-section'></div>", unsafe_allow_html=True)
st.header("Visualisations")
st.markdown(
    "*This section brings together the core visual tools of the project – ranked bar charts, "
    "a 2×2 scatterplot and a map of dispersed settlements – so that you can compare regions, "
    "spot outliers, and see where “retired people” and “retired places” most clearly overlap "
    "or diverge.*"
)

tab_ranked, tab_scatter, tab_disp = st.tabs(
    [
        "Ranked bars: Ageing vs vacancy",
        "Scatter: Retired people vs “retired” places",
        "Map: Dispersed settlements",
    ]
)


# ========= TAB 1: RANKED BARS =========
with tab_ranked:
    st.subheader("Ageing and housing vacancy: how Italian regions compare")

    st.markdown(
    "**_Research Question:_** *Which Italian regions rise to the top when we rank them by older residents (65+) or by empty homes, and how much does the leaderboard change when we switch between "
    "these two metrics?*"
)


    st.write(
        """
        This chart compares regions by the share of population aged 65+ and
        the share of unoccupied homes. You can display one or both metrics.
        The ranking metric defines Top-5 and the order of regions and cannot
        be hidden from the chart.
        """
    )

    # ---- Common options ----
    macro_options = ["All Italy"] + sorted(
        df_regions["macro_region"].dropna().unique()
    )

    # ---- Filters for the chart ----
    selected_macro_2 = st.selectbox(
        "Filter by macro-region",
        options=macro_options,
        index=0,
        key="macro_chart2",
    )

    show_top5_2 = st.checkbox(
        "Show only Top-5 regions (based on ranking metric)",
        value=True,
        help="Keeps the five most extreme regions according to the selected ranking metric.",
        key="top5_chart2",
    )

    # --- Ranking metric: which metric is used to rank regions (Top-5 + order) ---
    ranking_choices = {
        "Rank by ageing (share_65plus)": "share_65plus",
        "Rank by vacancy (share_unoccupied)": "share_unoccupied",
    }
    ranking_choice_label = st.selectbox(
        "Ranking metric",
        options=list(ranking_choices.keys()),
        index=0,
        key="ranking_chart2",
    )
    # 'share_65plus' or 'share_unoccupied'
    ranking_metric_2 = ranking_choices[ranking_choice_label]

    # --- Metrics to display (one or both) ---
    metric_display_options = {
        "Ageing (share_65plus)": "share_65plus",
        "Vacancy (share_unoccupied)": "share_unoccupied",
    }

    # init session_state on first run
    if "metrics_display_chart2" not in st.session_state:
        st.session_state["metrics_display_chart2"] = list(metric_display_options.keys())

    selected_metric_labels = st.multiselect(
        "Metrics to display",
        options=list(metric_display_options.keys()),
        default=st.session_state["metrics_display_chart2"],
        key="metrics_display_chart2",
        help="You can hide the secondary metric, but the ranking metric must remain visible.",
    )

    # --- Enforce: ranking metric must always be displayed ---
    selected_metrics = [metric_display_options[label] for label in selected_metric_labels]

    # label of the ranking metric inside the multiselect
    ranking_label_for_multiselect = [
        label for label, val in metric_display_options.items()
        if val == ranking_metric_2
    ][0]

    if ranking_metric_2 not in selected_metrics:
        # user tried to hide the ranking metric → add it back
        if ranking_label_for_multiselect not in st.session_state["metrics_display_chart2"]:
            st.session_state["metrics_display_chart2"].append(ranking_label_for_multiselect)

        st.info(
            "You are currently ranking regions by "
            f"**{ranking_label_for_multiselect}**, so this metric cannot be hidden."
        )

        # recompute selected metrics from corrected session_state
        selected_metric_labels = st.session_state["metrics_display_chart2"]
        selected_metrics = [metric_display_options[label] for label in selected_metric_labels]

    if len(selected_metrics) == 0:
        st.info("Please select at least one metric to display.")
    else:
        sort_option_2 = st.radio(
            "Sort order",
            options=["Highest first (descending)", "Lowest first (ascending)"],
            index=0,
            horizontal=True,
            key="sort_chart2",
        )
        # Highest → descending, Lowest → ascending
        ascending_2 = sort_option_2.startswith("Highest")

        # ---- Prepare data ----
        if selected_macro_2 == "All Italy":
            df_base_2 = df_regions.copy()
        else:
            df_base_2 = df_regions[df_regions["macro_region"] == selected_macro_2].copy()

        # Step 1: Top-5 by ranking metric (or all regions)
        if show_top5_2:
            df_ranked_2 = df_base_2.sort_values(
                ranking_metric_2, ascending=False
            ).head(5)
        else:
            df_ranked_2 = df_base_2.copy()

        # Step 2: final order according to ranking metric + sort order
        df_ranked_2 = df_ranked_2.sort_values(
            ranking_metric_2, ascending=ascending_2
        )

        # Long format: only selected metrics (one or both)
        df_long_2 = df_ranked_2.melt(
            id_vars=["region_norm"],
            value_vars=selected_metrics,
            var_name="metric",
            value_name="value",
        )

        metric_labels_2 = {
            "share_65plus": "Share of 65+",
            "share_unoccupied": "Share of unoccupied homes",
        }
        df_long_2["metric_label"] = df_long_2["metric"].map(metric_labels_2)

        # ---- Height ----
        base_height_2 = 350
        extra_per_bar_2 = 18
        n_regions_2 = df_ranked_2.shape[0]
        height_2 = base_height_2 + max(0, (n_regions_2 - 8) * extra_per_bar_2)

        # ---- Plot ----
        fig_bar_2 = px.bar(
            df_long_2,
            x="value",
            y="region_norm",
            color="metric_label",
            orientation="h",
            barmode="group",
            labels={
                "value": "Value",
                "region_norm": "Region",
                "metric_label": "Metric",
            },
            hover_data={"value": ":.2f"},
        )

        # keep region order as in df_ranked_2
        fig_bar_2.update_yaxes(
            categoryorder="array",
            categoryarray=df_ranked_2["region_norm"].tolist(),
        )

        fig_bar_2.update_layout(
            height=height_2,
            margin={"r": 40, "t": 20, "l": 120, "b": 40},
            legend_title="Metric",
        )

        st.plotly_chart(fig_bar_2, use_container_width=True)

# ========= TAB 2: SCATTER & DUMBBELL =========
with tab_scatter:
    st.subheader("Retired people vs “retired” places",)


    col1, col2 = st.columns(2)

    # ---------- COL1: SCATTER ----------
with col1:
    st.markdown("**How ageing and empty homes line up across Italian regions**")
    st.markdown(
    "**_Research Question:_** *When we split regions into four quadrants by ageing and vacancy thresholds, which territories combine high shares of older residents and empty homes, and which ones look “older but lived-in” or “younger but emptying”?*"
)

    with st.expander("How do thresholds work?", expanded=False):
        st.write(
            "The thresholds define the dashed lines that split regions into four groups:\n"
            "- X threshold → “younger” vs “older” regions\n"
            "- Y threshold → “lived-in” vs “emptier” regions\n"
            
            "Move them to see how regions change quadrant."
        )

    st.markdown("**Scatter controls**")

    default_65 = float(df_regions["share_65plus"].median())
    default_vac = float(df_regions["share_unoccupied"].median())

    threshold_65 = st.slider(
        "From which percentage should we consider a region ‘old’?",
        float(df_regions["share_65plus"].min()),
        float(df_regions["share_65plus"].max()),
        value=default_65,
        step=0.5,
        key="threshold_65",
        help="Sets the vertical dashed line between “younger” and “older” regions.",
    )

    threshold_vac = st.slider(
        "From which percentage should we consider housing ‘highly vacant’?",
        float(df_regions["share_unoccupied"].min()),
        float(df_regions["share_unoccupied"].max()),
        value=default_vac,
        step=0.5,
        key="threshold_vac",
        help="Sets the horizontal dashed line between “lived-in” and “emptier” regions.",
    )

    # ---- SCATTER ----
    df_scatter = df_regions.copy()

    cond_high_65 = df_scatter["share_65plus"] >= threshold_65
    cond_high_vac = df_scatter["share_unoccupied"] >= threshold_vac

    df_scatter["quad_label"] = np.select(
        [
            cond_high_65 & cond_high_vac,
            (~cond_high_65) & cond_high_vac,
            cond_high_65 & (~cond_high_vac),
        ],
        [
            "Old & Empty",
            "Younger but Emptying",
            "Old & Lived-in",
        ],
        default="Younger & Lived-in",
    )

    color_col = "macro_region"
    legend_title = "Macro-region"

    fig_scatter = px.scatter(
        df_scatter,
        x="share_65plus",
        y="share_unoccupied",
        color=color_col,
        hover_name="region_norm",
        custom_data=["share_65plus", "share_unoccupied"],
        labels={
            "share_65plus": "Share of 65+ (%)",
            "share_unoccupied": "Share of unoccupied homes (%)",
        },
    )

    fig_scatter.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Share of 65+: %{customdata[0]:.2f}%<br>"
            "Share of unoccupied homes: %{customdata[1]:.2f}%"
            "<extra></extra>"
        )
    )

    fig_scatter.add_vline(
        x=threshold_65,
        line_width=1,
        line_dash="dash",
        line_color="grey",
    )
    fig_scatter.add_hline(
        y=threshold_vac,
        line_width=1,
        line_dash="dash",
        line_color="grey",
    )

    x_min, x_max = df_scatter["share_65plus"].min(), df_scatter["share_65plus"].max()
    y_min, y_max = df_scatter["share_unoccupied"].min(), df_scatter["share_unoccupied"].max()

    x_left = (x_min + threshold_65) / 2
    x_right = (threshold_65 + x_max) / 2
    y_bottom = (y_min + threshold_vac) / 2
    y_top = (threshold_vac + y_max) / 2

    fig_scatter.add_annotation(
        x=x_right,
        y=y_top,
        text="Old & Empty",
        showarrow=False,
        font=dict(size=11),
        align="center",
        bgcolor="rgba(255,255,255,0.7)",
    )
    fig_scatter.add_annotation(
        x=x_left,
        y=y_top,
        text="Younger but Emptying",
        showarrow=False,
        font=dict(size=11),
        align="center",
        bgcolor="rgba(255,255,255,0.7)",
    )
    fig_scatter.add_annotation(
        x=x_right,
        y=y_bottom,
        text="Old & Lived-in",
        showarrow=False,
        font=dict(size=11),
        align="center",
        bgcolor="rgba(255,255,255,0.7)",
    )
    fig_scatter.add_annotation(
        x=x_left,
        y=y_bottom,
        text="Younger & Lived-in",
        showarrow=False,
        font=dict(size=11),
        align="center",
        bgcolor="rgba(255,255,255,0.7)",
    )

    fig_scatter.update_layout(
        legend_title=legend_title,
        margin={"r": 10, "t": 40, "l": 60, "b": 60},
        height=550,
    )

    st.plotly_chart(fig_scatter, use_container_width=True)


    # ---------- COL2: DUMBBELL ----------
    with col2:
        st.markdown("**When rankings by age and vacancy tell different stories**")
        st.markdown(
    "**_Research Question:_** *Which regions change position the most when we move from ranking by older "
        "residents (65+) to ranking by empty homes, and what does this divergence "
        "suggest about “retired people” versus “retired places”?*"
)
        st.write(
            "The dumbbell chart highlights how far apart the rankings are: rank by ageing (65+) vs rank by vacancy."
        )

        macro_options = ["All Italy"] + sorted(
            df_regions["macro_region"].dropna().unique()
        )
        selected_macro_dumb = st.selectbox(
            "Filter by macro-region (dumbbell chart)",
            options=macro_options,
            index=0,
            key="macro_dumbbell",
        )

        top_n_dumb = st.slider(
            "Number of regions to display (by absolute rank difference)",
            min_value=5,
            max_value=len(df_regions),
            value=min(10, len(df_regions)),
            step=1,
            key="topn_dumbbell",
        )

        if selected_macro_dumb == "All Italy":
            df_dumb = df_regions.copy()
        else:
            df_dumb = df_regions[df_regions["macro_region"] == selected_macro_dumb].copy()

        df_dumb["abs_rank_diff"] = df_dumb["rank_diff"].abs()
        df_dumb = df_dumb.sort_values("abs_rank_diff", ascending=False).head(top_n_dumb)
        df_dumb = df_dumb.sort_values("abs_rank_diff", ascending=True)

        fig_dumb = go.Figure()

        for _, row in df_dumb.iterrows():
            fig_dumb.add_trace(
                go.Scatter(
                    x=[row["rank_65"], row["rank_vac"]],
                    y=[row["region_norm"], row["region_norm"]],
                    mode="lines",
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

        fig_dumb.add_trace(
            go.Scatter(
                x=df_dumb["rank_65"],
                y=df_dumb["region_norm"],
                mode="markers",
                name="Rank by ageing (65+)",
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Rank by ageing: %{x}<br>"
                    "Rank by vacancy: %{customdata[0]}<extra></extra>"
                ),
                customdata=df_dumb[["rank_vac"]].to_numpy(),
            )
        )

        fig_dumb.add_trace(
            go.Scatter(
                x=df_dumb["rank_vac"],
                y=df_dumb["region_norm"],
                mode="markers",
                name="Rank by vacancy",
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Rank by vacancy: %{x}<br>"
                    "Rank by ageing: %{customdata[0]}<extra></extra>"
                ),
                customdata=df_dumb[["rank_65"]].to_numpy(),
            )
        )

        fig_dumb.update_layout(
            xaxis_title="Rank (lower = higher position)",
            yaxis_title="Region",
            xaxis=dict(autorange="reversed"),
            margin={"r": 40, "t": 40, "l": 160, "b": 40},
            height=550,
            legend_title="Metric",
        )

        st.plotly_chart(fig_dumb, use_container_width=True)


# ---------- TAB 3: DISPERSED SETTLEMENTS MAP ----------
with tab_disp:
    st.subheader("Where are Italy’s communities most dispersed?")

    st.markdown(
        "**_Research question:_** "
        "*Which Italian regions have the highest number of small settlements (villages/hamlets) per 1,000 inhabitants, and what does this reveal about more fragmented living patterns and potentially more expensive infrastructure?*"
    )

    st.write(
        """
        This map shows how “dispersed” the settlement pattern is in each region:
        the number of villages/hamlets per 1,000 inhabitants.
        Higher values mean more small settlements for a relatively small population,
        which implies fragmented living patterns and more expensive infrastructure.
        """
    )

    vmin = 0.0
    vmax = float(df_disp["dispersed_index"].quantile(0.95))

    fig_disp = px.choropleth(
        df_disp,
        geojson=regions_geojson,
        locations="region_code",
        featureidkey="properties.COD_REG",
        color="dispersed_index",
        range_color=(vmin, vmax),
        hover_name="region",
        hover_data={
            "region_code": False,
            "tot_pop": ":,.0f",
            "settlements_count": ":,.0f",
            "dispersed_index": ":.2f",
            "share_65plus": False,
            "share_unoccupied": False,
            "macro_region": False,
        },
        labels={
            "dispersed_index": "Dispersed Settlements Index\n(villages / 1,000 inhabitants)",
        },
    )

    fig_disp.update_geos(fitbounds="locations", visible=False)

    fig_disp.update_layout(
        margin={"r": 20, "t": 20, "l": 20, "b": 20},
        coloraxis_colorbar=dict(
            title="Villages / 1,000 inhabitants",
        ),
        height=550,
    )

    st.plotly_chart(fig_disp, use_container_width=True)

    with st.expander("How to read the colour scale", expanded=False):
        st.info(
        "The colour scale is capped at the 95th percentile of the index so that one "
        "extreme region (Dispersed Settlements Index ≈ 23) does not flatten differences "
        "between regions with values around 1–2. Regions above the cap are shown in the top colour."
        )

    # ---------- SCATTER: DISPERSED INDEX vs 65+ ----------
    st.markdown("---")
    st.subheader("How dispersed villages relate to older populations?")

    st.markdown(
    "**_Research Question:_** *Do Italian regions with more dispersed settlements "
    "(more villages and hamlets per 1,000 inhabitants) also tend to have a higher "
    "share of residents aged 65 and over — and how does housing vacancy vary across "
    "these patterns?*"
)


    st.write(
        """
        Each point is a region. The x-axis shows how dispersed the settlement pattern is
        (villages/hamlets per 1,000 inhabitants), the y-axis shows the share of people aged 65+,
        and the colour encodes the share of unoccupied homes.
        This helps to spot regions where ageing and vacancy concentrate in highly fragmented landscapes.
        """
    )

    macro_options = ["All Italy"] + sorted(df_regions["macro_region"].dropna().unique())
    selected_macro_disp_scatter = st.selectbox(
        "Filter by macro-region (scatter)",
        options=macro_options,
        index=0,
        key="macro_disp_scatter",
    )

    if selected_macro_disp_scatter == "All Italy":
        df_disp_scatter = df_disp.copy()
    else:
        df_disp_scatter = df_disp[
            df_disp["macro_region"] == selected_macro_disp_scatter
        ].copy()

    fig_disp_scatter = px.scatter(
        df_disp_scatter,
        x="dispersed_index",
        y="share_65plus",
        color="share_unoccupied",
        hover_name="region",
        hover_data={
            "dispersed_index": ":.2f",
            "share_65plus": ":.2f",
            "share_unoccupied": ":.2f",
            "macro_region": False,
        },
        labels={
            "dispersed_index": "Dispersed Settlements Index\n(villages / 1,000 inhabitants)",
            "share_65plus": "Share of 65+ (%)",
            "share_unoccupied": "Share of unoccupied homes (%)",
        },
        color_continuous_scale="Viridis",  
    )

    fig_disp_scatter.update_layout(
        margin={"r": 30, "t": 30, "l": 60, "b": 60},
        height=550,
        coloraxis_colorbar=dict(
            title="Share of\nunoccupied homes (%)",
        ),
    )

    st.plotly_chart(fig_disp_scatter, use_container_width=True)    




# ---------- RDF ASSERTION OF METADATA ----------
st.markdown("<div id='rdf-section'></div>", unsafe_allow_html=True)
st.header("RDF Assertion of the Metadata")

st.markdown(
        """
        *This section documents how dataset-level metadata is expressed as RDF and
how the serializations are published alongside the tabular data.*
        """
    )

@st.cache_data
def load_ttl_preview(relative_path: str, max_lines: int = 18) -> str:
    """
    Load a short preview of an RDF/Turtle file from the project tree.
    """
    base_path = Path(__file__).resolve().parent.parent 
    full_path = base_path / relative_path

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        snippet = "".join(lines[:max_lines])
        if len(lines) > max_lines:
            snippet += "\n# … (truncated for preview) …"
        return snippet
    except FileNotFoundError:
        return f"# Preview not available.\n# File not found: {full_path}"
    
tab_assert, tab_enrich, tab_interop = st.tabs(
    [
        "RDF Assertion and Serialization",
        "Semantic Enrichment of the Datasets",
        "RDF as a Model for Data Interoperability",
    ]
)


# ===== TAB 1: RDF ASSERTION + PREVIEWS =====
with tab_assert:
    st.subheader("RDF Assertion and Serialization")

    st.markdown(
    """
All source and project-generated datasets used in the *Retired Places* project — including the original ISTAT tables, the geospatial layers from OpenStreetMap, and the derived mashup and merged datasets — are described in RDF using the **[W3C Data Catalog Vocabulary (DCAT), Version 3.0.1 (2025)](https://semiceu.github.io/DCAT-AP/releases/3.0.1/)**.

The catalog metadata itself is published under **[CC0](https://creativecommons.org/public-domain/cc0/)**, while each dataset keeps the license inherited from its original source or, in the case of mashups, from the most restrictive input dataset used in its creation.
"""
)


    st.markdown("#### We created two RDF serializations:")

    ttl_catalog_rel = Path("rdf", "rdf_serialization") / "serialization_catalog.ttl"
    ttl_dataset_rel = Path("rdf", "rdf_serialization") / "serialization_datasets.ttl"
    
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("**Catalog-level metadata** describes the overall data catalog and lists all dataset entries.")
        st.code(
            load_ttl_preview(str(ttl_catalog_rel)),
            language="turtle",
        )
        
    with col_right:
        st.markdown("**Dataset-level metadata** contains detailed metadata for each individual dataset.")
        st.code(
            load_ttl_preview(str(ttl_dataset_rel)),
            language="turtle",
        )

    st.caption(
    "You can inspect and download the complete RDF files in the project repository:"
)
    
    col_cat, col_ds = st.columns(2)
    with col_ds:
      st.markdown("Full dataset metadata (TTL)")
      st.markdown(
        """
        <a class="button"
           href="https://github.com/eugeniavd/retired_places/blob/main/rdf/rdf_serialization/serialization_datasets.ttl"
           target="_blank">
           GO
        </a>
        """,
        unsafe_allow_html=True,
    )
      
    with col_cat:
      st.markdown("Full catalog metadata (TTL)")
      st.markdown(
        """
        <a class="button"
           href="https://github.com/eugeniavd/retired_places/blob/main/rdf/rdf_serialization/serialization_catalog.ttl"
           target="_blank">
           GO
        </a>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
    """
The catalog is modeled as a `dcat:Catalog` and is explicitly declared as conforming to
**[DCAT v3.0.1](https://semiceu.github.io/DCAT-AP/releases/3.0.1/)** via `dct:conformsTo`. Each dataset is represented as a `dcat:Dataset` and linked from the catalog via `dcat:dataset`.
"""
)
    col_catalog, col_dataset = st.columns(2)
    
    with col_catalog:
       st.markdown("**Catalog metadata (dcat:Catalog)**")
       st.markdown(
        """
- `dct:title`, `dct:description` – human-readable catalog description  
- `dct:issued`, `dct:modified` – creation and last update dates  
- `dct:publisher` – project-level publisher (`foaf:Organization`)  
- `dct:license` – **CC0 1.0 Universal** for the catalog metadata  
- `adms:identifier` – stable catalog identifier  
- `dct:language` – catalog documentation language  
- `dcat:themeTaxonomy` – link to the Publications Office of the EU “data-theme” controlled vocabulary used to classify datasets by topic  
        """
    )
       
with col_dataset:
       st.markdown("**Dataset metadata (dcat:Dataset)**")
       st.markdown(
        """
- `dct:title`, `dct:description` – with language tags  
- `dct:publisher`, `dct:creator` – ISTAT, Geofabrik/OSM, or the *Retired Places* project  
- `dct:issued` – publication year  
- `dct:spatial` – spatial coverage (Italy)  
- One or more `dcat:Distribution` nodes describing access URLs, file formats (CSV, XLSX, SHP, GPKG) and access rights  
- `dct:license` – either **CC BY 4.0** or **ODbL 1.0**, depending on the source and type of data  
- Thematic classification via the EU “data-theme” vocabulary (e.g. `SOCI` for “Population and society”, `REGI` for “Regions and cities”)  
        """
    )
       
    
st.markdown("---")


# ===== TAB 2: SEMANTIC ENRICHMENT =====

with tab_enrich:
    st.subheader("Semantic Enrichment of the Datasets")

    st.markdown(
        """
Semantic enrichment builds on top of the metadata inherited from the original sources
(**ISTAT** and **Geofabrik**) and adds a lightweight semantic layer that makes
the datasets easier to discover, link and reuse.
        """
    )

    st.markdown("### Ontology stack")

    ontology_items = [
    {
        "id": "dcat",
        "name": "DCAT",
        "subtitle": "Core vocabulary for catalog and dataset description",
        "details": """
**DCAT** is used as the core vocabulary for catalog and dataset description:

- `dcat:Catalog` – the Retired Places catalog  
- `dcat:Dataset` – individual source, mashup and merged datasets  
- `dcat:distribution` – links from datasets to their downloadable files  
- `dcat:mediaType` – MIME type of each distribution  
- `dcat:accessURL` – access URLs for CSV/XLSX/SHP/GPKG files  
- `dcat:theme` – thematic classification using the EU “data-theme” vocabulary  
- `dct:language` – languages of human-readable descriptions  
        """,
    },
    {
        "id": "dcterms",
        "name": "DCTERMS",
        "subtitle": "General metadata properties (Dublin Core Terms)",
        "details": """
**Dublin Core Terms (DCTERMS)** provide general metadata fields shared across datasets:

- `dct:title`, `dct:description` – human-readable titles and descriptions  
- `dct:creator`, `dct:publisher` – ISTAT, Geofabrik/OSM, or the Retired Places project  
- `dct:issued` – year of production or publication  
- `dct:spatial` – spatial coverage (Italy)  
- `dct:source` – link to the original source page  
- `dct:license` – dataset license (CC BY 4.0 or ODbL 1.0)  
- `dct:accessRights` – access conditions when relevant  
        """,
    },
    {
        "id": "prov",
        "name": "PROV-O",
        "subtitle": "Dataset lineage and derivation",
        "details": """
**PROV-O** is used to describe how mashup and merged datasets are derived:

- `prov:wasDerivedFrom` – links each mashup or merged dataset back to  
  its original ISTAT tables and OSM/Geofabrik geospatial sources  

This makes the transformation chains between source and project-generated datasets explicit.
        """,
    },
    {
        "id": "adms",
        "name": "ADMS",
        "subtitle": "Identifiers at catalog level",
        "details": """
**ADMS (Asset Description Metadata Schema)** is used at catalog level for:

- `adms:identifier` – stable identifier of the catalog  

This helps reference the catalog itself as a reusable asset.
        """,
    },
    {
        "id": "skos",
        "name": "SKOS",
        "subtitle": "Theme vocabulary and concept labels",
        "details": """
**SKOS** is used to model and interpret the external theme vocabulary:

- `skos:ConceptScheme` – the EU “data-theme” vocabulary  
- `skos:Concept` – individual theme entries (e.g. `SOCI`, `REGI`)  
- `skos:prefLabel` – human-readable labels for each theme  

These concepts are referenced from datasets via `dcat:theme`.
        """,
    },
    {
        "id": "foaf",
        "name": "FOAF",
        "subtitle": "Project-level publisher description",
        "details": """
**FOAF** is used in the catalog graph to describe the project-level publisher:

- `foaf:Organization` – the Retired Places project as an organisation  
- `foaf:name` – the organisation’s human-readable name  
        """,
    },
    {
        "id": "cc",
        "name": "Creative Commons (CC)",
        "subtitle": "License model for the catalog metadata",
        "details": """
**Creative Commons** terms are used to describe the catalog license:

- `cc:License`, `cc:legalcode` – reference the **CC0 1.0 Universal** legal code  

The catalog metadata is released under CC0, while individual datasets retain
their own licenses (e.g. CC BY 4.0, ODbL 1.0).
        """,
    },
]

    st.markdown('<div id="ontology-tiles">', unsafe_allow_html=True)

    cols = st.columns(3)
    for idx, item in enumerate(ontology_items):
        col = cols[idx % 3]
        with col:
        
            header = f"{item['name']}"
        
            with st.expander(header, expanded=False):
                st.markdown(item["details"])

    st.markdown("</div>", unsafe_allow_html=True)

    st.info(
    """
    Although the Italian profile [**DCAT-AP_IT**](https://docs.italia.it/italia/daf/linee-guida-cataloghi-dati-dcat-ap-it/it/stabile/dcat-ap_it.html) is not fully instantiated in the current RDF graphs 
    (no `dcatapit:` properties are directly used), the metadata model has been designed to remain 
    compatible with DCAT-AP_IT constraints. The catalog can be extended with DCAT-AP_IT-specific 
    properties (e.g. `dcatapit:identifier`, `dcatapit:publisher`) if integration with national open data 
    portals is required in the future.
    """
)    

    subtab_sources, subtab_layers = st.tabs(
        ["Source metadata", "Enrichment layers"]
    )

    # ---------- Subtab 1: Source metadata ----------
    with subtab_sources:
        st.markdown("### Where does the metadata come from?")

        col_istat, col_osm = st.columns(2)

        with col_istat:
            st.markdown("**ISTAT statistical tables**")
            st.markdown(
                """
- Official documentation for population and housing tables  
- Table-level descriptions, units and reference years  
- Region codes and territorial classifications  
                """
            )

        with col_osm:
            st.markdown("**Geofabrik / OpenStreetMap geospatial layers**")
            st.markdown(
                """
- Metadata for regional boundaries and settlement locations  
- Information on extraction date, coverage and feature types  
- Links back to OpenStreetMap and Geofabrik download pages  
                """
            )

        st.markdown(
            """
Additional metadata is added or clarified, for example:

- English titles and descriptions for all datasets and project documentation  
- Explicit links to the Publications Office **“data-theme”** vocabulary used for
  thematic classification  
            """
        )

    # ---------- Subtab 2: Enrichment layers ----------
    with subtab_layers:
        st.markdown("### What semantic enrichment is applied?")

        st.markdown("#### 1. Thematic classification (`dcat:theme`)")
        st.markdown(
            """
Each dataset is tagged with one or more `dcat:theme` values pointing to the
EU “data-theme” controlled vocabulary
(<http://publications.europa.eu/resource/authority/data-theme/…>), modeled as `skos:Concept`.

Examples:

- `SOCI` – **“Population and society”** for demographic and ageing indicators  
- `REGI` – **“Regions and cities”** for territorial and geospatial datasets  
            """
        )

        st.markdown("#### 2. Language information (`dct:language`)")
        st.markdown(
            """
Dataset titles and descriptions are annotated with `dct:language` using **Lexvo URIs**, e.g.:

- <http://lexvo.org/id/iso639-1/it> for Italian  
- <http://lexvo.org/id/iso639-1/en> for English  

This makes it explicit which language each human-readable field is written in and
supports multilingual discovery.
            """
        )

        st.markdown("#### 3. Provenance and derivation (`dct:source`, `prov:wasDerivedFrom`)")
        st.markdown(
            """
For mashup and merged datasets, provenance chains are recorded explicitly:

- `dct:source` – links each mashup back to the original source pages (ISTAT, Geofabrik/OSM, etc.)  
- `prov:wasDerivedFrom` – describes which input datasets were combined to produce
  a given mashup or merged dataset  

This allows users to see **exactly which sources** were used and to trace how the
tabular indicators and geospatial layers were constructed.
            """
        )


# ===== TAB 3: RDF FOR INTEROPERABILITY =====
with tab_interop:
    st.subheader("RDF as a Model for Data Interoperability")

    st.markdown(
        """
        All metadata is represented using the Resource Description Framework (**RDF**), 
        a W3C standard in which information is modeled as triples *(subject–predicate–object)*.  

        **This RDF-based representation:**

        - enables machine-readable linking of datasets across institutions;
        - aligns the project with European Open Data and Linked Data practices;
        - facilitates future federation with other LOD resources 
          (e.g. demographic or spatial knowledge graphs);
        - supports sustainable reuse of the datasets and their metadata, in line with the 
          course requirement to document data provenance, legal context and reuse conditions 
          in a transparent way.
        """
    )


# ---------- LICENSES AND CREDITS ----------
st.markdown("<div id='licenses-section'></div>", unsafe_allow_html=True)
st.header("Licenses and Credits")
st.markdown(
    """
    *This section summarises the licenses 
    applied to the source and mashup datasets, the derived materials created within the 
    project, and the software stack used.*
    """
)



st.write(
    """
    - **Data license:** [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en) / [**CC0**](https://creativecommons.org/public-domain/cc0/) / [**ODbL 1.0**](https://opendatacommons.org/licenses/odbl/1-0/)
    - **Code license:** [**MIT**](https://opensource.org/license/mit)
    - **Software used:** Streamlit, Python etc.
    """
)

with st.expander("More details"):
    st.markdown(
    """

##### Source datasets

**ISTAT open data (population, housing, regional boundaries)**  
- Publisher: *Istituto Nazionale di Statistica (ISTAT)*  
- License: **Creative Commons Attribution 4.0 International [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en)**  
- Official documentation and files are available via the ISTAT open-data portals.

**OpenStreetMap / Geofabrik extracts (settlements and places)**  
- Publisher: *© OpenStreetMap contributors*, distributed by Geofabrik  
- License: **Open Database License [**ODbL 1.0**](https://opendatacommons.org/licenses/odbl/1-0/)**  
- Any derived databases must credit OpenStreetMap and share adapted databases under ODbL 1.0.

---

##### Mashup and merged datasets

The project creates several derived tables (MD1–MD5, MED1) by cleaning, joining and aggregating
the source datasets.

- **ISTAT-derived indicators** (e.g. MD1, MD2, MD5, MED1)  
  - License: [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en)  
  - Reuse is allowed with appropriate attribution to ISTAT and this project.

- **OSM-derived indicators** (e.g. MD3, MD4 and any derived settlement/dispersion measures)  
  - License: [**ODbL 1.0**](https://opendatacommons.org/licenses/odbl/1-0/)  
  - Reuse requires attribution to *© OpenStreetMap contributors* and compliance with the
    share-alike provisions for derived databases.

- The catalog metadata itself is published under [**CC0**](https://creativecommons.org/public-domain/cc0/), while each dataset keeps the license inherited from its original source or, in the case of mashups, from the most restrictive input dataset used in its creation.    

Unless otherwise noted, textual documentation and code in this repository are released under  
**Creative Commons Attribution 4.0 International ([**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/deed.en))** for narrative material and an
[**MIT**](https://opensource.org/license/mit) license for scripts and notebooks.

---

##### Software and tools

This dashboard and the associated analysis were produced using:

- **Python 3** for data processing and analysis  
- **pandas** and **GeoPandas** for tabular and geospatial manipulation  
- **Plotly** for interactive charts  
- **Streamlit** for the web interface  
- **Jupyter Notebooks** for exploratory analysis and preprocessing

Where relevant, each tool is used in accordance with its open-source license.

---

##### Images and icons

Icons in the results section are rendered using standard Unicode emoji.

"""
)


# ---------- FOOTER ----------

st.markdown(
    """
    <hr>
    <div style="text-align: center;">
      <small>
      This website is a project developed by Evgeniia Vdovichenko for the course 
      <a href="https://www.unibo.it/en/study/course-units-transferable-skills-moocs/course-unit-catalogue/course-unit/2024/424645" target="_blank">
      Open Access and Digital Ethics
      </a>, held by 
      <a href="https://www.unibo.it/sitoweb/monica.palmirani/en" target="_blank">
      Prof. Monica Palmirani
      </a>, within the 
      <a href="https://corsi.unibo.it/2cycle/DigitalHumanitiesKnowledge" target="_blank">
      Digital Humanities and Digital Knowledge (DHDK) Master's Degree
      </a> at 
      <a href="https://www.unibo.it/en" target="_blank">
      Alma Mater Studiorum – University of Bologna
      </a>. Contact: 
      <a href="mailto:evgeniia.vdovichenko@studio.unibo.it">evgeniia.vdovichenko@studio.unibo.it</a>.
      <br>
      © OpenStreetMap contributors, data available under the 
      <a href="https://www.openstreetmap.org/copyright" target="_blank">
      Open Database License (ODbL) 1.0
      </a>.
      <br>
      Source code on 
      <a href="https://github.com/eugeniavd/retired_places" target="_blank">
      GitHub
      </a>.
      </small>
    </div>
    """,
    unsafe_allow_html=True,
)
