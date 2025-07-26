-- desviacion estandar por año
create view desviacion_estandar_anio as
SELECT
    anio,
    COUNT(*) AS cantidad_peliculas,
    AVG(calificacion) AS promedio_calificacion,
    STDDEV_SAMP(calificacion) AS desviacion_estandar
FROM
    peliculas
GROUP BY
    anio
ORDER BY
    anio;
