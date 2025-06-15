import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulateur de tir à l'arc", layout="centered")

st.title("🏹 Simulateur de tir à l'arc amélioré")

st.markdown("""
Ce simulateur calcule la trajectoire d'une flèche selon :
- **La force de l'arc** (en livres)
- **L’allonge de l’archer** (en pouces)
- **Le poids de la flèche** (en grammes)
- **La hauteur de départ par rapport au sol**
- **L’angle de tir**
- **Le vent (en m/s)**
""")

# Entrées utilisateur
force_lbs = st.slider("🎯 Force de l’arc (livres)", 20, 80, 38)
draw_length_in = st.slider("📏 Allonge de l’archer (pouces)", 24, 32, 29)
poids_fleche_g = st.slider("🏹 Poids de la flèche (grammes)", 20, 50, 30)
hauteur_depart = st.slider("📐 Hauteur initiale de tir (m)", 0.5, 2.0, 1.55)
angle = st.slider("🧭 Angle de tir (°)", -15, 45, 0, step=5)
vent = st.slider("🌬️ Vent frontal (m/s, positif = de face)", -10, 10, 0)

# Rendement de l'arc
rendement = st.slider("⚙️ Rendement de l'arc (%)", 50, 100, 65) / 100.0

# Conversions
force_N = force_lbs * 4.448
draw_m = draw_length_in * 0.0254
masse_kg = poids_fleche_g / 1000  # grammes → kg

# Vitesse initiale
Cd = 1.5  # Traînée augmentée pour limiter la portée  # Augmentation de la traînée pour réduire la portée  # Coefficient de traînée plus réaliste pour une flèche  # Coefficient de traînée (forme cylindrique)
rho = 1.225  # Densité de l'air (kg/m^3)
diametre_fleche_m = 0.007
surface = np.pi * (diametre_fleche_m / 2)**2  # surface frontale (m²)

# rendement défini via le slider ci-dessus
v0 = min(np.sqrt(2 * rendement * force_N * draw_m / masse_kg), 70.0)  # Limite v0 à 70 m/s
theta = np.radians(angle)
g = 9.81

# Composantes de vitesse
vx = v0 * np.cos(theta)
vy = v0 * np.sin(theta)

# Calcul de la trajectoire
t = np.linspace(0, 10, 1000)
x = vx * t + 0.5 * vent * t**2  # vent comme accélération horizontale
y = hauteur_depart + vy * t - 0.5 * g * t**2

# On arrête quand la flèche touche le sol
mask = y >= 0
x = x[mask]
y = y[mask]

# Résultats
temps_vol = t[len(x) - 1]
distance_max = x[-1]


# Affichage du graphique
fig, ax = plt.subplots()
ax.plot(x, y, label="Trajectoire")
ax.plot(x[-1], y[-1], 'ro', label="Impact au sol")
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Hauteur (m)")
ax.set_title("Trajectoire simulée de la flèche")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# (Graphique de vitesse supprimé)


st.success(f"📏 Distance parcourue : {distance_max:.2f} m")
st.success(f"⏱️ Temps de vol : {temps_vol:.2f} s")

st.caption("Fait avec ❤️ pour les passionnés de tir à l'arc.")
