import json
from datetime import datetime as dt
from datetime import timedelta
import datetime
from dateutil.relativedelta import relativedelta
import requests
import urllib

def elapsed_interval(start,end):
    elapsed = end - start
    min,secs=divmod(elapsed.days * 86400 + elapsed.seconds, 60)
    hour, minutes = divmod(min, 60)
    return '%.2d:%.2d:%.2d' % (abs(hour),abs(minutes),abs(secs))

class Tables:
    def __init__(self, url):
        with urllib.request.urlopen(url) as url:  
            self._data = json.loads(url.read().decode())

    
    def constroi_table(self):
        ticket = []
        cliente = []
        responsa = []
        status = []
        cont = 0
        tabela = []
        for x in range(len(self._data)):
            if ((self._data[x]["status"] == "Em atendimento") or (self._data[x]["status"] == "Novo")):
                horas = self._data[x]["createdDate"]
                horasacao = self._data[x]["lastActionDate"]
                acaba_hora = horas.find('.')
                datetim = dt.strptime(horas[:acaba_hora],"%Y-%m-%dT%H:%M:%S")
                datetim2 = dt.strptime(horasacao[:acaba_hora],"%Y-%m-%dT%H:%M:%S")
                datetim2 = datetim2 - timedelta(hours=3)
                datetim = datetim - timedelta(hours=3)
                hora_agora = dt.now()
                espera = elapsed_interval(datetim2, hora_agora)
                dia = datetim.strftime("%d/%m/%Y")
                dia2 = datetim2.strftime("%d/%m/%Y")
                horas = datetim.strftime("%H:%M:%S")
                ticket.append(json.dumps(self._data[x]["id"]))
                status.append(self._data[x]["status"])
                cliente.append(self._data[x]["createdBy"]["businessName"])
                responsa.append(self._data[x]["owner"]["businessName"])
                acha_dp = espera.find(':')
                esp_h = int(espera[:acha_dp])
                if (self._data[x]["slaResponseTime"] !=0):
                    falta_sla_h = self._data[x]["slaResponseTime"] - esp_h - 1
                    tabela.append({'dia':dia,'h':esp_h,
                                    'espera':espera,
                                    'falta': falta_sla_h})
                    cont+=1
                else:
                    tabela.append({'dia':dia,'h':esp_h,
                                    'espera':espera,
                                    'falta': 00})
                    cont+=1
        return tabela, ticket, status, cliente, responsa, cont

    def controi_table_aguardando(self):
        ticket_aguar = []
        responsa_aguar = []
        status_aguar = []
        cont_aguar = 0
        tabela_aguar = []
        for j in range(len(self._data)):
            if ((self._data[j]["status"] == "Aguardando") and (self._data[j]["slaSolutionTime"] != 0) ):
                horas = self._data[j]["createdDate"]
                acaba_hora = horas.find('.')
                datetim = dt.strptime(horas[:acaba_hora],"%Y-%m-%dT%H:%M:%S")
                datetim = datetim - timedelta(hours=3)
                hora_agora = dt.now()
                espera = elapsed_interval(datetim, hora_agora)
                dia = datetim.strftime("%d/%m/%Y")
                ticket_aguar.append(json.dumps(self._data[j]["id"]))
                status_aguar.append(self._data[j]["status"])
                responsa_aguar.append(self._data[j]["owner"]["businessName"])
                acha_dp=espera.find(':')
                if ((self._data[j]["slaSolutionTime"] != 0)):
                    esp_h = int(espera[:acha_dp])
                    esp_m = int(espera[acha_dp+1:acha_dp+3])
                    falta_sla_h = abs(self._data[j]["slaSolutionTime"] - esp_h - 1)
                    falta_sla_m = 60 - esp_m
                    tabela_aguar.append({'dia':dia,'falta': falta_sla_h,'falta_m': falta_sla_m})
                    cont_aguar+=1
                else:
                    tabela_aguar.append({'dia':dia,'falta': 00,'falta_m': 00})
                    cont_aguar+=1
                
        return tabela_aguar, ticket_aguar, status_aguar, responsa_aguar, cont_aguar
    
    def controi_table_urgency(self):
        ticket_urg = []
        responsa_urg = []
        status_urg = []
        urgencia = []
        cont_urg = 0
        tabela_urg = []
        for k in range(len(self._data)-1):
            if ("Alta" in self._data[k+1]["urgency"]) or ("Crítico" in self._data[k+1]["urgency"]):
                horas = self._data[k+1]["createdDate"]
                acaba_hora = horas.find('.')
                datetim = dt.strptime(horas[:acaba_hora],"%Y-%m-%dT%H:%M:%S")
                datetim = datetim - timedelta(hours=3)
                hora_agora = dt.now()
                espera = elapsed_interval(datetim, hora_agora)
                dia = datetim.strftime("%d/%m/%Y")
                ticket_urg.append(json.dumps(self._data[k+1]["id"]))
                status_urg.append(self._data[k+1]["status"])
                responsa_urg.append(self._data[k+1]["owner"]["businessName"])
                urgencia.append(self._data[k+1]["urgency"])
                acha_dp=espera.find(':')
                if (self._data[k+1]["slaSolutionTime"] != 0):
                    esp_h = int(espera[:acha_dp])
                    esp_m = int(espera[acha_dp+1:acha_dp+3])
                    falta_sla_h = abs(self._data[k+1]["slaSolutionTime"] - esp_h - 1)
                    falta_sla_m = 60 - esp_m
                    tabela_urg.append({'dia':dia,'falta': falta_sla_h,'falta_m': falta_sla_m})
                    cont_urg+=1
                else:
                    tabela_urg.append({'dia':dia,'falta': 00,'falta_m': 00})
                    cont_urg+=1
        return tabela_urg, ticket_urg, status_urg, responsa_urg, urgencia, cont_urg

    def controi_table_fab(self):
        ticket_fab = []
        responsa_fab = []
        status_fab = []
        just = []
        cont_fab = 0
        j=0
        tabela_fab = []
        for j in range(len(self._data)):
            if ((self._data[j]["justification"] == "Retorno do fabricante")):
                horas = self._data[j]["createdDate"]
                horasacao = self._data[j]["lastActionDate"]
                acaba_hora = horas.find('.')
                datetim = dt.strptime(horas[:acaba_hora],"%Y-%m-%dT%H:%M:%S")
                datetim2 = dt.strptime(horasacao[:acaba_hora],"%Y-%m-%dT%H:%M:%S")
                datetim = datetim - timedelta(hours=3)
                datetim2 = datetim2 - timedelta(hours=3)
                hora_agora = dt.now()
                espera = elapsed_interval(datetim, hora_agora)
                espera_2 = elapsed_interval(datetim2, hora_agora)
                dia = datetim.strftime("%d/%m/%Y")
                ticket_fab.append(json.dumps(self._data[j]["id"]))
                status_fab.append(self._data[j]["status"])
                responsa_fab.append(self._data[j]["owner"]["businessName"])
                just.append(self._data[j]["justification"])
                acha_dp=espera.find(':')
                if ((self._data[j]["slaSolutionTime"] != 0)):
                    esp_h = int(espera[:acha_dp])
                    esp_m = int(espera[acha_dp+1:acha_dp+3])
                    falta_sla_h = abs(self._data[j]["slaSolutionTime"] - esp_h - 1)
                    falta_sla_m = 60 - esp_m
                    tabela_fab.append({'dia':dia,'esp_h':espera_2 ,'falta': falta_sla_h,
                                       'falta_m': falta_sla_m})
                    cont_fab+=1
                else:
                    tabela_fab.append({'dia':dia,'esp_h':espera_2 ,'falta': 00,
                                       'falta_m': 00})
                    cont_fab+=1
                
        return tabela_fab, ticket_fab, status_fab, responsa_fab, just, cont_fab