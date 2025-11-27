# 🧪 Testing Guide - Disaster Management System

## Quick Start Testing

**Access the application:**
```
http://172.25.254.147:8000
or
http://localhost:8000
```

---

## 📋 Test Scenarios

### **1. Authentication Testing**

#### Signup (Create New User)
1. Open the app in browser
2. Click **"Sign Up"** button
3. Fill in the form:
   - **Name:** Test User
   - **Email:** testuser@example.com
   - **Password:** Password123
   - **Phone:** 9876543210
   - **Role:** Select "Citizen"
4. Click **"Sign Up"** button
5. ✅ Should redirect to login page with success message

#### Login
1. Click **"Login"** button
2. Enter credentials:
   - **Email:** admin@disaster.com (use this admin account)
   - **Password:** admin123
3. Click **"Login"**
4. ✅ Should redirect to Dashboard

#### Admin Login
- **Email:** admin@disaster.com
- **Password:** admin123
- ✅ Should show Admin Dashboard with all statistics

---

### **2. Citizen Features Testing**

#### Report a Disaster
1. Login as **Citizen** role
2. Click **"Report Disaster"** button
3. Fill disaster report form:
   - **Location:** (enter location or click map to select)
   - **Severity:** Select "High" / "Medium" / "Low"
   - **Description:** Describe the disaster incident
   - **Category:** Flood / Earthquake / Fire / etc.
4. Click **"Submit Report"**
5. ✅ Report should appear in "My Reports" list with "Pending" status

#### View My Reports
1. In Citizen Dashboard, click **"My Reports"**
2. ✅ Should show all submitted reports with:
   - Report ID
   - Location
   - Severity
   - Status (Pending, Acknowledged, In Progress, Resolved)
   - Date created

#### Track Report Status
1. Click on any report in "My Reports"
2. ✅ Should show:
   - Report details
   - Current status
   - Assigned volunteers (if any)
   - Updates/comments

#### View Active Disasters
1. Click **"Active Disasters"** tab
2. ✅ Should display all active disaster reports on map/list

#### Receive Alerts
1. Admin broadcasts an alert
2. ✅ Citizen should see notification:
   - Alert message
   - Timestamp
   - Severity level

---

### **3. Volunteer Features Testing**

#### Login as Volunteer
- **Email:** volunteer@disaster.com (or create new volunteer account)
- **Password:** volunteerpass123

#### View Assigned Tasks
1. Login as Volunteer
2. Go to **"My Tasks"**
3. ✅ Should show:
   - Task ID
   - Associated disaster report
   - Location
   - Status (Assigned, In Progress, Completed)
   - Assignment date

#### Update Task Status
1. Click on a task
2. Change status from "Assigned" → "In Progress"
3. Click **"Update Status"**
4. ✅ Status should update immediately
5. Repeat: Mark as "Completed"
6. ✅ Task should move to completed list

#### View Workload
1. Click **"Workload"** or **"Dashboard"**
2. ✅ Should show:
   - Total assigned tasks
   - Tasks in progress
   - Completed tasks
   - Efficiency metrics

---

### **4. Admin Features Testing**

#### Admin Login
- **Email:** admin@disaster.com
- **Password:** admin123

#### View Dashboard
1. Admin Dashboard should display:
   - ✅ Total disaster reports
   - ✅ Pending reports count
   - ✅ Active volunteers count
   - ✅ Total resources available
   - ✅ Recent alerts

#### Manage Reports
1. Go to **"Reports"** section
2. ✅ View all disaster reports with filters:
   - Filter by Status (Pending, Acknowledged, etc.)
   - Filter by Severity (High, Medium, Low)
   - Search by location
3. Click on a report
4. ✅ Should show report details with options to:
   - Update status
   - Assign volunteers
   - Add comments/notes

#### Assign Volunteers to Tasks
1. Go to a disaster report
2. Click **"Assign Volunteer"**
3. ✅ Select volunteer from list
4. ✅ Task should be created and assigned to volunteer
5. Volunteer should see it in their "My Tasks"

#### Manage Resources
1. Go to **"Resources"** section
2. ✅ Should show all resources:
   - Medical supplies
   - Shelter units
   - Food packets
   - Transport vehicles
3. Click **"Add Resource"**
4. Fill in resource details and availability
5. ✅ Resource should be added to inventory

