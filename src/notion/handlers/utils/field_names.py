from json import dumps


class FieldNames:
    def __init__(
            self,
            task_name_field: dict,
            project_field_name: dict | None,
            worker_field_name: dict | None,
            deadline_field_name: dict | None
    ):
        self._fields = dict()

        self._fields["task_name_field"] = task_name_field
        self._fields["deadline_field_name"] = deadline_field_name
        self._fields["project_field_name"] = project_field_name
        self._fields["worker_field_name"] = worker_field_name

    def __getitem__(self, item):
        return self._fields[item]

    def dict(self):
        return self._fields

    def __json__(self, dumped=False):
        if dumped:
            return dumps(self._fields)

        return self._fields.copy()
