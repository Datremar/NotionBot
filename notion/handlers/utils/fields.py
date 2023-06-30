class NameField:
    def __new__(cls, field_name: str, task_name: str):
        return field_name, {
            'title': [
                {
                    'text': {
                        'content': task_name,
                    }
                }
            ]
        }


class ProjectField:
    def __new__(cls, field_name: str, project_id: str):
        return field_name, {
            'relation': [
                {
                    'id': project_id
                }
            ]
        }


class WorkerField:
    def __new__(cls, field_name: str, worker_id: str):
        return field_name, {
            'relation': [
                {
                    'id': worker_id
                }
            ]
        }


class DeadlineField:
    def __new__(cls, field_name: str, deadline: str):
        return field_name, {
            'date': {
                'start': deadline
            }
        }
