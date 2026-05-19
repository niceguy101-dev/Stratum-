import streamlit as st
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt 

st.set_page_config(
    page_title="Stratum Lite",
    page_icon="🌐",
    layout="wide"
)

# ----------------------------
# Styling
# ----------------------------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 20px;
        color: #666666;
        margin-top: 0px;
    }
    .section-box {
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #e6e6e6;
        background-color: #fafafa;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="main-title">STRATUM Lite</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Cognitive infrastructure prototype for disruption modelling, cascade analysis, and operational coordination.</p>',
    unsafe_allow_html=True
)

st.divider()

# ----------------------------
# Build fictional infrastructure graph
# ----------------------------

G = nx.DiGraph()

assets = {
    "Main Port Gate": {
        "description": "Controls vehicle entry and exit.",
        "criticality": 4,
        "team": "Site Access Team"
    },
    "Customs Checkpoint": {
        "description": "Handles cargo clearance.",
        "criticality": 5,
        "team": "Customs Liaison Team"
    },
    "Warehouse A": {
        "description": "Stores general cargo.",
        "criticality": 3,
        "team": "Warehouse Operations"
    },
    "Cold Storage": {
        "description": "Stores temperature-sensitive goods.",
        "criticality": 5,
        "team": "Cold Chain Team"
    },
    "Electricity Supply": {
        "description": "Provides main power to the site.",
        "criticality": 5,
        "team": "Engineering Team"
    },
    "Backup Generator": {
        "description": "Provides emergency power.",
        "criticality": 4,
        "team": "Engineering Team"
    },
    "Fuel Depot": {
        "description": "Supplies fuel for generators and vehicles.",
        "criticality": 4,
        "team": "Fuel and Logistics Team"
    },
    "Rail Terminal": {
        "description": "Connects the port to inland freight routes.",
        "criticality": 4,
        "team": "Rail Operations"
    },
    "Road Access": {
        "description": "Main road link to the port.",
        "criticality": 5,
        "team": "Transport Coordination"
    },
    "Security Control Room": {
        "description": "Coordinates surveillance and site security.",
        "criticality": 5,
        "team": "Security Team"
    },
    "Emergency Command Room": {
        "description": "Coordinates incident response.",
        "criticality": 5,
        "team": "Incident Command"
    },
    "Network Operations": {
        "description": "Supports digital systems and communications.",
        "criticality": 5,
        "team": "Digital Operations"
    },
}

dependencies = [
    ("Electricity Supply", "Cold Storage"),
    ("Electricity Supply", "Customs Checkpoint"),
    ("Electricity Supply", "Security Control Room"),
    ("Electricity Supply", "Network Operations"),
    ("Backup Generator", "Cold Storage"),
    ("Fuel Depot", "Backup Generator"),
    ("Road Access", "Main Port Gate"),
    ("Main Port Gate", "Warehouse A"),
    ("Customs Checkpoint", "Warehouse A"),
    ("Rail Terminal", "Warehouse A"),
    ("Network Operations", "Customs Checkpoint"),
    ("Network Operations", "Security Control Room"),
    ("Security Control Room", "Emergency Command Room"),
    ("Road Access", "Emergency Command Room"),
]

for asset, info in assets.items():
    G.add_node(asset, **info)

G.add_edges_from(dependencies)
def draw_dependency_network(graph, disrupted_asset, affected_assets):
    fig, ax = plt.subplots(figsize=(12, 7))

    pos = nx.spring_layout(graph, seed=42, k=0.8)

    node_colours = []
    for node in graph.nodes():
        if node == disrupted_asset:
            node_colours.append("#ff4b4b")
        elif node in affected_assets:
            node_colours.append("#ffa500")
        else:
            node_colours.append("#7fb3d5")

    nx.draw_networkx_nodes(
        graph,
        pos,
        node_color=node_colours,
        node_size=1800,
        edgecolors="black",
        linewidths=1,
        ax=ax
    )

    nx.draw_networkx_edges(
        graph,
        pos,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=18,
        width=1.5,
        alpha=0.7,
        ax=ax
    )

    nx.draw_networkx_labels(
        graph,
        pos,
        font_size=8,
        font_weight="bold",
        ax=ax
    )

    ax.set_title(
        "Infrastructure Dependency Network",
        fontsize=16,
        fontweight="bold"
    )

    ax.axis("off")

    return fig
# ----------------------------
# Sidebar controls
# ----------------------------

st.sidebar.header("Scenario Controls")

disrupted_asset = st.sidebar.selectbox(
    "Select disrupted asset",
    list(assets.keys())
)

severity = st.sidebar.slider(
    "Disruption severity",
    min_value=1,
    max_value=5,
    value=3
)

scenario_type = st.sidebar.selectbox(
    "Scenario type",
    [
        "Power disruption",
        "Access disruption",
        "Digital systems disruption",
        "Logistics bottleneck",
        "Emergency resilience event"
    ]
)

st.sidebar.info(
    "This prototype uses fictional data for demonstration only. "
    "It supports human decision-making and does not replace operational authority."
)

# ----------------------------
# Calculate affected systems
# ----------------------------

affected = list(nx.descendants(G, disrupted_asset))

risk_scores = []

for asset in affected:
    dependency_distance = nx.shortest_path_length(G, disrupted_asset, asset)
    criticality = assets[asset]["criticality"]
    risk_score = max(1, severity * criticality * (6 - dependency_distance))

    risk_scores.append({
        "Affected Asset": asset,
        "Responsible Team": assets[asset]["team"],
        "Criticality": criticality,
        "Dependency Distance": dependency_distance,
        "Estimated Risk Score": risk_score,
        "Description": assets[asset]["description"]
    })

