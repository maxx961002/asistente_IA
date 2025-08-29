#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, json, os, sys, re
from datetime import datetime, date, timedelta

# ---------- Paths base ----------
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "data")
STATE_DIR = os.path.join(DATA_DIR, "state")
LOG_DIR = os.path.join(DATA_DIR, "logs")
CAL_DIR = os.path.join(DATA_DIR, "calendars")

CLIENTES = os.path.join(STATE_DIR, "clientes.json")
RESERVAS = os.path.join(STATE_DIR, "reservas.json")
TAREAS   = os.path.join(STATE_DIR, "tareas.json")
UNIDADES = os.path.join(STATE_DIR, "unidades.json")

CAL_RES  = os.path.join(CAL_DIR, "sim_reservas.txt")
CAL_PROV = os.path.join(CAL_DIR, "sim_proveedor.txt")
BITACORA = os.path.join(LOG_DIR,  "bitacora.csv")

# --- Bitácora (CSV) ---
import csv, json
from datetime import datetime

LOGS_DIR = os.path.join(DATA_DIR, "logs")
BITACORA = os.path.join(LOGS_DIR, "bitacora.csv")

def log_bitacora(origen, accion, objeto, objeto_id, before, after, extra):
    os.makedirs(LOGS_DIR, exist_ok=True)
    new_file = not os.path.exists(BITACORA)
    with open(BITACORA, "a", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        if new_file:
            w.writerow(["timestamp","origen","accion","objeto","objeto_id","before","after","extra"])
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        def _s(x):
            if isinstance(x, (dict, list)):
                return json.dumps(x, ensure_ascii=False)
            return x if x is not None else ""

        w.writerow([ts, origen, accion, objeto, objeto_id, _s(before), _s(after), _s(extra)])


# ---------- Helpers ----------
def ensure_dirs():
    for d in [DATA_DIR, STATE_DIR, LOG_DIR, CAL_DIR]:
        os.makedirs(d, exist_ok=True)
    for f, empty in [
        (CLIENTES, []),
        (RESERVAS, []),
        (TAREAS, []),
    ]:
        if not os.path.exists(f):
            with open(f, "w", encoding="utf-8") as fh:
                json.dump(empty, fh, ensure_ascii=False, indent=2)
    if not os.path.exists(BITACORA):
        with open(BITACORA, "w", encoding="utf-8") as fh:
            fh.write("timestamp,actor,accion,entidad,clave,antes,despues,nota\n")
    if not os.path.exists(CAL_RES):
        with open(CAL_RES, "w", encoding="utf-8") as fh:
            fh.write("# Simulador de calendario de reservas\n")
    if not os.path.exists(CAL_PROV):
        with open(CAL_PROV, "w", encoding="utf-8") as fh:
            fh.write("# Simulador de calendario de proveedores\n")

TAREAS = os.path.join(DATA_DIR, "state", "tareas.json")

def load_tareas():
    if not os.path.exists(TAREAS): return []
    with open(TAREAS, "r", encoding="utf-8") as fh:
        return json.load(fh)

def save_tareas(ts):
    with open(TAREAS, "w", encoding="utf-8") as fh:
        json.dump(ts, fh, ensure_ascii=False, indent=2)

def next_tarea_id(ts):
    # R-0001, R-0002...
    nums = [int(t["id"].split("-")[1]) for t in ts if t.get("id","").startswith("R-")]
    n = max(nums) + 1 if nums else 1
    return f"R-{n:04d}"


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)

def save_json(path, obj):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(accion, entidad, clave, antes="", despues="", nota=""):
    with open(BITACORA, "a", encoding="utf-8") as fh:
        fh.write(f"{ts()},cli,{accion},{entidad},{clave},{json.dumps(antes, ensure_ascii=False)},{json.dumps(despues, ensure_ascii=False)},{nota}\n")

def cal_write(path, line):
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line.strip()+"\n")

def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()

def overlap(a1, a2, b1, b2):
    # [a1, a2) intersects [b1, b2)
    return not (a2 <= b1 or b2 <= a1)

def normalize_name(s):
    s = s.lower()
    s = re.sub(r"[áàä]", "a", s)
    s = re.sub(r"[éèë]", "e", s)
    s = re.sub(r"[íìï]", "i", s)
    s = re.sub(r"[óòö]", "o", s)
    s = re.sub(r"[úùü]", "u", s)
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s

UNIDADES_CFG = os.path.join(DATA_DIR, "config", "unidades.json")
POL_OVERFLOW = os.path.join(DATA_DIR, "config", "politica_overflow.json")

def cfg_unidades():
    if not os.path.exists(UNIDADES_CFG):
        return []
    with open(UNIDADES_CFG, "r", encoding="utf-8") as fh:
        return json.load(fh)

def cfg_overflow():
    if not os.path.exists(POL_OVERFLOW):
        return {"reglas": []}
    with open(POL_OVERFLOW, "r", encoding="utf-8") as fh:
        return json.load(fh)

def solapa(ing1, egr1, ing2, egr2):
    return not (egr1 <= ing2 or egr2 <= ing1)

def unidad_disponible(unidad_id, ingreso_s, egreso_s):
    reservas = load_json(RESERVAS)
    ing, egr = parse_date(ingreso_s), parse_date(egreso_s)
    for r in reservas:
        if r.get("estado") != "Confirmado":
            continue
        if r.get("unidad_id") != unidad_id:
            continue
        r_ing, r_egr = parse_date(r["ingreso"]), parse_date(r["egreso"])
        if solapa(ing, egr, r_ing, r_egr):
            return False
    return True

def sugerir_unidades(tipo, ingreso_s, egreso_s, pax=2, amenidad=None, max_items=3):
    def _norm(s):
        return (s or "").strip().lower().replace(" ", "_").replace("-", "_")
    unidades = [u for u in cfg_unidades()
                if u["tipo"] == tipo
                and u["estado"] == "ACTIVA"
                and pax >= u["cap_min"] and pax <= u["cap_max"]
                and (_norm(amenidad) in [_norm(a) for a in u.get("amenidades", [])] if amenidad else True)
                and unidad_disponible(u["id"], ingreso_s, egreso_s)]
    # priorizar por "prioridad" y luego por nombre
    unidades.sort(key=lambda u: (u.get("prioridad", 99), u["nombre"]))
    if unidades:
        return unidades[:max_items], "primarias"

    # Overflow (upgrade) si no hay primarias
    pol = cfg_overflow()
    reglas = [r for r in pol.get("reglas", []) if r.get("tipo_solicitado") == tipo]
    if not reglas:
        return [], "sin_disponibilidad"

    fallback_ids = []
    for r in reglas:
        fallback_ids += r.get("usar_fallback_de", [])
    fallback = []
    by_id = {u["id"]: u for u in cfg_unidades()}
    for fid in fallback_ids:
        u = by_id.get(fid)
        if not u:
            continue
        if u["estado"] != "ACTIVA":
            continue
        if amenidad and _norm(amenidad) not in [_norm(a) for a in u.get("amenidades", [])]:
            continue
        if not unidad_disponible(u["id"], ingreso_s, egreso_s):
            continue
        fallback.append(u)
    fallback.sort(key=lambda u: (u.get("prioridad", 99), u["nombre"]))
    return fallback[:max_items], "overflow"


