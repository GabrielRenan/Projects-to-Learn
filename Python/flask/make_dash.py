import json
import requests
import urllib
import plotly.offline as py
import plotly.graph_objs as go
import plotly.io as pio

class Dash:
    def __init__(self, url):
        with urllib.request.urlopen(url) as url:  
           self._data = json.loads(url.read().decode())

    def constroi_graph(self):
        x_novo = []
        y_novo = []
        x_atendimento = []
        y_atendimento = []
        x_aguardando = []
        y_aguardando = []
        count1, count2, count3 = 0,0,0      
        for x in range(len(self._data)):
            if ((self._data[x]["status"] == "Em atendimento")):
                x_atendimento.append(self._data[x]["status"])
                y_atendimento.append(self._data[x]["id"])
                count1+=1
            elif ((self._data[x]["status"] == "Novo")):
                x_novo.append(self._data[x]["status"])
                y_novo.append(self._data[x]["id"])
                count2+=1
            elif ((self._data[x]["status"] == "Aguardando")):
                x_aguardando.append(self._data[x]["status"])
                y_aguardando.append(self._data[x]["id"])
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
        layout = go.Layout(xaxis = {'title': 'Status chamados'},
                        yaxis = {'title': 'Número Ticket'},
                        barmode = 'stack')
        fig = go.Figure(data=_graph, layout=layout)
        return pio.write_html(fig, file='./templates/teste.html', auto_open=False)