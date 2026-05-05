from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random as rd
import numpy as np
from typing import List

app = FastAPI(title="EPDS TS2 — Simulación Álbum Qatar 2022")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────
#  CÓDIGO ORIGINAL DEL NOTEBOOK (sin modificar)
# ──────────────────────────────────────────────

def crear_album(figus_total):
    """
    Crea un álbum nuevo, completamente vacío.

    Parámetros:
        figus_total (int): Cantidad total de figuritas únicas del álbum.

    Retorna:
        list: Vector de figus_total ceros (álbum vacío).
    """
    return [0] * figus_total


def comprar_paquete(figus_total, figus_paquete):
    """
    Simula la compra de un paquete de figuritas sin repetición (como garantiza Panini).

    Parámetros:
        figus_total   (int): Cantidad total de figuritas únicas del álbum.
        figus_paquete (int): Cantidad de figuritas por paquete.

    Retorna:
        list: Lista de figus_paquete enteros distintos en range(0, figus_total),
              que representan las figuritas obtenidas.
    """
    # rd.sample toma una muestra SIN reposición: garantía de no-repetición por paquete
    return rd.sample(range(0, figus_total), figus_paquete)


def pegar_figus(album, paquete):
    """
    Pega las figuritas del paquete en el álbum.

    Parámetros:
        album   (list): Vector del álbum (0 = faltante, 1 = pegada).
        paquete (list): Lista de figuritas obtenidas en el paquete.

    Retorna:
        list: El álbum actualizado con las nuevas figuritas marcadas con 1.
    """
    for figu in paquete:
        album[figu] = 1
    return album


def album_incompleto(album):
    """
    Indica si el álbum está incompleto.

    Parámetros:
        album (list): Vector del álbum (0 = faltante, 1 = pegada).

    Retorna:
        bool: True si falta al menos una figurita, False si el álbum está completo.
    """
    return 0 in album


def cuantos_paquetes(figus_total, figus_paquete):
    """
    Simula el llenado completo de un álbum y devuelve la cantidad de paquetes necesarios.

    Parámetros:
        figus_total   (int): Cantidad total de figuritas únicas del álbum.
        figus_paquete (int): Cantidad de figuritas por paquete (sin repetición interna).

    Retorna:
        int: Número de paquetes comprados para completar el álbum.
    """
    album = crear_album(figus_total)
    paquetes_comprados = 0

    while album_incompleto(album):
        paquete = comprar_paquete(figus_total, figus_paquete)
        album = pegar_figus(album, paquete)
        paquetes_comprados += 1

    return paquetes_comprados


def esperanza_teorica(n):
    return sum(n / (n - i + 1) for i in range(1, n + 1))


# ──────────────────────────────────────────────
#  ENDPOINTS
# ──────────────────────────────────────────────

class SimulacionResult(BaseModel):
    muestras: List[int]
    promedio: float
    mediana: float
    std: float
    minimo: int
    maximo: int
    valor_teorico: float
    error_relativo: float
    n: int
    figus_total: int
    figus_paquete: int


@app.get("/api/simular", response_model=SimulacionResult)
def simular(
    n: int = Query(default=100, ge=10, le=500, description="Cantidad de repeticiones"),
    figus_total: int = Query(default=860, ge=10, le=2000, description="Figuritas en el álbum"),
    figus_paquete: int = Query(default=5, ge=1, le=20, description="Figuritas por paquete"),
    seed: int = Query(default=42, description="Semilla aleatoria"),
):
    rd.seed(seed)
    muestras = [cuantos_paquetes(figus_total, figus_paquete) for _ in range(n)]

    promedio = float(np.mean(muestras))
    mediana  = float(np.median(muestras))
    std      = float(np.std(muestras))
    minimo   = int(np.min(muestras))
    maximo   = int(np.max(muestras))

    vt_figus   = esperanza_teorica(figus_total)
    vt_paquetes = vt_figus / figus_paquete
    error_rel  = abs(promedio - vt_paquetes) / vt_paquetes * 100

    return SimulacionResult(
        muestras=muestras,
        promedio=round(promedio, 2),
        mediana=round(mediana, 2),
        std=round(std, 2),
        minimo=minimo,
        maximo=maximo,
        valor_teorico=round(vt_paquetes, 2),
        error_relativo=round(error_rel, 2),
        n=n,
        figus_total=figus_total,
        figus_paquete=figus_paquete,
    )


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "EPDS-TS2-Simulacion"}