#### Broadcast Alerts
1. Go to **"Alerts"** section
2. Click **"Create Alert"**
3. Fill in:
   - **Message:** Alert content
   - **Severity:** High/Medium/Low
   - **Target Role:** (Admin/Volunteer/Citizen or All)
4. Click **"Send Alert"**
5. ✅ Alert should be broadcasted
6. Check if Citizens/Volunteers receive notification

---

### **5. API Testing (Using Postman or cURL)**

#### Health Check
```bash
curl http://localhost:8000/api/health
```
✅ Expected Response:
```json
{
  "status": "ok",
  "message": "Disaster Management System is running"
}
```

#### Signup via API
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API Test User",
    "email": "apitest@example.com",
    "password": "TestPass123",
    "phone": "9999999999",
    "role": "CITIZEN"
  }'
```

#### Login via API
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@disaster.com",
    "password": "admin123"
  }'
```

#### Get Public Disasters
```bash
curl http://localhost:8000/api/public/disasters
```
✅ Expected: List of all disaster reports

#### Create Disaster Report (Requires Login)
```bash
curl -X POST http://localhost:8000/api/citizen/report \
  -H "Content-Type: application/json" \
  -b "cookies.txt" \
  -d '{
    "location": "Downtown Area",
    "severity": "HIGH",
    "description": "Major flood in downtown",
    "category": "FLOOD"
  }'
```

---

## 🔍 Testing Checklist

### Frontend Testing
- [ ] **Signup** - User registration works
- [ ] **Login** - User login with valid credentials works
- [ ] **Navigation** - All menu items are accessible
- [ ] **Responsive Design** - Works on mobile/tablet/desktop
- [ ] **Form Validation** - Invalid inputs are rejected
- [ ] **Error Messages** - Clear error feedback shown
- [ ] **Success Messages** - Confirmation messages display

### Citizen Testing
- [ ] Submit disaster report
- [ ] View my reports
- [ ] Track report status
- [ ] View active disasters
- [ ] Receive alerts
- [ ] Update profile

### Volunteer Testing
- [ ] View assigned tasks
- [ ] Update task status
- [ ] View workload/dashboard
- [ ] Mark tasks as completed

### Admin Testing
- [ ] View dashboard statistics
- [ ] View all reports
- [ ] Filter reports by status/severity
- [ ] Assign volunteers to reports
- [ ] Add/manage resources
- [ ] Create and send alerts
- [ ] View system statistics

### API Testing
- [ ] Health check endpoint
- [ ] Signup endpoint
- [ ] Login endpoint
- [ ] Public disasters API
- [ ] Citizen report creation
- [ ] Volunteer task updates
- [ ] Admin report management

---

## 🐛 Common Issues & Solutions

### Issue: "Module not found" error
**Solution:** Make sure you're running from the `/backend` directory

### Issue: 404 error on root path
**Solution:** Ensure `static_folder` is properly configured in app.py

### Issue: Port already in use
**Solution:** Kill the process: `Get-Process python | Stop-Process -Force`

### Issue: Database not initialized
**Solution:** Delete `database/disaster.db` and restart the app

### Issue: Can't access from other devices
**Solution:** Make sure your firewall allows port 8000

---

## 📊 Test Data

### Default Admin Account
- **Email:** admin@disaster.com
- **Password:** admin123

### Sample Test Accounts
Create these using signup:
1. **Citizen:** citizen1@test.com / Pass123
2. **Volunteer:** volunteer1@test.com / Pass123
3. **Admin:** admin2@test.com / Pass123

---

## ✅ Expected Results

All tests should pass with:
- ✅ No console errors
- ✅ Proper HTTP status codes (200, 201, 400, 401, etc.)
- ✅ Data persistence (changes saved to database)
- ✅ Real-time updates reflected
- ✅ Proper error handling and user feedback
- ✅ Responsive interface across all devices

---

## 🚀 Performance Testing

### Load Testing (Optional)
Use tools like Apache JMeter or Locust:
```bash
pip install locust
# Create locustfile.py with test scenarios
locust -f locustfile.py
```

### Response Time
- API endpoints should respond in < 200ms
- Frontend should load in < 3 seconds

---

## 📝 Test Report Template

Document your findings:
```
Test Date: [Date]
Tester: [Name]

PASSED TESTS:
- [ ] Test 1
- [ ] Test 2

FAILED TESTS:
- [ ] Test 3 - Description of issue

BUGS FOUND:
- [ ] Bug 1 - Steps to reproduce

NOTES:
- Additional observations
```

---

**Happy Testing! 🎉**
