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

SELECT * FROM de_project.vacancies WHERE has(key_skills,'МСФО')

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

