class Cliente:
    def __init__(self, nome,email,cep,senha,cpf,cidade,estado,endereco):
        self.nome = nome
        self.email = email
        self.cep = cep
        self.senha = senha
        self.cpf = cpf
        self.cidade = cidade
        self.estado = estado
        self.endereco = endereco

class Prestador:
    def __init__(self, nome,email,cep,senha,cpf,cnpj,telefone,razao_social,cidade,estado,endereco):
        self.nome = nome
        self.email = email
        self.cep = cep
        self.senha = senha
        self.cpf = cpf
        self.cnpj = cnpj
        self.telefone = telefone
        self.razao_social = razao_social
        self.cidade = cidade
        self.estado = estado
        self.endereco = endereco

class Proposta:
    def __init__(self,id_proposta,data_proposta,cep,cidade,estado,endereco,horario_inicio,horario_fim,observacoes,data_criacao,valor,id_cliente, id_prestador):
        self.id_proposta = id_proposta