SELECT 
    table_name AS `Table Name`,
    table_rows AS `Number of Entries`
FROM 
    information_schema.tables
WHERE 
    table_schema = 'ieee_db';
