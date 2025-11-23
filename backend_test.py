import requests
import sys
from datetime import datetime, timedelta
import json

class KAAYJANGAPITester:
    def __init__(self, base_url="https://scholar-network.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.admin_token = None
        self.teacher_token = None
        self.student_token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name, method, endpoint, expected_status, data=None, token=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = f'Bearer {token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                self.test_results.append({"test": name, "status": "PASS", "details": f"Status: {response.status_code}"})
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"Response: {response.text[:200]}")
                self.test_results.append({"test": name, "status": "FAIL", "details": f"Expected {expected_status}, got {response.status_code}"})

            try:
                return success, response.json() if response.text else {}
            except:
                return success, {"raw_response": response.text}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results.append({"test": name, "status": "ERROR", "details": str(e)})
            return False, {}

    def test_admin_login(self):
        """Test admin login"""
        success, response = self.run_test(
            "Admin Login",
            "POST",
            "auth/login",
            200,
            data={"email": "admin@kaayjang.com", "password": "admin123"}
        )
        if success and 'access_token' in response:
            self.admin_token = response['access_token']
            print(f"Admin user role: {response.get('user', {}).get('role')}")
            return True
        return False

    def test_register_teacher(self):
        """Register a test teacher"""
        teacher_email = f"teacher_test_{datetime.now().strftime('%H%M%S')}@test.com"
        success, response = self.run_test(
            "Register Teacher",
            "POST",
            "auth/register",
            200,
            data={
                "email": teacher_email,
                "password": "teacher123",
                "name": "Test Teacher",
                "role": "teacher",
                "branch_id": "",
                "level_id": ""
            }
        )
        if success and 'access_token' in response:
            self.teacher_token = response['access_token']
            self.teacher_id = response['user']['id']
            print(f"Teacher registered with ID: {self.teacher_id}")
            return True
        return False

    def test_register_student(self):
        """Register a test student"""
        student_email = f"student_test_{datetime.now().strftime('%H%M%S')}@test.com"
        success, response = self.run_test(
            "Register Student",
            "POST",
            "auth/register",
            200,
            data={
                "email": student_email,
                "password": "student123",
                "name": "Test Student",
                "role": "student",
                "branch_id": "",
                "level_id": ""
            }
        )
        if success and 'access_token' in response:
            self.student_token = response['access_token']
            self.student_id = response['user']['id']
            print(f"Student registered with ID: {self.student_id}")
            return True
        return False

    def test_get_branches(self):
        """Test getting branches"""
        success, response = self.run_test(
            "Get Branches",
            "GET",
            "branches",
            200
        )
        if success and isinstance(response, list):
            print(f"Found {len(response)} branches")
            return True
        return False

    def test_get_subjects(self):
        """Test getting subjects"""
        success, response = self.run_test(
            "Get Subjects",
            "GET",
            "subjects",
            200
        )
        if success and isinstance(response, list):
            print(f"Found {len(response)} subjects")
            return True
        return False

    def test_admin_stats(self):
        """Test admin stats endpoint"""
        success, response = self.run_test(
            "Admin Stats",
            "GET",
            "admin/stats",
            200,
            token=self.admin_token
        )
        if success:
            print(f"Stats: {response}")
            return True
        return False

    def test_pending_teachers(self):
        """Test getting pending teachers"""
        success, response = self.run_test(
            "Get Pending Teachers",
            "GET",
            "admin/pending-teachers",
            200,
            token=self.admin_token
        )
        if success and isinstance(response, list):
            print(f"Found {len(response)} pending teachers")
            return True
        return False

    def test_validate_teacher(self):
        """Test teacher validation"""
        if hasattr(self, 'teacher_id'):
            success, response = self.run_test(
                "Validate Teacher",
                "PUT",
                f"admin/validate-teacher/{self.teacher_id}",
                200,
                token=self.admin_token
            )
            return success
        return False

    def test_get_topics(self):
        """Test getting forum topics"""
        success, response = self.run_test(
            "Get Topics",
            "GET",
            "topics",
            200,
            token=self.student_token
        )
        if success and isinstance(response, list):
            print(f"Found {len(response)} topics")
            return True
        return False

    def test_get_assignments(self):
        """Test getting assignments"""
        success, response = self.run_test(
            "Get Assignments",
            "GET",
            "assignments",
            200,
            token=self.student_token
        )
        if success and isinstance(response, list):
            print(f"Found {len(response)} assignments")
            return True
        return False

    def test_get_notifications(self):
        """Test getting notifications"""
        success, response = self.run_test(
            "Get Notifications",
            "GET",
            "notifications",
            200,
            token=self.student_token
        )
        if success and isinstance(response, list):
            print(f"Found {len(response)} notifications")
            return True
        return False

    def test_get_ad_banners(self):
        """Test getting ad banners"""
        success, response = self.run_test(
            "Get Ad Banners",
            "GET",
            "ad-banners",
            200
        )
        if success and isinstance(response, list):
            print(f"Found {len(response)} ad banners")
            return True
        return False

    def test_follow_system(self):
        """Test follow/unfollow functionality"""
        if hasattr(self, 'teacher_id') and hasattr(self, 'student_id'):
            # Student follows teacher
            success, response = self.run_test(
                "Follow User",
                "POST",
                f"follows?followed_id={self.teacher_id}",
                200,
                token=self.student_token
            )
            if success:
                # Check if following
                success2, response2 = self.run_test(
                    "Check Follow Status",
                    "GET",
                    f"follows/is-following/{self.teacher_id}",
                    200,
                    token=self.student_token
                )
                if success2 and response2.get('is_following'):
                    print("Follow system working correctly")
                    return True
        return False

def main():
    print("🚀 Starting KAAY-JANG API Tests...")
    tester = KAAYJANGAPITester()

    # Test authentication
    print("\n📋 Testing Authentication...")
    if not tester.test_admin_login():
        print("❌ Admin login failed, stopping tests")
        return 1

    if not tester.test_register_teacher():
        print("❌ Teacher registration failed")

    if not tester.test_register_student():
        print("❌ Student registration failed")

    # Test basic endpoints
    print("\n📋 Testing Basic Endpoints...")
    tester.test_get_branches()
    tester.test_get_subjects()
    tester.test_get_ad_banners()

    # Test admin functionality
    print("\n📋 Testing Admin Features...")
    tester.test_admin_stats()
    tester.test_pending_teachers()
    tester.test_validate_teacher()

    # Test forum and assignments
    print("\n📋 Testing Forum & Assignments...")
    tester.test_get_topics()
    tester.test_get_assignments()
    tester.test_get_notifications()

    # Test follow system
    print("\n📋 Testing Follow System...")
    tester.test_follow_system()

    # Print results
    print(f"\n📊 Test Results: {tester.tests_passed}/{tester.tests_run} passed")
    
    # Save detailed results
    with open('/app/test_reports/backend_test_results.json', 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_tests": tester.tests_run,
            "passed_tests": tester.tests_passed,
            "success_rate": (tester.tests_passed / tester.tests_run * 100) if tester.tests_run > 0 else 0,
            "detailed_results": tester.test_results
        }, f, indent=2)

    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())