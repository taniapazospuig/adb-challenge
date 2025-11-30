# Barcelona Water & Climate Vulnerability Assessment

A data-driven tool for identifying Barcelona census sections most vulnerable to heavy rainfall and heatwaves. The system integrates weather data, water infrastructure metrics, and socioeconomic indicators to generate daily vulnerability scores and interactive maps.

## Overview

This project calculates vulnerability scores for each of Barcelona's 1,068 census sections on a daily basis from January 2023 to December 2024. The scores combine three key dimensions:

- **Socioeconomic vulnerability**: Based on the IST (Territorial Socioeconomic Index)
- **Infrastructure vulnerability**: Based on water leak frequency, leak density, and consumption patterns
- **Weather vulnerability**: Based on temperature, precipitation, and humidity anomalies relative to local climatology

Two separate vulnerability indices are computed:
- **Rainfall vulnerability**: For intense precipitation events
- **Heatwave vulnerability**: For extreme heat events

## Project Structure

```
adb-challenge/
├── data/                          # Raw input data
│   ├── BarcelonaCiutat_SeccionsCensals.csv
│   ├── consum_avisos_missatges_v2.parquet
│   ├── consum_telelectura_v2.parquet
│   ├── Dades_meteorològiques_diàries_de_la_XEMA_20251119.csv
│   └── ist_per_seccio_censal.csv
│
├── cleaningEDA.ipynb              # Data cleaning and preprocessing pipeline
├── correlationAnalysis.ipynb      # Statistical analysis for variable selection
├── vulnerabilityScore.ipynb       # Main scoring pipeline
├── vulnerabilityMap.ipynb         # Interactive map visualization
├── vulnerability_score_config.json # Weather variable weights configuration
├── split_parquet.py               # Utility script for splitting large parquet files
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
└── .gitignore                     # Git ignore rules
```

**Key Files:**
- **Notebooks**: Run in sequence: `cleaningEDA.ipynb` → `correlationAnalysis.ipynb` → `vulnerabilityScore.ipynb` → `vulnerabilityMap.ipynb`
- **Data directory**: Contains raw input files. Processed data and split files are generated automatically by the notebooks.
- **Output**: After running the notebooks, `clean/vulnerability_daily.parquet` will contain the final dataset with daily vulnerability scores (777,504 rows covering 2023-01-04 to 2024-12-31).

## Data Sources

- **Weather stations**: Three active stations (D5, X4, X8) providing daily meteorological measurements (Generalitat de Catalunya)
- **Water consumption**: Daily meter readings (Aigües de Barcelona)
- **Leak incidents**: Water leak reports (Aigües de Barcelona)
- **Socioeconomic index**: 2022 IST index by census section (Idescat)
- **Census geometry**: 2022 Polygon boundaries for Barcelona's 1,068 census sections (OpenDataBCN)

## Vulnerability Scoring Methodology

### Component Scores

1. **Socioeconomic component** (`vuln_socioeconomic`): Inverse-normalized IST percentile (higher IST = lower vulnerability). Static across time periods.

2. **Infrastructure component**: Varies by hazard type:
   - **Heatwave infrastructure** (`vuln_infrastructure_heatwave`): 
     - 60% consumption surge (composite of consumption surge, contracts surge, and consumption intensity)
     - 40% baseline leak frequency (composite of leak frequency, leak density, and incident metrics)
   - **Rainfall infrastructure** (`vuln_infrastructure_rainfall`):
     - 60% leak response to rainfall (composite of leak frequency, contracts, and intensity during rain events)
     - 40% baseline leak frequency

3. **Weather component**: Data-driven variables selected through correlation analysis:
   - **Heatwave weather** (`vuln_weather_heatwave`): Weighted combination of 6 variables (average/min/max temperatures, evapotranspiration, solar radiation)
   - **Rainfall weather** (`vuln_weather_rainfall`): Weighted combination of 5 precipitation variables (30-min max, 1-hour max, 1-minute max, daily total, 8-hour accumulation)
   - Variables are normalized and weighted according to `vulnerability_score_config.json`, derived from correlation analysis with consumption and leak patterns

### Final Vulnerability Indices

Both vulnerability scores use the same component weights:

**Rainfall Vulnerability** (0-1 scale):
- 60% weather + 25% infrastructure + 15% socioeconomic

**Heatwave Vulnerability** (0-1 scale):
- 60% weather + 25% infrastructure + 15% socioeconomic

The infrastructure component differs between the two (as described above), while weather and socioeconomic components use the same calculation method but with hazard-specific variables and metrics.

## Getting Started

### Prerequisites

- Python 3.11+
- Required packages listed in `requirements.txt`

### Installation

```bash
# Create virtual environment
python3 -m venv adb
source adb/bin/activate  # On Windows: adb\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

1. **Data cleaning**: Run `cleaningEDA.ipynb` to process raw data and generate cleaned datasets
2. **Correlation analysis**: Run `correlationAnalysis.ipynb` to understand variable relationships (optional)
3. **Generate scores**: Run `vulnerabilityScore.ipynb` to calculate daily vulnerability scores
4. **Visualize**: Run `vulnerabilityMap.ipynb` to create interactive maps

## Output

The main output is `clean/vulnerability_daily.parquet`, containing:
- Daily vulnerability scores for rainfall and heatwaves per census section
- All intermediate component scores
- Date range: 2023-01-04 to 2024-12-31
- 777,504 total records (1,068 sections × ~728 days)

Maps use median aggregation by default (representing typical baseline vulnerability), with mean aggregation available as an alternative to include extreme event impacts.

## Technical Notes

- Census sections are identified by `SECCIO_CENSAL` (format: `080193` + district code + section code)
- All spatial data uses EPSG:4326 (WGS84) coordinate system
- Weather stations are assigned to census sections via nearest-neighbor spatial join
- Missing scores appear in gray on maps (preserved to indicate data availability)
- Large datasets are processed in chunks for memory efficiency
