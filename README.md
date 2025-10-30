# Resultados del Modelo de Detección DoS

## Informacion de contacto

**Mail:** noahkuperman@gmail.com  
**GitHub:** [https://github.com/6upernova](https://github.com/6upernova)

**Repositorio con el codigo utilizado para el informe:** [https://github.com/6upernova/DOS_Detecter](https://github.com/6upernova/DOS_Detecter)

**Link al video Explicativo:** [https://youtu.be/1bYhu99hbxQ](https://youtu.be/1bYhu99hbxQ)

## Información del Dataset

- **Total de registros:** 10,000  
- **Distribución de clases:** 50% Normal (5,000) | 50% DoS (5,000)  
- **División de datos:** 80% entrenamiento (8,000) | 20% prueba (2,000)  
- **Columnas:**

  - **`packet_rate`** → Es la **tasa de envío de paquetes**, generalmente medida como _paquetes por segundo (pps)_.  
    Indica cuántos paquetes de red se envían o reciben en promedio por unidad de tiempo.  
    Un valor alto puede reflejar una conexión muy activa o un ataque DoS.  
    Un valor bajo sugiere tráfico normal o inactivo.  
  - **`duration`** → Es la **duración total de la conexión o flujo**, en segundos o milisegundos.  
    Si se trata de un flujo TCP/UDP, es el tiempo entre el primer y el último paquete.  
    Duraciones extremadamente cortas o largas pueden ser indicios de comportamiento inusual.  
  - **`bytes_sent`** → Cantidad total de **bytes enviados** desde el host origen hacia el destino durante esa conexión.  
    En ataques o filtración de datos, este valor tiende a ser anormalmente alto.  
    En consultas o peticiones simples, suele ser bajo.  
  - **`bytes_received`** → Total de **bytes recibidos** por el host origen desde el destino durante la sesión.  
    Diferencias grandes entre enviados y recibidos pueden indicar un tipo de tráfico específico.  

## Algoritmo Utilizado

**Regresión Logística**:  
La regresión logística de _scikit-learn_ toma tus datos, calcula una combinación lineal de las variables, aplica una función sigmoide para convertirla en probabilidad y ajusta los pesos para minimizar el error logarítmico.  
Modela la **probabilidad de que una observación pertenezca a la clase positiva (1)** en función de las variables de entrada.

## Análisis de Correlación

|                | packet_rate | duration | bytes_sent | bytes_received |
|----------------|-------------|----------|-------------|----------------|
| packet_rate    | 1.000       | -0.550   | 0.623       | -0.602         |
| duration       | -0.550      | 1.000    | -0.469      | 0.443          |
| bytes_sent     | 0.623       | -0.469   | 1.000       | -0.513         |
| bytes_received | -0.602      | 0.443    | -0.513      | 1.000          |

**Observaciones:**

- Correlación positiva fuerte entre `packet_rate` y `bytes_sent` (0.623).  
- Correlación negativa fuerte entre `packet_rate` y `bytes_received` (-0.602).  
- La duración presenta correlación negativa con `packet_rate` (-0.550).  

## Modelo: Logistic Regression

### Coeficientes del Modelo

| Feature        | Coeficiente | Interpretación                         |
|----------------|-------------|----------------------------------------|
| packet_rate    | +8.038      | Mayor peso: alta tasa indica DoS       |
| bytes_sent     | +2.467      | Incremento aumenta probabilidad de DoS |
| bytes_received | -2.859      | Decremento aumenta probabilidad de DoS |
| duration       | -1.767      | Duración corta asociada a DoS          |

## Resultados del Modelo

### Métricas Principales

| Métrica   | Valor  | Porcentaje |
|-----------|--------|-------------|
| Accuracy  | 0.9970 | 99.70%     |
| Precision | 0.9960 | 99.60%     |
| Recall    | 0.9980 | 99.80%     |
| F1-Score  | 0.9970 | 99.70%     |

### Matriz de Confusión

|                 | Predicción Normal | Predicción DoS |
|-----------------|-------------------|----------------|
| **Real Normal** | 996 (TN)          | 4 (FP)         |
| **Real DoS**    | 2 (FN)            | 998 (TP)       |

### Tasas de Error

- **False Positive Rate (FPR):** 0.40% – tráfico normal marcado incorrectamente como DoS.  
- **False Negative Rate (FNR):** 0.20% – ataques DoS no detectados.  

## Classification Report

| Clase | Precision | Recall | F1-Score | Support |
|--------|------------|---------|-----------|----------|
| Normal | 0.9980 | 0.9960 | 0.9970 | 1000 |
| DoS | 0.9960 | 0.9980 | 0.9970 | 1000 |
| **Accuracy** |  |  | **0.9970** | **2000** |

## Interpretación de Resultados

### Análisis del Desempeño

El modelo alcanzó métricas excepcionales (Accuracy: 99.70%, F1-Score: 99.70%), demostrando una capacidad casi perfecta para distinguir entre tráfico normal y ataques DoS.  
La matriz de confusión revela solo 6 errores de clasificación en 2,000 muestras: 4 falsos positivos y 2 falsos negativos.  

### Características Discriminativas

`packet_rate` (+8.038) es el predictor más importante, seguido por `bytes_received` (-2.859) y `bytes_sent` (+2.467).  
Refleja el patrón característico de los ataques DoS: **alta tasa de paquetes**, **muchos bytes enviados**, **pocos recibidos**, y **conexiones cortas**.  

### Consideraciones Críticas

**Limitación del Dataset:**  
La precisión cercana al 100% sugiere una separación artificial entre clases.  
En el dataset sintético, los rangos de `packet_rate` no se superponen significativamente (Normal: 20–80 pps vs DoS: 300–800 pps), lo que permite al modelo aprender umbrales simples.  

**Implicaciones Prácticas:**  

El rendimiento podría disminuir en escenarios reales con:

- Tráfico legítimo con picos (streaming, descargas).  
- Ataques DoS de baja tasa (Slowloris).  
- Variabilidad natural del tráfico empresarial.  

A pesar de eso, el modelo demuestra la viabilidad de técnicas de Machine Learning para detección de DoS, con **99.8% de detección y 0.4% de falsas alarmas**.
