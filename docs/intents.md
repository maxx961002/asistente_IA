Convenciones generales

Lectura en voz alta (read-back): antes de ejecutar algo que impacta precio, unidad o calendario, el bot resume lo entendido y pide confirmación.

Relleno de slots: si faltan datos, pregunta; si hay defaults en CONFIGURACION.md, los usa y lo avisa.

Identificación de cliente (prioridad): DNI exacto > Tel normalizado (PHONE_REGION) > Nombre+Localidad > Nombre (si hay dudas, propone candidatos y pide DNI o Tel).

Estados de reserva: PendienteDatos → Pendiente → Confirmado → (Reprogramar) → Cancelado.

Flags de reserva:

datos_completos: ON/OFF

cliente_vinculado: ON/OFF

sugerencias_cliente: [] (candidatos por DNI/Tel/Nombre)

Asignación de unidad: usa MAPA Tipo→Unidades y reglas de OVERFLOW; respeta contenidos/amenidades (p. ej., camas separadas) si fueron solicitadas.

Fechas naturales que entiende: “este viernes”, “el finde”, “del 24 al 26”, “2 noches” (si decís noches, el egreso = ingreso + noches).

Bitácora: todo cambio relevante registra quién/cuándo y antes→después (y motivo si corresponde).

1) crear_reserva

Qué hace: crea una reserva nueva.

Frases típicas

“Cargá una reserva para Juan Pablo del 24/08 al 26/08 para 2 personas.”

“Reservá Departamento 4–5p para María Gómez, 20–23/09, 4 pax, camas separadas.”

“Reservá para Juan Topo, tel +54 9 3564…, este viernes, 2 noches, 2 personas.”

Slots

Requeridos: nombre_huesped/cliente, ingreso, egreso (o noches), personas.

Opcionales: tipo_solicitado, preferencias (camas separadas), servicios (desayuno normal/sin TACC), seña_monto, seña_medio, tel, dni, localidad, late_checkout.

Derivados: RID, unidad_asignada (o “Sin asignar”), resto.

Modo Rápido (express)

Si no decís tipo, se infiere por personas (ej.: 2 pax → “Loft 2 personas”) y se valida contra el MAPA.

Unidad: autoasigna una libre; si no hay, intenta OVERFLOW permitido.

Servicios (La Yema): servicio_1 = Desayuno a $0 → normales = personas, sin_tacc = 0 (editable luego).

Seña: si no informás, queda sin seña; Resto = total.

Cliente: busca por DNI/Tel/Nombre+Localidad; si no existe, pide DNI o Tel y crea ficha mínima.

Read-back:
“Voy a crear: {NOMBRE}, {INGRESO–EGRESO}, {PAX}, {TIPO}, Unidad: auto, Desayuno {normales} normal. Resto = $X. ¿Confirmo rápido o querés completar (seña, preferencias, otra unidad/servicio)?”

Modo Completo

Tras el read-back, permite ajustar tipo, unidad, amenidades, servicios (normal/sin TACC), seña y (si MAKE_ENABLED: ON) mensajes.

Validaciones

Egreso > Ingreso, capacidad tipo/unidad, choques de calendario, compatibilidad de amenidades, OVERFLOW respetando amenidades.

Si el usuario no aporta DNI/Tel en el momento, sugerir crear_reserva_rapida: deja la reserva en PendienteDatos y programa un recordatorio para completar.

2) crear_reserva_rapida

Qué hace: Crea reserva con mínimos (nombre, ingreso, egreso/noches, personas).

Frases

“Agendá rápido a Juan Pablo del 24/08 al 26/08 2 pax.”

Flujo

Genera RID, asigna tipo por pax y unidad auto (respeta overflow), setea servicios por defecto.

Estado = PendienteDatos, datos_completos=OFF.

Crea recordatorio “Completar datos de {RID} ({nombre})” para hoy (hora por defecto).

Read-back: “Quedó cargado {nombre}, {fechas}, {pax}, tipo auto. Estado Pendiente de completar. ¿Confirmo recordatorio?”

3) completar_reserva

Qué hace: Completa datos mínimos y vincula con un cliente existente si hay match.

Frases

“Completá {RID}: DNI 34…, Tel +54…, Localidad Tigre.”

Match (prioridad)

DNI exacto → match seguro (propone vincular).

Tel normalizado → si 1 match, propone; si varios (familia), lista candidatos.

Nombre+Localidad → exacto o fuzzy → lista si hay más de 1.

Sin match → crea Cliente nuevo.

Al confirmar

cliente_vinculado=ON, datos_completos=ON, sale de PendienteDatos.

Actualiza descripción del evento (DNI/Tel/Localidad).

Bitácora: match_cliente (criterio, resultado, ids).

4) resolver_homonimia

Qué hace: Muestra candidatos cuando hay muchos con el mismo nombre.

Frases

“Resolver homonimia Juan Pablo.”

Salida

Lista con DNI / Tel / Localidad / Veces (última visita); elegís 1.

5) vincular_a_cliente

Qué hace: Vincula esta reserva a un ClienteID/DNI específico.

Frases

“Vinculá esta reserva a DNI 34… / ClienteID cli_….”

6) (admin) fusionar_clientes

Qué hace: Fusiona Cliente A → Cliente B (conserva B; mueve historial).

Frases

“Fusioná ClienteID A en ClienteID B. Conservar B.”

7) abrir_reserva

Frases

