# === MVP Plataforma Energética: Streamlit ===

import streamlit as st
import pandas as pd
import datetime
import openai

# === Configuración general ===
st.set_page_config(page_title="Análisis Energético", layout="centered")
st.title("🔋 Plataforma de Diagnóstico Energético")
st.write("Ingresa tus datos de consumo para recibir recomendaciones personalizadas.")

# === Configurar la API de OpenAI ===
openai.api_key = st.secrets["openai_api_key"]

# === Formulario de entrada ===
with st.form("form_consumo"):
    tipo_cliente = st.selectbox("Tipo de cliente", ["Residencial", "PYME", "Industrial"])
    region = st.selectbox("Región", ["Metropolitana", "Valparaíso", "Biobío", "Araucanía", "Otra"])
    consumo_mensual_kwh = st.number_input("Consumo mensual (kWh)", min_value=0.0, step=10.0)
    costo_mensual = st.number_input("Costo mensual (CLP)", min_value=0.0, step=1000.0)
    carga_critica = st.number_input("% de consumo en horario punta (estimado)", min_value=0.0, max_value=100.0)
    submit = st.form_submit_button("Generar Informe")

# === Lógica de diagnóstico ===
if submit:
    ahorro_ee = consumo_mensual_kwh * 0.15
    ahorro_solar = consumo_mensual_kwh * 0.30
    potencia_recomendada_kwp = round(consumo_mensual_kwh / 120.0, 1)

    st.subheader("🔍 Diagnóstico Inicial")
    st.write(f"**Tipo de Cliente:** {tipo_cliente}")
    st.write(f"**Ubicación:** {region}")
    st.write(f"**Consumo mensual:** {consumo_mensual_kwh} kWh")
    st.write(f"**Costo mensual:** ${int(costo_mensual):,} CLP")

    st.subheader("💡 Recomendaciones")
    st.markdown(f"- Eficiencia Energética: podrías ahorrar **{ahorro_ee:.0f} kWh/mes** (~15%).")
    st.markdown(f"- Solar Fotovoltaico: podrías cubrir hasta **{ahorro_solar:.0f} kWh/mes** (~30%).")
    st.markdown(f"- Potencia recomendada para instalación solar: **{potencia_recomendada_kwp} kWp**.")

    # === Informe generado por IA ===
    st.subheader("📄 Informe Inteligente")
    with st.spinner("Generando informe personalizado con IA..."):
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asesor energético experto. Tu tarea es explicar recomendaciones de ahorro energético de forma clara y simple para clientes en Chile."},
                {"role": "user", "content": f"Cliente tipo: {tipo_cliente}. Región: {region}. Consumo mensual: {consumo_mensual_kwh} kWh. Costo mensual: {costo_mensual} CLP. Ahorro estimado por eficiencia energética: {ahorro_ee:.0f} kWh. Ahorro por solar: {ahorro_solar:.0f} kWh. Potencia solar recomendada: {potencia_recomendada_kwp} kWp."}
            ]
        )
        informe_ia = respuesta["choices"][0]["message"]["content"]
        st.success("Informe generado con éxito")
        st.text_area("Informe generado por IA", informe_ia, height=300)
        st.download_button(
            label="Descargar informe IA (.txt)",
            data=informe_ia,
            file_name="informe_energetico_IA.txt",
            mime="text/plain"
        )
