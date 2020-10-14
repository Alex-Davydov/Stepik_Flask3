import random

from flask import Flask, render_template, request, url_for, redirect

from db_controller import loader, db_manager
from helper_data import day_of_week, goals
from forms import BookingForm, RequestForm

TEACHERS_DATA = loader('teachers')

app = Flask(__name__)
app.secret_key = '123456789'


@app.route('/')
@app.route('/all/')
def main_view():
    if request.path == '/all/':
        return render_template('index.html', data=TEACHERS_DATA, goals=goals)
    else:
        return render_template('index.html', data=random.sample(TEACHERS_DATA, 6), goals=goals)


@app.route('/profiles/<int:teacher_id>/')
def profile_view(teacher_id):
    return render_template('profile.html', data=TEACHERS_DATA, id=teacher_id, day_of_week=day_of_week, goals=goals)


@app.route('/goals/<string:goal>/')
def goal_view(goal):
    return render_template('goal.html', data=TEACHERS_DATA, goal=goal, goals=goals)


@app.route('/booking/<int:teacher_id>/<string:day>/<int:hour>/')
def booking_view(teacher_id, day, hour):
    form = BookingForm()
    return render_template('booking.html', data=TEACHERS_DATA, day=day, hour=hour, day_of_week=day_of_week, form=form,
                           id=teacher_id)


@app.route('/booking_done/', methods=['POST', 'GET'])
def booking_done_view():
    form = BookingForm()
    day = form.clientWeekday.data
    time = form.clientTime.data
    teacher_id = form.clientTeacher.data
    if request.method == 'POST' and form.validate():
        name = form.name.data
        phone = form.phone.data
        # Create and update booking.json
        db_manager('booking', [{'name': name,
                                'phone': phone,
                                'teacher_id': teacher_id,
                                'weekDay': day,
                                'time': time}])
        # Timetable updating
        [teacher['free'][day].update({str(time) + ':00': False}) for teacher in TEACHERS_DATA if
         int(teacher['id']) == int(teacher_id)]
        return render_template('booking_done.html', day=day, hour=time, name=name,
                               phone=phone, day_of_week=day_of_week)
    else:
        return redirect(url_for('booking_view', data=TEACHERS_DATA,
                               day=day, hour=time, day_of_week=day_of_week, teacher_id=teacher_id, form=form))


@app.route('/request/')
def request_view():
    form = RequestForm()
    return render_template('request.html', form=form)


@app.route('/request_done/', methods=['POST'])
def request_done_view():
    form = RequestForm()
    if form.validate_on_submit():
        goal = form.goal.data
        time = form.time.data
        name = form.name.data
        phone = form.phone.data
        # Create and update request.json
        db_manager('request', [{'name': name,
                                'phone': phone,
                                'goal': goal,
                                'time': time}])
        return render_template('request_done.html', goals=goals, goal=goal, time=time, name=name, phone=phone)
    else:
        return redirect(url_for('request_view', form=form))


if __name__ == '__main__':
    app.run(debug=True)
