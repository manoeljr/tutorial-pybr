from typing import List
from uuid import UUID
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from api_pedidos.esquema import Item, HealthCheckResponse, ErrorResponse
from api_pedidos.excecao import PedidoNaoEncontradoError, FalhaDeComunicacaoError
from http import HTTPStatus


app = FastAPI()


def recuperar_itens_por_pedido(identificacao_do_pedido: UUID) -> List[Item]:
    pass


@app.exception_handler(PedidoNaoEncontradoError)
def tratar_erro_pedido_nao_encontrado(request: Request, exc: PedidoNaoEncontradoError):
    return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "Pedido não encontrado"})


@app.get(
    "/healthcheck",
    tags=["healthcheck"],
    summary="Integridade do sistema",
    description="Checa se o servidor está online"
)
async def healthcheck():
    return HealthCheckResponse(status="ok")


@app.get(
    "/orders/{identificacao_do_pedido}/items",
    responses={
        HTTPStatus.NOT_FOUND: {
            "description": "Pedido não encontrado",
            "model": ErrorResponse,
        },
        HTTPStatus.BAD_GATEWAY: {
            "description": "Falha de comunicação com o servidor remoto",
            "model": ErrorResponse,
        }}, summary="Itens de um pedido", tags=["pedidos"],
    description="Retorna todos os itens de um determinado pedido", response_model=List[Item])
async def listar_itens(items: List[Item] = Depends(recuperar_itens_por_pedido)):
    return items


@app.exception_handler(FalhaDeComunicacaoError)
def tratar_erro_falha_de_comunicacao(request: Request, exc: FalhaDeComunicacaoError):
    return JSONResponse(
        status_code=HTTPStatus.BAD_GATEWAY,
        content={
            "message": "Falha de comunicação com o servidor remoto"
        }
    )
