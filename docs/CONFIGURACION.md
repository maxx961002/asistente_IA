# BRANDING 
APP_NAME: Complejo La Yema

ID_PREFIX: YEM
ID_DATE_SOURCE: captura          # captura | ingreso | confirmacion (origen de la fecha para el RID)
PHONE_REGION: AR                 # normalización de teléfonos (ej. AR = Argentina)

LOGO_URL:

COLOR_BACKGROUND: #fff6e5
COLOR_CHAT: #f7f7f7
COLOR_CARD: #ffffff
COLOR_BUTTON: #16a34a
COLOR_TEXT_PRIMARY: #0f172a
COLOR_TEXT_SECONDARY: #334155

ESTADOS (colores): 
  Confirmado:   #22C55E
  Pendiente:    #F59E0B
  Cancelado:    #EF4444
  Reprogramar:  #6366F1

SEMAFORO_CLIENTE: 
  Verde:   #22C55E
  Amarillo:#6366F1    # (si preferís amarillo real: #F59E0B)
  Rojo:    #EF4444


# CALENDARIO & HORARIOS
CALENDAR_ID: maxx96pro@gmail.com
EVENTOS_CALENDAR: ON

CHECKIN_HORA (hh:mm): 12:00
CHECKOUT_HORA (hh:mm): 10:00

LATE_CHECKOUT_HHMM: 18:00
LATE_CHECKOUT_EXTRA_NOCHES: 0.5
LATE_CHECKOUT_EXTIENDE_DIA: ON


# UNIDADES & TIPOS

LISTA DE UNIDADES 

# id        | nombre     | tipo comercial                  | capacidad | prioridad | activo
unidad_1    | Loft-1     | Loft 2 personas                 | 2         | 1         | ON
unidad_2    | Loft-2     | Loft 2 personas                 | 2         | 1         | ON
unidad_3    | Loft-3     | Loft 2 personas                 | 2         | 1         | ON
unidad_4    | Loft-4     | Loft 2 personas                 | 2         | 1         | ON
unidad_5    | Loft-6     | Loft 2 personas                 | 2         | 1         | ON
unidad_6    | Loft-7     | Loft 2 personas                 | 2         | 1         | ON
unidad_7    | Loft-5     | Loft 3 y 4 personas             | 4         | 1         | ON
unidad_8    | Loft-8     | Loft 3 y 4 personas             | 4         | 1         | ON

unidad_9    | Dpto-A     | Departamento 4 y 5 personas     | 5         | 1         | ON
unidad_10   | Dpto-B     | Departamento 4 y 5 personas     | 5         | 1         | ON
unidad_11   | Dpto-C     | Departamento 4 y 5 personas     | 5         | 1         | ON
unidad_12   | Dpto-D     | Departamento 4 y 5 personas     | 5         | 1         | ON

unidad_13   | Cab-F      | Cabaña 2 y 3 personas           | 3         | 1         | ON
unidad_14   | Cab-G      | Cabaña 2 y 3 personas           | 3         | 1         | ON

unidad_15   | Cab-8-E    | Cabaña hasta 8 personas         | 8         | 1         | ON

unidad_16   | Sor-Rojo   | Habitación Sorelle              | 3         | 1         | ON
unidad_17   | Sor-Azul   | Habitación Sorelle              | 3         | 1         | ON
unidad_18   | Sor-Marron | Habitación Sorelle              | 3         | 1         | ON

unidad_19   |            | Por definir                     | 0         | 1         | OFF
unidad_20   |            | Por definir                     | 0         | 1         | OFF
                                                                     

TIPOS COMERCIALES 
  Loft 2 personas
  Loft 3 y 4 personas
  Cabaña 2 y 3 personas
  Departamento 4 y 5 personas
  Cabaña hasta 8 personas
  Habitación Sorelle

CAPACIDAD POR TIPO 
  Loft 2 personas → 1/2         
  Loft 3 y 4 personas → 2/4
  Cabaña 2 y 3 personas → 1/3
  Departamento 4 y 5 personas → 2/5
  Cabaña hasta 8 personas → 4/8 
  Habitación Sorelle → 1/3      