# ---------- Reportes: helpers ----------
def month_bounds(mes_yyyy_mm):
    # mes_yyyy_mm = "2025-01"
    y, m = mes_yyyy_mm.split("-")
    y, m = int(y), int(m)
    inicio = datetime(y, m, 1).date()
    if m == 12:
        fin = datetime(y+1, 1, 1).date()
    else:
        fin = datetime(y, m+1, 1).date()
    return inicio, fin

def rango_solapado(a1, a2, b1, b2):
    """ Intersección [a1,a2) ∩ [b1,b2). Devuelve (ini, fin) o (None,None) si no hay. """
    ini = max(a1, b1)
    fin = min(a2, b2)
    if fin <= ini:
        return None, None
    return ini, fin

def noches_en_rango(ingreso_s, egreso_s, r_ini, r_fin):
    a1, a2 = parse_date(ingreso_s), parse_date(egreso_s)
    i, f = rango_solapado(a1, a2, r_ini, r_fin)
    return 0 if i is None else (f - i).days

def calcular_alojamiento_en_rango(tipo, pax, ingreso_s, egreso_s, r_ini, r_fin):
    a1, a2 = parse_date(ingreso_s), parse_date(egreso_s)
    i, f = rango_solapado(a1, a2, r_ini, r_fin)
    if i is None:
        return 0
    # usamos el mismo motor sobre el sub-rango
    return calcular_alojamiento(i.strftime("%Y-%m-%d"), f.strftime("%Y-%m-%d"), tipo, pax, late=False)

# ---------- Dominio ----------
ID_PREFIX = "YEM"  # para La Yema
CHECKIN_HHMM  = "12:00"
CHECKOUT_HHMM = "10:00"

TIPO_POR_PAX = [
    (1,2, "Loft 2 personas"),
    (3,4, "Loft 3 y 4 personas"),
    (4,5, "Departamento 4 y 5 personas"),
    (6,8, "Cabaña hasta 8 personas"),
]

def tipo_por_personas(pax):
    for lo, hi, t in TIPO_POR_PAX:
        if lo <= pax <= hi:
            return t
    raise ValueError(f"No hay tipo definido para {pax} pax.")

def unidades_disponibles(unidades, reservas, tipo, ingreso, egreso, amenidad=None):
    res = []
    for u in unidades:
        if u.get("estado") != "ACTIVA":
            continue
        if u.get("tipo") != tipo:
            continue
        if amenidad and amenidad not in u.get("amenidades", []):
            continue
        libre = True
        for r in reservas:
            if r.get("estado") in ("Cancelado",):
                continue
            if r.get("unidad_id") != u["id"]:
                continue
            # fechas
            ri = parse_date(r["ingreso"])
            re = parse_date(r["egreso"])
            if overlap(ri, re, ingreso, egreso):
                libre = False
                break
        if libre:
            res.append(u)
    # prioridad ascendente
    res.sort(key=lambda x: x.get("prioridad", 999))
    return res

def generar_rid(fecha_base=None, corr=None):
    if fecha_base is None:
        fecha_base = date.today()
    if corr is None:
        # contador simple por día: cantidad+1
        reservas = load_json(RESERVAS)
        hoy = fecha_base.strftime("%Y%m%d")
        n = sum(1 for r in reservas if r.get("rid","").startswith(f"{ID_PREFIX}-{hoy}"))
        corr = n+1
    return f"{ID_PREFIX}-{fecha_base.strftime('%Y%m%d')}-{corr:03d}"

# ---------- Calculo: carga config y reglas ----------
CFG_DIR = os.path.join(DATA_DIR, "config")
TARIFAS = os.path.join(CFG_DIR, "tarifas.json")
VENTANAS = os.path.join(CFG_DIR, "ventanas.json")
DESCUENTOS = os.path.join(CFG_DIR, "descuentos.json")
POL_OVERFLOW = os.path.join(CFG_DIR, "politica_overflow.json")

def cfg_load(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)

SERVICIOS_CFG = os.path.join(DATA_DIR, "config", "servicios.json")

def cmd_debug_disponibilidad(args):
    tipo = args.tipo
    ingreso = args.ingreso
    egreso = args.egreso
    pax = int(args.pax or 2)
    amenidad = args.amenidad if args.amenidad else None

    print(f"[DEBUG] Tipo='{tipo}' | {ingreso}->{egreso} | pax={pax} | amenidad={amenidad or '-'}")
    unidades = cfg_unidades()
    if not unidades:
        print("No cargó ninguna unidad (revisá data/config/unidades.json).")
        return 1

    # listado de reservas confirmadas para el rango (para ver bloqueos reales)
    reservas = [r for r in load_json(RESERVAS) if r.get("estado") == "Confirmado"]
    print(f"[DEBUG] Reservas confirmadas en archivo: {len(reservas)}")
    for r in reservas:
        if not (parse_date(r["egreso"]) <= parse_date(ingreso) or parse_date(r["ingreso"]) >= parse_date(egreso)):
            print(f"  - BLOQUEA {r['unidad_id']} ({r['unidad_nombre']}) RID {r['rid']} {r['ingreso']}→{r['egreso']}")

    def _norm(s):
        return (s or "").strip().lower().replace(" ", "_").replace("-", "_")

    candidatos = [u for u in unidades if u["tipo"] == tipo]
    if not candidatos:
        print("No hay unidades con ese 'tipo' exacto. (Chequeá ortografía/espacios en 'tipo').")
        return 0

    for u in sorted(candidatos, key=lambda x: x["nombre"]):
        reasons = []
        if u.get("estado") != "ACTIVA":
            reasons.append("estado!=ACTIVA")
        if not (pax >= u["cap_min"] and pax <= u["cap_max"]):
            reasons.append(f"capacidad({u['cap_min']}-{u['cap_max']}) no cubre pax={pax}")
        if amenidad and _norm(amenidad) not in [_norm(a) for a in u.get("amenidades", [])]:
            reasons.append(f"sin_amenidad:{amenidad}")
        libre = unidad_disponible(u["id"], ingreso, egreso)
        if not libre:
            reasons.append("ocupada_en_rango")

        ok = "OK" if not reasons else "NO"
        print(f"{ok} | {u['id']} {u['nombre']} | cap {u['cap_min']}-{u['cap_max']} | amen={','.join(u.get('amenidades', [])) or '-'} | {'; '.join(reasons) or 'disponible'}")
    return 0


