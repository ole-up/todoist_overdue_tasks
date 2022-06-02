
BODY_START = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Просроченные задачи</title>
    <style type="text/css">
        table {
            border: 1px solid grey;
            }
        th {
            border: 1px solid grey;
            }
        td {
            border: 1px solid grey;
            }
  </style>
</head>
<body>
<h1>Список просроченных задач</h1>
<br>
<hr>
<br>
"""

BODY_END = """</body>
</html>
"""
TABLE_HEADER = """<table>
<thead>
<tr><th style="text-align: center;">Задача</th><th>Срок выполнения</th><th>Приоритет</th><th>Ссылка</th></tr>
</thead>
<tbody>
"""
TABEL_END_TAG = """</tbody>
</table>
"""
