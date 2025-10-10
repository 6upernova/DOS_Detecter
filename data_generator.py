import pandas as pd
import numpy as np

np.random.seed(42)

cant_reg = 5000
# Tráfico Normal 
normal = pd.DataFrame({
    'packet_rate': np.random.normal(60, 25, 5000).clip(10, 150),  # Más variabilidad
    'duration': np.random.normal(5, 3, 5000).clip(0.5, 15),
    'bytes_sent': np.random.normal(2500, 1200, 5000).clip(500, 8000),
    'bytes_received': np.random.normal(2500, 1200, 5000).clip(500, 8000),
    'label': 'normal'
})

# Ataques DoS 
dos = pd.DataFrame({
    'packet_rate': np.random.normal(250, 80, 5000).clip(100, 600),  # Menor media, más overlap
    'duration': np.random.normal(1.5, 1.0, 5000).clip(0.1, 5),  # Más overlap
    'bytes_sent': np.random.normal(6000, 2000, 5000).clip(2000, 12000),  # Overlap significativo
    'bytes_received': np.random.normal(800, 500, 5000).clip(100, 3000),  # Más variabilidad
    'label': 'dos'
})

# Combinar y mezclar
data = pd.concat([normal, dos], ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)
data = data.round(2)
# Guardar
data.to_csv('synthetic_network_data.csv', index=False)
print(f" Dataset creado: {len(data)} registros")