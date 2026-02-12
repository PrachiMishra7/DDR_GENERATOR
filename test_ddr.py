import unittest
import os
import json
from main import DDRGenerator

class TestDDRGenerator(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = DDRGenerator()
    
    def test_file_loading(self):
        """Test that documents can be loaded"""
        # Test with actual input file
        if os.path.exists("input/inspection_report.txt"):
            text = self.generator.load_document("input/inspection_report.txt")
            self.assertIsNotNone(text, "Document should not be None")
            self.assertGreater(len(text), 0, "Document should have content")
            print("✅ File loading test passed")
        else:
            self.skipTest("Input file not found")
    
    def test_extraction_returns_json(self):
        """Test that extraction returns valid JSON structure"""
        sample_text = """
        Master Bedroom: Water stain observed on ceiling near window.
        Temperature reading: 15°C
        Severity: High
        """
        result = self.generator.extract_observations(sample_text, "inspection")
        
        # Check structure
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertIn('observations', result, "Result should have 'observations' key")
        self.assertIsInstance(result['observations'], list, "Observations should be a list")
        print("✅ Extraction format test passed")
    
    def test_merge_groups_by_location(self):
        """Test that merging correctly groups observations by location"""
        inspection = {
            "observations": [
                {"location": "Bedroom", "issue": "Water stain", "severity": "High"}
            ]
        }
        thermal = {
            "observations": [
                {"location": "Bedroom", "issue": "Cold spot detected", "severity": "Medium"}
            ]
        }
        
        merged = self.generator.merge_observations(inspection, thermal)
        
        # Check that bedroom has both observations
        self.assertIn("Bedroom", merged, "Merged data should have 'Bedroom' location")
        self.assertEqual(len(merged["Bedroom"]), 2, "Bedroom should have 2 observations")
        print("✅ Merge grouping test passed")
    
    def test_output_directory_exists(self):
        """Test that output directory is created"""
        self.assertTrue(os.path.exists("output"), "Output directory should exist")
        print("✅ Output directory test passed")
    
    def test_api_key_loaded(self):
        """Test that API key is properly loaded"""
        self.assertIsNotNone(self.generator.client, "Groq client should be initialized")
        print("✅ API key test passed")

def run_tests():
    """Run all tests and print summary"""
    print("\n" + "="*60)
    print("🧪 RUNNING DDR GENERATOR TESTS")
    print("="*60 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDDRGenerator)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failed: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)