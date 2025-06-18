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
force_lbs       = st.slider("🎯 Force de l'arc (lbs)",        20, 80, 38)
draw_length_in  = st.slider("📏 Allonge (inches)",           20, 30, 29)
poids_fleche_g  = st.slider("🏹 Poids de la flèche (g)",     20, 50, 30)
hauteur_depart  = st.slider("📐 Hauteur initiale (m)",       0.5, 2.0, 1.55)
angle_deg       = st.slider("🧭 Angle de tir (°)",          -15, 45, 0, step=5)

# --- Conversions physiques ---
force_N  = force_lbs * 4.44822       # lbs → N
draw_m   = draw_length_in * 0.0254    # inches → m
masse_kg = poids_fleche_g / 1000.0    # g → kg
theta    = np.radians(angle_deg)
g        = 9.81                         # m/s²

# --- Vitesse initiale sans rendement ni vent ---
v0 = np.sqrt(2 * force_N * draw_m / masse_kg)
v0 = min(v0, 70.0)  # Plafonnement à 70 m/s

# --- Frottements d'air ---
Cd       = 0.47      # coefficient de traînée de la flèche
rho      = 1.225     # densité de l'air (kg/m³)
diam_f   = 0.007     # m, diamètre de la flèche
surface  = np.pi * (diam_f/2)**2

# --- Simulation Euler explicite ---
dt       = 0.01
x_vals   = [0.0]
y_vals   = [hauteur_depart]
vx       = v0 * np.cos(theta)
vy       = v0 * np.sin(theta)
t        = 0.0

# --- Boucle jusqu'à impact ---
# Simule tant que la flèche est en l'air (sécurité t_max=20s)
t_max = 20.0
while y_vals[-1] >= 0 and t < t_max:
    v   = np.hypot(vx, vy)
    Fd  = 0.5 * rho * Cd * surface * v**2
    ax  = - (Fd * vx / v) / masse_kg
    ay  = -g - (Fd * vy / v) / masse_kg
    vx += ax * dt
    vy += ay * dt
    x_prev, y_prev = x_vals[-1], y_vals[-1]
    x_new = x_prev + vx * dt
    y_new = y_prev + vy * dt
    t    += dt
    if y_new < 0:
        # interpolation linéaire pour l'impact
        dx    = x_new - x_prev
        dy    = y_new - y_prev
        frac  = -y_prev / dy if dy != 0 else 0
        x_imp = x_prev + frac * dx
        x_vals.append(x_imp)
        y_vals.append(0.0)
        break
    x_vals.append(x_new)
    y_vals.append(y_new)

# --- Résultats ---
distance = x_vals[-1]
temps_vol = t

# Affichage de la trajectoire
fig, ax = plt.subplots()
ax.plot(x_vals, y_vals, label="Trajectoire")
ax.plot(distance, 0, 'ro', label="Impact au sol")
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Hauteur (m)")
ax.set_title("Trajectoire simulée de la flèche")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Affichage des résultats
st.success(f"📏 Distance parcourue : {distance:.2f} m")
st.success(f"⏱️ Temps de vol      : {temps_vol:.2f} s")

st.caption("Fait avec ❤️ pour les passionnés de tir à l'arc")



