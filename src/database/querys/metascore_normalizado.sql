SELECT
    titulo,
    anio,
    calificacion,
    metascore,
    ROUND(metascore / 10, 2) AS metascore_normalizado,
    ROUND(
        ABS(calificacion - (metascore / 10)) / calificacion * 100,
        2
    ) AS diferencia_porcentual
FROM
    peliculas
WHERE
    calificacion IS NOT NULL
    AND metascore IS NOT NULL
    AND ABS(calificacion - (metascore / 10)) / calificacion > 0.20
ORDER BY
    diferencia_porcentual DESC;
