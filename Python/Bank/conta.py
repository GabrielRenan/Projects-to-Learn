class Conta:
    
     
    def __init__(self, numero, titular,saldo,limite):
        self.__numero  = numero
        self.__titular = titular
        self.__saldo   = saldo
        self.__limite  = limite

    def extrato(self):
        print("Saldo {} do titular {}".format(self.__saldo, self.__titular))

    def __pode_sacar(self, valor_para_sacar):
        limite_disponivel = self.__saldo + self.__limite
        return valor_para_sacar <= limite_disponivel

    def saca(self, valor):
        if (self.__pode_sacar(valor)):
            self.__saldo -= valor
        else:
            print('O valor {}R$ ultrapassou o limite.'.format(valor))

    def deposita(self, valor):
        self.__saldo += valor

    def transfere (self, valor, destino):
        self.saca(valor)
        destino.deposita(valor)
    @property
    def saldo(self):
        return self.__saldo

    @property
    def limite(self):
        return self.__limite
    @property
    def titular(self):
        return self.__titular

    @limite.setter
    def limite(self, limite):
        self.__limite = limite
    
    @staticmethod
    def codigo_banco():
        return {'BB': '001', 'Caixa': '104', 'Bradesco': '237'}