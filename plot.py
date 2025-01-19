import streamlit as st
import matplotlib.pyplot as plt
from ramachandraw.utils import plot
from io import BytesIO
import requests

def get_alphafold_structure(sequence):
    url = 'https://colabfold.com/api/v1/predict'
    payload = {'sequence': sequence}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        try:
            data = response.json()  # Intenta decodificar el JSON
            if 'pdb_url' in data:
                return data['pdb_url']  # Devuelve el enlace al archivo PDB
            else:
                st.error("No se encontró el archivo PDB en la respuesta.")
                return None
        except ValueError:
            st.error(f"Error al decodificar la respuesta JSON: {response.text}")
            return None
    else:
        st.error(f"Error en la solicitud: {response.status_code} - {response.text}")
        return None

# Título de la aplicación
st.title("Generador de Diagrama de Ramachandran con AlphaFold")
st.text("Autor: Leonardo Marcelo Abanto-Florez")

sequence = st.text_input("Escribe la secuencia de aminoácidos: ", "")

if sequence:
    alphafold_structure = get_alphafold_structure(sequence)
    if alphafold_structure:
        # Obtener el archivo PDB desde la URL proporcionada
        pdb_file_response = requests.get(alphafold_structure)
        
        if pdb_file_response.status_code == 200:
            pdb_file = pdb_file_response.text
            plt.figure()
            plot(pdb_file)  # Visualiza el diagrama de Ramachandran

            st.markdown("**Resultado :gift:**")
            st.pyplot(plt.gcf())

            
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            st.download_button(
                label="Descargar imagen",
                data=buffer,
                file_name="diagrama_ramachandran.png",
                mime="image/png"
            )

            st.balloons()
        else:
            st.error(f"No se pudo obtener el archivo PDB desde la URL: {alphafold_structure}")
    else:
        st.error("No se pudo obtener la estructura de AlphaFold.")
