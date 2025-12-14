# NOTES_choices.md  
## Decisiones, renuncias y criterios del modelo mínimo

**Proyecto:** Ventana de Resiliencia  
**Autor:** Ernesto Cisneros Cino  
**Versión:** 1.0  
**Propósito:** Documentar el *porqué* de cada elección en el marco y el toy model

---

## 0. Por qué existe este archivo

La mayoría de los trabajos científicos publican resultados,
pero **ocultan el proceso de decisión** que los hizo posibles.

Este archivo existe para:
- preservar el razonamiento,
- hacer visibles las renuncias,
- dejar constancia de lo que *no* se hizo y por qué.

No es un apéndice técnico.
Es **memoria epistemológica**.

---

## 1. Por qué un modelo escalar (1D)

El toy model usa un sistema **escalar discreto**:

- No por simplicidad matemática,
- sino para evitar esconder el fenómeno bajo dimensionalidad.

Un modelo de mayor dimensión:
- introduce grados de libertad irrelevantes,
- dificulta la identificación de regímenes,
- hace menos visible la transición entre caos, resiliencia y rigidez.

**Decisión consciente:**  
Preferir *claridad fenomenológica* sobre realismo.

---

## 2. Por qué tiempo discreto y no continuo

Se eligió una dinámica discreta:

- para reflejar procesos iterativos reales (aprendizaje, decisión),
- para evitar introducir derivadas continuas sin necesidad,
- para facilitar simulación directa y reproducible.

El fenómeno tratado **no depende** de continuidad temporal,
sino de:
- memoria,
- retroalimentación,
- irreversibilidad.

---

## 3. Por qué memoria exponencial y no ventana dura

La memoria se modela como promedio exponencial:

$$
M_t = (1-\alpha)M_{t-1} + \alpha x_t
$$

y no como ventana deslizante dura porque:

- introduce olvido gradual,
- evita discontinuidades artificiales,
- representa mejor costos energéticos reales.

Una ventana dura:
- es computacionalmente simple,
- pero conceptualmente menos realista.

**Renuncia consciente:**  
No modelar memoria perfecta ni cortes abruptos.

---

## 4. Por qué el entorno es una senoide ruidosa

El entorno se define como:

$$
e_t = \sin(\omega t) + \xi_t
$$

Esta elección no pretende realismo ambiental.

Sirve para:
- introducir estructura reconocible,
- permitir seguimiento imperfecto,
- diferenciar copia trivial de adaptación.

Un entorno puramente aleatorio:
- no permite distinguir rigidez de caos.

Un entorno demasiado complejo:
- oscurece la intuición.

---

## 5. Por qué la predicción es igual a la memoria

Se define:

$$
\hat e_t = M_t
$$

Esto es deliberadamente ingenuo.

El objetivo es:
- no introducir un modelo predictivo adicional,
- aislar el rol de la memoria,
- evitar confundir capacidad predictiva con estructura del sistema.

Cualquier predictor más sofisticado
ocultaría el fenómeno central.

---

## 6. Por qué el término no lineal es tanh

La función:

$$
\tanh(M_t)
$$

se elige porque:

- es saturante,
- evita explosiones numéricas,
- introduce no linealidad mínima.

No se busca:
- universalidad,
- ni ajuste fino.

Se busca:
- una frontera clara entre lineal y no lineal.

---

## 7. Por qué el error tiene un término cúbico

El término:

$$
\sigma \varepsilon_t^3
$$

no es un adorno.

Introduce:
- asimetría,
- exploración estructurada,
- sensibilidad a errores grandes.

El término cúbico:
- no domina para errores pequeños,
- se activa solo cuando el sistema se aleja.

Esto refleja la idea de:
**error integrado, no eliminado**.

---

## 8. Por qué no se optimiza ningún parámetro

No se ajustan parámetros para maximizar métricas.

Esto es deliberado.

Optimizar:
- desplaza el foco al rendimiento,
- borra la transición de regímenes,
- traiciona el propósito del modelo.

El modelo **debe poder fallar**.

---

## 9. Por qué las métricas son heurísticas

Las métricas usadas (RMSE, volatilidad, rigidez) son:

- proxies,
- no observables fundamentales.

No se busca:
- definir una función de Lyapunov,
- ni demostrar estabilidad formal.

Se busca:
- identificar regiones cualitativas,
- no demostrar teoremas.

---

## 10. Por qué no hay pruebas formales

Este trabajo **no es un paper matemático**.

Formalizar en exceso:
- cerraría el marco,
- eliminaría ambigüedad fértil,
- lo volvería dogmático.

La ambigüedad aquí es **funcional**, no un descuido.

---

## 11. Por qué se conserva la versión 1.0

Esta versión:
- contiene decisiones crudas,
- muestra dudas implícitas,
- conserva errores potenciales.

Cualquier versión posterior
**debe coexistir**, no reemplazarla.

Eliminar la 1.0
sería una pérdida irreversible de información conceptual.

---

## 12. Declaración final

Este proyecto no busca demostrar que el marco es correcto,
sino **mostrar cómo se piensa cuando aún no se sabe**.

El criterio,
las renuncias
y las decisiones parciales
son parte del resultado.

Aquí termina el modelo.
El resto pertenece al lector.

---

**Fin de NOTES_choices.md**
