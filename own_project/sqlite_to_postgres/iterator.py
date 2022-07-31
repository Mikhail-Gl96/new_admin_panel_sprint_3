from typing import Dict, List, TypeVar

from utils import ConnectionSqlite, PipelineElement

T = TypeVar("T")


class Iterator:
    def __init__(self, connection: ConnectionSqlite):
        self.connection = connection

    @staticmethod
    def get_field_names_from_cursor(
            curs,
            fields_to_rename: Dict[str, str] = None
    ) -> List[str]:
        field_names = []

        for e in curs.description:
            temp_name = e[0]

            if fields_to_rename and temp_name in fields_to_rename:
                temp_name = fields_to_rename[temp_name]

            field_names.append(temp_name)

        return field_names

    def make_table_iterable(
            self,
            fields_to_rename: Dict[str, str],
            query: str
    ):
        curs = self.connection.cursor()
        curs.execute(query)

        field_names = self.get_field_names_from_cursor(
            curs=curs,
            fields_to_rename=fields_to_rename
        )

        while execute := curs.fetchone():
            yield {field_names[e]: execute[e] for e in range(len(execute))}


def iter_table_chunked(
        pipe_element: PipelineElement,
        iterator: Iterator,
        query: str,
        chunk_size: int = 50
):
    elements = []

    for row in iterator.make_table_iterable(
            fields_to_rename=pipe_element.fields_to_rename,
            query=query
    ):
        if pipe_element.skip_empty_fields and \
                set(pipe_element.skip_empty_fields) <= set(row.keys()):
            for field_name in pipe_element.skip_empty_fields:
                del row[field_name]

        element = pipe_element.model(**row)
        elements.append(element)

        if len(elements) >= chunk_size:
            yield elements
            elements.clear()

    yield elements
