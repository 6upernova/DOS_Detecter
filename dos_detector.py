from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Consumo el data set
df = pd.read_csv('synthetic_network_data.csv')


print("INFORMACIÓN DEL DATASET\n")
print(f"Total de registros: {len(df)}")
print(f"Distribución de clases:\n   {df['label'].value_counts()}")
print(f"\nPrimeras 5 filas:")
print(df.head())

# Preparacion

# Codificar labels
df['label_num'] = df['label'].map({'normal': 0, 'dos': 1})

feature_cols = ['packet_rate', 'duration', 'bytes_sent', 'bytes_received']

X = df[feature_cols]
y = df['label_num']


# Análisis de correlación
print("\n MATRIZ DE CORRELACIÓN")
correlation_matrix = X.corr()
print(correlation_matrix)

# Division y escalado

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n DIVISIÓN DE DATOS")
print(f"   Entrenamiento: {len(X_train)} muestras")
print(f"   Prueba: {len(X_test)} muestras")
print(f"   Distribución train: Normal={sum(y_train==0)}, DoS={sum(y_train==1)}")
print(f"   Distribución test: Normal={sum(y_test==0)}, DoS={sum(y_test==1)}")

# Escalado
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)
model_name = "Logistic Regression"

# Coeficientes del modelo
coef_df = pd.DataFrame({
    'Feature': feature_cols,
    'Coefficient': model.coef_[0]
}).sort_values('Coefficient', key=abs, ascending=False)

print("\n COEFICIENTES DEL MODELO:")
print(coef_df.to_string(index=False))

# Metricas de machine learning

y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

fpr_rate = fp / (fp + tn)  # False Positive Rate
fnr_rate = fn / (fn + tp)  # False Negative Rate
specificity = tn / (tn + fp)  # Specificity

print(" MÉTRICAS PRINCIPALES")
print(f"   Accuracy:        {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"   Precision:       {precision:.4f} ({precision*100:.2f}%)")
print(f"   Recall:          {recall:.4f} ({recall*100:.2f}%)")
print(f"   F1-Score:        {f1:.4f} ({f1*100:.2f}%)")

print("\n TASAS DE ERROR")
print(f"   False Positive Rate: {fpr_rate:.4f} ({fpr_rate*100:.2f}%)")
print(f"   False Negative Rate: {fnr_rate:.4f} ({fnr_rate*100:.2f}%)")

print("\n MATRIZ DE CONFUSIÓN")
print(f"   False Positives: {fp} ")
print(f"   True Negatives:  {tn} ")
print(f"   False Negatives: {fn} ")
print(f"   True Positives:  {tp} ")

print(f"\n{'='*70}")
print("CLASSIFICATION REPORT")
print(f"{'='*70}\n")
print(classification_report(y_test, y_pred, target_names=['Normal', 'DoS'], digits=4))



