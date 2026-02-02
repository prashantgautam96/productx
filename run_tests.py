#!/usr/bin/env python3
"""
Comprehensive Test Runner for ResumeOS Compiler Engine
Runs all tests and provides a summary report
"""

import sys
import subprocess
import os
from pathlib import Path


def print_header(text: str):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def print_section(text: str):
    """Print a section divider"""
    print("\n" + "-" * 80)
    print(f"  {text}")
    print("-" * 80 + "\n")


def check_dependencies():
    """Check if required dependencies are installed"""
    print_header("Checking Dependencies")
    
    required_modules = {
        'jinja2': 'Jinja2 (for LaTeX rendering)',
        'json': 'JSON (standard library)',
    }
    
    missing = []
    for module, description in required_modules.items():
        try:
            __import__(module)
            print(f"✓ {description}")
        except ImportError:
            print(f"✗ {description} - MISSING")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies installed!")
    return True


def check_required_files():
    """Check if required data files exist"""
    print_header("Checking Required Files")
    
    required_files = [
        'example_master_resume.json',
        'example_job_descriptions.py',
        'resume_compiler.py',
        'latex_renderer.py',
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            missing.append(file)
    
    if missing:
        print(f"\n⚠️  Missing required files: {', '.join(missing)}")
        return False
    
    print("\n✅ All required files present!")
    return True


def run_test(test_file: str, description: str) -> bool:
    """Run a test file and return success status"""
    print_section(f"Running: {description}")
    
    if not os.path.exists(test_file):
        print(f"✗ Test file not found: {test_file}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=False,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"\n✅ {description} - PASSED")
            return True
        else:
            print(f"\n✗ {description} - FAILED (exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"\n✗ {description} - TIMEOUT (exceeded 60 seconds)")
        return False
    except Exception as e:
        print(f"\n✗ {description} - ERROR: {str(e)}")
        return False


def run_demo(demo_file: str, description: str) -> bool:
    """Run a demo file"""
    print_section(f"Running: {description}")
    
    if not os.path.exists(demo_file):
        print(f"✗ Demo file not found: {demo_file}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, demo_file],
            capture_output=False,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print(f"\n✅ {description} - COMPLETED")
            return True
        else:
            print(f"\n✗ {description} - FAILED (exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"\n✗ {description} - TIMEOUT (exceeded 120 seconds)")
        return False
    except Exception as e:
        print(f"\n✗ {description} - ERROR: {str(e)}")
        return False


def check_output_files():
    """Check if test output files were generated"""
    print_header("Checking Generated Output Files")
    
    expected_files = [
        'tailored_ai_engineer.json',
        'tailored_backend_engineer.json',
        'tailored_devops_engineer.json',
        'resume_ai_engineer.tex',
    ]
    
    found = []
    missing = []
    
    for file in expected_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✓ {file} ({size} bytes)")
            found.append(file)
        else:
            print(f"✗ {file} - Not generated")
            missing.append(file)
    
    if found:
        print(f"\n✅ Generated {len(found)} output file(s)")
    if missing:
        print(f"\n⚠️  {len(missing)} expected output file(s) not found")
        print("   (This is OK if tests haven't been run yet)")
    
    return len(found) > 0


def main():
    """Main test runner"""
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║                  ResumeOS Compiler Engine - Test Suite                  ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Pre-flight checks
    if not check_dependencies():
        print("\n⚠️  Please install missing dependencies before running tests.")
        print("   Run: pip install -r requirements.txt")
        sys.exit(1)
    
    if not check_required_files():
        print("\n⚠️  Missing required files. Cannot run tests.")
        sys.exit(1)
    
    # Run tests
    print_header("Running Test Suite")
    
    tests = [
        ('test_compiler.py', 'Compiler Engine Tests'),
        ('test_renderer.py', 'LaTeX Renderer Tests'),
    ]
    
    demos = [
        ('complete_demo.py', 'Complete Pipeline Demo'),
    ]
    
    results = []
    
    # Run unit tests
    for test_file, description in tests:
        success = run_test(test_file, description)
        results.append((description, success))
    
    # Run demos
    for demo_file, description in demos:
        success = run_demo(demo_file, description)
        results.append((description, success))
    
    # Check output files
    check_output_files()
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASSED" if success else "✗ FAILED"
        print(f"  {status:12} - {description}")
    
    print(f"\n{'=' * 80}")
    print(f"  Results: {passed}/{total} tests passed")
    print(f"{'=' * 80}\n")
    
    if passed == total:
        print("🎉 All tests passed! The ResumeOS Compiler Engine is working correctly.\n")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Please review the output above.\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
