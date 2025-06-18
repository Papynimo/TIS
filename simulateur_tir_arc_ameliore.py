import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Simulateur de tir à l'arc amélioré", layout="centered")
st.title("🏹 Simulateur de tir à l'arc amélioré")

st.markdown("""
Ce simulateur calcule la trajectoire d'une flèche selon :
- **Force de l'arc** (livres)
- **Allonge de l'archer** (pouces)
- **Poids de la flèche** (grammes)
- **Hauteur de tir** (m)
- **Angle de tir** (°)
""")

# --- Entrées utilisateur ---
force_lbs = st.slider("🎯 Force de l'arc (lbs)", 20, 80, 40)
draw_length_in = st.slider("📏 Allonge (inches)", 20, 30, 28)
poids_fleche_g = st.slider("🏹 Poids de la flèche (g)", 20, 50, 30)
hauteur_depart = st.slider("📐 Hauteur initiale (m)", 0.5, 2.0, 1.5)
angle_deg = st.slider("🧭 Angle de tir (°)", -15, 45, 0, step=5)  # de -15° à 45°("🧭 Angle de tir (°)", 0, 90, 45)

# --- Conversions ---
force_N = force_lbs * 4.44822       # lbs → N
draw_m = draw_length_in * 0.0254    # inches → m
masse_kg = poids_fleche_g / 1000.0  # g → kg
theta = np.radians(angle_deg)
g = 9.81

# --- Vitesse initiale sans rendement ---
v0 = np.sqrt(2 * force_N * draw_m / masse_kg)
# Plafonnage réaliste à 70 m/s
v0 = min(v0, 70.0)

# --- Paramètres frottements ---
Cd = 0.47           # coefficient de traînée de la flèche
rho = 1.225         # densité de l'air (kg/m³)
diam_f = 0.007      # diamètre approximatif de la flèche (m)
surf = np.pi*(diam_f/2)**2  # surface frontale

# --- Initialisation de la simulation ---
dt = 0.01
x_vals = [0.0]
y_vals = [hauteur_depart]
vx = v0 * np.cos(theta)
vy = v0 * np.sin(theta)
t = 0.0

# --- Boucle de simulation (Euler explicite) ---
# On limite à 6 s et 250 m max pour éviter les valeurs irréalistes
while y_vals[-1] >= 0 and t < 6.0 and x_vals[-1] < 250.0:[-1] < 250.0:
    v = np.hypot(vx, vy)
    Fd = 0.5 * rho * Cd * surf * v**2
    ax = - (Fd * vx / v) / masse_kg
    ay = -g - (Fd * vy / v) / masse_kg
    # intégration des vitesses
    vx += ax * dt
    vy += ay * dt
    # sauvegarde des anciennes positions
    x_prev, y_prev = x_vals[-1], y_vals[-1]
    # intégration des positions
    x_new = x_prev + vx * dt
    y_new = y_prev + vy * dt
    x_vals.append(x_new)
    y_vals.append(y_new)
    # temps
    t += dt
    # arrêt si la flèche touche le sol
    if y_new < 0:
        # interpolation linéaire pour l'impact au sol
        dy = y_new - y_prev
        dx = x_new - x_prev
        frac = -y_prev / dy if dy != 0 else 0
        x_impact = x_prev + frac * dx
        y_impact = 0.0
        x_vals[-1] = x_impact
        y_vals[-1] = y_impact
        break

# --- Calculs finaux ---
# distance et temps de vol
# Si on est sorti sans toucher le sol (limite temps ou distance), on prend le dernier point
distance = x_vals[-1]
temps_vol = t
distance = x_vals[-1]
temps_vol = t

# --- Affichage de la trajectoire ---
fig, ax = plt.subplots()
ax.plot(x_vals, y_vals, label="Trajectoire")
ax.plot(distance, y_vals[-1], 'ro', label="Impact")
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Hauteur (m)")
ax.set_title("Trajectoire de la flèche")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# --- Résultats ---
st.success(f"📏 Distance parcourue : {distance:.2f} m")
st.success(f"⏱️ Temps de vol      : {temps_vol:.2f} s")

st.caption("Fait avec ❤️ pour les passionnés de tir à l'arc")