def cmd_costo_proveedor_mes(args):
    mes = args.mes
    inicio, fin = month_bounds(mes)
    reservas = load_json(RESERVAS)

    # leer costos de desayuno desde config
    sdef = servicio_por_key("servicio_1")  # Desayuno
    costo_norm = costo_sintacc = 0
    if sdef:
        for st in sdef.get("subtipos", []):
            if st.get("id") == "normal":
                costo_norm = int(st.get("costo_proveedor_pp", 0))
            if st.get("id") == "sin_tacc":
                costo_sintacc = int(st.get("costo_proveedor_pp", 0))

    total = 0
    items = []
    for r in reservas:
        if r.get("estado") != "Confirmado":
            continue
        # filtra por mes de ingreso
        if not (parse_date(r["ingreso"]) >= inicio and parse_date(r["ingreso"]) < fin):
            continue

        servs = r.get("servicios", {})
        # Desayuno (normal/sin_tacc)
        dz = servs.get("Desayuno")
        if isinstance(dz, dict):
            n = int(dz.get("normal", 0))
            s = int(dz.get("sin_tacc", 0))
            c = n * costo_norm + s * costo_sintacc
            if c:
                total += c
                items.append((r["rid"], r["nombre"], c, f"Desayuno n={n} s={s}"))

        # otros servicios con costo_proveedor
        for k, v in servs.items():
            if k == "Desayuno":
                continue
            cprov = v.get("costo_proveedor")
            if isinstance(cprov, (int, float)) and cprov > 0:
                total += int(cprov)
                items.append((r["rid"], r["nombre"], int(cprov), k))

    print(f"[Costo proveedor] {mes} = ${total}")
    for rid, nombre, c, label in items:
        print(f"  - {rid} {nombre}: ${c} ({label})")
    return 0

def cmd_preguntar_disponibilidad(args):
    tipo = args.tipo
    ingreso = args.ingreso
    egreso = args.egreso
    pax = int(args.pax or 2)
    amenidad = args.amenidad if args.amenidad else None
    max_items = int(args.max or 3)

    unidades, modo = sugerir_unidades(tipo, ingreso, egreso, pax=pax, amenidad=amenidad, max_items=max_items)

    if not unidades:
        print("No hay disponibilidad para ese criterio.")
        return 0

    label = "Primarias" if modo == "primarias" else "Overflow (upgrade)"
    print(f"{label} disponibles para {tipo} · {ingreso}→{egreso} · {pax} pax" + (f" · amenidad={amenidad}" if amenidad else ""))
    for u in unidades:
        print(f"  - {u['id']} | {u['nombre']} | cap {u['cap_min']}-{u['cap_max']} | amenidades={','.join(u.get('amenidades', [])) or '-'}")
    return 0


def cmd_ingresos_mes(args):
    mes = args.mes
    inicio, fin = month_bounds(mes)
    reservas = load_json(RESERVAS)

    total = 0
    detalle = []
    for r in reservas:
        if r.get("estado") != "Confirmado":
            continue
        pax = int(r.get("pax", 2))
        aloj = calcular_alojamiento_en_rango(r["tipo"], pax, r["ingreso"], r["egreso"], inicio, fin)
        if aloj > 0:
            total += aloj
            detalle.append((r["rid"], r["nombre"], aloj))

    print(f"[Ingresos alojamiento] {mes} = ${total}")
    for rid, nombre, monto in detalle:
        print(f"  - {rid} {nombre}: ${monto}")
    return 0


def cfg_servicios():
    if not os.path.exists(SERVICIOS_CFG):
        return []
    with open(SERVICIOS_CFG, "r", encoding="utf-8") as fh:
        return json.load(fh)

def servicio_por_key(key):
    for s in cfg_servicios():
        if s.get("key") == key:
            return s
    return None

def agregar_servicio_en_reserva(r, key, personas):
    sdef = servicio_por_key(key)
    if not sdef:
        raise ValueError(f"Servicio {key} no encontrado en config.")
    nombre = sdef.get("nombre", key)
    unit = int(sdef.get("precio_unitario_pp", 0))
    sumar = bool(sdef.get("sumar_al_resto", True))
    total_huesped = int(unit * int(personas))

    r.setdefault("servicios", {})
    r["servicios"][nombre] = {
        "personas": int(personas),
        "precio_huesped": total_huesped,
        "sumar_al_resto": sumar
    }

    # costo proveedor (si existe un costo_pp único; desayuno usa subtipos en otro comando)
    costo_pp = sdef.get("costo_proveedor_pp")
    if isinstance(costo_pp, (int, float)):
        r["servicios"][nombre]["costo_proveedor"] = int(costo_pp) * int(personas)

def cmd_ocupacion_mes(args):
    mes = args.mes
    total_unidades = int(args.total_unidades)
    inicio, fin = month_bounds(mes)
    dias_mes = (fin - inicio).days

    reservas = load_json(RESERVAS)
    noches_ocupadas = 0
    for r in reservas:
        if r.get("estado") != "Confirmado":
            continue
        noches_ocupadas += noches_en_rango(r["ingreso"], r["egreso"], inicio, fin)

    capacidad = total_unidades * dias_mes
    pct = 0.0 if capacidad == 0 else (noches_ocupadas * 100.0 / capacidad)
    print(f"[Ocupación] {mes}: {noches_ocupadas}/{capacidad} noches = {pct:.1f}% (unidades={total_unidades}, días={dias_mes})")
    return 0

def quitar_servicio_en_reserva(r, key_o_nombre):
    servicios = r.get("servicios", {})
    # admitir key o nombre visible
    # primero intenta por nombre visible:
    if key_o_nombre in servicios:
        servicios.pop(key_o_nombre, None)
        return True
    # si vino la key, buscá por config:
    sdef = servicio_por_key(key_o_nombre)
    if sdef:
        nombre = sdef.get("nombre", key_o_nombre)
        if nombre in servicios:
            servicios.pop(nombre, None)
            return True
    return False

def recalc_si_confirmada(r):
    if r.get("estado") != "Confirmado":
        return None
    aloj = calcular_alojamiento(r["ingreso"], r["egreso"], r["tipo"], int(r["pax"]), late=bool(r.get("late", False)))
    serv = total_servicios_huesped(r.get("servicios"))
    sen  = int(r.get("seña", {}).get("monto", 0))
    resto = int(aloj + serv - sen)
    r["resto"] = resto
    return {"aloj": aloj, "serv": serv, "senia": sen, "resto": resto}

