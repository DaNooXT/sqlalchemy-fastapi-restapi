from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, func, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{BASE_DIR}/banco.db"
db = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


#declara a base 
Base = declarative_base()

#cria a tabela de usuarios 
class users (Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False, unique=True)
    senha = Column("senha", String)
    data_criacao = Column("data_criacao", DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __init__ (self, nome, senha, email):
        self.nome = nome 
        self.senha = senha
        self.email = email

#cria a tabela de produdtos
class products (Base):

    __tablename__ = "products"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    descricao = Column("descricao", String)
    preco = Column("preco",Float)
    estoque = Column("estoque", Integer)
    data_criacao = Column("data_criacao", DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __init__ (self, nome, descricao, preco):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco

#cria a tabla de pedidos 
class orders (Base):

    __tablename__ = "orders"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", ForeignKey("users.id"))
    data_pedido = Column("data_pedido", DateTime(timezone=True), server_default=func.now(), nullable=False)
    total = Column("total", Numeric(10,2))
    status = Column("status", String)

    def __init__ (self, user_id, status):
        self.user_id = user_id
        self.status = status

#cria atabel ade item do pedido 
class order_itens (Base):

    __tablename__ = "order_itens"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    order_id = Column("order_id", ForeignKey("orders.id"))
    product_id = Column("product_id" , ForeignKey("products.id"))
    quantidade = Column("quantidade", Integer)
    preco_unitario = Column("preco_unitario", Float)

    def __init__ (self, order_id, product_id, quantidade, preco_unitario):
        self.order_id = order_id
        self.product_id = product_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario