from pathlib import Path

# header/footer для всех страниц  
head_footer = {'head' : '''
    <html lang="ru">
    <head>
        <META CONTENT="text/html; charset=UTF-8; width=device-width; initial-scale=1.0">
        <title>DE Project</title>
        <link rel="stylesheet" type="text/css" href="/static/styles.css">
    </head>
    <body>
        <div class="app-container">    
            <nav class="warm-nav">
                <div class="owner-info">
                    <div class="logo">
                        <img src="/static/img/logo.png" alt="Logo" width="54" height="54">
                    </div>
                    <div class="owner-details">
                        <h3 class="owner-name">Романов Алексей</h3>
                        <p class="owner-subtitle">Программист</p>
                    </div>
                </div>
                <ul class="nav-links">
                    <li><a href="/" class="nav-button">Главная</a></li>
                    <li><a href="/vacancies" class="nav-button">Вакансии</a></li>
                    <li><a href="/about" class="nav-button">Обо мне </a></li>
                    <li><a href="/contacts" class="nav-button">Обратная связь</a></li>
                </ul>
            </nav>
               <main class="content-pages">
    ''',
        'footer' : '''
    </main>
    <footer class="warm-footer">
            <p>© 2025 Data Engineer Project</p>
        </footer>        
        <script src="/static/script.js"></script>
    </body>
    </html>
    '''
    }

# Ключевые навыки
k_s = [
    'Python','SQL','ETL','Linux', 'ClickHouse', 'Oracle Pl/SQL', 'CI/CD', 'Flask',
    'Английский — B1 — Средний','Docker','Apache Airflow', 'ELT', 'Bash', 'FastAPI',
    'DWH','Git','ORACLE','Airflow','API','REST API', 'PostgreSQL', 'СМЭВ', 'Parsing'
    ]

# Получаем html из templates и добавляем header/footer
def get_html_body(name: str) -> str:
    main_html = ''
    with open(Path(f'app/templates/{name}.html').resolve(), 'r', encoding='utf-8') as file:
        main_html = file.read()
    return head_footer['head'] + main_html + head_footer['footer']

# Генерируем html страницу с вакансиями
def get_vacancies_html(vacancies: list, key_skils: list) -> str:    
    html = head_footer['head'] +'<div class="page-content"><h3>Для отбора вакансий использовались ключевые навыки:</h3>'
    for key in key_skils:
        html += f'<div class="nav-button" style="line-height: 0.7;">{key}</div>'
    html += '<div class="scrollable-content" style="height: 60vh !important;">'
    for vacancy in vacancies:
        html += f'<div class="vac-container"><h2 style="color: #a77a09;">{vacancy[2]}</h2>Компания - <a href="{vacancy[5]}"'\
                f' target="_blank">{vacancy[4]}</a><br>Дата публикации - {vacancy[3]}<br><a href="https://hh.ru/vacancy/{vacancy[1]}" '\
                f'target="_blank">Head Hunter</a><br>{vacancy[0]} - навыков совпало<br>'
        # for skill in vacancy[7]:
        #         html += f'{skill}<br>'
        html += f'{vacancy[8][0]}<br><a href="/vacancy_id?id={vacancy[1]}">Описание</a></div>'
    return html + head_footer['footer']

# Получаем html страницу с описанием вакансии
def get_vacancy_html(vacancy: list, id: str) -> str:
     return f'{head_footer["head"]}<div class="page-content services-description">{vacancy[0][0]}<br><div class="scrollable-content">{vacancy[0][1]}'\
            f'<br><a href="https://hh.ru/vacancy/{id}" target="_blank">Откликнуться</a></div></div>{head_footer["footer"]}'

# Получаем html диаграммы с частотой повторяющихся клшючевых навыков по профессиям
def get_html_skill_frequency(db_skill_frequency: list) -> str:
    html = f'{head_footer["head"]}<section id="home"><div class="page-content"><h1>Частота встречаемости ключевых навыков по профессиям</h1><div class="scrollable-content">'
    for frequency in db_skill_frequency:
        profession = list(frequency.keys())[0]
        html += f'<h3>{profession}</h3><div style="align-items: center; display: inline-block; margin: 20px; width: 90%"><div class="profession">'
        percent = frequency[profession][0][1]/100
        for skil in frequency[profession]:
            html += f'<div class="frequency"><span>{skil[0]}</span><div style="flex: 1;"><div style="background-color: rgba(1, 54, 23, 0.514); width: {round(skil[1]/(percent),2)}%; height: 30px;"></div></div><span style="text-align: right;">{skil[1]}</span></div>'
        html += '</div></div>'
    return html + '</div></div>' + head_footer['footer']