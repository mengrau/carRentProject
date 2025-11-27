from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.config import get_db
from entities import Cliente, Vehiculo, Contrato
from auth.deps import get_current_user

router = APIRouter(
    prefix="/dashboard", tags=["Dashboard"], dependencies=[Depends(get_current_user)]
)


@router.get("/counts")
def get_counts(db: Session = Depends(get_db)):
    total_clientes = db.query(Cliente).count()
    total_vehiculos = db.query(Vehiculo).count()
    total_contratos = db.query(Contrato).count()
    return {
        "clientes": total_clientes,
        "vehiculos": total_vehiculos,
        "contratos": total_contratos,
    }
