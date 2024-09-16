-- Crea la tabla temporal 'temp_comercios_trx' si no existe ya en la base de datos.
-- Esta tabla se llena con los resultados de la consulta que sigue a continuación.

CREATE TABLE IF NOT EXISTS temp_comercios_trx AS
SELECT 
        -- Selecciona las siguientes columnas de la tabla 'apicall' (alias t1):
        t1.date_api_call,              -- Fecha en la que se realizó la llamada a la API.
        t1.commerce_id,                -- Identificador del comercio en la llamada a la API.
        t1.ask_status,                 -- Estado de la solicitud en la llamada a la API.
        t1.is_related,                 -- Indicador de si la llamada a la API está relacionada.
        
        -- Selecciona las siguientes columnas de la tabla 'commerce' (alias t2):
        t2.commerce_nit,               -- NIT del comercio (Número de Identificación Tributaria).
        t2.commerce_name,              -- Nombre del comercio.
        t2.commerce_status,            -- Estado del comercio.
        t2.commerce_email              -- Correo electrónico del comercio.
        
    FROM   
        -- Especifica la tabla 'apicall' con el alias 't1'.
        apicall AS t1
        
    -- Realiza una combinación (join) con la tabla 'commerce' usando el alias 't2'.
    INNER JOIN 
        commerce AS t2
        
    -- La condición de combinación es que el campo 'commerce_id' de ambas tablas debe coincidir.
    ON 
        trim(t1.commerce_id) = trim(t2.commerce_id);
        -- Utiliza la función trim para eliminar espacios en blanco antes de realizar la comparación.
