def create_table_from_rows(rows):
    table_rows = ""
    for row in rows:
        table_row = "<tr>"
        for value in row.values():
            table_row += f"<td>{value}</td>"
        table_row += "</tr>"
        table_rows += table_row

    return table_rows


class HTMLGenerator:
    def __init__(self, s3_bucket_uri: str):
        self.s3_bucket_uri = s3_bucket_uri

    def generate_html(self, rows, current_time):
        raise NotImplementedError("Subclasses must implement the 'generate_html' method.")
