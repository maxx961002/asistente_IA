Diccionario de Acciones — Recordatorios, Tareas y Listas

Config relevantes (CONFIGURACION.md)

RECORDATORIOS_ENABLED: ON

RECORDATORIOS_CANAL_DEFAULT: CHAT

RECORDATORIOS_HORA_DEFECTO: 09:00

RECORDATORIOS_SNOOZE_MIN: [5,10,30,60]

RECORDATORIOS_CANCEL_MOTIVO_REQUIRED: ON

RECORDATORIOS_LOG_EN_BITACORA: ON · RECORDATORIOS_LOG_TIPO: recordatorio

Listas: LISTAS_ENABLED: ON, LISTAS_PREDEFINIDAS, LISTAS_PLANTILLAS, LISTAS_EXTRAS_POR_ESTA_VEZ: ON.

1) crear_recordatorio

Frases: “Haceme acordar hoy a las 17: tirarle agua a la pileta.”
Slots: titulo/nota, fecha_hora (o “hoy/mañana + hora”), opcionales canal, prioridad, lista.
Read-back: “Hoy 17:00, canal CHAT, prioridad media. ¿Confirmo?”
Resultado: notificación a la hora; acciones: Posponer 10/30/60 | Hecho | Reprogramar | Cancelar (pide motivo).

2) crear_recordatorio_recurrente (simple)

Frases: “Dejá fija todos los días a las 17: tirarle agua a la pileta.” · “Todos los lunes 9: revisar caldera.”
Read-back: “Programo diario 17:00 en CHAT. ¿Confirmo?”
Resultado: serie recurrente; no se pausa sola.

3) cancelar_recordatorio_de_hoy (con motivo)

Frases: “Cancelá el de la pileta de hoy.”
Flujo: pide motivo; registra en bitácora y cancela solo hoy. La serie sigue.

4) reprogramar_recordatorio_de_hoy

Frases: “Reprogramá pileta para 19:00.”
Resultado: mueve solo la instancia de hoy; la serie continúa igual.

5) listar_recordatorios

Frases: “¿Qué recordatorios tengo hoy?” · “Mostrá los próximos.” · “Mostrá los cancelados de hoy.”
Salida: lista con hora, título, canal, prioridad, y botones: Hecho / Posponer / Reprogramar / Cancelar.

6) completar_tarea / borrar_recordatorio

Frases: “Marcá hecho el de pileta.” · “Borrá el de comprobante a María.”
Notas: “Hecho” registra cierre; “Borrar” elimina sin ejecutar.

7) crear_tarea_operativa

Frases: “Creá tarea en Loft-1: cambiar cuerito (30 min).” · “Para Mantenimiento: pintar reja el viernes 15:00.”
Resultado: tarea operativa Pendiente/Agendada; puede ir a HOUSEKEEPING_CALENDAR_ID.

8) listas — plantillas + extras “por esta vez”

Frases (plantilla): “Armá lista del Super con lo de siempre.”
Extras solo instancia: “En Super agregá carbón 3 bolsas y hielo 5 kg, por esta vez.”
Mostrar/gestionar: “Mostrame Super.” · “Marcá hielo como comprado.” · “Quitá pintura de Ferretería.” · “Vaciar Super.”
Compartir: “Enviá Super por WhatsApp.”

Notas

“Por esta vez” no modifica la plantilla base (LISTAS_PLANTILLAS).

Si querés cambiar la plantilla: “Actualizá la plantilla de Super: lavandina 6 botellas”.

Ejemplos rápidos

A) Diario fijo

Tú: “Dejá fija todos los días 17: tirarle agua a la pileta.”

Bot: “Programo diario 17:00 por CHAT. ¿Confirmo?” → “Sí.”

B) Cancelar hoy con motivo

Tú: “Cancelá pileta de hoy.”

Bot: “¿Motivo?” → “llovió fuerte.”

Bot: “Cancelado solo hoy. Registré en bitácora: ‘llovió fuerte’.”

C) Reprogramar hoy

Tú: “Reprogramá pileta a 19:00.”

Bot: “Listo: hoy 19:00. La serie diaria sigue a las 17 desde mañana.”

D) Lista con plantilla + extras

Tú: “Armá Super con lo de siempre y agregá carbón 3 y hielo 5 kg, por esta vez.”

Bot: “Hecho. ¿Te la muestro o la envío por WhatsApp?”

Defaults

Canal: CHAT.

Hora por defecto (cuando decís solo el día): RECORDATORIOS_HORA_DEFECTO.

Snooze: 10 min (también 5/30/60).

Prioridad: media.

TZ: usa la del calendario principal si no definís otra.