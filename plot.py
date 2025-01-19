import streamlit as st
import matplotlib.pyplot as plt
from ramachandraw.parser import get_phi_psi
from ramachandraw.utils import fetch_pdb 
from ramachandraw.utils import plot
from io import BytesIO 

st.title("Generador de Diagrama de Ramachandran")
st.text("Autor: Jesús Alvarado-Huayhuaz")

st.sidebar.image("ramachandran_logo.png", caption="inRamachandran")

pdb_id = st.text_input("Escribe el código PDB de 4 dígitos, por ejemplo: ", "3PL1")
pdb_file = fetch_pdb(pdb_id)
plt.figure()
plot(pdb_file)

st.markdown("**Resultado :gift:**")
st.pyplot(plt.gcf())

# Buffer de memoria para guardar la imagen
buffer = BytesIO()
plt.savefig(buffer, format='png')
buffer.seek(0)  

# Botón de descarga
st.download_button(
    label="Descargar imagen",
    data=buffer,
    file_name=f"diagrama_ramachandran_{pdb_id}.png",
    mime="image/png"
)

st.balloons()

