
import json
import pandas as pd
from flask import Flask,render_template,request,redirect,url_for,session
from plotly import tools
import records,plotly
import plotly.graph_objs as go

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oh_so_secret'
def patient_detail(name):
    patient_details = records.patient_details(name)
    return patient_details
def vital(name):
    obs = records.vitals(name)
    observations = pd.DataFrame(obs)
    Description = observations['Description']
    if (len(Description) > 6):
        Description = observations['Description'].value_counts().head(6)
    else:
        Description =""
        return Description


    Description = pd.DataFrame(Description).reset_index()
    Description.columns = ['Parameter', 'Values']
    Required = Description['Parameter']
    lst = Required.values.tolist()
    observations_imp = observations[observations['Description'].isin(lst)]
    observations_imp['Value'] = pd.to_numeric(observations_imp['Value'].copy())
    pt = pd.pivot_table(observations_imp, index='Date', columns=['Description', 'Units'], values="Value")
    pt_transpose = pt.values.T
    X = pt.index
    trace = [None] * len(pt_transpose)
    for i in range(0, len(pt_transpose)):
        trace[i] = go.Scatter(x = tuple(X.tolist()), y= tuple(pt_transpose[i].tolist()))

    row = 2
    col = 3
    fig = tools.make_subplots(
        rows=row,
        cols=col,
        subplot_titles=(str(pt.columns[0]),str(pt.columns[1]),str(pt.columns[2]),str(pt.columns[3]),str(pt.columns[4]),str(pt.columns[5]))
    )
    val = 0
    for i in range(1, row + 1):

        for j in range(1, col + 1):
            fig.append_trace(trace[val], i, j)
            val += 1

    fig['layout'].update(title='Vitals')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def medications(name):
    medication = records.medications(name)
    return medication

def conditions (name):
    condition = records.conditions(name)
    return condition

def procedures (name):
    procedure = records.procedures(name)
    return procedure

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['patient_name'] = request.form.get('name')
    return render_template('home.html')


@app.route('/patientdetails/',methods=['GET', 'POST'])
def detail():
    if request.method == 'POST':
        session['patient_name'] = request.form.get('name')
    patient_name = session['patient_name']
    patient_details = patient_detail(patient_name)

    return render_template('Patient.html', patient_details=patient_details)



@app.route('/medicationdetails',methods=['GET', 'POST'])
def med ():
    if request.method == 'POST':
        session['patient_name'] = request.form.get('name')
    patient_name = session['patient_name']

    medication_details = medications(patient_name)

    return render_template ('Medications.html', medication_details = medication_details)

@app.route('/conditiondetails',methods=['GET', 'POST'])
def con ():
    if request.method == 'POST':
        session['patient_name'] = request.form.get('name')
    patient_name = session['patient_name']

    condition_details = conditions(patient_name)

    return render_template ('Conditions.html', condition_details = condition_details)


@app.route('/procedure', methods=['GET', 'POST'])
def procedure():
    if request.method == 'POST':
        session['patient_name'] = request.form.get('name')
    patient_name = session['patient_name']

    procedure_details = procedures(patient_name)

    return render_template('Procedures.html', procedure_details=procedure_details)

@app.route('/vitaldetails', methods=['GET', 'POST'])
def vital_details():
    if request.method == 'POST':
        session['patient_name'] = request.form.get('name')
    patient_name = session['patient_name']

    vital_details = vital(patient_name)

    return render_template('Vitals.html',vital_details=vital_details)




if __name__ == '__main__':
    app.run(debug=True, port=8090)
