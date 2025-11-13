-- Check null values in each column of consum
SELECT 
    'consum' as dataset,
    'POLIZA_SUMINISTRO' as column_name,
    COUNT(*) - COUNT(POLIZA_SUMINISTRO) as null_count,
    COUNT(*) as total_rows,
    ROUND(100.0 * (COUNT(*) - COUNT(POLIZA_SUMINISTRO)) / COUNT(*), 2) as null_percentage
FROM 'data/consum_telelectura_v2.parquet'
UNION ALL
SELECT 'consum', 'FECHA', COUNT(*) - COUNT(FECHA), COUNT(*), ROUND(100.0 * (COUNT(*) - COUNT(FECHA)) / COUNT(*), 2)
FROM 'data/consum_telelectura_v2.parquet'
UNION ALL
SELECT 'consum', 'CONSUMO_REAL', COUNT(*) - COUNT(CONSUMO_REAL), COUNT(*), ROUND(100.0 * (COUNT(*) - COUNT(CONSUMO_REAL)) / COUNT(*), 2)
FROM 'data/consum_telelectura_v2.parquet'
UNION ALL
SELECT 'consum', 'SECCIO_CENSAL', COUNT(*) - COUNT(SECCIO_CENSAL), COUNT(*), ROUND(100.0 * (COUNT(*) - COUNT(SECCIO_CENSAL)) / COUNT(*), 2)
FROM 'data/consum_telelectura_v2.parquet'
UNION ALL
SELECT 'consum', 'US_AIGUA_GEST', COUNT(*) - COUNT(US_AIGUA_GEST), COUNT(*), ROUND(100.0 * (COUNT(*) - COUNT(US_AIGUA_GEST)) / COUNT(*), 2)
FROM 'data/consum_telelectura_v2.parquet'
UNION ALL
SELECT 'consum', 'DATA_INST_COMP', COUNT(*) - COUNT(DATA_INST_COMP), COUNT(*), ROUND(100.0 * (COUNT(*) - COUNT(DATA_INST_COMP)) / COUNT(*), 2)
FROM 'data/consum_telelectura_v2.parquet'
UNION ALL
-- Check null values in each column of fuites
SELECT 'fuites', 'POLISSA_SUBM', COUNT(*) - COUNT(POLISSA_SUBM), COUNT(*), ROUND(100.0 * (COUNT(*) - COUNT(POLISSA_SUBM)) / COUNT(*), 2)
FROM 'data/consum_avisos_missatges_v2.parquet'
UNION ALL
SELECT 'fuites', 'DATA_INI_FACT', COUNT(*) - COUNT(DATA_INI_FACT), COUNT(*), ROUND(100.0 * (COUNT(*) - COUNT(DATA_INI_FACT)) / COUNT(*), 2)
FROM 'data/consum_avisos_missatges_v2.parquet'
UNION ALL
SELECT 'fuites', 'DATA_FIN_FACT', COUNT(*) - COUNT(DATA_FIN_FACT), COUNT(*), ROUND(100.0 * (COUNT(*) - COUNT(DATA_FIN_FACT)) / COUNT(*), 2)
FROM 'data/consum_avisos_missatges_v2.parquet'
UNION ALL
SELECT 'fuites', 'FECHA_HORA', COUNT(*) - COUNT(FECHA_HORA), COUNT(*), ROUND(100.0 * (COUNT(*) - COUNT(FECHA_HORA)) / COUNT(*), 2)
FROM 'data/consum_avisos_missatges_v2.parquet'
UNION ALL
SELECT 'fuites', 'SECCIO_CENSAL', COUNT(*) - COUNT(SECCIO_CENSAL), COUNT(*), ROUND(100.0 * (COUNT(*) - COUNT(SECCIO_CENSAL)) / COUNT(*), 2)
FROM 'data/consum_avisos_missatges_v2.parquet'
UNION ALL
SELECT 'fuites', 'CONSUMO_REAL', COUNT(*) - COUNT(CONSUMO_REAL), COUNT(*), ROUND(100.0 * (COUNT(*) - COUNT(CONSUMO_REAL)) / COUNT(*), 2)
FROM 'data/consum_avisos_missatges_v2.parquet'
ORDER BY dataset, column_name;
