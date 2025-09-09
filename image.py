import os
import streamlit as st
from openai import OpenAI

def generate_image():
    client = openai.OpenAI(api_key=openai_api_key)
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"Generate a famous landmark of the {city}"
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url
    st.image(image_url, caption=prompt)
    return image_url

def image_loader(city):
    image_dir = "images"  # your image folder
    image_file = f"{city}"  # replace with your image filename

    image_path = os.path.join(image_dir, image_file)
    if os.path.exists(image_path):
        st.image(image_path, caption=image_file)
    elif not os.path.exists(image_dir):
        generate_image()
        
#else:
    #st.warning(f"Image {image_file} not found in {image_dir}.")


