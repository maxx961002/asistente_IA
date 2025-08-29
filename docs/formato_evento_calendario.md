1) Dónde se crean/actualizan

Reservas huéspedes: CALENDAR_ID (config).

Housekeeping (limpieza/mantenimiento): HOUSEKEEPING_CALENDAR_ID (opcional; si no está, las tareas viven en la tarjeta).

Proveedores (p. ej., Desayuno): email_calendar del proveedor definido en la tarjeta del servicio.

2) Evento de RESERVA (huésped)
Título (template)
{NOMBRE_HUESPED} — {NOMBRE_UNIDAD}


Si aún no hay unidad:
{NOMBRE_HUESPED} — Sin asignar ({TIPO_SOLICITADO})

Horario

Inicio: {CHECKIN_HORA} del día Ingreso

Fin: {CHECKOUT_HORA} del día Egreso

Late checkout ON: extender Egreso operativo (ej.: +0.5 noches) para bloquear limpieza si corresponde.

Descripción (template)
RID: {RID}
Tipo: {TIPO_SOLICITADO}
Unidad: {NOMBRE_UNIDAD} ({UNIDAD_ID})
Personas: {PAX}
Amenidades: {AMENIDADES_ACTIVAS}    # ej.: Camas separadas
Servicios: {SERVICIOS_RESUMEN}      # ej.: Desayuno 1 normal / 1 sin TACC

Cliente
  Nombre: {NOMBRE}
  DNI: {DNI}
  Tel: {TEL}
  Localidad: {LOCALIDAD}

Noches: {NOCHES}   # +0.5 si late
Seña: {SEÑA_MONTO} {SEÑA_MEDIO}
Resto: {RESTO}

Notas: {NOTAS_RESERVA}

Color del evento

Por estado:

Confirmado → ESTADOS.Confirmado

Pendiente / PendienteDatos → ESTADOS.Pendiente

Reprogramar → ESTADOS.Reprogramar

Cancelado → ESTADOS.Cancelado (opcional: borrar evento)

(Opcional) Por unidad: si preferís, mapear color por unidad/tipo en vez de estado.

Reglas de actualización

Cambian fechas / late: recrear o mover el evento completo.

Cambia unidad/tipo/amenidad/servicios/personas: actualizar descripción; si unidad cambia, verificar choques y mover a la nueva.

Cancelar: eliminar el evento (o marcar “Cancelado” en título y color si preferís histórico visible).

3) Evento de HOUSEKEEPING (opcional pero recomendado)
Disparadores

Al Checkout de una reserva → crear tarea LIMPIEZA {NOMBRE_UNIDAD} para el día del checkout, después de {CHECKOUT_HORA}.

Al poner REPARACION en una unidad → crear tarea REPARACION {NOMBRE_UNIDAD} con la nota.

Título (templates)

Limpieza: LIMPIEZA — {NOMBRE_UNIDAD}

Reparación: REPARACION — {NOMBRE_UNIDAD}

Descripción
Unidad: {NOMBRE_UNIDAD} ({UNIDAD_ID})
Origen: {RID} (si viene de checkout)
Notas: {NOTA_MANTENIMIENTO}

Colores sugeridos

Limpieza: verde suave / azul claro

Reparación: naranja / rojo suave

Cierre

Acción “Marcar lista (ACTIVA)” → borrar/complete el evento de housekeeping o marcarlo como “Done”.

4) Evento de PROVEEDOR (ej. Desayuno)
Cuándo se crea/actualiza

Cuando en una reserva confirmada agregás el servicio con cantidad/subtipo.

Calendario destino

email_calendar del proveedor (definido en la tarjeta del servicio).

Título (template)
{TITULO_TEMPLATE_DEL_SERVICIO}
# Ej. "Desayuno {fecha} — {normales} normal / {sin_tacc} sin TACC"

Horario

Dentro de horario/ventana configurada, por defecto el primer slot libre dentro de esa ventana.

Descripción
Reserva: {RID}
Huésped: {NOMBRE} — {TEL}
Personas: {PAX}
Detalle: {DETALLE_SERVICIO}    # ej. 1 normal, 1 sin TACC
Unidad: {NOMBRE_UNIDAD}
Notas: {NOTAS_SERVICIO}

Reglas

Cambia la cantidad/subtipo → actualizar evento proveedor.

Quitar servicio → eliminar el evento proveedor.

5) Casos borde (qué hace el bot)

Unidad no disponible al cambiar: sugiere hasta 3 alternativas del mismo tipo; si no hay, intenta OVERFLOW compatible con amenidades.

Amenidad solicitada no permitida en la unidad destino: ofrece otra unidad compatible o quitar amenidad.

Confirmar con datos incompletos (PendienteDatos): crea evento con datos mínimos (sin DNI/tel); deja recordatorio para completar y actualizar descripción.

DNI duplicado al completar: propone vincular con la ficha existente (o fusionar con soporte/admin).

6) Ejemplos rápidos
A) Reserva confirmada sin amenidades

Título: María Gómez — Loft-1

Descripción: incluye RID, PAX=2, Desayuno 2 normal, Tel/DNI/Localidad, Resto…

B) Cambio de unidad

Read-back: “Mover a Depto A (unidad_9, Dpto 4/5). ¿Confirmo?”

Al confirmar: evento se mueve a Depto A; descripción actualizada.

C) Checkout → Limpieza

Crea en HOUSEKEEPING_CALENDAR_ID: LIMPIEZA — Loft-1 con referencia al RID.

“Marcá Loft-1 ACTIVA” → cierra/borra ese evento.

7) Check final (listo para QA)

Ver que crear_reserva / confirmar / reprogramar / cambiar_unidad / cancelar impacten el evento como arriba.

Ver que Desayuno cree/actualice/borre el evento del proveedor.

Ver que Checkout cree LIMPIEZA y “Marcar lista” lo cierre.