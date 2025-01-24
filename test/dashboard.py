import streamlit as st
import pandas as pd
import os

# Læs CSV-filen
df = pd.read_csv('Data/test_logdata.csv')

# Funktion til at vise billeder for en valgt cyklus
def show_images_for_cycle(selected_cycle):
    # Filtrer DataFrame for den valgte cyklus
    cycle_data = df[df['Cycle'] == selected_cycle]
    
    # Tjek om der er billeder for den valgte cyklus
    if 'LoggedImageFiles' in cycle_data.columns:
        logged_images = cycle_data['LoggedImageFiles'].iloc[-1]  # Få billedfilene for den første række
        
        # Hvis logged_images ikke er NaN, så splittes den
        if pd.notna(logged_images):
            image_files = [image.strip() for image in logged_images.split(',')]  # Trim ekstra mellemrum
            image_dir = os.path.abspath(r'C:\Users\student\Visualisering Scape\images')  # Absolut sti
            
            st.write(f"Showing images for Cycle {selected_cycle}:")
            
            # Vis billederne
            for image_file in image_files:
                image_path = os.path.join(image_dir, image_file)
                if os.path.exists(image_path):  # Tjek om billedfilen eksisterer
                    st.image(image_path, caption=image_file, use_container_width=True)
                else:
                    st.warning(f"Image file {image_file} was not found.")
        else:
            st.warning(f"No images found for Cycle {selected_cycle}.")
    else:
        st.warning(f"No images found for Cycle {selected_cycle}.")

# Streamlit app layout
st.title("Cycle Image Viewer")

# Dropdown menu til at vælge cyklus
cycles = df['Cycle'].unique()  # Hent unikke cyklusser fra DataFrame
selected_cycle = st.selectbox("Choose a cycle", cycles)

# Vis billeder for den valgte cyklus
if selected_cycle is not None:
    show_images_for_cycle(selected_cycle)

