import streamlit as st
import pandas as pd
import json
import plotly.express as px
from pathlib import Path
import numpy as np
import plotly.graph_objects as go


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

tab_ranked, tab_scatter, tab_overview = st.tabs(
    ["Ranked bars: Ageing vs vacancy", "Scatter: Retired people vs retired places", "Data Preprocessing"]
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



# ========= TAB 3: OVERVIEW =========
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
