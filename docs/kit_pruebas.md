A. Captura rápida + completar datos

Reserva rápida:
“Agendá rápido a Pedro Silva, del 10/10 al 12/10, 2 pax.”

Esperado: RID nuevo, Pendiente de completar, recordatorio sugerido.

Completar & vincular:
“Completá {RID_de_Pedro}: DNI 31.234.567, Tel +54 9 3564…, Localidad Rafaela.”

Esperado: propone vincular (si existe) o crea cliente; datos_completos=ON.

B. Reserva completa + amenidad + cambio de unidad

Reserva completa:
“Reservá para DNI 34.567.890, 20/10–23/10, 2 pax.”

Esperado: Confirmación con Loft 2p y Unidad auto.

Amenidad:
“Agregá camas separadas.”

Esperado: si la unidad no admite, sugiere compatibles.

Cambio de unidad (por nombre):
“Pasá a Loft 1.”

Esperado: read-back con Loft 1 (unidad_1); calendario movido.

C. Servicios + pagos + reprogramar

Servicios (Desayuno):
“Sumá Desayuno: 1 sin TACC y 1 normal.”

Esperado: precio huésped $0; costo proveedor mostrado.

Seña:
“Registrá seña $50.000 por transferencia.”

Esperado: Resto recalculado.

Reprogramar:
“Reprogramá al 22/10–25/10.”

Esperado: noches recalculadas; evento actualizado.

D. Housekeeping

Checkout:
“Registrá checkout de {RID}.”

Esperado: unidad en LIMPIEZA + tarea.

Marcar lista:
“Marcá Loft 1 ACTIVA.”

Esperado: unidad vuelve a ACTIVA (ofertable).

E. Búsquedas y homónimos

Buscar por nombre + localidad:
“Buscá Juan Carrizo de Marull.”

Esperado: abre ficha o lista de candidatos.

Resolver homonimia:
“Resolver homonimia Juan Pablo.”

Esperado: lista con DNI/Tel/Localidad/visitas para elegir.