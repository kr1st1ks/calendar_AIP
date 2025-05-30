import spacy
from collections import defaultdict

# Загружаем модель для русского языка
nlp = spacy.load("ru_core_news_sm")

class ScheduleManager:
    def __init__(self):
        self.schedule = defaultdict(list)

    def add_event(self, date, start_time, end_time, theme, color, description):
        self.schedule[date].append({
            'start_time': start_time,
            'end_time': end_time,
            'theme': theme,
            'color': color,
            'description': description
        })
        self.schedule[date].sort(key=lambda event: event['start_time'])

    def delete_event(self, date, start_time, end_time, theme, color, description):
        for event in self.schedule[date]:
            if (event['start_time'] == start_time and
                    event['end_time'] == end_time and
                    event['theme'] == theme and
                    event['color'] == color and
                    event['description'] == description):
                self.schedule[date].remove(event)
                break

    def edit_event(self, date, old_start_time, old_end_time, old_theme, old_color, old_description, new_start_time, new_end_time, new_theme, new_color, new_description):
        self.delete_event(date, old_start_time, old_end_time, old_theme, old_color, old_description)
        self.add_event(date, new_start_time, new_end_time, new_theme, new_color, new_description)

    def get_schedule(self, date=None):
        if date:
            return self.schedule.get(date, [])
        return self.schedule

    def lemmatize_text(self, text):
        # Обрабатываем текст с помощью spacy
        doc = nlp(text)
        # Возвращаем леммы (нормализованные формы) слов в тексте
        return ' '.join([token.lemma_ for token in doc])

    def search_events(self, search_term):
        filtered_schedule = defaultdict(list)
        # Лемматизируем поисковый запрос
        lemmatized_search_term = self.lemmatize_text(search_term.lower())

        for date, events in self.schedule.items():
            for event in events:
                # Лемматизируем описание и тему события
                lemmatized_theme = self.lemmatize_text(event['theme'].lower())
                lemmatized_description = self.lemmatize_text(event['description'].lower())
                # print(lemmatized_theme,lemmatized_description,lemmatized_search_term)

                # Ищем частичное совпадение с леммами
                if (lemmatized_search_term in lemmatized_theme or
                        lemmatized_search_term in lemmatized_description):
                    filtered_schedule[date].append(event)

        return filtered_schedule