risk_df = pd.DataFrame(risk_scores)

if not risk_df.empty:
    highest_risk = risk_df["Estimated Risk Score"].max()
    top_asset = risk_df.sort_values(
        by="Estimated Risk Score",
        ascending=False
    ).iloc[0]["Affected Asset"]
else:
    highest_risk = 0
    top_asset = "None"

if severity >= 4 and len(affected) >= 3:
    incident_level = "High"
elif severity >= 3 or len(affected) >= 2:
    incident_level = "Moderate"
else:
    incident_level = "Low"

# ----------------------------
# Metrics
# ----------------------------

m1, m2, m3, m4 = st.columns(4)

m1.metric("Disrupted Asset", disrupted_asset)
m2.metric("Affected Systems", len(affected))
m3.metric("Incident Level", incident_level)
m4.metric("Highest Risk Score", highest_risk)

st.divider()

# ----------------------------
# Tabs
# ----------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "System Overview",
        "Simulation Results",
        "Operational Briefing",
        "Response Workflow"
    ]
)

with tab1:
    st.header("System Overview")

    st.write(
        "Stratum Lite models a fictional port environment as a dependency network. "
        "Each asset has a criticality level, a responsible team, and downstream dependencies."
    )

    asset_table = pd.DataFrame([
        {
            "Asset": asset,
            "Description": info["description"],
            "Criticality": info["criticality"],
            "Responsible Team": info["team"]
        }
        for asset, info in assets.items()
    ])

    st.dataframe(asset_table, use_container_width=True)

    st.subheader("Dependency Links")


    dependency_table = pd.DataFrame(
        dependencies,
        columns=["Source Asset", "Dependent Asset"]
    )

    st.dataframe(dependency_table, use_container_width=True)

    st.subheader("Visual Dependency Network")

    st.write(
        "The network below shows how assests depend on each other."
        "The disrupted assetis highlighted in red. Downstream affected systems are highlighted in orange."
    )

    network_fig = draw_dependency_network(G, disrupted_asset, affected)

    st.pyplot(network_fig)

with tab2:
    st.header("Simulation Results")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Disrupted Asset")
        st.error(disrupted_asset)
        st.write(assets[disrupted_asset]["description"])
        st.write(f"Responsible team: **{assets[disrupted_asset]['team']}**")
        st.write(f"Scenario type: **{scenario_type}**")
        st.write(f"Severity: **{severity}/5**")

    with col2:
        st.subheader("Cascade Summary")

        if affected:
            st.warning(
                f"{len(affected)} downstream systems may be affected by this disruption."
            )
            st.write(f"Highest-risk affected asset: **{top_asset}**")
        else:
            st.success("No downstream dependencies identified.")

    if not risk_df.empty:
        st.subheader("Affected Systems Ranked by Risk")
        st.dataframe(
            risk_df.sort_values(by="Estimated Risk Score", ascending=False),
            use_container_width=True
        )
    else:
        st.info("No cascading effects found for this asset.")

with tab3:
    st.header("Operational Briefing")

    if affected:
        top_risks = risk_df.sort_values(
            by="Estimated Risk Score",
            ascending=False
        ).head(5)

        briefing = f"""
STRATUM LITE — INITIAL OPERATIONAL BRIEFING

Incident:
Disruption to {disrupted_asset}

Scenario Type:
{scenario_type}

Severity Level:
{severity}/5

Incident Level:
{incident_level}

Initial Assessment:
The disruption to {disrupted_asset} may affect {len(affected)} connected systems within the modelled operational environment.

The most exposed systems appear to be:
{", ".join(top_risks["Affected Asset"].tolist())}

Likely Consequences:
- Reduced operational visibility
- Slower cargo, site, or transport movement
- Increased pressure on manual coordination
- Possible delays to linked systems
- Greater risk of cascading disruption if not contained early

Priority Actions:
1. Confirm the operational status of {disrupted_asset}.
2. Notify {assets[disrupted_asset]["team"]} and relevant downstream teams.
3. Activate backup or manual procedures where available.
4. Monitor the highest-risk affected systems.
5. Record decisions and actions in the incident log.
6. Escalate if disruption expands beyond the current affected system list.

Governance Note:
This briefing is decision-support only. Human operators remain responsible for final judgement, escalation, and action.
"""

        st.text_area("Generated Briefing", briefing, height=420)
    else:
        st.info(
            "No downstream effects were identified. Continue monitoring the asset and confirm whether hidden dependencies exist."
        )

with tab4:
    st.header("Response Workflow")

    if affected:
        workflow_items = []

        sorted_risks = risk_df.sort_values(
            by="Estimated Risk Score",
            ascending=False
        )

        for index, row in sorted_risks.iterrows():
            workflow_items.append({
                "Priority": len(workflow_items) + 1,
                "Action": f"Assess operational status of {row['Affected Asset']}",
                "Responsible Team": row["Responsible Team"],
                "Status": "Pending",
                "Rationale": f"Risk score {row['Estimated Risk Score']}"
            })

        workflow_df = pd.DataFrame(workflow_items)

        st.dataframe(workflow_df, use_container_width=True)

        st.subheader("Escalation Triggers")

        st.write(
            "- Criticality 5 asset becomes unavailable\n"
            "- More than three downstream systems affected\n"
            "- Manual fallback procedures unavailable\n"
            "- Incident duration exceeds expected recovery window\n"
            "- Public safety, security, or continuity risk increases"
        )
    else:
        st.success("No response workflow required beyond monitoring at this stage.")