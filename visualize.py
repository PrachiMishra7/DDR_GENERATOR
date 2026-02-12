import json
import matplotlib.pyplot as plt
from collections import Counter

def visualize_severity(merged_data):
    """Create severity distribution chart"""
    severities = []
    for location, observations in merged_data.items():
        for obs in observations:
            severities.append(obs.get('severity', 'unknown'))
    
    severity_counts = Counter(severities)
    
    plt.figure(figsize=(8, 6))
    colors = {'high': 'red', 'medium': 'orange', 'low': 'green', 'unknown': 'gray'}
    bar_colors = [colors.get(sev.lower(), 'gray') for sev in severity_counts.keys()]
    
    plt.bar(severity_counts.keys(), severity_counts.values(), color=bar_colors)
    plt.title('Issue Severity Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Severity Level', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('output/severity_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Severity chart saved to output/severity_chart.png")

def generate_summary_stats(inspection_data, thermal_data):
    """Generate statistics"""
    stats = {
        "total_inspection_observations": len(inspection_data.get('observations', [])),
        "total_thermal_observations": len(thermal_data.get('observations', [])),
        "unique_locations": len(set(
            [obs['location'] for obs in inspection_data.get('observations', [])] + 
            [obs['location'] for obs in thermal_data.get('observations', [])]
        )),
        "sources_processed": 2
    }
    
    with open('output/statistics.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"✅ Statistics saved to output/statistics.json")
    print(f"   📊 Total observations: {stats['total_inspection_observations'] + stats['total_thermal_observations']}")
    print(f"   📍 Unique locations: {stats['unique_locations']}")
    return stats