import sys
import csv

csvFile = open('data.csv', encoding = 'utf-8')
csvReader = csv.reader(csvFile)
csvData = list(csvReader)

with open('output.html', 'w') as html:
    html.write('''<!-- Latest compiled and minified CSS -->

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.8.1/bootstrap-table.min.css">

<!-- Latest compiled and minified CSS -->

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"> ''')
    html.write('<table data-toggle = "table" data-pagination = "true">\r')
    i = 0
    for row in csvData:
        if i == 0:
            html.write('\t<thead>\r\t\t<tr>\r')
            for col in row:
                html.write('\t\t\t<th data-sortable="true">' + col + '</th>\r')
            html.write('\t\t</tr>\r\t</thead>\r')
            html.write('\t<tbody>\r')
        else:
            html.write('\t\t<tr>\r')
            for col in row:
                html.write('\t\t\t<td>' + col + '</td>\r')
            html.write('\t\t</tr>\r')
        i += 1
    html.write('\t</tbody>\r')
    html.write('</table>\r')
    html.write('''
<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.0/jquery.min.js"></script>

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

<!-- Latest compiled and minified JavaScript -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.8.1/bootstrap-table.min.js"></script>
''')
