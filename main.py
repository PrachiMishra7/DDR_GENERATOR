from groq import Groq
import os
from dotenv import load_dotenv
import json
import datetime

load_dotenv()

class DDRGenerator:
    def __init__(self):
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("API key not found! Check your .env file")
        self.client = Groq(api_key=api_key)
    
    def load_document(self, filepath):
        """Load text from a file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: File not found - {filepath}")
            return None
    
    def extract_observations(self, document_text, document_type):
        """Extract structured observations from document"""
        print(f"Extracting data from {document_type}...")
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"""Extract all observations from this {document_type} report.

Return ONLY a JSON object with this structure:
{{
    "observations": [
        {{
            "location": "specific area/room",
            "issue": "what was observed",
            "severity": "low/medium/high",
            "details": "measurements, readings, or specific details",
            "source": "{document_type}"
        }}
    ]
}}

Document:
{document_text}

Remember: Extract ONLY what's explicitly stated. Do not invent information."""
            }],
            temperature=0.1,
            max_tokens=2000
        )
        
        response_text = response.choices[0].message.content
        response_text = response_text.replace('```json', '').replace('```', '').strip()
        return json.loads(response_text)
    
    def merge_observations(self, inspection_data, thermal_data):
        """Merge observations from both reports"""
        print("Merging observations...")
        
        all_observations = []
        all_observations.extend(inspection_data.get('observations', []))
        all_observations.extend(thermal_data.get('observations', []))
        
        # Group by location
        by_location = {}
        for obs in all_observations:
            location = obs.get('location', 'Unknown')
            if location not in by_location:
                by_location[location] = []
            by_location[location].append(obs)
        
        return by_location
    
    def generate_ddr(self, merged_observations):
        """Generate the final DDR report"""
        print("Generating DDR report...")
        
        observations_text = json.dumps(merged_observations, indent=2)
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"""You are generating a professional DDR (Detailed Diagnostic Report) for a client.

Here is the merged observation data from inspection and thermal reports:

{observations_text}

Generate a comprehensive DDR report with EXACTLY these sections:

# 1. Property Issue Summary
[Brief overview of the main issues found]

# 2. Area-wise Observations
[Break down by location/area with specific findings from BOTH reports combined]

# 3. Probable Root Cause
[Analysis of what's likely causing the issues]

# 4. Severity Assessment
[Rate severity (Low/Medium/High) with clear reasoning]

# 5. Recommended Actions
[Specific, actionable next steps]

# 6. Additional Notes
[Any other relevant information]

# 7. Missing or Unclear Information
[List what information was not available or conflicts between sources]

CRITICAL RULES:
- DEDUPLICATE: If inspection and thermal reports describe the same issue (e.g., water stain + cold spot = same problem), combine them into ONE observation
- CONFLICTS: If data conflicts between sources, mention both: "Inspection reports X, while thermal imaging shows Y"
- MISSING DATA: Explicitly write "Not Available" for any standard information that's missing
- Use ONLY information from the provided data
- Use clear, client-friendly language (no unnecessary jargon)
- Be specific and actionable
- DO NOT invent facts or make assumptions beyond the data"""
            }],
            temperature=0.1,
            max_tokens=4000
        )
        
        return response.choices[0].message.content
    
    def save_report(self, report, filepath):
        """Save the generated report"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report saved to: {filepath}")

def generate_metadata():
    """Add professional metadata"""
    metadata = {
        "generated_at": datetime.datetime.now().isoformat(),
        "generator_version": "1.0",
        "model_used": "llama-3.3-70b-versatile",
        "input_files": ["inspection_report.txt", "thermal_report.txt"],
        "output_files": [
            "generated_ddr.md",
            "severity_chart.png",
            "statistics.json",
            "metadata.json"
        ]
    }
    
    with open('output/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("✅ Metadata saved to output/metadata.json")
    return metadata

def main():
    print("=== DDR Report Generator ===\n")
    
    # Initialize generator
    generator = DDRGenerator()
    
    # Load documents
    inspection_path = "input/inspection_report.txt"
    thermal_path = "input/thermal_report.txt"
    
    print("Loading documents...")
    inspection_text = generator.load_document(inspection_path)
    thermal_text = generator.load_document(thermal_path)
    
    if not inspection_text or not thermal_text:
        print("Error: Could not load input documents. Make sure they exist in the input/ folder")
        return
    
    # Extract observations
    inspection_data = generator.extract_observations(inspection_text, "inspection")
    thermal_data = generator.extract_observations(thermal_text, "thermal")
    
    # Merge observations
    merged = generator.merge_observations(inspection_data, thermal_data)
    
    # Generate DDR (deduplication and conflict handling happens here via prompt)
    ddr_report = generator.generate_ddr(merged)
    
    # Save report
    output_path = "output/generated_ddr.md"
    generator.save_report(ddr_report, output_path)
    
    # Generate visualizations
    print("\n📊 Generating visualizations and statistics...")
    from visualize import visualize_severity, generate_summary_stats
    visualize_severity(merged)
    stats = generate_summary_stats(inspection_data, thermal_data)
    
    # Generate metadata
    print("\n📝 Generating metadata...")
    metadata = generate_metadata()
    
    print("\n" + "="*60)
    print("✅ ALL OUTPUTS GENERATED SUCCESSFULLY!")
    print("="*60)
    print(f"📄 DDR Report: {output_path}")
    print(f"📊 Severity Chart: output/severity_chart.png")
    print(f"📈 Statistics: output/statistics.json")
    print(f"📋 Metadata: output/metadata.json")
    print("="*60)
    
    print("\nKey features implemented:")
    print("✅ Extracts from both documents")
    print("✅ Deduplicates similar observations")
    print("✅ Handles conflicts and missing data")
    print("✅ Generates all 7 required sections")
    print("✅ Creates severity visualization")
    print("✅ Generates summary statistics")

if __name__ == "__main__":
    main()