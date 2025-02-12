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
        </div>
        <script src="/static/script.js"></script>
    </body>
    </html>
    '''
    }

def get_vacancies_html(vacancies: list, key_skils: list) -> str:    
    html = head_footer['head'] +'<div class="page-content"><h2>Для отбора вакансий использовались ключевые навыки:</h2>'
    for key in key_skils:
        html += f'<div class="nav-button">{key}</div>'
    html += '<div class="scrollable-content">'
    for vacancy in vacancies:
        html += f'<div class="vac-container"><h2 style="color: #edb217;">{vacancy[2]}</h2>Компания - <a href="{vacancy[5]}"'\
                f' target="_blank">{vacancy[4]}</a><br>Дата публикации - {vacancy[3]}<br><a href="https://hh.ru/vacancy/{vacancy[1]}" '\
                f'target="_blank">Head Hunter</a><br>{vacancy[0]} - навыков совпало<br>Навыки:<br>'
        for skill in vacancy[7]:
                html += f'{skill}<br>'
        html += f'{vacancy[8][0]}<br><a href="/vacancy_id?id={vacancy[1]}">Описание</a></div>'
    return html + '</div></div>' + head_footer['footer']

def get_vacancy_html(vacancy: list, id: str) -> str:
     return f'{head_footer["head"]}<div class="page-content services-description">{vacancy[0][0]}<br>{vacancy[0][1]}'\
            f'<br><a href="https://hh.ru/vacancy/{id}" target="_blank">Откликнуться</a></div>{head_footer["footer"]}'