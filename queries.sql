-- Count rows where SECCIO_CENSAL starts with 8019 in consum
-- SELECT COUNT(*) as count_rows_8019
-- FROM 'data/consum_telelectura_v2.parquet'
-- WHERE CAST(SECCIO_CENSAL AS VARCHAR) LIKE '8019%';

-- Count total number of rows
SELECT COUNT(*) as total_rows
FROM 'data/consum_telelectura_v2.parquet';
