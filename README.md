# Barcelona Water & Climate Vulnerability Explorer

Decision-support toolkit for identifying Barcelona census sections most exposed to heavy rainfall or heatwaves. It blends network leak metrics, consumption, socioeconomic data, and weather signals into daily vulnerability scores, then wraps them in interactive Folium maps plus supporting EDA notebooks.

---

## Repository structure

| Item | Description |
| --- | --- |
| `data/BarcelonaCiutat_SeccionsCensals.csv` | Polygon geometry (WKT, EPSG:4326) plus census metadata used to draw maps. |
| `clean/vulnerability_daily.parquet` | Master daily table with rainfall and heatwave vulnerability scores per census section from 2023‑01‑04 to 2024‑12‑31. |
| `cleaningEDA.ipynb` | Data sanity checks and preprocessing diagnostics (missing values, outlier distributions, schema validation) executed before scoring. |
| `correlationAnalysis.ipynb` | Exploratory notebook quantifying relationships between consumption, leaks, weather variables, and vulnerability components. |
| `vulnerabilityScore.ipynb` | End-to-end feature engineering and scoring pipeline. Builds component indices, weights them, and writes `clean/vulnerability_daily.parquet`. |
| `vulnerabilityMap.ipynb` | Loads geometry + scores, renders daily and aggregated Folium maps, adds infrastructure overlays, and prints descriptive statistics. |
| `README.md` | Project documentation (this file). |

---

## Data & feature engineering (`vulnerabilityScore.ipynb`)

1. **Inputs** – Weather observations, consumption logs, leak incidents, IST socioeconomic index, and census geometry are merged into `gdf_daily` (one row per section per day).
2. **Component scores**  
   * `vuln_socio`: inverse-normalized IST percentile.  
   * `vuln_infrastructure`: composites of leak frequency, leaks per 1 000 m, daily incidents, and consumption per meter.  
   * Weather stresses: precipitation anomaly (`vuln_precip`), humidity anomaly, temperature anomaly, and low-humidity exposure—each standardized vs. section/month climatology.
3. **Final indices (0–100 scale)**  
   * Rainfall score = 0.25 socio + 0.35 infrastructure + 0.40 weather (70 % precip, 30 % humidity).  
   * Heatwave score = 0.35 socio + 0.20 infrastructure + 0.45 weather (70 % temperature, 30 % low humidity).
4. **Outputs** – Writes `clean/vulnerability_daily.parquet` with all intermediate components and final hazard scores.

---

## Supporting analysis notebooks

* **`cleaningEDA.ipynb`** – Verifies raw feeds (value ranges, duplicates, spatial joins), documents data cleaning steps, and exports sanitized tables consumed by the scoring pipeline.
* **`correlationAnalysis.ipynb`** – Investigates pairwise and multi-factor relationships (e.g., leaks vs. IST, humidity vs. consumption), guiding the weight choices and sanity-checking the final indices.

---

## Visualization workflow (`vulnerabilityMap.ipynb`)

1. **Daily focus date** – `target_date` defaults to **2024‑07‑15**; change it to inspect any day in the dataset.
2. **Hazard maps** – Separate Folium layers for rainfall (Blues palette) and heatwave (OrRd palette) vulnerability with tooltips showing census section, district, neighborhood, and score.
3. **Combined comparison** – Dual-layer map that overlays both hazards and shares colorbars.
4. **Infrastructure overlays** – Optional maps coloring sections by `vuln_infrastructure` or `leaks_per_1000_meters`.
5. **Daily stats** – `describe()`, top/bottom 5 sections per hazard, and cross-hazard correlation.
6. **Global aggregated maps** – Scores aggregated across 2023‑01‑04 to 2024‑12‑31 (mean, 95th percentile, max) for each hazard:
   | Metric | Interpretation |
   | --- | --- |
   | `RAIN_MEAN` | Chronic rainfall stress. |
   | `RAIN_P95` | Recurring high-end rainfall stress. |
   | `RAIN_MAX` | Worst recorded rainfall stress. |
   | `HEAT_MEAN` | Chronic heat stress. |
   | `HEAT_P95` | Recurring high-end heat stress. |
   | `HEAT_MAX` | Worst recorded heat stress. |
7. **Aggregated stats** – Summary tables listing distribution metrics plus top/bottom sections for all six global maps.

---

## Getting started

1. **Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Run cleaning/EDA (optional)** – Execute `cleaningEDA.ipynb` if upstream feeds changed; use `correlationAnalysis.ipynb` for exploratory diagnostics.
3. **Rebuild scores** – Run `vulnerabilityScore.ipynb` to regenerate `clean/vulnerability_daily.parquet`.
4. **Explore maps** – Open `vulnerabilityMap.ipynb`, adjust `target_date`, and run all cells to view Folium maps inline.

---

## Notes & assumptions

* Geometry and vulnerability tables share `SECCIO_CENSAL` (`080193` + district + section code).
* All spatial data are treated as EPSG:4326.
* Missing scores render in gray on Folium maps.
* Extend `metric_configs` to visualize additional aggregated indicators.

