# Interactive Vulnerability Prediction Map

This interactive dashboard allows you to predict vulnerability scores for Barcelona census sections based on different weather conditions. Adjust weather parameters and see how vulnerability changes in real-time across the city.

## Features

- **Interactive Weather Controls**: Adjust temperature, precipitation, and humidity parameters
- **Real-time Updates**: Maps and statistics update automatically when parameters change
- **Dual Vulnerability Views**: Switch between rainfall and heatwave vulnerability maps
- **Seasonal Baselines**: Select month for seasonal comparison
- **Statistical Summary**: View mean, min, max, and standard deviation of vulnerability scores
- **Top Vulnerable Areas**: See which census sections are most at risk

## Installation

### Option 1: Panel Dashboard (Recommended)

```bash
pip install panel folium geopandas pandas numpy
```

Then run:
```bash
panel serve interactive_vulnerability_map.py --show
```

The dashboard will open in your browser automatically.

### Option 2: Streamlit Dashboard (Alternative)

```bash
pip install streamlit streamlit-folium folium geopandas pandas numpy
```

Then run:
```bash
streamlit run interactive_vulnerability_map_streamlit.py
```

## How It Works

### Vulnerability Score Calculation

The vulnerability scores are calculated using normalized metrics from correlation analysis:

#### Rainfall Vulnerability Score
- **Socioeconomic (25%)**: Based on IST (Índex socioeconòmic territorial) - lower IST = higher vulnerability
- **Infrastructure (35%)**: Based on:
  - Leak frequency (`leaks_per_year`)
  - Leak density (`leaks_per_1000_meters`)
  - Daily leak incidents
  - Consumption intensity (`consumption_per_meter`)
- **Weather (40%)**: Based on:
  - Precipitation extremes (70%)
  - High humidity conditions (30%)

#### Heatwave Vulnerability Score
- **Socioeconomic (35%)**: Based on IST - higher weight for heat-related vulnerability
- **Infrastructure (20%)**: Same components as rainfall (lower weight)
- **Weather (45%)**: Based on:
  - Temperature extremes (70%)
  - Low humidity conditions (30%)

### Weather Parameter Effects

- **Temperature**: Higher temperatures increase heatwave vulnerability, especially when above seasonal averages
- **Precipitation**: Higher precipitation increases rainfall vulnerability, particularly during intense rainfall events
- **Humidity**: 
  - High humidity increases rainfall vulnerability
  - Low humidity increases heatwave vulnerability
- **Month Selection**: Affects seasonal baseline for anomaly calculation

## Usage Tips

1. **Start with default values** to see current vulnerability patterns
2. **Adjust parameters gradually** to observe how different weather conditions affect vulnerability
3. **Compare scenarios**:
   - Heatwave scenario: High temperature (35-40°C), low humidity (30-40%)
   - Rainstorm scenario: Moderate temperature, high precipitation (50-100mm), high humidity (80-90%)
4. **Use month selector** to account for seasonal variations
5. **Switch between vulnerability types** to see how the same weather affects different risk factors

## Data Sources

- **Census Sections**: Barcelona administrative boundaries
- **Vulnerability Metrics**: Calculated from:
  - Consumption data (water meters, daily consumption)
  - Leak incident reports
  - Socioeconomic index (IST)
  - Weather station data (temperature, precipitation, humidity)

## Technical Details

- **Base Data**: Loaded from `clean/vulnerability_daily.parquet`
- **Census Geometry**: Loaded from `data/BarcelonaCiutat_SeccionsCensals.csv`
- **Scoring Method**: Uses normalized metrics from correlation analysis to ensure each component provides distinct information
- **Weather Normalization**: Uses seasonal averages per census section to calculate anomalies

## Troubleshooting

- **If maps don't load**: Ensure all data files are in the correct directories
- **If performance is slow**: The first load caches data; subsequent updates should be faster
- **If scores seem off**: Check that weather parameters are within reasonable ranges for Barcelona (temp: 15-45°C, precip: 0-100mm, humidity: 20-100%)

## Future Enhancements

Potential improvements:
- Historical weather scenario comparison
- Export predicted scores to CSV/GeoJSON
- Additional weather variables (wind speed, pressure)
- Time-series prediction for multiple days
- Integration with weather forecast APIs

