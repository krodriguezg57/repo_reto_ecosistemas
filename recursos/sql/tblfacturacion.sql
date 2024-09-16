-- Crea la tabla 'tblfacturacion' si no existe ya en la base de datos.
-- Esta tabla se llena con los resultados de la consulta que sigue a continuación.
CREATE TABLE IF NOT EXISTS tblfacturacion AS
-- Crea una tabla temporal con varios pasos de procesamiento de datos.
WITH temp AS (
    -- Selecciona columnas específicas de la tabla 'temp_comercios_trx' con ciertas condiciones.
    SELECT 
        date_api_call,               -- Fecha en la que se realizó la llamada a la API.
        commerce_id,                 -- Identificador del comercio en la llamada a la API.
        ask_status,                  -- Estado de la solicitud en la llamada a la API.
        is_related,                  -- Indicador de si la llamada a la API está relacionada.
        commerce_nit,                -- NIT del comercio.
        commerce_name,               -- Nombre del comercio.
        commerce_status,             -- Estado del comercio.
        commerce_email               -- Correo electrónico del comercio.
    FROM   
        temp_comercios_trx           -- La tabla de origen es 'temp_comercios_trx'.
    WHERE 
        DATE(date_api_call) BETWEEN '2024-07-01' AND '2024-08-31'   -- Filtra las llamadas a la API dentro del rango de fechas especificado.
        AND commerce_status = 'Active'                               -- Solo incluye comercios activos.
), 
-- Calcula las estadísticas de solicitudes para cada comercio.
trx AS (
    SELECT
        commerce_nit,                -- NIT del comercio.
        commerce_name,               -- Nombre del comercio.
        commerce_email,              -- Correo electrónico del comercio.
        COUNT(CASE WHEN ask_status = 'Successful' THEN 1 END) AS successful_requests, -- Cuenta el número de solicitudes exitosas.
        COUNT(CASE WHEN ask_status = 'Unsuccessful' THEN 1 END) AS failed_requests    -- Cuenta el número de solicitudes fallidas.
    FROM
        temp                        -- Usa la tabla temporal 'temp'.
    GROUP BY
        commerce_nit                 -- Agrupa los resultados por el NIT del comercio.
), 
-- Calcula las comisiones basadas en las solicitudes exitosas y el NIT del comercio.
facturacion AS (
    SELECT
        commerce_nit,                -- NIT del comercio.
        commerce_name,               -- Nombre del comercio.
        commerce_email,              -- Correo electrónico del comercio.
        successful_requests,         -- Número de solicitudes exitosas.
        failed_requests,             -- Número de solicitudes fallidas.
        CASE
            WHEN commerce_nit = '445470636' THEN successful_requests * 300
            WHEN commerce_nit = '198818316' THEN successful_requests * 600
            WHEN commerce_nit = '919341007' THEN successful_requests * 300
            WHEN commerce_nit = '452680670' THEN
                CASE
                    WHEN successful_requests <= 10000 THEN successful_requests * 250
                    WHEN successful_requests <= 20000 THEN successful_requests * 200
                    ELSE successful_requests * 170
                END
            WHEN commerce_nit = '28960112' THEN
                CASE
                    WHEN successful_requests <= 22000 THEN successful_requests * 250
                    ELSE successful_requests * 130
                END
        END AS comisiones              -- Calcula la comisión según el NIT del comercio y el número de solicitudes exitosas.
    FROM
        trx                         -- Usa la tabla temporal 'trx'.
), 
-- Aplica descuentos a las comisiones y genera un índice.
descuentos AS (
    SELECT
        commerce_nit,                -- NIT del comercio.
        commerce_name,               -- Nombre del comercio.
        commerce_email,              -- Correo electrónico del comercio.
        successful_requests,         -- Número de solicitudes exitosas.
        failed_requests,             -- Número de solicitudes fallidas.
        comisiones,                  -- Comisión calculada.
        CASE
            WHEN commerce_nit = '28960112' AND failed_requests > 6000 THEN comisiones * 0.95
            WHEN commerce_nit = '919341007' AND failed_requests BETWEEN 2500 AND 4500 THEN comisiones * 0.95
            WHEN commerce_nit = '919341007' AND failed_requests > 4500 THEN comisiones * 0.92
            ELSE comisiones
        END AS comi_con_descuento,   -- Aplica descuentos a las comisiones según el NIT del comercio y el número de solicitudes fallidas.
    ROW_NUMBER() OVER (ORDER BY NULL) AS indice
    FROM 
        facturacion                  -- Usa la tabla temporal 'facturacion'.
)
-- Selecciona los datos finales y genera el ID de facturación y los montos finales.
SELECT
    printf('%s%02d', strftime('%Y%m%d', 'now'), indice) AS id_facturacion, -- Genera un ID de facturación basado en la fecha actual y el índice.
    CURRENT_DATE AS fecha_facturacion,        -- Fecha actual como fecha de facturación.
    commerce_nit,                             -- NIT del comercio.
    commerce_name,                            -- Nombre del comercio.
    commerce_email,                           -- Correo electrónico del comercio.
    successful_requests,                      -- Número de solicitudes exitosas.
    failed_requests,                          -- Número de solicitudes fallidas.
    comisiones,                               -- Comisión calculada.
    comi_con_descuento,                       -- Comisión con descuento aplicado.
    comi_con_descuento * 0.19 AS valor_cobrado_por_iva,  -- Calcula el valor del IVA basado en la comisión con descuento.
    comi_con_descuento + (comi_con_descuento * 0.19) AS total_facturado -- Calcula el total facturado sumando la comisión con descuento y el IVA.
FROM
    descuentos;                             -- Usa la tabla temporal 'descuentos'.
