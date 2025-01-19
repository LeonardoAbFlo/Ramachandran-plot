import streamlit as st
import matplotlib.pyplot as plt
from ramachandraw.parser import get_phi_psi
from ramachandraw.utils import fetch_pdb 
from ramachandraw.utils import plot
from io import BytesIO 

st.title("Generador de Diagrama de Ramachandran")
st.text("Autor: Leonardo Marcelo Abanto-Florez")

st.sidebar.image("ramachandran_logo.png", caption="inRamachandran")

# Opciones para ingresar el archivo PDB
pdb_option = st.radio("Selecciona cómo ingresar el archivo PDB:", ('Por URL', 'Por código PDB', 'Subir archivo PDB'))

# Opción 1: Ingresar URL
if pdb_option == 'Por URL':
    pdb_url = st.text_input("Ingresa la URL del archivo PDB (por ejemplo: https://files.rcsb.org/view/3PL1.pdb):")
    if pdb_url:
        try:
            response = requests.get(pdb_url)
            response.raise_for_status()  # Verifica si la solicitud fue exitosa
            pdb_file = response.text
        except requests.exceptions.RequestException as e:
            st.error(f"Error al intentar descargar el archivo: {e}")

# Opción 2: Ingresar código PDB
elif pdb_option == 'Por código PDB':
    pdb_id = st.text_input("Escribe el código PDB (ej: 3PL1):", "3PL1")
    if pdb_id:
        pdb_file = fetch_pdb(pdb_id)

# Opción 3: Subir archivo PDB local
elif pdb_option == 'Subir archivo PDB':
    pdb_file = st.file_uploader("Carga tu archivo PDB", type="pdb")
    if pdb_file:
        pdb_file = pdb_file.read().decode("utf-8")

# Si se tiene el archivo PDB
if pdb_file:
    # Visualización del diagrama de Ramachandran
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
