"""
Integration test to verify new microservices work correctly
This test should be run after docker-compose is up
"""
import os
import sys

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"{GREEN}✓{RESET} {description}: {filepath}")
        return True
    else:
        print(f"{RED}✗{RESET} {description}: {filepath} NOT FOUND")
        return False

def main():
    print("\n" + "="*60)
    print("VERIFYING GPT-2 MICROSERVICES IMPLEMENTATION")
    print("="*60 + "\n")
    
    all_checks_passed = True
    
    # Check sentiment-analyzer files
    print(f"{YELLOW}Sentiment Analyzer Service:{RESET}")
    base = "backend/sentiment-analyzer"
    checks = [
        (f"{base}/Dockerfile", "Dockerfile"),
        (f"{base}/requirements.txt", "Requirements"),
        (f"{base}/app/__init__.py", "App init"),
        (f"{base}/app/analyzer.py", "Analyzer module"),
        (f"{base}/app/consumer.py", "Consumer"),
        (f"{base}/app/db.py", "Database module"),
        (f"{base}/tests/test_analyzer.py", "Tests"),
    ]
    for filepath, desc in checks:
        if not check_file_exists(filepath, desc):
            all_checks_passed = False
    print()
    
    # Check text-generator files
    print(f"{YELLOW}Text Generator Service:{RESET}")
    base = "backend/text-generator"
    checks = [
        (f"{base}/Dockerfile", "Dockerfile"),
        (f"{base}/requirements.txt", "Requirements"),
        (f"{base}/app/__init__.py", "App init"),
        (f"{base}/app/generator.py", "Generator module"),
        (f"{base}/app/consumer.py", "Consumer"),
        (f"{base}/app/db.py", "Database module"),
        (f"{base}/tests/test_generator.py", "Tests"),
    ]
    for filepath, desc in checks:
        if not check_file_exists(filepath, desc):
            all_checks_passed = False
    print()
    
    # Check updated backend files
    print(f"{YELLOW}Backend Updates:{RESET}")
    checks = [
        ("backend/app/database.py", "Updated database.py"),
        ("backend/app/models.py", "Updated models.py"),
        ("backend/app/routes.py", "Updated routes.py"),
        ("backend/app/messaging.py", "Updated messaging.py"),
    ]
    for filepath, desc in checks:
        if not check_file_exists(filepath, desc):
            all_checks_passed = False
    print()
    
    # Check GitHub Actions
    print(f"{YELLOW}GitHub Actions:{RESET}")
    checks = [
        (".github/workflows/test.yml", "Test workflow"),
        (".github/workflows/docker-build-push.yml", "Docker build workflow"),
    ]
    for filepath, desc in checks:
        if not check_file_exists(filepath, desc):
            all_checks_passed = False
    print()
    
    # Check docker-compose
    print(f"{YELLOW}Docker Compose:{RESET}")
    if check_file_exists("docker-compose.yml", "Docker Compose"):
        with open("docker-compose.yml", 'r') as f:
            content = f.read()
            if "sentiment-analyzer:" in content:
                print(f"{GREEN}✓{RESET} Sentiment analyzer service configured")
            else:
                print(f"{RED}✗{RESET} Sentiment analyzer service NOT in docker-compose.yml")
                all_checks_passed = False
                
            if "text-generator:" in content:
                print(f"{GREEN}✓{RESET} Text generator service configured")
            else:
                print(f"{RED}✗{RESET} Text generator service NOT in docker-compose.yml")
                all_checks_passed = False
    print()
    
    # Summary
    print("="*60)
    if all_checks_passed:
        print(f"{GREEN}✓ ALL CHECKS PASSED!{RESET}")
        print("\nYou can now run:")
        print("  docker-compose up --build")
        return 0
    else:
        print(f"{RED}✗ SOME CHECKS FAILED{RESET}")
        print("Please review the errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
