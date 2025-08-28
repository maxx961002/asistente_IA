Convenciones generales

Lectura en voz alta (read-back): antes de ejecutar algo que impacta precio, unidad o calendario, el bot resume lo entendido y pide confirmación.

Relleno de slots: si faltan datos, pregunta; si hay defaults en CONFIGURACION.md, los usa y lo avisa.

Identificación de cliente: si das solo nombre, intenta matchear con DNI/Tel/Nombre; si hay dudas, propone candidatos y pide DNI o Tel.

Estados de reserva: Pendiente → Confirmado → (Reprogramar) → Cancelado.

Asignación de unidad: usa MAPA Tipo→Unidades y reglas de OVERFLOW; respeta contenidos/amenidades (p. ej., camas separadas) si fueron solicitadas.

1) crear_reserva

Qué hace: crea una reserva nueva.

Frases típicas

“Cargá una reserva para Juan Pablo del 24/08 al 26/08 para 2 personas.”

“Reservá Departamento 4–5p para María Gómez, 20–23/09, 4 pax, camas separadas.”

Slots

Requeridos: nombre_huesped, ingreso, egreso, personas.

Opcionales: tipo_solicitado, preferencias (ej. camas separadas), servicios (ej. desayuno normal/sin TACC), seña_monto, seña_medio, tel, dni, localidad, late_checkout.

Derivados: RID, unidad_asignada (o “Sin asignar”), resto.

Modo Rápido (express)

Si no decís tipo, se infiere por personas (ej.: 2 pax → “Loft 2 personas”), valida contra el MAPA.

Unidad: autoasigna una libre del tipo; si no hay, intenta OVERFLOW permitido.

Servicios por defecto (La Yema): servicio_1 = Desayuno a $0 → asume normales = personas, sin_tacc = 0 (editable luego).

Preferencias: ninguna (salvo que la pidas).

Seña: si no informás, queda sin seña; Resto = total.

Cliente: busca por nombre; si no existe, pide DNI o Tel y crea ficha mínima (Nombre, DNI, Tel, Localidad).

Read-back:
“Voy a crear: {NOMBRE}, {INGRESO–EGRESO}, {PAX}, {TIPO}, Unidad: auto, Desayuno {normales} normal. Resto = $X. ¿Confirmo así rápido o querés completar (seña, preferencias, otra unidad/servicio)?”

Modo Completo

Tras el read-back, ofrece completar: tipo, unidad, preferencias, servicios (reparto normal/sin TACC), seña (monto/medio), mensajes (si MAKE_ENABLED: ON).

Validaciones

Egreso > Ingreso, capacidad tipo/unidad, choques de calendario, compatibilidad de amenidades (p. ej., camas separadas), OVERFLOW que respeta amenidades si fueron pedidas.

2) abrir_reserva

Frases: “Abrí la ficha de María Gómez / DNI 34.567.890 / RID YEM-20240920-001.”
Slots: identificador (nombre+DNI/fecha, DNI/Tel, o RID).

3) cambiar_unidad

Frases: “En la reserva de María, pasá a unidad_7.” / “Movela a Loft 5.”
Slots: reserva_id, nueva_unidad.
Notas: verifica disponibilidad/amenidades; read-back y confirma; actualiza calendario.

4) editar_datos_huesped

Frases: “Actualizá el teléfono de María a +54 9 11 2222-3333.”
Slots: reserva_id o cliente_id, campo, nuevo_valor.
Reglas: DNI/Tel requieren confirmación adicional.

5) agregar_servicio / quitar_servicio

Frases: “Sumá Desayuno: 1 sin TACC y 1 normal a Juan Pablo.” / “Quitá el desayuno de María.”
Slots: reserva_id, servicio_key/nombre, personas_por_subtipo.
Notas (La Yema): precio al huésped $0; se computa costo proveedor ($2000 normal, $2500 sin TACC).

6) set_preferencia / quitar_preferencia

Frases: “Agregá camas separadas a Juan.” / “Sacá camas separadas.”
Notas: si la unidad actual no admite, sugiere cambio de unidad compatible (respeta OVERFLOW).

7) confirmar_reserva / cancelar_reserva / reprogramar_reserva

confirmar_reserva: crea/actualiza evento en CALENDAR_ID y dispara mensajes si están activos.

cancelar_reserva: libera calendario; puede pedir motivo (guarda en bitácora).

reprogramar_reserva: cambia fechas; mantiene pax/servicios/preferencias; valida disponibilidad.

Frases: “Confirmá / Cancelá / Reprogramá la reserva de María al 22/09.”

8) abrir_unidad / estado_unidad / set_activa

Frases: “Mostrame unidad_1 / Loft-1.” · “Poné Loft-1 en REPARACION (nota: cambiar mixer).” · “Marcala ACTIVA.”
Efectos: bloqueos operativos, exclusión de sugerencias, recordatorios para volver a ACTIVA si querés.

9) preguntar_disponibilidad

Frases: “¿Qué Loft 2p hay libres para 12–14/10?”
Salida: lista priorizada; excluye mantenimiento/limpieza; si no hay, propone OVERFLOW.

10) tareas_hoy / marcar_limpia

Frases: “¿Cuántas unidades hay que limpiar hoy y cuáles?” · “Marcá Loft-1 como lista (ACTIVA).”
Efecto: checkout → LIMPIEZA + tarea en HOUSEKEEPING_CALENDAR_ID; “lista” → ACTIVA.

11) ver_calendario

Frases: “Mostrame el calendario del finde / semana que viene.”
Salida: eventos de check-in/out + (si aplica) servicios/housekeeping.

12) Reportes

ingresos_mes: “Ingresos de septiembre.”

costo_proveedor: “Gasto en Desayunos esta semana.”

ocupacion: “Ocupación del mes y esta semana.”

mejores_clientes: “Top 10 clientes por estadías en 12 meses.”

Frases sinónimas (atajos)

crear_reserva: “cargá”, “reservá”, “agendá”.

abrir_reserva/unidad: “abrí”, “mostrá”, “mostrame”.

cambiar_unidad: “cambiá”, “pasá a”, “mové a”.

confirmar: “confirmá”, “dejalo confirmado”.

cancelar: “cancelá”, “dalo de baja”.

marcar_limpia: “dejala lista”, “marcala activa”.

Defaults del Modo Rápido

Tipo inferido por personas (valida con MAPA).

Unidad autoasignada; si pediste amenidad (p. ej., camas separadas), filtra solo unidades que la tengan; si no hay, aplica OVERFLOW compatible.

Servicios (La Yema): Desayuno $0 → normales = pax, sin_tacc = 0.

Seña: si no decís, sin seña (Resto = total).

Cliente: si no existe, pide DNI/Tel y crea ficha mínima.

Recordatorio de verificación: si usaste Modo Rápido, crea “Verificar datos reserva” para ajustar detalles luego.

Validaciones & salvavidas

Fechas válidas; capacidad min/max; choques de calendario; compatibilidad de amenidades; OVERFLOW que respeta amenidades; duplicados de huésped (desambiguación por DNI/Tel).