def cmd_agregar_servicio(args):
    reservas = load_json(RESERVAS)
    r = next((x for x in reservas if x["rid"] == args.rid), None)
    if not r:
        print("RID no encontrado.")
        return 1
    antes = dict(r)
    try:
        agregar_servicio_en_reserva(r, args.key, args.personas)
    except Exception as e:
        print(f"Error: {e}")
        return 1

    recalculo = recalc_si_confirmada(r)
    save_json(RESERVAS, reservas)

    titulo = f"{r['nombre']} — {r.get('unidad_nombre','Sin asignar')}"
    if recalculo:
        desc = (f"RID {r['rid']} | {r['tipo']} | {r['pax']} pax | "
                f"Aloj ${recalculo['aloj']} + Serv ${recalculo['serv']} − Seña ${recalculo['senia']} = Resto ${recalculo['resto']}")
        cal_write(CAL_RES, f"UPDATE | {r['rid']} | {titulo} | {r['ingreso']} {CHECKIN_HHMM} -> {r['egreso']} {CHECKOUT_HHMM} | CONFIRMADO · {desc}")
    log("agregar_servicio_generico", "reserva", r["rid"], antes=antes, despues=r, nota=f"key={args.key}, personas={args.personas}")
    print("OK: Servicio agregado.")
    return 0

def cmd_quitar_servicio(args):
    reservas = load_json(RESERVAS)
    r = next((x for x in reservas if x["rid"] == args.rid), None)
    if not r:
        print("RID no encontrado.")
        return 1
    antes = dict(r)
    ok = quitar_servicio_en_reserva(r, args.key)
    if not ok:
        print("Servicio no encontrado en la reserva.")
        return 1

    recalculo = recalc_si_confirmada(r)
    save_json(RESERVAS, reservas)

    titulo = f"{r['nombre']} — {r.get('unidad_nombre','Sin asignar')}"
    if recalculo:
        desc = (f"RID {r['rid']} | {r['tipo']} | {r['pax']} pax | "
                f"Aloj ${recalculo['aloj']} + Serv ${recalculo['serv']} − Seña ${recalculo['senia']} = Resto ${recalculo['resto']}")
        cal_write(CAL_RES, f"UPDATE | {r['rid']} | {titulo} | {r['ingreso']} {CHECKIN_HHMM} -> {r['egreso']} {CHECKOUT_HHMM} | CONFIRMADO · {desc}")
    log("quitar_servicio", "reserva", r["rid"], antes=antes, despues=r, nota=f"key={args.key}")
    print("OK: Servicio quitado.")
    return 0
def cmd_agendar_recordatorio(args):
    ts = load_tareas()
    rid = next_tarea_id(ts)
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Modo: uno / diario / semanal
    if args.cuando:
        fecha_hora = args.cuando  # "YYYY-MM-DD HH:MM"
        programacion = {"modo": "uno", "fecha_hora": fecha_hora}
    elif args.diario:
        programacion = {"modo": "diario", "hora": args.diario}  # "HH:MM"
    elif args.semanal and args.hora:
        dias = [d.strip().upper() for d in args.semanal.split(",")]  # LU,MA,MI,JU,VI,SA,DO
        programacion = {"modo": "semanal", "hora": args.hora, "dias": dias}
    else:
        print("Faltan datos de programación: usa --cuando 'YYYY-MM-DD HH:MM' o --diario 'HH:MM' o --semanal 'LU,MI' --hora 'HH:MM'")
        return 1

    tarea = {
        "id": rid,
        "tipo": "GENERAL",
        "titulo": args.titulo,
        "estado": "pendiente",        # pendiente | completado | cancelado
        "programacion": programacion,
        "nota": args.nota or "",
        "creado_en": ahora,
        "completado_en": None,
        "cancelado_motivo": None,
        "origen": "cli"
    }
    ts.append(tarea)
    save_tareas(ts)
    log_bitacora("cli", "agendar_recordatorio", "tarea", rid, "", tarea, "")
    print(f"OK · creado {rid}: {tarea['titulo']} · prog={programacion}")
    return 0

def cmd_listar_recordatorios(args):
    ts = load_tareas()
    if not ts:
        print("No hay tareas/recordatorios.")
        return 0

    estado_filtro = args.estado.upper() if args.estado else None
    tipo_filtro = args.tipo.upper() if getattr(args, "tipo", None) else None
    hoy = datetime.now().strftime("%Y-%m-%d")
    dow = ["LU","MA","MI","JU","VI","SA","DO"][datetime.now().weekday()]

    def es_de_hoy(t):
        # GENERAL: por programación; LIMPIEZA: por fecha exacta
        if t.get("tipo") == "GENERAL":
            p = t.get("programacion", {})
            if p.get("modo") == "uno":
                return str(p.get("fecha_hora", "")).startswith(hoy)
            if p.get("modo") == "diario":
                return True
            if p.get("modo") == "semanal":
                return dow in (p.get("dias") or [])
            return False
        # LIMPIEZA u otros: si tienen fecha exacta para hoy
        return t.get("fecha") == hoy

    def pasa_filtros(t):
        if estado_filtro and t.get("estado","").upper() != estado_filtro:
            return False
        if tipo_filtro and t.get("tipo","").upper() != tipo_filtro:
            return False
        if args.hoy and not es_de_hoy(t):
            return False
        return True

    filtradas = [t for t in ts if pasa_filtros(t)]
    if not filtradas:
        print("No hay recordatorios para ese filtro.")
        return 0

    print(f"Recordatorios/Tareas ({len(filtradas)}):")
    for t in filtradas:
        tipo = t.get("tipo","-")
        tid = t.get("id") or f"LIMP-{t.get('unidad_id','?')}"
        titulo = t.get("titulo") or f"LIMPIEZA {t.get('unidad_nombre','')}".strip() or "Tarea"
        prog = t.get("programacion", "-") if tipo == "GENERAL" else {"modo":"uno", "fecha": t.get("fecha","-")}
        nota = t.get("nota","-")
        estado = t.get("estado","-")
        print(f" - {tid} | {estado} | {tipo} | {titulo} | prog={prog} | nota={nota}")
    return 0