MAPA TipoSolicitado → ListaUnidades 
  Loft 2 personas → [unidad_1, unidad_2, unidad_3, unidad_4, unidad_5, unidad_6]
  Loft 3 y 4 personas → [unidad_7, unidad_8]
  Departamento 4 y 5 personas → [unidad_9, unidad_10, unidad_11, unidad_12]
  Cabaña 2 y 3 personas → [unidad_13, unidad_14]
  Cabaña hasta 8 personas → [unidad_15]
  Habitación Sorelle → [unidad_16, unidad_17, unidad_18]

# CONTENIDOS / AMENIDADES POR UNIDAD (hasta 4)
CONTENIDOS_UNIDAD_ENABLED: ON

# Política de overflow: si el contenido es requerido al sugerir,
# probar overflow SOLO si la unidad fallback también lo tiene.
CONTENIDOS_RESPETA_OVERFLOW: ON

# Catálogo de contenidos (slots configurables)
CONTENIDOS_CATALOGO:
  - id: unidad_cont_1
    nombre: Camas separadas
    filtra_sugerencias: ON            # si el huésped lo pide, filtra solo unidades que lo tienen
    politica_precio: SIN_RECARGO      # SIN_RECARGO | RECARGO_FIJO_POR_ESTADIA | RECARGO_FIJO_POR_NOCHE
    recargo_monto: 0
    tarea_operativa:
      enabled: ON
      descripcion: "Preparar camas separadas (twin/split)"
      duracion_min: 20
      antelacion_min: 60
    permitido_por_tipo:
      Loft 2 personas: ON
      Loft 3 y 4 personas: ON
      Departamento 4 y 5 personas: ON
      Cabaña 2 y 3 personas: OFF
      Cabaña hasta 8 personas: OFF
      Habitación Sorelle: OFF
    unidades_admitidas:
      - unidad_1
      - unidad_4
      - unidad_7
      - unidad_9
      - unidad_10
      - unidad_12

  - id: unidad_cont_2
    nombre: Jacuzzi                       # La Yema: sin unidades; para otros hoteles
    filtra_sugerencias: ON
    politica_precio: SIN_RECARGO          # si otro hotel cobra, cambialo a RECARGO_* y monto
    recargo_monto: 0
    tarea_operativa:
      enabled: OFF
    permitido_por_tipo:
      Loft 2 personas: ON
      Loft 3 y 4 personas: ON
      Departamento 4 y 5 personas: ON
      Cabaña 2 y 3 personas: ON
      Cabaña hasta 8 personas: ON
      Habitación Sorelle: ON
    unidades_admitidas: []                # vacío = no disponible en La Yema

  - id: unidad_cont_3
    nombre: ""                            # libre
    filtra_sugerencias: ON
    politica_precio: SIN_RECARGO
    recargo_monto: 0
    tarea_operativa:
      enabled: OFF
    permitido_por_tipo:
      Loft 2 personas: ON
      Loft 3 y 4 personas: ON
      Departamento 4 y 5 personas: ON
      Cabaña 2 y 3 personas: ON
      Cabaña hasta 8 personas: ON
      Habitación Sorelle: ON
    unidades_admitidas: []

  - id: unidad_cont_4
    nombre: ""                            # libre
    filtra_sugerencias: ON
    politica_precio: SIN_RECARGO
    recargo_monto: 0
    tarea_operativa:
      enabled: OFF
    permitido_por_tipo:
      Loft 2 personas: ON
      Loft 3 y 4 personas: ON
      Departamento 4 y 5 personas: ON
      Cabaña 2 y 3 personas: ON
      Cabaña hasta 8 personas: ON
      Habitación Sorelle: ON
    unidades_admitidas: []


