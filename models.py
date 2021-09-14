class Cliente:
    def __init__(self, id_cliente, nome,email,cep,senha,cpf,cidade,estado,endereco,data_nascimento,telefone):
        self.id = id_cliente
        self.nome = nome
        self.email = email
        self.cep = cep
        self.senha = senha
        self.cpf = cpf
        self.cidade = cidade
        self.estado = estado
        self.endereco = endereco
        self.data_nascimento = data_nascimento
        self.telefone = telefone

class Prestador:
    def __init__(self, id_prestador,nome,email,cep,senha,documento, tipo_documento,telefone,razao_social,cidade,estado,endereco, data_nascimento, imagem_perfil,descricao,apresentacao,foto_perfil):
        self.id_prestador = id_prestador
        self.nome = nome
        self.email = email
        self.cep = cep
        self.senha = senha
        self.documento = documento
        if tipo_documento == 'cpf':
            self.tipo_documento = 1
        else:
            self.tipo_documento = 2
        self.telefone = telefone
        self.razao_social = razao_social
        self.cidade = cidade
        self.estado = estado
        self.endereco = endereco
        self.data_nascimento = data_nascimento
        self.imagem_perfil = imagem_perfil
        self.descricao = descricao
        self.apresentacao = apresentacao
        self.tipos_prestador = []
        self.foto_perfil = foto_perfil

class TipoPrestador:
    def __init__(self,idtipo_prestador,descricao,icone) -> None:
        self.idtipo_prestador = idtipo_prestador
        self.descricao = descricao
        self.icone = icone

class Proposta:
    def __init__(self,id_proposta,data_proposta,cep,cidade,estado,endereco,horario_inicio,horario_fim,observacoes,data_criacao,valor,id_cliente, id_prestador):
        self.id_proposta = id_proposta