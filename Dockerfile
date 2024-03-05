FROM python:3.11.7

# Создается рабочая директория
WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копируется туда файл, Устанавливаются библиотеки из файла
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# копируется сам проект
COPY . /code/

# Команда для запуска приложения Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



