from flask import *
import xlrd
from xlutils.copy import copy


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    with open('index.html', 'r', encoding='utf-8') as file:
        html = file.read()
    return html


@app.route('/submit/', methods=['POST'])
def submit():
    name = request.form.get('name')
    number = int(request.form.get('id'))
    school = request.form.get('school')
    workbook = xlrd.open_workbook('submit.xls')
    sheet = workbook.sheet_by_index(0)
    i = int(sheet.cell(0, 0).value)
    for x in range(2, i):
        if number == int(sheet.cell(x, 1).value):
            if school == sheet.cell(x, 2).value:
                return str(int(sheet.cell(x, 3).value))
    new = copy(workbook)
    newsheet = new.get_sheet(0)
    newsheet.write(0, 0, i + 1)
    newsheet.write(i, 0, name)
    newsheet.write(i, 1, number)
    newsheet.write(i, 2, school)
    new.save('submit.xls')
    return str(int(sheet.cell(i, 3).value))


@app.route('/check/', methods=['GET'])
def check_get():
    with open('check.html', 'r', encoding='utf-8') as file:
        html = file.read()
    return html


@app.route('/check/', methods=['POST'])
def check_post():
    number = int(request.form.get('id'))
    workbook = xlrd.open_workbook('submit.xls')
    sheet = workbook.sheet_by_index(0)
    returndata = []
    for i in range(2, int(sheet.cell(0, 0).value)):
        if number == int(sheet.cell(i, 3).value):
            data = {
                'name': sheet.cell(i, 0).value,
                'id': int(sheet.cell(i, 1).value),
                'school': sheet.cell(i, 2).value
            }
            returndata.append(data)
    return str(returndata)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=14250, threaded=True)
