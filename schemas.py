from pydantic import BaseModel
from typing import Optional, List

class UsarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True


class PedidoSchema(BaseModel):
    id_usuario: int

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str
    senha: str 

    class Config:
        from_attributes = True

class ItemPedidoSchema(BaseModel):
    quant: int
    sabor: str
    tamanho:str
    preco_unid: float
   
    class Config:
        from_attributes = True

class RespostaPedidoSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[ItemPedidoSchema]
    
    class Config:
        from_attributes = True