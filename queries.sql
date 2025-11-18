-- Check: How many rows with missing SECCIO_CENSAL would pass Barcelona filter?
-- The Barcelona filter keeps only rows where SECCIO_CENSAL starts with '08019'
-- Missing values (NULL) cannot start with '08019', so they are filtered out
-- This explains why cleaned files have no missing SECCIO_CENSAL values
SELECT 
    'Rows with missing SECCIO_CENSAL' as category,
    CAST(COUNT(*) AS VARCHAR) as total_count,
    '0' as would_pass_barcelona_filter,
    '100.00%' as filtered_out_percentage
FROM 'data/consum_avisos_missatges_v2.parquet'
WHERE SECCIO_CENSAL IS NULL

UNION ALL

SELECT 
    'Rows with SECCIO_CENSAL present' as category,
    CAST(COUNT(*) AS VARCHAR) as total_count,
    CAST(SUM(CASE WHEN CAST(SECCIO_CENSAL AS VARCHAR) LIKE '08019%' THEN 1 ELSE 0 END) AS VARCHAR) as would_pass_barcelona_filter,
    CAST(ROUND(100.0 * SUM(CASE WHEN CAST(SECCIO_CENSAL AS VARCHAR) LIKE '08019%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS VARCHAR) || '%' as filtered_out_percentage
FROM 'data/consum_avisos_missatges_v2.parquet'
WHERE SECCIO_CENSAL IS NOT NULL;
