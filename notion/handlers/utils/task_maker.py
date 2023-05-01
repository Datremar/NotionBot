class TaskMaker:
    def __new__(cls, name: str, worker_id: str | None, project_id: str | None, deadline: str) -> dict:
        request = {
            "Наименование задачи": {
                'id': 'title',
                'type': 'title',
                'title': [{'type': 'text', 'text': {'content': name, 'link': None},
                           'annotations': {'bold': False, 'italic': False, 'strikethrough': False, 'underline': False,
                                           'code': False, 'color': 'default'},
                           'plain_text': 'Тестирование новых продуктов', 'href': None}]
            },
            "Дата выполнения": {
                'id': 'yO_X',
                'type': 'date',
                'date': {'start': deadline, 'end': None, 'time_zone': None}
            }
        }

        if project_id is not None:
            request["🧩Проекты"] = {
                'id': 'rtdb', 'type': 'relation', 'relation': [{'id': project_id}],
                'has_more': False
            }
        if worker_id is not None:
            request["Ответственный"] = {
                'id': 'W%60c%5E',
                'type': 'relation',
                'relation': [{'id': worker_id}],
                'has_more': False
            }

        return request
