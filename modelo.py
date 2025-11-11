import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from dataset import usuarios  

def obtener_estadisticas_reales():
    scores, tiempos, grabs, posiciones = [], [], [], []

    for usuario in usuarios:
        score = float(usuario.get("TotalScore", 0))
        grab_attempts = float(usuario.get("GrabAttempts", 0))

        situaciones = usuario.get("Situations", {})
        if situaciones:
            tiempos_usuario = [float(v) for v in situaciones.values()]
            tiempo_prom = np.mean(tiempos_usuario)
        else:
            tiempo_prom = np.random.uniform(10, 18)

        posiciones_usuario = usuario.get("Positions", {})
        num_posiciones = len(posiciones_usuario) if posiciones_usuario else np.random.randint(100, 400)

        scores.append(score)
        tiempos.append(tiempo_prom)
        grabs.append(grab_attempts)
        posiciones.append(num_posiciones)

    return {
        "score_mean": np.mean(scores),
        "score_std": np.std(scores),
        "tiempo_mean": np.mean(tiempos),
        "tiempo_std": np.std(tiempos),
        "grab_mean": np.mean(grabs),
        "grab_std": np.std(grabs),
        "pos_mean": np.mean(posiciones),
        "pos_std": np.std(posiciones)
    }

def simular_jugador(stats):
    score = np.random.normal(stats["score_mean"], stats["score_std"])
    tiempo_prom = np.random.normal(stats["tiempo_mean"], stats["tiempo_std"])
    grab_attempts = np.random.normal(stats["grab_mean"], stats["grab_std"])
    num_posiciones_prom = np.random.normal(stats["pos_mean"], stats["pos_std"])

    apto = 1 if (score >= 600 and tiempo_prom <= 12 and grab_attempts <= 10 and num_posiciones_prom <= 350) else 0
    return [score, tiempo_prom, grab_attempts, num_posiciones_prom], apto

def construir_dataset_combinado(n_simulados=2000):
    stats = obtener_estadisticas_reales()
    X, y = [], []

    for u in usuarios:
        score = float(u.get("TotalScore", 0))
        grab_attempts = float(u.get("GrabAttempts", 0))

        situaciones = u.get("Situations", {})
        if situaciones:
            tiempos_usuario = [float(v) for v in situaciones.values()]
            tiempo_prom = np.mean(tiempos_usuario)
        else:
            tiempo_prom = np.random.uniform(10, 18)

        posiciones_usuario = u.get("Positions", {})
        num_posiciones_prom = len(posiciones_usuario) if posiciones_usuario else np.random.randint(100, 400)

        apto = 1 if (score >= 600 and tiempo_prom <= 12 and grab_attempts <= 10 and num_posiciones_prom <= 350) else 0
        X.append([score, tiempo_prom, grab_attempts, num_posiciones_prom])
        y.append(apto)

    for _ in range(n_simulados):
        features, etiqueta = simular_jugador(stats)
        X.append(features)
        y.append(etiqueta)

    return np.array(X), np.array(y)

def crear_modelo():
    X, y = construir_dataset_combinado(3000)
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
