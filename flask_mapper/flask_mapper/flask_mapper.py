from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from sheets import Sheet
from local_settings import II_SHEET_ID, II_SHEET_RANGE

app = Flask(__name__)
app.config.from_object(__name__)

innovating_instruction = Sheet(
    II_SHEET_ID,
    II_SHEET_RANGE)


@app.route('/')
def hello_world():
    return render_template('map.html',
                           locations=innovating_instruction.get_locations())
