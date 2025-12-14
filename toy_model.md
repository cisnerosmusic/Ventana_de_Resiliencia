# toy_model.md  
## Modelo mínimo de Ventana de Resiliencia

**Proyecto:** Ventana de Resiliencia  
**Autor:** Ernesto Cisneros Cino  
**Versión:** 1.0  
**Objetivo:** Ilustrar, de forma mínima, la emergencia de una ventana de resiliencia  
**Advertencia:** Este modelo es deliberadamente simple y no pretende realismo cuantitativo.

---

## 0. Intención del modelo

Este *toy model* no busca optimizar ni predecir sistemas reales.  
Su único propósito es mostrar que:

- con memoria finita,
- error integrado,
- y no linealidad,

emerge un rango intermedio de comportamiento estable  
que desaparece cuando la memoria es demasiado corta o demasiado larga.

---

## 1. Variables del sistema

Definimos un sistema escalar discreto:

- \( x_t \): estado interno del sistema  
- \( e_t \): entorno externo  
- \( M_t \): memoria efectiva  
- \( \tau \): escala de memoria  

---

## 2. Entorno

El entorno es una señal lenta con ruido:

$$
e_t = \sin(\omega t) + \xi_t
$$

donde:

- \( \omega \ll 1 \) (variación lenta)
- \( \xi_t \sim \mathcal{N}(0,\sigma_e^2) \)

---

## 3. Memoria finita

La memoria se define como un promedio exponencial del pasado:

$$
M_t = (1-\alpha) M_{t-1} + \alpha x_t
$$

con:

$$
\alpha = \frac{1}{\tau}
$$

- \( \tau \to 0 \) → memoria casi inexistente  
- \( \tau \to \infty \) → memoria rígida  

---

## 4. Predicción y error

El sistema predice el entorno a partir de su memoria:

$$
\hat e_t = M_t
$$

El error es:

$$
\varepsilon_t = e_t - \hat e_t
$$

---

## 5. Dinámica del sistema

La actualización del estado incluye:

1. atracción no lineal,
2. corrección por error,
3. variación generativa.

$$
x_{t+1} =
(1-\gamma)x_t
+ \tanh(M_t)
+ \eta\,\varepsilon_t
+ \sigma\,\varepsilon_t^3
$$

donde:

- \( \tanh(M_t) \): no linealidad saturante  
- \( \eta \): ganancia correctiva  
- \( \sigma \): exploración generativa  

---

## 6. Regímenes observables

Al variar \( \tau \), se observan tres regímenes cualitativos:

### 6.1 Memoria corta (\( \tau \ll 1 \))

- El sistema olvida rápidamente.
- El error domina.
- Comportamiento errático.
- No emerge identidad estable.

**Régimen:** Caos adaptativo.

---

### 6.2 Memoria larga (\( \tau \gg 1 \))

- El sistema se aferra al pasado.
- La corrección pierde efectividad.
- El estado se congela o se vuelve insensible.

**Régimen:** Rigidez.

---

### 6.3 Memoria intermedia (\( \tau \approx \tau^\* \))

- El error es integrado sin colapso.
- El sistema sigue al entorno sin copiarlo.
- Aparece una trayectoria estable pero flexible.

**Régimen:** Ventana de Resiliencia.

---

## 7. Medidas cualitativas

Definimos informalmente:

- **Caos:** varianza alta de \( x_t \) sin estructura.
- **Rigidez:** derivada temporal cercana a cero.
- **Resiliencia:** capacidad de seguir \( e_t \) con desfase limitado.

No se introduce una métrica formal a propósito.  
La distinción es **fenomenológica**, no estadística.

---

## 8. Qué muestra este modelo (y qué no)

### Muestra:

- que la memoria finita no es un defecto,
- que el error puede ser generativo,
- que la estabilidad emerge en un rango intermedio.

### No muestra:

- optimalidad,
- convergencia global,
- universalidad.

Este modelo **no escala** y **no debe escalarse** sin repensar sus supuestos.

---

## 9. Relación con el marco general

Este *toy model* es una instancia mínima de:

- no linealidad,
- memoria con costo,
- error integrado,
- ventana dependiente del parámetro \( \tau \).

Sirve como intuición operativa, no como prueba.

---

## 10. Nota epistemológica

Este archivo existe para **mostrar el camino**,  
no para cerrar el argumento.

Cualquier versión más compleja  
debería conservar este modelo como referencia histórica (v1.0).

Eliminarlo sería perder información conceptual.

---

**Fin del toy_model.md**
