# Casos de prueba — Calculadora de Consumo Energético de Laboratorio

La tarifa indicada se expresa en soles por kWh. Los resultados se calculan con:

- Consumo mensual (kWh) = Potencia (W) × Cantidad × Horas diarias × Días mensuales / 1000
- Costo mensual (S/) = Consumo mensual (kWh) × Tarifa (S/kWh)

## Caso 1: Un equipo

**Datos de entrada**

- Equipo: Computadora
- Potencia: 200 W
- Cantidad: 2
- Horas diarias: 8
- Días mensuales: 22
- Tarifa: S/ 0.80 por kWh

**Resultados esperados**

- Consumo mensual: 200 × 2 × 8 × 22 / 1000 = **70.400 kWh**
- Costo mensual: 70.400 × 0.80 = **S/ 56.32**

## Caso 2: Dos equipos y total

**Datos de entrada**

Tarifa común: **S/ 0.75 por kWh**

| Equipo | Potencia | Cantidad | Horas/día | Días/mes |
|---|---:|---:|---:|---:|
| Microscopio | 100 W | 3 | 5 | 20 |
| Refrigeradora | 300 W | 1 | 24 | 30 |

**Resultados esperados**

- Microscopio: 100 × 3 × 5 × 20 / 1000 = **30.000 kWh**; costo = **S/ 22.50**
- Refrigeradora: 300 × 1 × 24 × 30 / 1000 = **216.000 kWh**; costo = **S/ 162.00**
- Consumo total: **246.000 kWh**
- Costo total: **S/ 184.50**
- Equipo de mayor consumo: **Refrigeradora**

## Caso 3: Validación de entradas

**Datos de entrada a intentar**

- Nombre vacío.
- Potencia igual a 0 W.
- Horas diarias igual a 25.
- Días mensuales igual a 32.

**Resultados esperados**

- No se debe agregar un equipo con nombre vacío.
- No se debe agregar un equipo con potencia cero.
- El control de horas no debe permitir más de 24 horas diarias.
- El control de días no debe permitir más de 31 días mensuales.
- La aplicación debe mostrar mensajes de validación cuando corresponda y conservar los equipos válidos ya registrados.
