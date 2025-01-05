WITH InputArtefacto AS (
  -- Definir el artefacto que quieres buscar
  SELECT
    'Crimson Witch of Flames' AS set_name,
    'Pyro DMG Bonus' AS main_stat,
    ['Crit Rate', 'Crit DMG', 'HP%', 'Elemental Mastery'] AS sub_stats
)

SELECT 
  personajes.name AS personaje,
  artefact.name AS artefacto_set,
  artefact.slot AS slot_artefacto,
  artefact.main_stat AS main_stat_artefacto,
  artefact.sub_stats AS sub_stats_artefacto
FROM 
  `micros-chile.genshin.personajes_v2` AS personajes,
  UNNEST(personajes.artifacts) AS artefact,
  InputArtefacto
WHERE 
  artefact.name = InputArtefacto.set_name
  AND artefact.main_stat = InputArtefacto.main_stat
  AND ARRAY_LENGTH(
      ARRAY(
          SELECT sub_stat
          FROM UNNEST(InputArtefacto.sub_stats) AS sub_stat
          WHERE sub_stat IN UNNEST(artefact.sub_stats)
      )
  ) = ARRAY_LENGTH(InputArtefacto.sub_stats)
