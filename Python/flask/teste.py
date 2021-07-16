from flask import Flask, render_template
import json
import subprocess
import requests
import urllib
from datetime import datetime as dt
from datetime import timedelta
import datetime
from dateutil.relativedelta import relativedelta
from tabulate import tabulate
import plotly.offline as py
import plotly.graph_objs as go
import plotly.io as pio
from tabulate import tabulate
import io
import base64

def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)

    return base64.b64encode(img.getvalue())

app = Flask(__name__)

def elapsed_interval(start,end):
    elapsed = end - start
    min,secs=divmod(elapsed.days * 86400 + elapsed.seconds, 60)
    hour, minutes = divmod(min, 60)
    return '%.2dh%.2dmin%.2ds' % (abs(hour),abs(minutes),abs(secs))

@app.route('/graph')
def ola():
    with urllib.request.urlopen("https://api.movidesk.com/public/v1/tickets?token=&$select=id,subject,status,justification,lastActionDate,createdDate&$filter=createdDate%20gt%202021-01-01T00:00:00.00z&$expand=owner,createdBy&$orderby=id%20desc&$top=100") as url:  
        data = json.loads(url.read().decode())
    x_novo = []
    y_novo = []
    x_atendimento = []
    y_atendimento = []
    x_aguardando = []
    y_aguardando = []
    count1, count2, count3 = 0,0,0      
    for x in range(len(data)):
        if ((data[x]["status"] == "Em atendimento") and (data[x]["createdBy"]["businessName"] != "SOC-NTSec-CLIENT")):
            x_atendimento.append(data[x]["status"])
            y_atendimento.append(data[x]["id"])
            count1+=1
        elif ((data[x]["status"] == "Novo") and (data[x]["createdBy"]["businessName"] != "SOC-NTSec-CLIENT")):
            x_novo.append(data[x]["status"])
            y_novo.append(data[x]["id"])
            count2+=1
        elif ((data[x]["status"] == "Aguardando") and (data[x]["createdBy"]["businessName"] != "SOC-NTSec-CLIENT")):
            x_aguardando.append(data[x]["status"])
            y_aguardando.append(data[x]["id"])
            count3+=1

    py.init_notebook_mode(connected=True)
    #so marcadores
    trace_novo = go.Bar(x = x_novo,
                y = y_novo,
                name = f'Novos: {count2}',
                marker = {'color': '#009F1B'})
    trace_atendi = go.Bar(x = x_atendimento,
                y = y_atendimento,
                name = f'Em Atendimento: {count1}',
                marker = {'color': '#42D40B'})
    trace_aguard = go.Bar(x = x_aguardando,
                y = y_aguardando,
                name = f'Aguardando: {count3}',
                marker = {'color': '#46FF00'})

    _graph = [trace_novo, trace_atendi, trace_aguard]
    layout = go.Layout(title = 'Grafico de barras chamados Ntsec',
                    xaxis = {'title': 'Status chamados'},
                    yaxis = {'title': 'Número Ticket'},
                    barmode = 'stack')
    fig = go.Figure(data=_graph, layout=layout)
    pio.write_html(fig,file='./templates/teste.html', auto_open=False)
    return render_template('dashboard.html')
    
app.run()
 