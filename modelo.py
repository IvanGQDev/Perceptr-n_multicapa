import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split

def simular_jugador():
    score = np.random.randint(400, 1500)
    tiempo_prom = np.random.uniform(10, 18)
    grab_attempts = np.random.randint(1, 20)
    num_posiciones_prom = np.random.randint(140, 430)
    apto = 1 if (score >= 600 and tiempo_prom <= 12 and grab_attempts <= 10 and num_posiciones_prom <= 350) else 0
    return [score, tiempo_prom, grab_attempts, num_posiciones_prom], apto

def simular_dataset(n=2000):
    X, y = [], []
    for _ in range(n):
        features, etiqueta = simular_jugador()
        X.append(features)
        y.append(etiqueta)
    return np.array(X), np.array(y)

def crear_modelo():
    X, y = simular_dataset(5000)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = models.Sequential([
        layers.Input(shape=(X.shape[1],)),
        layers.Dense(32, activation='relu'),
        layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])

    modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    modelo.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))

    loss, acc = modelo.evaluate(X_test, y_test)
    print(f"\nPrecisión del modelo en test: {acc:.2f}")
    return modelo

def evaluar_speedrun(modelo, speedrun, umbral=0.4):
    X_real = np.array([[speedrun['score'], speedrun['tiempo_prom'],
                        speedrun['grab_attempts'], speedrun['num_posiciones_prom']]])
    pred = modelo.predict(X_real)[0][0]
    speedrun['resultado_final'] = 1 if pred >= umbral else 0
    speedrun['prob_apto'] = float(pred)
    speedrun['clasificacion'] = 1 if pred >= umbral else 0
    return speedrun
