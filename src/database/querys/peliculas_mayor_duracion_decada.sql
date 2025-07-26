WITH
    peliculas_con_ranking AS (
        SELECT
            FLOOR(anio / 10) * 10 AS decada,
            titulo,
            anio,
            duracion,
            ROW_NUMBER() OVER (
                PARTITION BY
                    FLOOR(anio / 10) * 10
                ORDER BY
                    duracion DESC
            ) AS rk
        FROM
            peliculas
    )
SELECT
    decada,
    titulo,
    anio,
    duracion
FROM
    peliculas_con_ranking
WHERE
    rk <= 5
ORDER BY
    decada,
    rk;