import streamlit as st
import pandas as pd
import json
import plotly.express as px
from pathlib import Path


# ---------- DATA LOADING (CACHED) ----------

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

    # ⚠️ поменяй имя файла на свой финальный CSV с метриками по регионам
    df = pd.read_csv(data_path / "homes_pop_it.csv")

    df["COD_REG"] = df["region_code"].astype(int)

    with open(data_path / "italy_regions.geojson", "r", encoding="utf-8") as f:
        geojson = json.load(f)

    return df, geojson

df_regions, regions_geojson = load_data()

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Open Data Project",
    layout="wide"
)

# ---------- SIDEBAR NAVIGATION ----------
NAV_ITEMS = [
    ("Hero / Top", "#top"),
    ("About", "#about-section"),
    ("Results & Visualisations", "#results-section"),
    ("Scenario", "#scenario-section"),
    ("Datasets", "#datasets-section"),
    ("Key Findings", "#findings-section"),
    ("Documentation", "#docs-section"),
    ("Metadata (DCAT-AP / PROV)", "#metadata-section"),
    ("Preprocessing", "#preprocessing-section"),
    ("RDF Assertion", "#rdf-section"),
    ("Sustainability", "#sustainability-section"),
    ("Licenses & Credits", "#licenses-section"),
    ("Team", "#team-section"),
]

with st.sidebar:
    st.title("Navigation")
    st.markdown("Jump to section:")
    for label, anchor in NAV_ITEMS:
        st.markdown(f"- [{label}]({anchor})")

# ---------- SESSION STATE ----------
if "show_all_charts" not in st.session_state:
    st.session_state["show_all_charts"] = False


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
st.header("Results & Visualisations")

tab_summary, tab_map = st.tabs(["Summary chart", "Map"])

with tab_summary:
    st.subheader("Summary chart")
    st.write("non-map chart or KPIs.")

with tab_map:
    st.subheader("M1: Choropleth map")

    # ---- filters based on the metrics DataFrame ----
    macro_list = sorted(df_regions["macro_region"].dropna().unique())
    selected_macro = st.multiselect(
        "Filter by macro-region",
        options=macro_list,
        default=macro_list,
    )

    show_ageing = st.checkbox("Show ageing layer (share_65plus)", value=True)
    show_vacancy = st.checkbox("Show vacancy layer (share_unoccupied)", value=False)

    # Filter metrics by selected macro-regions
    df_map = df_regions[df_regions["macro_region"].isin(selected_macro)]

    if not show_ageing and not show_vacancy:
        st.info("Select at least one layer to display the map.")

    elif show_ageing and not show_vacancy:
        # only ageing layer
        fig_age = px.choropleth(
            df_map,
            geojson=regions_geojson,
            locations="COD_REG",                # join on region code from the metrics DF
            featureidkey="properties.COD_REG",  # region code in the GeoJSON properties
            color="share_65plus",
            hover_name="region",               # label on hover (from metrics, если есть)
            projection="mercator",
        )
        fig_age.update_geos(fitbounds="locations", visible=False)
        fig_age.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            coloraxis_colorbar_title="Share of 65+",
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
            hover_name="region",
            projection="mercator",
        )
        fig_vac.update_geos(fitbounds="locations", visible=False)
        fig_vac.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            coloraxis_colorbar_title="Share of unoccupied homes",
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
                coloraxis_colorbar_title="Share of 65+",
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
                coloraxis_colorbar_title="Share of unoccupied homes",
            )
            st.plotly_chart(fig_vac, use_container_width=True)


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

st.subheader("Dataset Overview")

col_orig, col_out = st.columns(2)

with col_orig:
    st.markdown("### Original Dataset")
    st.write(
        """
        - **Source:** …
        - **Records:** N = …
        - **Format:** CSV / JSON / RDF / …
        - **Size:** … MB
        """
    )
    st.download_button(
        label="Download original dataset",
        data="PLACEHOLDER_ORIGINAL_DATA",
        file_name="original_dataset_placeholder.txt",
        mime="text/plain",
        key="download_original",
    )

