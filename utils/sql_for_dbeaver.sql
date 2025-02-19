ALTER TABLE de_project.vacancies DELETE WHERE id in (
SELECT id FROM de_project.vacancies
GROUP BY id
HAVING COUNT(id)>1
)

DROP TABLE IF EXISTS de_project.vacancies

SELECT * FROM system.mutations

SELECT COUNT(*) FROM de_project.vacancies -- должно быть 599

SELECT COUNT(*) FROM de_project.ids_from_req_profession 

SELECT * FROM de_project.ids_from_req_profession WHERE req_profession = 'python data backend'
ORDER BY id DESC

SELECT * FROM de_project.vacancies where id in (
select id from de_project.ids_from_req_profession WHERE 
req_profession = 'python data backend'
)



SELECT id FROM de_project.vacancies

SELECT * FROM de_project.vacancies WHERE id in (
SELECT id FROM de_project.ids_from_req_profession
GROUP BY id
HAVING COUNT(id)>1
)

SELECT id, name, company_name, , key_skills FROM de_project.vacancies
LIMIT 10

SELECT topK(10)(key_skills) FROM de_project.vacancies

SELECT
    element,
    COUNT(*) AS count
FROM
(
    SELECT arrayJoin(key_skills) AS element
    FROM de_project.vacancies
)
GROUP BY element
ORDER BY count DESC

SELECT 
length(arrayIntersect(key_skills, ['Python','SQL','ETL','Linux',
'Английский — B1 — Средний','Docker','Apache Airflow','DWH','Git',
'ORACLE','Airflow','API','REST API'])) AS intersect_count,
id, name, formatDateTime(publicationDate,'%d.%m.%Y'), company_visible_name,
company_site_url, area_name, description, key_skills ,translation
 FROM de_project.vacancies HAVING intersect_count>2
ORDER BY toDayOfYear(publicationDate) DESC, intersect_count DESC
LIMIT 50

SELECT * FROM de_project.vacancies WHERE has(key_skills,'МСФО')

                    SELECT 
                    length(arrayIntersect(key_skills,  ['Python','SQL','ETL','Linux',
'Английский — B1 — Средний','Docker','Apache Airflow','DWH','Git',
'ORACLE','Airflow','API','REST API'])) AS intersect_count,
                    id, name, formatDateTime(publicationDate,'%d.%m.%Y'), company_visible_name,
                    company_site_url, area_name, description, key_skills ,translation
                    FROM de_project.vacancies ORDER BY toDayOfYear(publicationDate) DESC,
                    intersect_count DESC LIMIT 50


--удаляем кривую загрузку
SELECT * FROM de_project.vacancies WHERE
id in (
                            SELECT id FROM de_project.ids_from_req_profession
                            WHERE req_profession = 'python data backend'
                            GROUP BY id
                            HAVING COUNT(id)=1
                            )


ALTER TABLE de_project.vacancies DELETE WHERE
id in (
                            SELECT id FROM de_project.ids_from_req_profession
                            WHERE req_profession = 'python data backend'
                            GROUP BY id
                            HAVING COUNT(id)=1
                            )

ALTER TABLE de_project.ids_from_req_profession DELETE WHERE 
req_profession = 'python data backend'

duarF101


select distinct req_profession from de_project.ids_from_req_profession

                        SELECT
                            element,
                            COUNT(1) AS count
                        FROM
                        (
                            SELECT arrayJoin(key_skills) AS element
                            FROM de_project.vacancies WHERE id IN
                              (SELECT id FROM de_project.ids_from_req_profession 
                              WHERE req_profession='data engineer')
                        )
                        GROUP BY element                        
                        ORDER BY count DESC LIMIT 50