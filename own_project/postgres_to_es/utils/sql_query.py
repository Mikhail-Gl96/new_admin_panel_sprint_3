all_data_query = """
        SELECT fw.id,
        fw.rating AS imdb_rating,
        ARRAY_AGG(DISTINCT g.name) AS genre,
        fw.title,
        fw.description,
        ARRAY_AGG(DISTINCT p.full_name)
        FILTER(WHERE pfw.role = 'director') AS director,
        ARRAY_AGG(DISTINCT p.full_name)
        FILTER(WHERE pfw.role = 'actor') AS actors_names,
        ARRAY_AGG(DISTINCT p.full_name)
        FILTER(WHERE pfw.role = 'writer') AS writers_names,
        JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER(WHERE pfw.role = 'actor') AS actors,
        JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
        FILTER(WHERE pfw.role = 'writer') AS writers
        FROM film_work fw
        LEFT OUTER JOIN genre_film_work gfw ON (fw.id = gfw.film_work_id)
        LEFT OUTER JOIN genre g ON (gfw.genre_id = g.id)
        LEFT OUTER JOIN person_film_work pfw ON (fw.id = pfw.film_work_id)
        LEFT OUTER JOIN person p ON (pfw.person_id = p.id)
        WHERE GREATEST(fw.modified, p.modified, g.modified) > '%s'
        GROUP BY fw.id;
        """
