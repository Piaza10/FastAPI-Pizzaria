from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship



#criação do banco//conexão
db = create_engine("sqlite:///meu_banco.db")

#cria a base do banco de dados
Base = declarative_base()

#cria as classes/tabelas do banco de dados
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    __tablename__ = "pedidos"

    # status_pedidos = (
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO")
    # )
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) #Pedente, Cancelado, Finalizado
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    itens = relationship("Itens", cascade="all, delete")

    def __init__(self,usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco

    def calcular_preco(self):
        #percorrer todos os itens do pedido
        #somar todos os precos de todos os itens dos pedidos
        #editar no campo "preco" o valor final do preco do pedido
        self.preco = sum(item.preco_unid * item.quant for item in self.itens)

class Itens(Base):
    __tablename__ = "itens"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quant =  Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unid = Column("preco_unidade", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))
    

    def __init__(self, quant, sabor, tamanho, preco_unid, pedido):
        self.quant = quant
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unid = preco_unid
        self.pedido = pedido


#executa a criação dos metadados(cria_efetivamente)

