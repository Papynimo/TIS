```python
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulateur de tir à l'arc", layout="centered")
st.title("🏹 Simulateur de tir à l'arc simplifié")

st.markdown("""
Ce simulateur calcule la trajectoire d'une flèche selon :
- **La force de l'arc** (en livres)
- **L’allonge de l’archer** (en pouces)
- **Le poids de la flèche** (en grammes)
- **La hauteur de départ par rapport au sol**
- **L’angle de tir**
""")

# Entrées utilisateur
force_lbs      = st.slider("🎯 Force de l’arc (livres)",     20, 80, 40)
draw_length_in = st.slider("📏 Allonge de l’archer (pouces)", 24, 32, 28)
poids_fleche_g = st.slider("🏹 Poids de la flèche (grammes)", 20, 50, 30)
hauteur_depart = st.slider("📐 Hauteur initiale de tir (m)",  0.5,  2.0, 1.5)
angle_deg      = st.slider("🧭 Angle de tir (°)",           0,  90, 45)

# Conversions physiques
force_N  = force_lbs * 4.44822      # livres → newtons
draw_m   = draw_length_in * 0.0254  # pouces → mètres
masse_kg = poids_fleche_g / 1000.0  # grammes → kg
theta    = np.radians(angle_deg)
g        = 9.81                      # m/s²

# Vitesse initiale (énergie d’arc sans rendement)
v0 = np.sqrt(2 * force_N * draw_m / masse_kg)
# Plafond réaliste de la vitesse
v0 = min(v0, 70.0)

# Paramétrage du temps
dt = 0.01
x_vals = [0.0]
y_vals = [0.0]
t = 0.0

# Composantes de la vitesse initiale
vx = v0 * np.cos(theta)
vy = v0 * np.sin(theta)

# Boucle Euler jusqu'à impact ou limites réalistes
while y_vals[-1] >= 0 and t < 6.0 and x_vals[-1] < 250.0:
    # Mise à jour des positions
    x_new = x_vals[-1] + vx * dt
    y_new = y_vals[-1] + vy * dt
    x_vals.append(x_new)
    y_vals.append(y_new)
    # Gravité
    vy = vy - g * dt
    # Avance temporel
    t += dt

# Résultats
distance_max = x_vals[-1]
temps_vol    = t

# Affichage de la trajectoire
fig, ax = plt.subplots()
ax.plot(x_vals, y_vals, label="Trajectoire")
ax.plot(distance_max, y_vals[-1], 'ro', label="Impact au sol")
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Hauteur (m)")
ax.set_title("Trajectoire simplifiée de la flèche")
ax.legend()
st.pyplot(fig)

# Résultats clés
st.success(f"📏 Distance parcourue : {distance_max:.2f} m")
st.success(f"⏱️ Temps de vol      : {temps_vol:.2f} s")

st.caption("Fait avec ❤️ pour les passionnés de tir à l'arc.")
```
