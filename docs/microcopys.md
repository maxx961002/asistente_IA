Confirmación (estándar)

Read-back (impacta precio/unidad/calendario):
“Entiendo: {NOMBRE}, {INGRESO–EGRESO}, {PAX}, {TIPO}, {UNIDAD}. {DETALLE_EXTRA}. ¿Confirmo?”

OK ejecutado:
“Listo ✅ {ACCION}. RID {RID}.”

Cancelado por el usuario:
“Perfecto, no hice cambios.”

Crear reserva

Read-back (modo rápido):
“Voy a crear: {NOMBRE}, {FECHAS}, {PAX}, {TIPO}, Unidad: auto. Desayuno {NORM} normal. Resto = ${RESTO}. ¿Confirmo rápido o querés completar?”

Creada (completa):
“Reserva creada ✅ RID {RID}. Evento en calendario actualizado.”

Creada (PendienteDatos):
“Reserva cargada como Pendiente de completar. ¿Programo recordatorio para pedir DNI/Tel/Localidad?”

Completar reserva / vincular cliente

Match DNI exacto:
“Coincide con {NOMBRE} (DNI {DNI}). ¿Vinculo esta reserva a su ficha?”

Match por Tel (1 opción):
“El teléfono coincide con {NOMBRE} (DNI {DNI}). ¿Vinculo?”

Varios candidatos:
“Encontré varios {NOMBRE}. Elegí: {LISTA: NOMBRE – DNI – Localidad – visitas}.”

Sin coincidencias:
“No encontré coincidencias. Creo cliente nuevo con esos datos. ¿Confirmo?”

Cambiar unidad (por nombre visible o alias)

Read-back:
“Mover a {NOMBRE_UNIDAD} ({UNIDAD_ID}, {TIPO}). ¿Confirmo?”

No disponible:
“{UNIDAD} no está disponible en esas fechas. Te sugiero: {ALT1}, {ALT2}, {ALT3}. ¿Elijo una?”

Amenidad incompatible (p. ej., camas separadas):
“{UNIDAD} no admite {AMENIDAD}. ¿Querés probar {UNIDAD_COMPATIBLE} o quitar la preferencia?”

Reprogramar

Read-back:
“Reprogramo {RID}: {FECHAS_ANTES} → {FECHAS_NUEVAS}. Noches: {N_ANTES} → {N_NUEVAS}. ¿Confirmo?”

Hecho:
“Listo ✅ reprogramado. Calendario actualizado.”

Servicios (Desayuno La Yema)

Agregar:
“Agrego Desayuno: {NORM} normal / {SINT} sin TACC (precio huésped $0). Costo proveedor: ${COSTO}. ¿Confirmo?”

Quitar:
“Quito Desayuno. ¿Confirmo?”

Pagos

Seña:
“Registro seña ${MONTO} por {MEDIO}. Nuevo Resto: ${RESTO}. ¿Confirmo?”

Housekeeping

Checkout:
“Registro checkout de {RID}. La unidad pasa a LIMPIEZA. ¿Aviso al equipo?”

Marcar lista:
“Perfecto, {UNIDAD} vuelve a ACTIVA.”

Búsqueda / homónimos

Buscar cliente:
“Te muestro {N} resultado(s) para {CRITERIO}.”

Tip educativo:
“Tip: podés decir DNI o Tel para reservar en un paso. También ‘Nombre + Localidad’.”

Errores y validaciones

Fechas inválidas:
“La fecha de egreso debe ser posterior al ingreso.”

Capacidad:
“{PAX} excede la capacidad de {TIPO/UNIDAD} ({CAP_MIN}/{CAP_MAX}).”

Choque de calendario:
“La unidad tiene otra reserva en ese rango. Probá: {ALT1}, {ALT2}.”

DNI duplicado:
“Ese DNI ya existe. ¿Vinculo a la ficha existente o querés fusionar (admin)?”