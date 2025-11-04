## Data Dictionary

### consum

- **Rows**: 17112709
- **Columns**: 12
- **Overall missing (%)**: 49.58

| Column | Dtype | Missing (%) | #Unique | Example |
|---|---|---:|---:|---|
| POLIZA_SUMINISTRO | object | 0.0 | 11797 | VECWAVDUULZDSBOP |
| FECHA | object | 0.0 | 1458 | 2021-01-01 |
| CONSUMO_REAL | int64 | 0.0 | 29879 | 1758 |
| SECCIO_CENSAL | float64 | 66.11 | 448 | 801903025.0 |
| US_AIGUA_GEST | object | 66.11 | 3 | C |
| NUM_MUN_SGAB | float64 | 66.11 | 4 | 0.0 |
| NUM_DTE_MUNI | float64 | 66.11 | 8 | 3.0 |
| NUM_COMPLET | object | 66.11 | 3999 | N5ER4KUNPNXOQQCE |
| DATA_INST_COMP | object | 66.11 | 453 | 2016-04-25 |
| MARCA_COMP | object | 66.11 | 4 | 5557SZ47QZAZ56EQ |
| CODI_MODEL | float64 | 66.11 | 11 | 23.0 |
| DIAM_COMP | float64 | 66.11 | 3 | 30.0 |

### fuites

- **Rows**: 76372248
- **Columns**: 11
- **Overall missing (%)**: 10.04

| Column | Dtype | Missing (%) | #Unique | Example |
|---|---|---:|---:|---|
| POLISSA_SUBM | object | 0.0 | 2697 | RGYFWIZ4ZRRZKX2K |
| DATA_INI_FACT | object | 0.0 | 485 | 2023-09-13 00:00:00 |
| DATA_FIN_FACT | object | 0.0 | 464 | 2023-11-14 00:00:00 |
| CREATED_MENSAJE | datetime64[ns] | 30.53 | 2861 | 2023-12-03 15:43:34 |
| CODIGO_MENSAJE | object | 30.53 | 2 | FUITA |
| TIPO_MENSAJE | object | 30.53 | 2 | Mail |
| US_AIGUA_SUBM | object | 0.0 | 4 | DOMÈSTIC |
| SECCIO_CENSAL | object | 1.77 | 918 | 0801907090 |
| NUMEROSERIECONTADOR | object | 0.0 | 2802 | IBAJ44VHSIRRTASA |
| CONSUMO_REAL | float64 | 17.11 | 9375 | 0.0 |
| FECHA_HORA | datetime64[ns] | 0.0 | 11243406 | 2024-01-01 00:00:00 |

### meteo

- **Rows**: 1096
- **Columns**: 7
- **Overall missing (%)**: 0.0

| Column | Dtype | Missing (%) | #Unique | Example |
|---|---|---:|---:|---|
| year | int64 | 0.0 | 3 | 2022 |
| month | int64 | 0.0 | 12 | 1 |
| day | int64 | 0.0 | 31 | 1 |
| PPT | float64 | 0.0 | 97 | 0.0 |
| TX | float64 | 0.0 | 265 | 22.1 |
| TN | float64 | 0.0 | 242 | 14.9 |
| Data | datetime64[ns] | 0.0 | 1096 | 2022-01-01 00:00:00 |

### socio

- **Rows**: 444
- **Columns**: 6
- **Overall missing (%)**: 16.67

| Column | Dtype | Missing (%) | #Unique | Example |
|---|---|---:|---:|---|
| any | int64 | 0.0 | 1 | 2022 |
| municipi | object | 0.0 | 1 | Barcelona |
| barris de Barcelona | object | 0.0 | 74 | el Raval |
| concepte | object | 0.0 | 6 | població ocupada (%) |
| estat | float64 | 100.0 | 0 |  |
| valor | float64 | 0.0 | 303 | 57.5 |