def cmd_completar_recordatorio(args):
    ts = load_tareas()
    for t in ts:
        if t["id"] == args.id and t["estado"] == "pendiente":
            t["estado"] = "completado"
            t["completado_en"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tareas(ts)
            log_bitacora("cli","completar_recordatorio","tarea",t["id"],"",t,"")
            print(f"OK · {t['id']} marcado COMPLETADO")
            return 0
    print("No se pudo completar (id inexistente o ya no está pendiente).")
    return 1

def cmd_cancelar_recordatorio(args):
    ts = load_tareas()
    for t in ts:
        if t["id"] == args.id and t["estado"] in ("pendiente","completado"):
            t["estado"] = "cancelado"
            t["cancelado_motivo"] = args.motivo or ""
            save_tareas(ts)
            log_bitacora("cli","cancelar_recordatorio","tarea",t["id"],"",t,args.motivo or "")
            print(f"OK · {t['id']} CANCELADO · motivo: {t['cancelado_motivo']}")
            return 0
    print("No se pudo cancelar (id inexistente).")
    return 1


def night_rules_for(date_obj, ventanas):
    """ Devuelve la regla más específica que aplica esa noche. """
    winners = []
    for v in ventanas:
        d1 = parse_date(v["desde"])
        d2 = parse_date(v["hasta"])
        if d1 <= date_obj < d2 + timedelta(days=1):  # hasta inclusive
            winners.append(( (d2 - d1).days + 1, v))  # (duración, ventana)
    if not winners:
        return {"regla": "precio_normal"}
    winners.sort(key=lambda x: x[0])  # más corta = más específica
    ganadora = winners[0][1]
    return ganadora

def precio_por_noche(tipo, pax, regla, tarifas):
    t = tarifas.get(tipo, {})
    fila = t.get(str(pax))
    if not fila:
        # Fallback simple: usar la “clave” más cercana (hacia abajo)
        claves = sorted(int(k) for k in t.keys())
        cercanas = [k for k in claves if k <= pax]
        if not cercanas:
            raise ValueError(f"Tarifa no definida para tipo={tipo}, pax={pax}")
        fila = t[str(max(cercanas))]
    if regla == "precio_especial":
        return int(fila.get("especial", fila.get("normal", 0)))
    elif regla == "descuento_pct":
        base = int(fila.get("normal", 0))
        return base  # el descuento se aplica aparte a nivel noche
    else:
        return int(fila.get("normal", 0))

def calcular_alojamiento(ingreso_s, egreso_s, tipo, pax, late=False):
    tarifas = cfg_load(TARIFAS, {})
    ventanas = cfg_load(VENTANAS, [])
    descuentos = cfg_load(DESCUENTOS, [])
    pol_over = cfg_load(POL_OVERFLOW, {"precio_fuente": "TIPO_SOLICITADO"})

    ingreso = parse_date(ingreso_s)
    egreso  = parse_date(egreso_s)
    if egreso <= ingreso:
        raise ValueError("egreso debe ser posterior a ingreso")

    total = 0
    d = ingreso
    while d < egreso:
        regla = night_rules_for(d, ventanas)
        r = regla.get("regla", "precio_normal")
        base = precio_por_noche(tipo, pax, r, tarifas)

        if r == "descuento_pct":
            pct = int(regla.get("valor", 0))
            base = int(round(base * (100 - pct) / 100.0))

        total += base
        d += timedelta(days=1)

    # Late checkout como fracción de la última noche (La Yema: 0.5)
    if late:
        extra_frac = 0.5
        # usar la “regla” de la última noche real:
        ultima_noche = egreso - timedelta(days=1)
        regla = night_rules_for(ultima_noche, ventanas)
        r = regla.get("regla", "precio_normal")
        base_ultima = precio_por_noche(tipo, pax, r, tarifas)
        if r == "descuento_pct":
            pct = int(regla.get("valor", 0))
            base_ultima = int(round(base_ultima * (100 - pct) / 100.0))
        total += int(round(base_ultima * extra_frac))

    # Descuentos por estadía (p. ej., 7 noches o más −10%)
    noches_base = (egreso - ingreso).days
    for dsc in descuentos:
        if dsc.get("condicion") == "noches_minimas" and noches_base >= int(dsc.get("noches", 0)):
            pct = int(dsc.get("descuento_pct", 0))
            total = int(round(total * (100 - pct) / 100.0))

    return int(total)

def total_servicios_huesped(servicios):
    """Suma solo lo que paga el huésped (Desayuno en La Yema = 0)."""
    if not servicios:
        return 0
    total = 0
    for k, v in servicios.items():
        # si hay precio_huesped, lo sumamos; si no, 0
        precio = v.get("precio_huesped")
        if isinstance(precio, (int, float)):
            total += int(precio)
    return int(total)


# ---------- Acciones ----------
def cmd_reservar_rapido(args):
    clientes = load_json(CLIENTES)
    reservas = load_json(RESERVAS)
    unidades = load_json(UNIDADES)

    ingreso = parse_date(args.ingreso)
    egreso  = parse_date(args.egreso)
    if egreso <= ingreso:
        print("Error: egreso debe ser posterior a ingreso.")
        return 1
    pax = int(args.pax)
    tipo = tipo_por_personas(pax)

    # amenidad opcional
    amenidad = "camas_separadas" if args.camas_separadas else None

    # buscar unidad
    uds = unidades_disponibles(unidades, reservas, tipo, ingreso, egreso, amenidad=amenidad)
    unidad = uds[0] if uds else None

    rid = generar_rid()
    reserva = {
        "rid": rid,
        "nombre": args.nombre,
        "ingreso": ingreso.strftime("%Y-%m-%d"),
        "egreso": egreso.strftime("%Y-%m-%d"),
        "noches": (egreso - ingreso).days,
        "pax": pax,
        "tipo": tipo,
        "unidad_id": unidad["id"] if unidad else None,
        "unidad_nombre": unidad["nombre"] if unidad else "Sin asignar",
        "estado": "PendienteDatos",
        "datos_completos": False,
        "cliente_vinculado": False,
        "servicios": {
            "Desayuno": {"normal": pax, "sin_tacc": 0, "precio_huesped": 0}
        },
        "seña": {"monto": 0, "medio": None},
        "resto": 0,
        "amenidades": ["camas_separadas"] if amenidad else [],
        "notas": ""
    }
    reservas.append(reserva)
    save_json(RESERVAS, reservas)

    titulo = f"{args.nombre} — {reserva['unidad_nombre']}"
    desc = f"RID {rid} | {tipo} | {reserva['pax']} pax | Desayuno {pax} normal / 0 sin TACC"
    cal_write(CAL_RES, f"ADD | {rid} | {titulo} | {reserva['ingreso']} {CHECKIN_HHMM} -> {reserva['egreso']} {CHECKOUT_HHMM} | {desc}")
    log("crear_reserva_rapida", "reserva", rid, antes="", despues=reserva, nota="")

    print(f"OK: Reserva rápida creada en Pendiente de completar.")
    print(f"RID: {rid}")
    print(f"Tipo: {tipo} | Unidad: {reserva['unidad_nombre']}")
    return 0

def find_cliente(clientes, nombre=None, dni=None, tel=None, localidad=None):
    # prioridad: DNI > Tel > Nombre+Localidad > Nombre
    if dni:
        for c in clientes:
            if c.get("dni") == dni:
                return c, "dni"
    if tel:
        for c in clientes:
            if c.get("tel") == tel:
                return c, "tel"
    if nombre and localidad:
        cand = [c for c in clientes if c.get("nombre","").lower()==nombre.lower() and c.get("localidad","").lower()==localidad.lower()]
        if len(cand)==1:
            return cand[0], "nombre+localidad"
    if nombre:
        cand = [c for c in clientes if c.get("nombre","").lower()==nombre.lower()]
        if len(cand)==1:
            return cand[0], "nombre"
    return None, None

def cmd_completar_reserva(args):
    reservas = load_json(RESERVAS)
    clientes = load_json(CLIENTES)

    r = next((x for x in reservas if x["rid"]==args.rid), None)
    if not r:
        print("RID no encontrado.")
        return 1

    # intento de match
    c, criterio = find_cliente(clientes, nombre=r.get("nombre"), dni=args.dni, tel=args.tel, localidad=args.localidad)

    if c is None:
        # crear cliente nuevo
        c = {
            "cliente_id": f"cli_{len(clientes)+1:04d}",
            "nombre": r.get("nombre"),
            "dni": args.dni,
            "tel": args.tel,
            "localidad": args.localidad,
            "veces": 0,
            "first_seen": date.today().isoformat(),
            "last_seen": date.today().isoformat(),
            "semaforo": "Verde"
        }
        clientes.append(c)
        save_json(CLIENTES, clientes)
        criterio = "nuevo_cliente"

    # vincular
    antes = dict(r)
    r["cliente_id"] = c["cliente_id"]
    r["datos_completos"] = True
    r["cliente_vinculado"] = True
    # actualizar “evento” simulado
    titulo = f"{r['nombre']} — {r['unidad_nombre']}"
    desc = f"RID {r['rid']} | {r['tipo']} | DNI {c.get('dni')} | Tel {c.get('tel')} | {r['pax']} pax"
    cal_write(CAL_RES, f"UPDATE | {r['rid']} | {titulo} | {r['ingreso']} {CHECKIN_HHMM} -> {r['egreso']} {CHECKOUT_HHMM} | {desc}")
    save_json(RESERVAS, reservas)
    log("completar_reserva", "reserva", r["rid"], antes=antes, despues=r, nota=f"criterio={criterio}")

    print(f"OK: Datos completados y reserva vinculada a {c['cliente_id']} ({criterio}).")
    return 0

def cmd_confirmar_reserva(args):
    reservas = load_json(RESERVAS)
    r = next((x for x in reservas if x["rid"] == args.rid), None)
    if not r:
        print("RID no encontrado.")
        return 1
    if not r.get("datos_completos"):
        print("Faltan datos del huésped (dni/tel/localidad). Completá antes de confirmar.")
        return 1
    if not r.get("unidad_id"):
        print("No hay unidad asignada.")
        return 1

    # Calcular totales
    tipo = r.get("tipo")
    pax = int(r.get("pax", 2))
    ingreso = r.get("ingreso")
    egreso  = r.get("egreso")
    late = bool(args.late)

    aloj = calcular_alojamiento(ingreso, egreso, tipo, pax, late=late)
    serv = total_servicios_huesped(r.get("servicios"))
    senia = int(r.get("seña", {}).get("monto", 0))
    resto = int(aloj + serv - senia)

    antes = dict(r)
    r["resto"] = resto
    r["estado"] = "Confirmado"
    save_json(RESERVAS, reservas)

    # Actualizar “evento” simulado
    titulo = f"{r['nombre']} — {r['unidad_nombre']}"
    desc = (f"RID {r['rid']} | {r['tipo']} | {r['pax']} pax | "
            f"Aloj ${aloj} + Serv ${serv} − Seña ${senia} = Resto ${resto}")
    cal_write(CAL_RES, f"UPDATE | {r['rid']} | {titulo} | {r['ingreso']} {CHECKIN_HHMM} -> {r['egreso']} {CHECKOUT_HHMM} | CONFIRMADO · {desc}")

    log("confirmar_reserva", "reserva", r["rid"],
        antes=antes,
        despues={"aloj": aloj, "serv": serv, "senia": senia, "resto": resto, "late": late},
        nota="confirmado")
    print(f"OK: Confirmada. Aloj ${aloj} + Serv ${serv} − Seña ${senia} = RESTO ${resto}.")
    return 0

def cmd_cancelar_reserva(args):
    reservas = load_json(RESERVAS)
    r = next((x for x in reservas if x["rid"] == args.rid), None)
    if not r:
        print("RID no encontrado.")
        return 1
    if r.get("estado") == "Cancelado":
        print("La reserva ya estaba cancelada.")
        return 0

    antes = dict(r)
    r["estado"] = "Cancelado"
    # anota motivo en notas (no pisa lo anterior)
    notas_prev = r.get("notas") or ""
    motivo_txt = (args.motivo or "").strip()
    r["notas"] = (notas_prev + (" | " if notas_prev and motivo_txt else "") + (f"Cancelada: {motivo_txt}" if motivo_txt else "")).strip()

    save_json(RESERVAS, reservas)

    titulo = f"{r['nombre']} — {r.get('unidad_nombre','Sin asignar')}"
    cal_write(CAL_RES, f"CANCEL | {r['rid']} | {titulo} | {r['ingreso']} {CHECKIN_HHMM} -> {r['egreso']} {CHECKOUT_HHMM} | Motivo: {motivo_txt}")

    log("cancelar_reserva", "reserva", r["rid"], antes=antes, despues=r, nota=motivo_txt)
    print("OK: Reserva cancelada.")
    return 0


def cmd_registrar_senia(args):
    reservas = load_json(RESERVAS)
    r = next((x for x in reservas if x["rid"] == args.rid), None)
    if not r:
        print("RID no encontrado.")
        return 1
    antes = dict(r)
    r.setdefault("seña", {})
    r["seña"]["monto"] = int(args.monto)
    r["seña"]["medio"] = args.medio
    save_json(RESERVAS, reservas)
    log("registrar_senia", "reserva", r["rid"], antes=antes, despues=r, nota="")
    print(f"OK: Seña registrada ${int(args.monto)} ({args.medio}).")
    return 0


def resolve_unidad_by_name(unidades, nombre):
    key = normalize_name(nombre)
    for u in unidades:
        if normalize_name(u["nombre"]) == key:
            return u
    # fallback: unidad_#
    if nombre.startswith("unidad_"):
        for u in unidades:
            if u["id"] == nombre:
                return u
    return None

def cmd_cambiar_unidad(args):
    reservas = load_json(RESERVAS)
    unidades = load_json(UNIDADES)

    r = next((x for x in reservas if x["rid"]==args.rid), None)
    if not r:
        print("RID no encontrado.")
        return 1
    destino = resolve_unidad_by_name(unidades, args.unidad)
    if not destino:
        print("Unidad destino no encontrada (por nombre visible o unidad_#).")
        return 1

    # validar capacidad
    if not (destino["cap_min"] <= r["pax"] <= destino["cap_max"]):
        print("La capacidad de la unidad destino no admite esa cantidad de personas.")
        return 1
    # validar solape
    ingreso = parse_date(r["ingreso"])
    egreso  = parse_date(r["egreso"])
    reservas_all = [x for x in reservas if x["rid"]!=r["rid"] and x.get("unidad_id")==destino["id"] and x.get("estado")!="Cancelado"]
    for rr in reservas_all:
        if overlap(parse_date(rr["ingreso"]), parse_date(rr["egreso"]), ingreso, egreso):
            print("La unidad destino no está libre en esas fechas.")
            return 1

    antes = dict(r)
    r["unidad_id"] = destino["id"]
    r["unidad_nombre"] = destino["nombre"]
    save_json(RESERVAS, reservas)
    cal_write(CAL_RES, f"MOVE | {r['rid']} | {r['nombre']} — {r['unidad_nombre']} | {r['ingreso']} {CHECKIN_HHMM} -> {r['egreso']} {CHECKOUT_HHMM} | Cambio de unidad")
    log("cambiar_unidad", "reserva", r["rid"], antes=antes, despues=r, nota=f"destino={destino['id']}")
    print(f"OK: MOVIDA a {destino['nombre']} ({destino['id']}).")
    return 0

def cmd_agregar_desayuno(args):
    reservas = load_json(RESERVAS)
    r = next((x for x in reservas if x["rid"]==args.rid), None)
    if not r:
        print("RID no encontrado.")
        return 1
    normales = int(args.normales)
    sintacc  = int(args.sin_tacc)
    r["servicios"]["Desayuno"] = {"normal": normales, "sin_tacc": sintacc, "precio_huesped": 0}
    save_json(RESERVAS, reservas)
    detalle = f"{normales} normal / {sintacc} sin TACC"
    cal_write(CAL_PROV, f"ADD| {r['ingreso']} | Desayunos Anita | RID {r['rid']} {r['nombre']} {detalle}")
    log("agregar_servicio", "reserva", r["rid"], antes="", despues={"Desayuno": r["servicios"]["Desayuno"]}, nota="")
    print(f"OK: Desayuno actualizado ({detalle}).")
    return 0

def cmd_reprogramar(args):
    reservas = load_json(RESERVAS)
    r = next((x for x in reservas if x["rid"] == args.rid), None)
    if not r:
        print("RID no encontrado.")
        return 1

    # mover fechas
    antes = dict(r)
    r["ingreso"] = args.ingreso
    r["egreso"]  = args.egreso
    try:
        r["noches"] = (parse_date(r["egreso"]) - parse_date(r["ingreso"])).days
    except Exception:
        r["noches"] = r.get("noches", 0)

    titulo = f"{r['nombre']} — {r.get('unidad_nombre','Sin asignar')}"
    cal_write(CAL_RES, f"MOVE | {r['rid']} | {titulo} | {r['ingreso']} {CHECKIN_HHMM} -> {r['egreso']} {CHECKOUT_HHMM} | Reprogramación")

    # Si estaba confirmada, recalcular totales y actualizar calendario
    if r.get("estado") == "Confirmado":
        tipo = r.get("tipo")
        pax  = int(r.get("pax", 2))
        late = bool(r.get("late", False))  # si no lo guardaste antes, queda False

        aloj  = calcular_alojamiento(r["ingreso"], r["egreso"], tipo, pax, late=late)
        serv  = total_servicios_huesped(r.get("servicios"))
        senia = int(r.get("seña", {}).get("monto", 0))
        resto = int(aloj + serv - senia)
        r["resto"] = resto

        desc = (f"RID {r['rid']} | {r['tipo']} | {r['pax']} pax | "
                f"Aloj ${aloj} + Serv ${serv} − Seña ${senia} = Resto ${resto}")
        cal_write(CAL_RES, f"UPDATE | {r['rid']} | {titulo} | {r['ingreso']} {CHECKIN_HHMM} -> {r['egreso']} {CHECKOUT_HHMM} | CONFIRMADO · {desc}")

        save_json(RESERVAS, reservas)
        log("reprogramar_reserva", "reserva", r["rid"],
            antes=antes,
            despues={"aloj": aloj, "serv": serv, "senia": senia, "resto": resto, "recalculo": True},
            nota="confirmada_recalculada")
        print(f"OK: Reprogramada y recalculada. Nuevo RESTO ${resto}.")
        return 0

    # si no estaba confirmada, solo guardamos el move
    save_json(RESERVAS, reservas)
    log("reprogramar_reserva", "reserva", r["rid"], antes=antes, despues=r, nota="pendiente")
    print("OK: Reprogramada (pendiente).")
    return 0


def cmd_checkout(args):
    reservas = load_json(RESERVAS)
    unidades = load_json(UNIDADES)
    tareas   = load_json(TAREAS)

    r = next((x for x in reservas if x["rid"]==args.rid), None)
    if not r:
        print("RID no encontrado.")
        return 1
    # tarea de limpieza
    tarea = {
        "tipo": "LIMPIEZA",
        "unidad_id": r.get("unidad_id"),
        "unidad_nombre": r.get("unidad_nombre"),
        "origen_rid": r["rid"],
        "fecha": date.today().isoformat(),
        "estado": "pendiente"
    }
    tareas.append(tarea)
    save_json(TAREAS, tareas)
    cal_write(CAL_RES, f"UPDATE | {r['rid']} | {r['nombre']} — {r['unidad_nombre']} | {r['ingreso']} {CHECKIN_HHMM} -> {r['egreso']} {CHECKOUT_HHMM} | Checkout → LIMPIEZA")
    log("checkout", "reserva", r["rid"], antes="", despues=tarea, nota="")
    print("OK: Checkout registrado. Tarea de LIMPIEZA creada.")
    return 0

def cmd_marcar_activa(args):
    unidades = load_json(UNIDADES)
    u = resolve_unidad_by_name(unidades, args.unidad)
    if not u:
        print("Unidad no encontrada.")
        return 1
    antes = dict(u)
    u["estado"] = "ACTIVA"
    save_json(UNIDADES, unidades)
    log("unidad_activa", "unidad", u["id"], antes=antes, despues=u, nota="")
    print(f"OK: {u['nombre']} marcada ACTIVA.")
    return 0

# ---------- CLI ----------
def main():
    ensure_dirs()
    ap = argparse.ArgumentParser(description="CLI demo asistente (dry-run)")
    sub = ap.add_subparsers(dest="cmd")

    p1 = sub.add_parser("reservar_rapido")
    p1.add_argument("--nombre", required=True)
    p1.add_argument("--ingreso", required=True)   # YYYY-MM-DD
    p1.add_argument("--egreso", required=True)    # YYYY-MM-DD
    p1.add_argument("--pax", required=True, type=int)
    p1.add_argument("--camas_separadas", action="store_true")
    pr1 = sub.add_parser("ingresos_mes")
    pr1.add_argument("--mes", required=True)   # ej: 2025-01
    pr1.set_defaults(func=cmd_ingresos_mes)
    p1.set_defaults(func=cmd_reservar_rapido)

    p2 = sub.add_parser("completar_reserva")
    p2.add_argument("--rid", required=True)
    p2.add_argument("--dni")
    p2.add_argument("--tel")
    p2.add_argument("--localidad")
    pr2 = sub.add_parser("costo_proveedor_mes")
    pr2.add_argument("--mes", required=True)   # ej: 2025-01
    pr2.set_defaults(func=cmd_costo_proveedor_mes)
    p2.set_defaults(func=cmd_completar_reserva)

    p3 = sub.add_parser("cambiar_unidad")
    p3.add_argument("--rid", required=True)
    p3.add_argument("--unidad", required=True)  # nombre visible o unidad_#
    pr3 = sub.add_parser("ocupacion_mes")
    pr3.add_argument("--mes", required=True)               # ej: 2025-01
    pr3.add_argument("--total_unidades", required=True)    # ej: 18
    pr3.set_defaults(func=cmd_ocupacion_mes)
    p3.set_defaults(func=cmd_cambiar_unidad)

    p4 = sub.add_parser("agregar_desayuno")
    p4.add_argument("--rid", required=True)
    p4.add_argument("--normales", required=True, type=int)
    p4.add_argument("--sin_tacc", required=True, type=int)
    p4.set_defaults(func=cmd_agregar_desayuno)

    p5 = sub.add_parser("reprogramar")
    p5.add_argument("--rid", required=True)
    p5.add_argument("--ingreso", required=True)
    p5.add_argument("--egreso", required=True)
    p5.set_defaults(func=cmd_reprogramar)

    p6 = sub.add_parser("checkout")
    p6.add_argument("--rid", required=True)
    p6.set_defaults(func=cmd_checkout)

    p7 = sub.add_parser("marcar_activa")
    p7.add_argument("--unidad", required=True)  # nombre visible o unidad_#
    p7.set_defaults(func=cmd_marcar_activa)

    p8 = sub.add_parser("registrar_senia")
    p8.add_argument("--rid", required=True)
    p8.add_argument("--monto", required=True, type=int)
    p8.add_argument("--medio", required=True)
    p8.set_defaults(func=cmd_registrar_senia)

    p9 = sub.add_parser("confirmar_reserva")
    p9.add_argument("--rid", required=True)
    p9.add_argument("--late", action="store_true")
    p9.set_defaults(func=cmd_confirmar_reserva)

    p10 = sub.add_parser("cancelar_reserva")
    p10.add_argument("--rid", required=True)
    p10.add_argument("--motivo", default="")
    p10.set_defaults(func=cmd_cancelar_reserva)

    ps1 = sub.add_parser("agregar_servicio")
    ps1.add_argument("--rid", required=True)
    ps1.add_argument("--key", required=True)          # ej: servicio_2
    ps1.add_argument("--personas", required=True, type=int)
    ps1.set_defaults(func=cmd_agregar_servicio)

    ps2 = sub.add_parser("quitar_servicio")
    ps2.add_argument("--rid", required=True)
    ps2.add_argument("--key", required=True)          # key o nombre visible
    ps2.set_defaults(func=cmd_quitar_servicio)

    pd = sub.add_parser("preguntar_disponibilidad")
    pd.add_argument("--tipo", required=True)
    pd.add_argument("--ingreso", required=True)
    pd.add_argument("--egreso", required=True)
    pd.add_argument("--pax", default=2)
    pd.add_argument("--amenidad")    # ej: camas_separadas
    pd.add_argument("--max", default=3)
    pd.set_defaults(func=cmd_preguntar_disponibilidad)

    dbg = sub.add_parser("debug_disponibilidad")
    dbg.add_argument("--tipo", required=True)
    dbg.add_argument("--ingreso", required=True)
    dbg.add_argument("--egreso", required=True)
    dbg.add_argument("--pax", default=2)
    dbg.add_argument("--amenidad")
    dbg.set_defaults(func=cmd_debug_disponibilidad)

    # agendar_recordatorio
    ar = sub.add_parser("agendar_recordatorio")
    ar.add_argument("--titulo", required=True)
    ar.add_argument("--cuando")            # "YYYY-MM-DD HH:MM"
    ar.add_argument("--diario")            # "HH:MM"
    ar.add_argument("--semanal")           # "LU,MI,VI"
    ar.add_argument("--hora")              # "HH:MM" (para semanal)
    ar.add_argument("--nota")
    ar.set_defaults(func=cmd_agendar_recordatorio)

    # listar_recordatorios
    lr = sub.add_parser("listar_recordatorios")
    lr.add_argument("--estado")  # pendiente|completado|cancelado
    lr.add_argument("--hoy", action="store_true")
    lr.add_argument("--tipo", choices=["GENERAL", "LIMPIEZA"])
    lr.set_defaults(func=cmd_listar_recordatorios)

    # completar_recordatorio
    cr = sub.add_parser("completar_recordatorio")
    cr.add_argument("--id", required=True)
    cr.set_defaults(func=cmd_completar_recordatorio)

    # cancelar_recordatorio
    xr = sub.add_parser("cancelar_recordatorio")
    xr.add_argument("--id", required=True)
    xr.add_argument("--motivo")
    xr.set_defaults(func=cmd_cancelar_recordatorio)

    args = ap.parse_args()
    if not hasattr(args, "func"):
        ap.print_help()
        return 1
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())

