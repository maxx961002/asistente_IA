Objetivo

Definir cómo el asistente calcula Total Alojamiento, Servicios, Resto, y cómo reaccionan ante cambios (fechas, pax, unidad, seña, late, ventanas).

Entradas

CONFIGURACION.md: TARIFAS por tipo + pax, VENTANAS (precio especial o % descuento), DESCUENTOS (p. ej., 7 noches -10%), LATE (LATE_CHECKOUT_EXTRA_NOCHES, LATE_CHECKOUT_EXTIENDE_DIA), SERVICIOS_SUMAR_AL_RESTO_DEFAULT.

Reserva: ingreso, egreso, pax, tipo_solicitado (o inferido), unidad, servicios, seña.

Overflow: precio = TIPO_SOLICITADO (La Yema) o UNIDAD_REAL (otros complejos).

Definiciones

Noches base = egreso - ingreso (en días).

Late: si ON → noches = noches_base + LATE_CHECKOUT_EXTRA_NOCHES (La Yema: +0.5).

Ventanas: por noche, se etiqueta cada noche como especial o normal (o se aplica % desc.).

Tarifa aplicable: por tipo y pax. Si cruzás ventanas, se prorratea por noche.

Servicios:

UNITARIO: precio_unitario_pp * cantidad_personas (o 0 si gratis).

Si sumar_al_resto = ON → suma a Total; si OFF, queda solo para control/costo proveedor.

Resto = Total Alojamiento + Servicios sumables − Seña.

Moneda y redondeo: ARS, sin centavos (enteros). Si hay % → redondeo al entero más cercano.

Orden de cálculo

Determinar tipo (si no viene): por pax según mapeo.

Calcular noches (agregar late si corresponde).

Etiquetar cada noche con ventana (normal/especial o % desc).

Alojamiento = ∑ (precio_por_noche_de_ese_día).

Si % desc, aplicar sobre precio normal/especial de esa noche.

Servicios: sumar solo los que tengan sumar_al_resto = ON.

Resto = Alojamiento + ServiciosSumables − Seña.

Overflow: si la unidad real es un “upgrade”, facturar según regla:

La Yema: precio = TIPO_SOLICITADO (aunque duermas en Loft-5/8, se cobra Loft 2p).

Control (para reportes): guardar costo_proveedor de cada servicio.

Disparadores de recálculo (read-back + confirmación)

Cambia ingreso/egreso, pax, tipo/unidad, late, ventanas activas (por fecha), servicios, seña.

El bot siempre lee: “Total alojamiento ${X} + servicios ${Y} − seña ${Z} = Resto ${R}. ¿Confirmo?”

Ejemplos (La Yema)

Loft 2p, 2 noches normal (sin late)
2 × $75.000 = $150.000; servicios $0; seña $50.000 → Resto $100.000.

Loft 2p, 2 noches + late 0,5
2,5 × $75.000 = $187.500; seña $20.000 → Resto $167.500.

Loft 3–4p, 3 pax, 3 noches especial
3 × $120.000 = $360.000; seña $0 → Resto $360.000.

Cruza ventanas (1 noche normal + 1 especial), Loft 2p
$75.000 + $95.000 = $170.000; seña $0 → Resto $170.000.

Overflow Loft 2p → duerme en Loft-5 (regla TIPO_SOLICITADO)
Se cobra Loft 2p (no Loft-5).

Servicio pago (ej. servicio_2 a $5.000 pp x 2 pax)
Alojamiento $150.000 + servicios $10.000 − seña $0 → Resto $160.000.

Descuento estadía larga (7 noches −10%)
7 × $75.000 = $525.000 → 10% OFF = $472.500; seña $0 → Resto $472.500.

Prorrateo para reportes (Control)

Ingreso por noche: repartir el total de alojamiento por noche real (respeta ventanas/late).

Mes: asignar cada noche al mes calendario correspondiente.