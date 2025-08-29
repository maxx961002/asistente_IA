Usá estos escenarios para validar que los números (manual por ahora) te cierran con tarifas/ventanas reales.

A) Casos base

Loft 2p · 10/10→12/10 (2 noches) · 2 pax · sin late · seña $50.000
Esperado: Aloj $150.000 → Resto $100.000.

Loft 2p · 10/10→12/10 (2 noches) · late ON (+0.5) · seña $20.000
Esperado: Aloj $187.500 → Resto $167.500.

B) Ventanas

Loft 2p · 15/09→17/09 (1 noche normal + 1 especial)
Esperado: $75.000 + $95.000 = $170.000 (sin seña).

C) Overflow

Loft 2p sin disponibilidad → asignada Loft-5 (regla TIPO_SOLICITADO)
Esperado: cobrar como Loft 2p (según ventana).

D) Servicios

Agregar servicio_2 (UNITARIO $5.000 pp) con 2 pax y sumar_al_resto=ON
Si Aloj $150.000 → Total $160.000.

E) Descuento

Loft 2p · 7 noches · descuento −10%
Esperado: $525.000 → $472.500.

Tip: anotá en un cuaderno el desglose por noche y marcá cuáles caen en ventana especial. Si tus ventanas reales difieren, cambiá las fechas de prueba.