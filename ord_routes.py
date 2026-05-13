from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema, RespostaPedidoSchema
from models import Pedido, Usuario, Itens
from typing import List


ord_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

@ord_router.get("/")
async def pedidos():
    """
    1. ESSA É A ROTA PADRÃO DE PEDIDOS.
    2. TODAS AS ROTAS DE PEDIDOS PRECISAM DE AUTENTICAÇÃO.
    """
    return {"mensagem": "Você acessou a rota de pedidos"}
 
@ord_router.post("/pedido")
async def criar_pedido(
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    novo_pedido = Pedido(usuario=usuario.id)
    session.add(novo_pedido)
    session.commit()

    return {
        "mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"
    }


@ord_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    #usuario.admin == True
    #usuario.id = pedido.usuario
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="pedido inexistente :(")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Negado!, sem autonomia para fazer isto.")
    pedido.status = "CANCELADO"

    session.commit()
    return {"mensagem": f"Pedido → {pedido.id}, cancelado com sucesso",
            "pedido": pedido
            
            }

@ord_router.get("/lista")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if usuario.admin == False:
        raise HTTPException(status_code=401, detail="sem autorização para fazer essa operação.")
    else:
        pedidos = session.query(Pedido).all()
        return {"pedidos": pedidos}
    

@ord_router.post("/pedido/adcionar-item/{id_pedido}")
async def adcionar_item_pedido(
    id_pedido: int,
    item_pedido_schema: ItemPedidoSchema,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)):

    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="pedido inexistente")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="sem autorização para fazer essa operação")
    item_pedido = Itens(item_pedido_schema.quant, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unid, id_pedido)

    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }


@ord_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(
    id_item_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)):

    item_pedido = session.query(Itens).filter(Itens.id==id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()

    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item inexistente")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="sem autorização para fazer essa operação")

    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": "Item removido com sucesso",
        "quant_itens_pedido": len(pedido.itens),
        "pedido": pedido

    }

#Finalizar_Pedido
@ord_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="pedido inexistente :(")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Negado!, sem autonomia para fazer isto.")
    pedido.status = "FINALIZADO"

    session.commit()
    return {"mensagem": f"Pedido → {pedido.id}, finalizado com sucesso",
            "pedido": pedido
            }

#Visualizar_pedido
@ord_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="pedido inexistente :(")
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Negado!, sem autonomia para fazer isto.")
    
    return {
        "quant_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

#visualizar_todos_os_pedidos
@ord_router.get("/listar/pedidos-{id_usuario}", response_model=List[RespostaPedidoSchema])
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
        pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
        
        return pedidos
                
                


