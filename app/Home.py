import streamlit as st
import pandas as pd
import json
import plotly.express as px
from pathlib import Path
import numpy as np
import plotly.graph_objects as go


# ---------- DATA LOADING ----------

st.set_page_config(page_title="Retired Places", layout="wide")

@st.cache_data
def load_data():
    """
    Load regional metrics and the GeoJSON with regional boundaries.

    We join the metrics table to the GeoJSON using the region code (COD_REG). 
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


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Open Data Project",
    layout="wide"
)

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
    ("Team", "#team-section"),
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
.rdf-button,
.rdf-button:link,
.rdf-button:visited,
.rdf-button:hover,
.rdf-button:active {
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

.rdf-button:hover {
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
    st.title("Project Title Placeholder")
    st.subheader("Research question: How does X relate to Y across Z?")

    # CTA: anchor to About section
    st.markdown(
        "<a href='#about-section' style='text-decoration:none;'>"
        "🡇 Learn more about the project</a>",
        unsafe_allow_html=True
    )
    st.write("---")


# ---------- ABOUT ----------
st.markdown("<h2 id='about-section'>About</h2>", unsafe_allow_html=True)
st.write(
    """
    Short description of the project goes here.
    Explain the context, goals, and why this dataset matters.
    """
)

st.write("---")


# ---------- RESULTS & VISUALISATIONS ----------
st.markdown("<div id='results-section'></div>", unsafe_allow_html=True)
st.header("Key Findings")

tab_map, tab_summary = st.tabs(["Map", "Summary chart"])

with tab_map:
    st.subheader("M1: Choropleth map")

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
                "COD_REG": False,        
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
                "COD_REG": False,
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
    st.write("we found some results.....")


# ---------- SCENARIO ----------
st.markdown("<div id='scenario-section'></div>", unsafe_allow_html=True)
st.header("Scenario")
st.subheader("Problem and Research Questions")
st.write(
    """
    **Problem statement.**  
    Briefly describe the societal / policy / cultural problem.

    **Research questions.**
    - RQ1: …
    - RQ2: …
    - RQ3: …
    """
)

st.write("---")


# ---------- DATASETS ----------
st.markdown("<div id='datasets-section'></div>", unsafe_allow_html=True)
st.header("Datasets")

def render_dataset_card(ds: dict):
   
    provenance_or_compiler = ds.get("provenance") or ds.get("compiler") or "—"

    
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
            <strong>Provenance / Compiler:</strong> {provenance_or_compiler}<br>
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
        "provenance": "Istat",
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
        "provenance": "IstatData",
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
        "provenance": "Istat",
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
        "provenance": "Geofabric",
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
        "provenance": "Geofabric",
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
        "provenance": "Geofabric",
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
        "provenance": "Geofabric",
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
        "provenance": "Geofabric",
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
        "compiler": "Evgeniia Vdovichenko",
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
        "compiler": "Evgeniia Vdovichenko",
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
        "compiler": "Evgeniia Vdovichenko",
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
        "compiler": "Evgeniia Vdovichenko",
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
        "compiler": "Evgeniia Vdovichenko",
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
        "compiler": "Evgeniia Vdovichenko",
        "format": "GPKG",
        "metadata": "Provided",
        "uri": "https://github.com/eugeniavd/retired_places/blob/main/data/processed/MED1_settlements_italy.gpkg ",
        "uri_label": "MED1_settlements_italy",
        "license": "CC BY 4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
    },
   
]


tab_source, tab_mashup, tab_merged = st.tabs(
    ["Source datasets", "Mashup datasets", "Merged datasets"]
)

cols_per_row = 3  

with tab_source:
    n = len(source_datasets)
    for i in range(0, n, cols_per_row):
        row_items = source_datasets[i : i + cols_per_row]
        cols = st.columns(cols_per_row)

        if len(row_items) == 2 and i + cols_per_row >= n:
            start_idx = 0 
        else:
            start_idx = 0

        for ds, col in zip(row_items, cols[start_idx : start_idx + len(row_items)]):
            with col:
                render_dataset_card(ds)

with tab_mashup:
    n = len(mashup_datasets)
    for i in range(0, n, cols_per_row):
        row_items = mashup_datasets[i : i + cols_per_row]
        cols = st.columns(cols_per_row)

        if len(row_items) == 2 and i + cols_per_row >= n:
            start_idx = 0  # или 1, по вкусу
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

st.write("---")


# ---------- Analysis ----------
st.markdown("<div id='docs-section'></div>", unsafe_allow_html=True)
st.header("Analysis")

with st.expander("Quality"):
    st.write("Short summary of data quality assessment (completeness, accuracy, consistency, timeliness, etc.).")
    st.download_button(
        label="Download full Quality report (PDF/MD)",
        data="PLACEHOLDER_QUALITY_DOC",
        file_name="quality_report_placeholder.txt",
        mime="text/plain",
        key="download_quality",
    )

with st.expander("Legal"):
    st.write("Short summary of legal analysis (GDPR, lawful basis, licenses, reuse conditions, etc.).")
    st.download_button(
        label="Download full Legal report (PDF/MD)",
        data="PLACEHOLDER_LEGAL_DOC",
        file_name="legal_report_placeholder.txt",
        mime="text/plain",
        key="download_legal",
    )

with st.expander("Ethics"):
    st.write("Short summary of ethical analysis (bias, fairness, discrimination, representation, etc.).")
    st.download_button(
        label="Download full Ethics report (PDF/MD)",
        data="PLACEHOLDER_ETHICS_DOC",
        file_name="ethics_report_placeholder.txt",
        mime="text/plain",
        key="download_ethics",
    )

with st.expander("Technical"):
    st.write("Short summary of technical aspects (formats, encoding, URIs, APIs, pipelines, etc.).")
    st.download_button(
        label="Download full Technical documentation (PDF/MD)",
        data="PLACEHOLDER_TECH_DOC",
        file_name="technical_documentation_placeholder.txt",
        mime="text/plain",
        key="download_technical",
    )

st.write("---")

# ---------- SUSTAINABILITY OF DATASET UPDATES ----------
st.markdown("<div id='sustainability-section'></div>", unsafe_allow_html=True)
st.header("Sustainability of Dataset Updates Over Time")

st.write(
    """
    Explain how the datasets will be updated and maintained:

    - Update frequency and triggers
    - Responsibilities and governance
    - Versioning and archival strategies
    - Long-term sustainability (funding, hosting, community)
    """
)

st.write("---")


# ---------- VISUALISATIONS ----------
st.markdown("<div id='graphs-section'></div>", unsafe_allow_html=True)
st.header("Visualisations")

tab_ranked, tab_scatter, tab_disp, tab_overview = st.tabs(
    [
        "Ranked bars: Ageing vs vacancy",
        "Scatter: Retired people vs retired places",
        "Map: Dispersed settlements",
        "Data Preprocessing",
    ]
)


# ========= TAB 1: RANKED BARS =========
with tab_ranked:
    st.subheader("Chart. Ageing vs vacancy (two metrics per region)")

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
    st.subheader("Retired people vs retired places")

    col1, col2 = st.columns(2)

    # ---------- COL1: SCATTER ----------
with col1:
    st.markdown("**Scatter: retired people vs retired places**")

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
        st.markdown("**Dumbbell: rank by ageing vs rank by vacancy**")
        st.write(
            "The dumbbell chart highlights how far apart the rankings are: "
            "rank by ageing (65+) vs rank by vacancy."
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
    st.subheader("Map. Dispersed Settlements Index")

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
    st.subheader("Scatter. Dispersed Settlements Index vs share of 65+")

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


# ========= TAB 4: OVERVIEW =========
with tab_overview:
    st.write(
        """
        Brief description of the preprocessing pipeline:

        - Input formats and initial checks.
        - Cleaning, harmonisation, handling of missing values.
        - Aggregations / transformations used to build the main visualisations.
        - Tools and scripts used (KNIME, Python, etc.).
        """
    )


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
All source and project-generated datasets used in the *Retired Places* project — including the original ISTAT tables, the geospatial layers from OpenStreetMap, and the derived mashup and merged datasets — are described in RDF using the **[W3C Data Catalog Vocabulary (DCAT), Version 3 (2024)](https://www.w3.org/TR/vocab-dcat-3/)**.

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
        <a class="rdf-button"
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
        <a class="rdf-button"
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
**[DCAT v3](https://www.w3.org/TR/vocab-dcat-3/)** via `dct:conformsTo`. Each dataset is represented as a `dcat:Dataset` and linked from the catalog via `dcat:dataset`.
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
- `dcat:language` – catalog documentation language  
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
        "name": "DCAT (v3)",
        "subtitle": "Core vocabulary for catalog and dataset description",
        "details": """