# SUSTITUCIONES (OVERFLOW)
OVERFLOW_ENABLED: ON
OVERFLOW_REGLAS:
  - tipo_solicitado: Loft 2 personas
    usar_fallback_de: [unidad_7, unidad_8]
    condicion: cuando_primaria_sin_disponibilidad
    precio: TIPO_SOLICITADO
    prioridad_fallback: round_robin
    limite_porcentaje_mes: sin_limite
    nota_confirmacion: "Upgrade cortesía a loft mayor, facturado como 2 personas."


# DISPONIBILIDAD
AVAIL_PRIORIDAD: min_unidades          # o min_costo
AVAIL_MAX_PROPUESTAS: 3

BLOQUEOS (si hay mantenimiento):
  # unidad | desde | hasta
  # (dejar vacío si no hay)


# TARIFAS & VENTANAS
TARIFAS ALOJAMIENTO (por tipo + personas): 
  Loft 2 personas
    2 pax → $75.000 por noche (precio normal)
    2 pax → $95.000 por noche (precio especial)

  Loft 3 y 4 personas
    3 pax → $92.000 por noche (normal)
    3 pax → $120.000 por noche (especial)
    4 pax → $125.000 por noche (normal)
    4 pax → $165.000 por noche (especial)

  Cabaña 2 y 3 personas
    2 pax → $85.000 por noche (precio normal)
    2 pax → $110.000 por noche (precio especial)
    3 pax → $105.000 por noche (normal)
    3 pax → $135.000 por noche (especial)

  Departamento 4 y 5 personas
    4 pax → $135.000 por noche (normal)
    4 pax → $170.000 por noche (especial)
    5 pax → $145.000 por noche (normal)
    5 pax → $190.000 por noche (especial)

  Cabaña hasta 8 personas
    6 pax → $195.000 por noche (normal)
    6 pax → $255.000 por noche (especial)
    7 pax → $225.000 por noche (normal)
    7 pax → $295.000 por noche (especial)
    8 pax → $250.000 por noche (normal)
    8 pax → $330.000 por noche (especial)

  Habitación Sorelle
    2 pax → $75.000 por noche (normal)
    2 pax → $95.000 por noche (especial)
    3 pax → $92.000 por noche (normal)    
    3 pax → $120.000 por noche (especial) 

VENTANAS (desde–hasta + regla: precio especial o % descuento):
  # Ejemplos (ajustar a tus fechas)
  # 01/01–31/01 → precio especial
  # 01/07–31/07 → precio especial
  # 28/03–31/03 (Semana Santa) → precio especial
  # Feriados largos → 15% descuento

DESCUENTOS (si aplica):
  # Ej.: 7 noches o más → 10% descuento


# SERVICIOS (SLOTS GENÉRICOS)
SERVICIOS_ENABLED: ON
SERVICIOS_SUMAR_AL_RESTO_DEFAULT: ON
SERVICIO_VENTANAS (horas):               # (no aplica en La Yema hoy)
SERVICIO_DURACION_MIN: 45
SERVICIO_PRIVACIDAD: MINIMA

# Precios: UNITARIO = precio_por_persona * cantidad_personas.
# Si TABLA tuviera valores, TABLA gana; si falta N, cae a UNITARIO.

