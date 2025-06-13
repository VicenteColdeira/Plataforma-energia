# === MVP Plataforma Energética: Streamlit ===

import streamlit as st
import pandas as pd
import datetime
from openai import OpenAI

# === Configuración general ===
st.set_page_config(page_title="Análisis Energético", layout="centered")
st.title("🔋 Plataforma de Diagnóstico Energético")
st.write("Ingresa tus datos de consumo para recibir recomendaciones personalizadas.")

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

    st.subheader("📄 Informe Generado")
    informe = f"""
    Informe Energético
    ------------------
    Tipo de cliente: {tipo_cliente}
    Región: {region}
    Consumo mensual: {consumo_mensual_kwh} kWh
    Costo mensual: ${int(costo_mensual):,} CLP

    Diagnóstico:
    - Eficiencia Energética: Se estima un ahorro potencial de {ahorro_ee:.0f} kWh mensuales.
    - Energía Solar: Hasta un 30% de cobertura con una instalación de aproximadamente {potencia_recomendada_kwp} kWp.
    - Recomendación especial: Considerar medidas en horario punta si supera el 20% del consumo total.

    Fecha de generación: {datetime.datetime.now().strftime('%d-%m-%Y')}
    """
    st.text(informe)

    # Botón para descarga futura
    st.download_button(
        label="Descargar informe como TXT",
        data=informe,
        file_name="informe_energetico.txt",
        mime="text/plain"
    )