**DCAT (v3)** is used as the core vocabulary for catalog and dataset description:

- `dcat:Catalog` – the Retired Places catalog  
- `dcat:Dataset` – individual source, mashup and merged datasets  
- `dcat:distribution` – links from datasets to their downloadable files  
- `dcat:mediaType` – MIME type of each distribution  
- `dcat:accessURL` – access URLs for CSV/XLSX/SHP/GPKG files  
- `dcat:theme` – thematic classification using the EU “data-theme” vocabulary  
- `dcat:language` – languages of human-readable descriptions  
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
- `dct:language` – language of labels and descriptions, via Lexvo URIs  
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
    Although the Italian profile **DCAT-AP_IT** is not fully instantiated in the current RDF graphs 
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

st.write(
    """
    - **Data license:** e.g., CC BY 4.0 / CC0 / ODbL …
    - **Code license:** e.g., MIT / Apache-2.0 …
    - **Software used:** Streamlit, Python, KNIME, QGIS, etc.
    """
)

with st.expander("More details"):
    st.write(
        """
        Detailed license statements, third-party attributions, and any additional
        acknowledgements can be listed here.
        """
    )

st.write("---")


# ---------- TEAM ----------
st.markdown("<div id='team-section'></div>", unsafe_allow_html=True)
st.header("Team")

st.write(
    """
    - **Project lead:** Name Surname (affiliation)
    - **Data curation:** …
    - **Legal & ethics:** …
    - **Visualisation & frontend:** …
    """
)

st.write("---")


# ---------- FOOTER ----------
st.markdown(
    """
    <hr>
    <small>
    This one-page site is part of an open data & digital ethics project.  
    Contact: <a href="mailto:contact@example.org">contact@example.org</a>
    </small>
    """,
    unsafe_allow_html=True,
)
