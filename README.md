#Stratum Lite
A prototype for exploring infrastructure dependencies and potential cascading disruption.

Stratum Lite is an independent Python project that models a fictional port environment as a directed graph. It allows users to select an infrastructure asset and explore which connected systems could be affected if that asset were disrupted.

The current application is an interactive proof of concept, not a validated prediction system or a tool for managing real incidents.
What the prototype does
- Represents 12 fictional infrastructure assets and 14 directed dependency links using NetworkX.
- Associates assets with descriptions, criticality levels and responsible teams.
- Allows users to select a disrupted asset, a severity level (1–5) and a scenario category.
- Identifies all downstream assets reachable from the selected asset in the dependency graph.
- Calculates an illustrative, heuristic risk score for reachable assets using severity, criticality and shortest-path distance.
- Displays a colour-coded dependency graph, summary metrics, a ranked results table, an automatically generated briefing and a suggested response workflow.
Technologies
- Python — application and modelling logic
- Streamlit — interactive interface
- NetworkX — directed graph and dependency traversal
- pandas — tables and ranking
- Matplotlib — network visualisation
Run locally
You will need Python and the packages listed in requirements.txt.
1. Download or clone this repository and open a terminal in its folder.
2. Install dependencies:
   python -m pip install -r requirements.txt
3. Launch the application:
   python -m streamlit run app.py
4. Open the local address shown in the terminal, usually http://localhost:8501.
If python is not recognised on your system, try python3 in both commands.
How to use it
1. Choose an asset in the sidebar, such as Electricity Supply or Road Access.
2. Adjust the disruption severity slider.
3. Select a scenario category.
4. Examine the System Overview, Simulation Results, Operational Briefing and Response Workflow tabs.
The selected scenario category is currently descriptive: it appears in the briefing but does not change the dependency or risk calculations.
Modelling assumptions and limitations
The current model is deliberately simplified:
- Reachability is not confirmed failure. If an asset is downstream of a disrupted asset, the application marks it as potentially affected. It does not establish that the dependent asset would actually fail.
- Redundancy is not yet simulated. Backup power and alternative pathways appear in the network, but there is no logic to test whether they keep a service operating.
- Risk scores are illustrative. They are computed from the selected severity, an assigned asset criticality and the shortest dependency-path distance. They are not calibrated probabilities, independently validated estimates or real-world risk measurements.
- No time dynamics. The current model does not simulate failure propagation over time, recovery, capacity constraints or resource depletion.
- No scenario-specific propagation. Changing the scenario category does not alter the underlying graph calculation.
- Fictional data only. The port, assets, dependencies and assigned values are examples, not a representation of an actual facility.
These limitations mean that results should be interpreted as exploratory dependency analysis, not operational forecasts.
Potential next steps
The longer-term research direction is to explore:
- Different dependency types and conditional failure relationships.
- Redundancy and partial service availability.
- Time-dependent disruption and recovery.
- Uncertainty and sensitivity analysis.
- Comparison with simpler modelling baselines and explicit validation tests.
These are planned research directions, not features already implemented in this version.
Project status
Status: Implemented Python prototype under development; exploratory and not externally validated.

The project is intended to investigate how graph-based representations may support clearer reasoning about interdependent systems. It is not designed to replace human judgement or operational authority
