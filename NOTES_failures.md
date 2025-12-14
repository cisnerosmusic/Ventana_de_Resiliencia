# NOTES_failures.md  
## Intentos fallidos, límites y caminos descartados

**Proyecto:** Ventana de Resiliencia  
**Autor:** Ernesto Cisneros Cino  
**Versión:** 1.0  
**Propósito:** Registrar lo que no funcionó, lo que se descartó y por qué

---

## 0. Por qué documentar los fallos

En la práctica científica real, los fallos:
- ocupan más tiempo que los aciertos,
- moldean el criterio,
- rara vez se publican.

Este archivo existe para **no borrar esa información**.

No busca justificar errores,
sino **preservar decisiones negativas** que contienen aprendizaje.

---

## 1. Intento de memoria infinita

### Qué se intentó  
Modelar el sistema con memoria acumulativa sin decaimiento.

### Qué ocurrió  
- El sistema se volvió rígido.
- El estado dejó de responder al entorno.
- El error se acumuló sin capacidad de integración.

### Conclusión  
La memoria infinita **no mejora estabilidad**.  
La destruye.

Este fallo motivó directamente
la noción de **ventana de resiliencia**.

---

## 2. Minimización estricta del error

### Qué se intentó  
Eliminar términos generativos y forzar:

$$
\min \|\varepsilon_t\|
$$

### Qué ocurrió  
- El sistema se volvió frágil.
- Pequeños cambios del entorno producían colapso.
- No emergía identidad dinámica.

### Conclusión  
Eliminar el error **elimina exploración**.  
El sistema se vuelve óptimo pero no viable.

---

## 3. Modelo completamente lineal

### Qué se intentó  
Usar dinámica puramente lineal:

$$
x_{t+1} = a x_t + b e_t
$$

### Qué ocurrió  
- No aparecieron regímenes diferenciados.
- No hubo transición cualitativa.
- No emergió ventana intermedia.

### Conclusión  
El fenómeno **no existe en sistemas lineales**.  
Este intento justifica explícitamente el dominio de validez.

---

## 4. Entorno puramente aleatorio

### Qué se intentó  
Definir el entorno como ruido blanco.

### Qué ocurrió  
- No era posible distinguir adaptación de ruido.
- El sistema parecía errático incluso en regímenes estables.
- Se perdió interpretabilidad.

### Conclusión  
Un mínimo de estructura ambiental es necesario
para observar resiliencia.

---

## 5. Entorno excesivamente complejo

### Qué se intentó  
Introducir señales multiescala y no periódicas desde el inicio.

### Qué ocurrió  
- El comportamiento del sistema se volvió opaco.
- No era posible atribuir causas a efectos.
- La intuición se perdió.

### Conclusión  
La complejidad prematura **oculta el fenómeno**.

---

## 6. Predictores sofisticados

### Qué se intentó  
Usar modelos predictivos más complejos para \( \hat e_t \).

### Qué ocurrió  
- La capacidad predictiva dominó la dinámica.
- El rol de la memoria se volvió secundario.
- El sistema parecía “inteligente” sin ser resiliente.

### Conclusión  
Mejor predicción **no implica** mejor estabilidad.

---

## 7. Optimización de parámetros

### Qué se intentó  
Ajustar parámetros para maximizar métricas de rendimiento.

### Qué ocurrió  
- La ventana de resiliencia se desplazó artificialmente.
- El modelo perdió robustez.
- El fenómeno se volvió dependiente del tuning.

### Conclusión  
La optimización borra el paisaje dinámico.

---

## 8. Métricas excesivamente formales

### Qué se intentó  
Definir criterios estrictos de estabilidad matemática.

### Qué ocurrió  
- Se perdió conexión con el fenómeno cualitativo.
- El modelo se volvió defensivo, no exploratorio.
- El lenguaje dejó de ser compartible.

### Conclusión  
No todo fenómeno necesita formalización extrema
en su fase inicial.

---

## 9. Generalización apresurada

### Qué se intentó  
Extender el modelo a múltiples dominios simultáneamente.

### Qué ocurrió  
- Aparecieron contradicciones conceptuales.
- El marco se diluyó.
- Se perdió precisión.

### Conclusión  
La generalidad debe emerger,
no declararse.

---

## 10. Cierre prematuro

### Qué se intentó  
Forzar conclusiones fuertes.

### Qué ocurrió  
- El marco se volvió dogmático.
- Se cerraron preguntas fértiles.
- Se traicionó el espíritu original.

### Conclusión  
Cerrar demasiado pronto
es una forma de error epistemológico.

---

## 11. Lección global

Los fallos no fueron obstáculos,
sino **instrumentos de delimitación**.

Cada intento descartado:
- redujo el espacio de hipótesis,
- afinó el dominio de validez,
- clarificó qué **no** es este marco.

---

## 12. Declaración final

Este archivo no documenta debilidad,
sino **rigor honesto**.

El conocimiento que no conserva sus fallos
es frágil.

Este proyecto los conserva.

---

**Fin de NOTES_failures.md**
