from collections import defaultdict

class ScheduleManager:
    def __init__(self):
        self.schedule = defaultdict(list)

    def add_event(self, date, start_time, end_time, theme, description):
        self.schedule[date].append({
            'start_time': start_time,
            'end_time': end_time,
            'theme': theme,
            'description': description
        })
        self.schedule[date].sort(key=lambda event: event['start_time'])

    def delete_event(self, date, start_time, end_time, theme, description):
        for event in self.schedule[date]:
            if (event['start_time'] == start_time and
                    event['end_time'] == end_time and
                    event['theme'] == theme and
                    event['description'] == description):
                self.schedule[date].remove(event)
                break

    def edit_event(self, date, old_start_time, old_end_time, old_theme, old_description, new_start_time, new_end_time, new_theme, new_description):
        self.delete_event(date, old_start_time, old_end_time, old_theme, old_description)
        self.add_event(date, new_start_time, new_end_time, new_theme, new_description)

    def get_schedule(self, date=None):
        if date:
            return self.schedule.get(date, [])
        return self.schedule

    def search_events(self, search_term):
        filtered_schedule = defaultdict(list)
        for date, events in self.schedule.items():
            for event in events:
                if (search_term in event['theme'].lower() or
                        search_term in event['description'].lower()):
                    filtered_schedule[date].append(event)
        return filtered_schedule