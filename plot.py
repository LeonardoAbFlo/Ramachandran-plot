import streamlit as st
import matplotlib.pyplot as plt
from ramachandraw.utils import plot
from io import BytesIO
import requests

# Función para obtener la estructura de AlphaFold
def get_alphafold_structure(sequence):
    url = 'https://colabfold.com/api/v1/predict'
    payload = {'sequence': sequence}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()  # Esto devuelve la estructura generada por AlphaFold
    else:
        return None

# Título de la aplicación
st.title("Generador de Diagrama de Ramachandran con AlphaFold")
st.text("Autor: Leonardo Marcelo Abanto-Florez")

# Entrada de texto para la secuencia de aminoácidos
sequence = st.text_input("Escribe la secuencia de aminoácidos: ", "")

if sequence:
    # Obtener estructura de AlphaFold
    alphafold_structure = get_alphafold_structure(sequence)
    if alphafold_structure:
        pdb_file = alphafold_structure['pdb']  # Suponiendo que recibes un archivo PDB
        plt.figure()
        plot(pdb_file)  # Visualiza el diagrama de Ramachandran

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
            file_name="diagrama_ramachandran.png",
            mime="image/png"
        )

        st.balloons()
    else:
        st.error("No se pudo obtener la estructura de AlphaFold.")
    
