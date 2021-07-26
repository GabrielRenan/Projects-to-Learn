from flask import Flask, render_template
from make_dash import Dash
from make_tables import Tables
import time


app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'

@app.route('/')
def ola():
    url = "https://api.movidesk.com/public/v1/tickets?token=e9368c54-8ec6-4cb5-a311-1ef7ec4350cc&$select=id,subject,status,ownerTeam,slaResponseTime,slaSolutionTime,justification,urgency,lastActionDate,createdDate&$filter=createdDate%20gt%202021-01-01T00:00:00.00z%20and%20status%20ne%20%27Fechado%27%20and%20status%20ne%20%27Cancelado%27%20and%20status%20ne%20%27Resolvido%27%20and%20ownerTeam%20ne%20%27Monitoramento%20Nordeste%27%20and%20ownerTeam%20ne%20%27Suporte%20Nordeste%27%20and%20ownerTeam%20ne%20%27Suporte-N1%20Nordeste%27%20and%20ownerTeam%20ne%20%27Suporte-N2%20Nordeste%27%20and%20ownerTeam%20ne%20%27Suporte-N3%20Nordeste%27%20and%20ownerTeam%20ne%20%27SIEM%20Nordeste%27%20and%20ownerTeam%20ne%20%27SOC%20NTSec%27&$expand=owner,createdBy&$orderby=id%20desc&$top=1500"

    graph = Dash(url)
    graph.constroi_graph()
    
    tabela = Tables(url)
    table, ticket, status, cliente, responsa, cont = tabela.constroi_table()
    
    table_aguar, ticket_aguar, status_aguar, responsa_aguar, cont_aguar = tabela.controi_table_aguardando()
    
    table_urg, ticket_urg, status_urg, responsa_urg, urgencia, cont_urg = tabela.controi_table_urgency()
    
    tabela_fab, ticket_fab, status_fab, responsa_fab, just, cont_fab = tabela.controi_table_fab()
    while True:
        return render_template('lista.html', tabela=table, contador=cont,
                               id= ticket, status=status, cliente=cliente,
                               responsa=responsa, tabela_a=table_aguar,
                                id_a= ticket_aguar, status_a=status_aguar,
                                responsa_a=responsa_aguar, contador_a=cont_aguar,
                                tabela_u=table_urg,id_u= ticket_urg,
                                status_u=status_urg, urgencia=urgencia,
                                responsa_u=responsa_urg, contador_u=cont_urg,
                                tabela_f=tabela_fab,id_f= ticket_fab,
                                status_f=status_fab, fab=just,
                                responsa_f=responsa_fab, contador_f=cont_fab)
        
app.run(debug=True)
 