SERVICIOS_CATALOGO:
  - key: servicio_1
    nombre: Desayuno
    categoria: alimentacion
    aplica_a_tipos: [TODOS]
    modo_precio: UNITARIO
    precio_unitario_pp: 0                # Sin costo para el huésped
    precios_por_personas: {}
    sumar_al_resto: ON
    visible_en_onboarding: ON
    subtipos:
      - id: normal
        label: Normal
        costo_proveedor_por_persona: 2000
      - id: sin_tacc
        label: Sin TACC
        costo_proveedor_por_persona: 2500
    proveedor:
      nombre: Desayunos Anita
      email_calendar: desayunos.layema@gmail.com
      horario: 07:30-09:30
      crear_evento_horas_antes: 24
      recordatorio_min_antes: 60
      ubicacion: Cocina principal
      titulo_template: "Desayuno {fecha} — {normales} normal / {sin_tacc} sin TACC"

  - key: servicio_2
    nombre: ""
    categoria: extra
    aplica_a_tipos: [TODOS]
    modo_precio: UNITARIO
    precio_unitario_pp: 0
    precios_por_personas: {}
    sumar_al_resto: ON
    visible_en_onboarding: ON

  key: servicio_3
    nombre: ""
    categoria: extra
    aplica_a_tipos: [TODOS]
    modo_precio: UNITARIO
    precio_unitario_pp: 0
    precios_por_personas: {}
    sumar_al_resto: ON
    visible_en_onboarding: ON

 key: servicio_4
    nombre: ""
    categoria: extra
    aplica_a_tipos: [TODOS]
    modo_precio: UNITARIO
    precio_unitario_pp: 0
    precios_por_personas: {}
    sumar_al_resto: ON
    visible_en_onboarding: ON

 key: servicio_5
    nombre: ""
    categoria: extra
    aplica_a_tipos: [TODOS]
    modo_precio: UNITARIO
    precio_unitario_pp: 0
    precios_por_personas: {}
    sumar_al_resto: ON
    visible_en_onboarding: ON

 key: servicio_6
    nombre: ""
    categoria: extra
    aplica_a_tipos: [TODOS]
    modo_precio: UNITARIO
    precio_unitario_pp: 0
    precios_por_personas: {}
    sumar_al_resto: ON
    visible_en_onboarding: ON

 key: servicio_7
    nombre: ""
    categoria: extra
    aplica_a_tipos: [TODOS]
    modo_precio: UNITARIO
    precio_unitario_pp: 0
    precios_por_personas: {}
    sumar_al_resto: ON
    visible_en_onboarding: ON

 key: servicio_8
    nombre: ""
    categoria: extra
    aplica_a_tipos: [TODOS]
    modo_precio: UNITARIO
    precio_unitario_pp: 0
    precios_por_personas: {}
    sumar_al_resto: ON
    visible_en_onboarding: ON

 key: servicio_9
    nombre: ""
    categoria: extra
    aplica_a_tipos: [TODOS]
    modo_precio: UNITARIO
    precio_unitario_pp: 0
    precios_por_personas: {}
    sumar_al_resto: ON
    visible_en_onboarding: ON

 key: servicio_10
    nombre: ""
    categoria: extra
    aplica_a_tipos: [TODOS]
    modo_precio: UNITARIO
    precio_unitario_pp: 0
    precios_por_personas: {}
    sumar_al_resto: ON
    visible_en_onboarding: ON

# MAKE
MAKE_ENABLED: OFF
WHATSAPP_FROM:
WEBHOOKS:
  confirmacion:
  pre_checkin:
  codigos_reglas:
  post_checkout:
PLANTILLAS:
  # Pegar aquí tus textos con {placeholders}: {NOMBRE}, {RID}, {INGRESO}, {UNIDAD}, etc.

# RECORDATORIOS & LISTAS
RECORDATORIOS_ENABLED: ON
RECORDATORIOS_CANAL_DEFAULT: CHAT
RECORDATORIOS_HORA_DEFECTO: 09:00
RECORDATORIOS_SNOOZE_MIN: [5,10,30,60]
RECORDATORIOS_TZ: auto



# Política de cancelación manual (se aplica a recordatorios puntuales y recurrentes)
RECORDATORIOS_CANCEL_MOTIVO_REQUIRED: ON          # al cancelar, el bot pide motivo
RECORDATORIOS_LOG_EN_BITACORA: ON                 # guarda cancelación+motivo en "Registro/Bitácora"
RECORDATORIOS_LOG_TIPO: recordatorio              # etiqueta para filtrar en reportes
                   # permite compartir por WhatsApp/Email si MAKE_ENABLED/EMAIL activo


# CONTROL & LIMPIEZA
TOTAL_UNIDADES: 18               # lofts-8 + Dpto-4 + Cab-23-2 + Cab-8-1 + Sorelle-3
CONTROL_COMISION_PCT: 3
ARCHIVADO_CLIENTES_MES: 36


# REGLAS SEMAFORO
Verde: excelente huesped
Amarillo: inconvenientes en su ultima reserva
Rojo: no admitido