“Abrí la ficha de María Gómez / DNI 34.567.890 / RID YEM-20240920-001.”

Slots

identificador (nombre+DNI/fecha, DNI/Tel, o RID).

8) cambiar_unidad (por nombre visible)

Frases

“En la reserva de María, pasá a Depto A.”

“Movela a Cabaña G.”

“Cambiá a Loft 5.”

(fallback) “Pasá a unidad_7.”

Cómo identifica la unidad (prioridad)

Nombre visible (normaliza acentos, guiones, espacios y may/min).

Aliases (si definís en config).

Patrón Tipo+número/letra: “loft 5”, “cabaña g”, “departamento b”.

UnidadID (unidad_#).

Flujo

Resuelve la unidad → valida disponibilidad y amenidades → read-back:
“Mover a {Nombre} ({UnidadID}, {Tipo}). ¿Confirmo?”

Si no disponible, sugiere alternativas del mismo tipo (y OVERFLOW si corresponde).

Si la amenidad solicitada no aplica en destino, ofrece:
a) otra unidad compatible, o b) quitar la amenidad.

Al confirmar: mueve/actualiza evento, recalcula si cambia tarifa, y registra en bitácora.

9) editar_datos_huesped

Frases

“Actualizá el teléfono de María a +54 9 11 2222-3333.”

Slots

reserva_id o cliente_id, campo, nuevo_valor.

Reglas

Cambios en DNI/Tel piden confirmación extra.

Sincroniza con la ficha Cliente y ajusta descripción en eventos futuros.

10) agregar_servicio / quitar_servicio

Frases

“Sumá Desayuno: 1 sin TACC y 1 normal a Juan Pablo.”

“Quitá el desayuno de María.”

Notas (La Yema)

Precio al huésped $0; se computa costo proveedor ($2000 normal, $2500 sin TACC).

11) set_preferencia / quitar_preferencia

Frases

“Agregá camas separadas a Juan.” / “Sacá camas separadas.”

Notas

Si la unidad actual no admite, sugiere cambio a una compatible (respeta OVERFLOW).

12) confirmar_reserva / cancelar_reserva / reprogramar_reserva

confirmar_reserva → crea/actualiza evento en CALENDAR_ID y dispara mensajes si están activos.
cancelar_reserva → libera evento; pide motivo (bitácora).
reprogramar_reserva → cambia fechas; mantiene pax/servicios/preferencias; valida disponibilidad.

Frases

“Confirmá / Cancelá / Reprogramá la reserva de María al 22/09.”

13) abrir_unidad / estado_unidad / set_activa

Frases

“Mostrame Depto A / Cabaña G / Loft 5.” · (fallback) “Mostrame unidad_1.”

“Poné Loft 1 en REPARACION (nota: ‘cambiar mixer’).”

“Marcala ACTIVA.”

Efectos

Bloqueos operativos, exclusión de sugerencias, recordatorios para volver a ACTIVA si querés.

14) preguntar_disponibilidad

Frases

“¿Qué Loft 2p hay libres para 12–14/10?”

Salida

Lista priorizada; excluye mantenimiento/limpieza; si no hay, propone OVERFLOW.

15) tareas_hoy / marcar_limpia

Frases

“¿Cuántas unidades hay que limpiar hoy y cuáles?”

“Marcá Loft 1 como lista (ACTIVA).”

Efecto

Checkout → LIMPIEZA + tarea (housekeeping); “lista” → ACTIVA.

16) ver_calendario

Frases

“Mostrame el calendario del finde / semana que viene.”

Salida

Eventos de check-in/out + (si aplica) servicios/housekeeping.

17) Reportes

ingresos_mes: “Ingresos de septiembre.”

costo_proveedor: “Gasto en Desayunos esta semana.”

ocupacion: “Ocupación del mes y esta semana.”

mejores_clientes: “Top 10 clientes por estadías en 12 meses.”

18) buscar_cliente (consulta directa)

Frases

“Buscá Juan Carrizo de Marull.”

“Buscá por dni 34….”

“Buscá por tel +54 9 3564….”

Salida

Ficha directa o lista de candidatos (Nombre, DNI, Tel, Localidad, Veces/last_seen) para elegir 1.

Frases sinónimas (atajos)

crear_reserva: “cargá”, “reservá”, “agendá”.

abrir_reserva/unidad: “abrí”, “mostrá”, “mostrame”.

cambiar_unidad: “cambiá”, “pasá a”, “mové a”.

confirmar: “confirmá”, “dejalo confirmado”.

cancelar: “cancelá”, “dalo de baja”.

marcar_limpia: “dejala lista”, “marcala activa”.

buscar_cliente: “buscá”, “encontrá”, “mostrá cliente”.

Defaults del Modo Rápido

Tipo inferido por personas (valida con MAPA).

Unidad autoasignada; si pediste amenidad, filtra solo unidades que la tengan; si no hay, aplica OVERFLOW compatible.

Servicios (La Yema): Desayuno $0 → normales = pax, sin_tacc = 0.

Seña: si no decís, sin seña (Resto = total).

Cliente: si no existe, pide DNI/Tel y crea ficha mínima.

Recordatorio de verificación: si usaste Modo Rápido, crea “Verificar datos reserva” para ajustar detalles luego.

Validaciones & salvavidas

Fechas válidas; capacidad min/max; choques de calendario; compatibilidad de amenidades; OVERFLOW que respeta amenidades; duplicados de huésped (desambiguación por DNI/Tel).