with col_out:
    st.markdown("### Output Dataset (Cleaned / Enriched)")
    st.write(
        """
        - **Records:** N = …
        - **Format:** CSV / RDF / …
        - **Transformations:** cleaning, harmonisation, enrichment…
        - **Size:** … MB
        """
    )
    st.download_button(
        label="Download output dataset",
        data="PLACEHOLDER_OUTPUT_DATA",
        file_name="output_dataset_placeholder.txt",
        mime="text/plain",
        key="download_output",
    )

with st.expander("Show schema / full data dictionary"):
    st.write(
        """
        Data dictionary / schema description goes here.
        - Field 1: description, example
        - Field 2: description, example
        - …
        """
    )

st.write("---")


# ---------- KEY FINDINGS ----------
st.markdown("<div id='findings-section'></div>", unsafe_allow_html=True)
st.header("Key Findings")

st.write(
    """
    Main takeaways from the analysis (4–6 bullet points):

    - Data quality: …
    - Limitations and caveats: …
    - Ethical considerations: …
    - Policy or practical recommendations: …
    - Future work: …
    """
)

st.write("---")


# ---------- DOCUMENTATION ----------
st.markdown("<div id='docs-section'></div>", unsafe_allow_html=True)
st.header("Documentation")

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

with st.expander("Sustainability"):
    st.write("Short summary of sustainability aspects (maintenance, governance, update cycles, costs, etc.).")
    st.download_button(
        label="Download full Sustainability plan (PDF/MD)",
        data="PLACEHOLDER_SUSTAIN_DOC",
        file_name="sustainability_plan_placeholder.txt",
        mime="text/plain",
        key="download_sustainability",
    )

st.write("---")


# ---------- METADATA (DCAT-AP / PROV) ----------
st.markdown("<div id='metadata-section'></div>", unsafe_allow_html=True)
st.header("Metadata and Provenance (DCAT-AP / PROV)")

col_meta1, col_meta2, col_meta3 = st.columns([1, 1, 2])

with col_meta1:
    st.download_button(
        label="Download JSON-LD",
        data="PLACEHOLDER_JSON_LD",
        file_name="metadata.jsonld",
        mime="application/ld+json",
        key="download_jsonld",
    )

with col_meta2:
    st.download_button(
        label="Download Turtle (TTL)",
        data="PLACEHOLDER_TTL",
        file_name="metadata.ttl",
        mime="text/turtle",
        key="download_ttl",
    )

with col_meta3:
    st.markdown("**Validation status**")
    st.success("✓ Valid (example status – replace with real validation results)")
    # Or, if there are warnings:
    # st.warning("! Warnings – see validation report for details.")

with st.expander("Show metadata snippet"):
    st.code(
        """
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix dct:  <http://purl.org/dc/terms/> .
        @prefix prov: <http://www.w3.org/ns/prov#> .

        <https://example.org/dataset/1> a dcat:Dataset ;
            dct:title "Example dataset"@en ;
            dct:publisher <https://example.org/organisation/1> ;
            prov:wasGeneratedBy <https://example.org/activity/cleaning> .
        """,
        language="turtle",
    )

st.write("---")


# ---------- PREPROCESSING ----------
st.markdown("<div id='preprocessing-section'></div>", unsafe_allow_html=True)
st.header("Preprocessing of Data and Visualisations")

st.write(
    """
    Brief description of the preprocessing pipeline:

    - Input formats and initial checks
    - Cleaning, harmonisation, handling of missing values
    - Aggregations / transformations used to build visualisations
    - Tools and scripts used (KNIME, Python, etc.)
    """
)

st.write("---")


# ---------- RDF ASSERTION OF METADATA ----------
st.markdown("<div id='rdf-section'></div>", unsafe_allow_html=True)
st.header("RDF Assertion of the Metadata")

st.write(
    """
    Describe how the metadata is exposed as RDF:

    - Vocabularies used (DCAT-AP, DCTERMS, PROV, etc.)
    - URI strategy for datasets, distributions, organisations
    - How the RDF is published (files, SPARQL endpoint, API, etc.)
    """
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
