import streamlit as st
import os
from main import DDRGenerator
from visualize import visualize_severity, generate_summary_stats
import json
from datetime import datetime

st.set_page_config(
    page_title="DDR Report Generator",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 DDR Report Generator")
st.markdown("### AI-Powered Detailed Diagnostic Report Generation")
st.markdown("---")

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)
os.makedirs("temp_uploads", exist_ok=True)

# Sidebar
with st.sidebar:
    st.header("📋 Instructions")
    st.markdown("""
    1. Upload your **Inspection Report** (txt file)
    2. Upload your **Thermal Report** (txt file)
    3. Click **Generate DDR Report**
    4. Download the generated report
    
    ---
    
    ### ✨ Features
    - ✅ Extracts observations from both reports
    - ✅ Intelligent deduplication
    - ✅ Conflict detection
    - ✅ Missing data handling
    - ✅ Severity visualization
    
    ---
    
    ### 🎯 Output Includes
    - 📄 Structured DDR Report (Markdown)
    - 📊 Severity Distribution Chart
    - 📈 Summary Statistics
    - 📋 Generation Metadata
    """)

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Upload Inspection Report")
    inspection_file = st.file_uploader(
        "Choose inspection report file",
        type=['txt'],
        key="inspection"
    )
    
    if inspection_file:
        st.success(f"✅ Loaded: {inspection_file.name}")
        inspection_preview = inspection_file.read().decode('utf-8')
        with st.expander("Preview Inspection Report"):
            st.text_area("Content", inspection_preview, height=200, key="insp_preview")
        inspection_file.seek(0)  # Reset file pointer

with col2:
    st.subheader("🌡️ Upload Thermal Report")
    thermal_file = st.file_uploader(
        "Choose thermal report file",
        type=['txt'],
        key="thermal"
    )
    
    if thermal_file:
        st.success(f"✅ Loaded: {thermal_file.name}")
        thermal_preview = thermal_file.read().decode('utf-8')
        with st.expander("Preview Thermal Report"):
            st.text_area("Content", thermal_preview, height=200, key="therm_preview")
        thermal_file.seek(0)  # Reset file pointer

st.markdown("---")

# Generate button
if st.button("🚀 Generate DDR Report", type="primary", use_container_width=True):
    if not inspection_file or not thermal_file:
        st.error("⚠️ Please upload both inspection and thermal reports!")
    else:
        try:
            with st.spinner("🔄 Processing documents..."):
                # Save uploaded files temporarily
                inspection_path = "temp_uploads/inspection_report.txt"
                thermal_path = "temp_uploads/thermal_report.txt"
                
                with open(inspection_path, 'wb') as f:
                    f.write(inspection_file.read())
                with open(thermal_path, 'wb') as f:
                    f.write(thermal_file.read())
                
                # Initialize generator
                generator = DDRGenerator()
                
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Load documents
                status_text.text("📖 Loading documents...")
                progress_bar.progress(10)
                inspection_text = generator.load_document(inspection_path)
                thermal_text = generator.load_document(thermal_path)
                
                # Extract observations
                status_text.text("🔍 Extracting observations from inspection report...")
                progress_bar.progress(30)
                inspection_data = generator.extract_observations(inspection_text, "inspection")
                
                status_text.text("🌡️ Extracting observations from thermal report...")
                progress_bar.progress(50)
                thermal_data = generator.extract_observations(thermal_text, "thermal")
                
                # Merge observations
                status_text.text("🔄 Merging and deduplicating observations...")
                progress_bar.progress(70)
                merged = generator.merge_observations(inspection_data, thermal_data)
                
                # Generate DDR
                status_text.text("📝 Generating DDR report...")
                progress_bar.progress(85)
                ddr_report = generator.generate_ddr(merged)
                
                # Save report
                output_path = "output/generated_ddr.md"
                generator.save_report(ddr_report, output_path)
                
                # Generate visualizations
                status_text.text("📊 Creating visualizations...")
                progress_bar.progress(95)
                visualize_severity(merged)
                stats = generate_summary_stats(inspection_data, thermal_data)
                
                # Generate metadata
                metadata = {
                    "generated_at": datetime.now().isoformat(),
                    "generator_version": "1.0",
                    "model_used": "llama-3.3-70b-versatile",
                    "input_files": [inspection_file.name, thermal_file.name],
                    "statistics": stats
                }
                
                with open('output/metadata.json', 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                progress_bar.progress(100)
                status_text.text("✅ Generation complete!")
                
                st.success("🎉 DDR Report generated successfully!")
                
                # Display results
                st.markdown("---")
                st.subheader("📊 Summary Statistics")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Inspection Observations", stats['total_inspection_observations'])
                with col2:
                    st.metric("Thermal Observations", stats['total_thermal_observations'])
                with col3:
                    st.metric("Unique Locations", stats['unique_locations'])
                
                # Display severity chart
                st.subheader("📈 Severity Distribution")
                if os.path.exists("output/severity_chart.png"):
                    st.image("output/severity_chart.png", use_container_width=True)
                
                # Display report preview
                st.subheader("📄 Generated DDR Report")
                with st.expander("View Report", expanded=True):
                    st.markdown(ddr_report)
                
                # Download buttons
                st.markdown("---")
                st.subheader("⬇️ Download Files")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    with open(output_path, 'r') as f:
                        st.download_button(
                            label="📄 Download DDR Report",
                            data=f.read(),
                            file_name="DDR_Report.md",
                            mime="text/markdown"
                        )
                
                with col2:
                    if os.path.exists("output/severity_chart.png"):
                        with open("output/severity_chart.png", 'rb') as f:
                            st.download_button(
                                label="📊 Download Chart",
                                data=f.read(),
                                file_name="severity_chart.png",
                                mime="image/png"
                            )
                
                with col3:
                    with open("output/statistics.json", 'r') as f:
                        st.download_button(
                            label="📈 Download Statistics",
                            data=f.read(),
                            file_name="statistics.json",
                            mime="application/json"
                        )
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.error("Please check your API key and input files.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Built with ❤️ using Groq API (Llama 3.3 70B) + Streamlit</p>
    <p>DDR Report Generator v1.0</p>
</div>
""", unsafe_allow_html=True)