# Опис: Файл маршрутів, які визначають логіку відображення сторінок
#      та обробки запитів користувачів
#      Використовується фреймворк Flask
from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Survey, Option

# Визначаємо маршрути
# Для кожного маршруту вказуємо шлях, за яким буде доступний маршрут
# Також вказуємо методи, які можуть викликати маршрут
# Для кожного маршруту вказуємо функцію, яка буде виконуватися при виклику маршруту
# Функція повертає відповідь сервера
# Відповідь сервера - це HTML сторінка, яку ми відображаємо користувачу
# Для відображення сторінки використовується шаблонізатор Jinja2
@app.route('/')
# Функція, яка виконується при виклику маршруту
def index():
    surveys = Survey.query.all()
    # Повертаємо сторінку зі списком опитувань
    return render_template('index.html', surveys=surveys)

# Для маршруту /survey/<int:survey_id> вказуємо параметр survey_id
# Цей параметр буде передаватися в функцію survey
# Цей параметр буде цілим числом
# Це означає, що в URL маршруту буде передаватися ціле число
@app.route('/survey/<int:survey_id>')
# Функція, яка виконується при виклику маршруту
def survey(survey_id):
    # Отримуємо опитування за id
    survey = Survey.query.get_or_404(survey_id)
    # Повертаємо сторінку з опитуванням
    return render_template('survey.html', survey=survey)

# Для маршруту /vote/<int:option_id> вказуємо параметр option_id
# Цей параметр буде передаватися в функцію vote
# Цей параметр буде цілим числом
@app.route('/vote', methods=['POST'])
def vote():
    option_id = request.form.get('option')
    if option_id:
        option = Option.query.get_or_404(option_id)
        option.votes += 1
        db.session.commit()
        return redirect(url_for('result', survey_id=option.survey_id))
    return redirect(url_for('index'))

# Для маршруту /result/<int:survey_id> вказуємо параметр survey_id
# Цей параметр буде передаватися в функцію result
# Цей параметр буде цілим числом
# Це означає, що в URL маршруту буде передаватися ціле число
@app.route('/result/<int:survey_id>')
# Функція, яка виконується при виклику маршруту
# Функція відображає сторінку з результатами опитування
def result(survey_id):
    # Отримуємо опитування за id
    survey = Survey.query.get_or_404(survey_id)
    # Повертаємо сторінку з результатами опитування
    return render_template('result.html', survey=survey)