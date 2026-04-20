from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from datetime import date as Date

class StatusEnum(str, Enum):
    '''
    Define os valores permitidos para o campo de status.
    '''
    CONCLUIDO = '✅ Concluído'
    INICIADO = '🚀 Iniciado'
    AGUARDANDO = '⏰ Aguardando'
    CANCELADO = '❌ Cancelado'

class Project(BaseModel):
    '''
    Modelo para um único projeto.
    '''
    idproject: str = Field(..., description="Código do projeto")
    name: str = Field(..., description="Nome do projeto")
    description: str = Field(..., description="Descrição do projeto")
    status: StatusEnum = Field(..., description="Status do projeto")

class Milestones(BaseModel):
    '''
    Modelo para os grupos dentro de um projeto.
    '''
    idmilestone: str = Field(..., description="Código do marco")
    name: str = Field(..., description="Nome do marco")
    status: StatusEnum = Field(..., description="Status do marco")
    sequence: int = Field(..., description="Sequência do marco")

class Action(BaseModel):
    '''
    Modelo para as ações, que podem ou não estar associadas a um grupo.
    '''
    idmilestone: Optional[str] = Field(None, description="Código do marco associado (opcional)")
    idaction: str = Field(..., description="Código da ação")
    name: str = Field(..., description="Nome da ação")
    status: StatusEnum = Field(..., description="Status da ação")
    sequence: int = Field(..., description="Sequência da ação")

class Issues(BaseModel):
    '''
    Modelo para as issues (problemas/tarefas).
    '''
    idissues: str = Field(..., description="Código da issue")
    description: str = Field(..., description="Descrição da issue")
    status: StatusEnum = Field(..., description="Status da issue")
    date: str = Field(..., description="Data da issue (formato YYYY-MM-DD)")
    sequence: int = Field(..., description="Sequência da issue")

class WorkLog(BaseModel):
    '''
    Modelo para os trabalhos (apontamentos de horas).
    '''
    idwork: str = Field(..., description="Código do trabalho")
    idaction: Optional[str] = Field(None, description="Código da ação associada")
    idissue: Optional[str] = Field(None, description="Código da issue associada")
    description: str =  Field(..., description="Descrição do trabalho")
    time: float = Field(..., description="Tempo em horas")
    date: str = Field(..., description="Data do trabalho (formato YYYY-MM-DD)")
    sequence: int = Field(..., description="Sequência do trabalho")




