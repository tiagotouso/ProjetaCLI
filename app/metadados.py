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
    cdproject: str
    name: str
    description: str
    status: StatusEnum

class Milestones(BaseModel):
    '''
    Modelo para os grupos dentro de um projeto.
    '''
    cdmilestone: str
    name: str
    status: StatusEnum

class Action(BaseModel):
    '''
    Modelo para as ações, que podem ou não estar associadas a um grupo.
    '''
    cdmilestone: Optional[str] = None
    cdaction: str
    name: str
    status: StatusEnum

class Issues(BaseModel):
    '''
    Modelo para as issues (problemas/tarefas).
    '''
    cdissues: str
    description: str
    status: StatusEnum
    date: str

class WorkLog(BaseModel):
    '''
    Modelo para os trabalhos (apontamentos de horas).
    '''
    code: str
    description: str
    time: str
    date: str

