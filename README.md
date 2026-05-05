# EPDS TS2 — Simulación Álbum Qatar 2022

**Grupo:** EPDS_TS2_1D_G5: C.Fuentes, M.Salinas, S.Sanchez, C.Rodas, M.Escurra.
**Cátedra:** Estadística y Probabilidades para el Desarrollo de Software

Aplicación web interactiva que ejecuta el código Python original del Trabajo de Simulación 2 (Coupon Collector's Problem) y visualiza los resultados en tiempo real.

---

## Estructura del proyecto

```
epds-ts2/
├── api/
│   └── index.py          ← Backend Python (FastAPI) con el código original
├── frontend/
│   └── index.html        ← Frontend interactivo (HTML/CSS/JS)
├── requirements.txt      ← Dependencias Python
├── vercel.json           ← Configuración de despliegue
└── README.md
```

---

## Deploy en Vercel (paso a paso)

### Opción A — Vercel CLI (recomendada)

```bash
# 1. Instalar Vercel CLI
npm install -g vercel

# 2. Desde la raíz del proyecto
cd epds-ts2
vercel

# 3. Seguir las instrucciones interactivas:
#    - Set up and deploy: Y
#    - Which scope: (tu cuenta)
#    - Link to existing project: N
#    - Project name: epds-ts2-simulacion
#    - Directory: ./
#    - Override settings: N

# 4. Para producción:
vercel --prod
```

### Opción B — Vercel Dashboard (sin CLI)

1. Subir el proyecto a GitHub/GitLab
2. Ir a https://vercel.com/new
3. Importar el repositorio
4. Dejar todos los valores por defecto
5. Hacer clic en **Deploy**

---

## Desarrollo local

```bash
# Instalar dependencias Python
pip install fastapi numpy uvicorn

# Correr el backend
uvicorn api.index:app --reload --port 8000

# Abrir el frontend
# Desde otra terminal, servir el frontend en el mismo origen:
cd frontend
python -m http.server 5500
# Luego abrir http://localhost:5500
# (el frontend apunta a /api/... que deberás redirigir o usar un proxy)
```

### Alternativa más simple (local sin proxy)

Editar temporalmente en `frontend/index.html` la línea:
```js
const url = `/api/simular?...`
```
por:
```js
const url = `http://localhost:8000/api/simular?...`
```

---

## Código Python original (sin modificar)

El archivo `api/index.py` contiene exactamente el mismo código del notebook `EPDS_TS2_1D_G5_Simulacion2.ipynb`:

| Función | Descripción |
|---|---|
| `crear_album(figus_total)` | Vector de `n` ceros |
| `comprar_paquete(figus_total, figus_paquete)` | `rd.sample` sin reposición |
| `pegar_figus(album, paquete)` | Marca con `1` las posiciones |
| `album_incompleto(album)` | `0 in album` |
| `cuantos_paquetes(figus_total, figus_paquete)` | Orquesta con `while` + contador |

El endpoint `/api/simular` acepta parámetros via query string:
- `n` → repeticiones (default: 100)
- `figus_total` → figuritas (default: 860)
- `figus_paquete` → por paquete (default: 5)
- `seed` → semilla aleatoria (default: 42)
