/**
 * Disaster Management System Frontend
 */

// API Base URL - Dynamic based on current host
const API_BASE = `${window.location.protocol}//${window.location.host}/api`;

// Global state
let currentUser = null;
let currentSection = 'home';

/**
 * Initialize app on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    checkAuth();
    loadInitialData();
});

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Login form
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    
    // Signup form
    document.getElementById('signupForm').addEventListener('submit', handleSignup);
    
    // Report form
    document.getElementById('reportForm').addEventListener('submit', handleReportSubmit);
}

/**
 * Check authentication status
 */
async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE}/auth/me`, {
            credentials: 'include'
        });
        
        if (response.ok) {
            currentUser = await response.json();
            updateUIForLoggedInUser();
        } else {
            updateUIForLoggedOutUser();
        }
    } catch (error) {
        console.log('Not authenticated');
        updateUIForLoggedOutUser();
    }
}

/**
 * Update UI for logged in user
 */
function updateUIForLoggedInUser() {
    const authLink = document.getElementById('authLink');
    authLink.textContent = currentUser.name;
    authLink.onclick = handleLogout;
    
    const navMenu = document.getElementById('navMenu');
    navMenu.innerHTML = `
        <a href="#" class="nav-link" onclick="navigateTo('home')">Home</a>
        <a href="#" class="nav-link" onclick="navigateTo('alerts')">Alerts</a>
        <a href="#" class="nav-link" onclick="navigateTo('disasters')">Active Disasters</a>
        <a href="#" class="nav-link" onclick="navigateTo('dashboard')">Dashboard</a>
        <div class="nav-divider"></div>
        <span class="nav-user">
            <i class="fas fa-user-circle"></i>
            ${currentUser.name}
            <span class="role-badge">${currentUser.role}</span>
        </span>
        <a href="#" class="nav-link nav-auth" onclick="handleLogout(event)">Logout</a>
    `;
}

/**
 * Update UI for logged out user
 */
function updateUIForLoggedOutUser() {
    const authLink = document.getElementById('authLink');
    if (authLink) {
        authLink.textContent = 'Sign In';
        authLink.onclick = () => showModal('authModal');
    }
}

/**
 * Load initial data
 */
async function loadInitialData() {
    await loadStatistics();
    await loadAlerts();
}

/**
 * Load statistics
 */
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE}/public/statistics`);
        const data = await response.json();
        
        document.getElementById('statActive').textContent = data.disaster_stats.active_reports;
        document.getElementById('statResolved').textContent = data.disaster_stats.resolved_reports;
        document.getElementById('statResources').textContent = data.resource_stats.available;
        document.getElementById('statVolunteers').textContent = '--';
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

/**
 * Load disasters
 */
async function loadDisasters() {
    try {
        const response = await fetch(`${API_BASE}/public/disasters`);
        const data = await response.json();
        
        const list = document.getElementById('disastersList');
        
        if (data.disasters.length === 0) {
            list.innerHTML = '<p class="empty-state">No active disasters reported</p>';
            return;
        }
        
        list.innerHTML = data.disasters.map(disaster => `
            <div class="disaster-card">
                <div class="card-header">
                    <h3>${disaster.title}</h3>
                    <span class="severity-badge severity-${disaster.severity.toLowerCase()}">${disaster.severity.toUpperCase()}</span>
                </div>
                <div class="card-body">
                    <p><strong>Location:</strong> ${disaster.location}</p>
                    <p><strong>Description:</strong> ${disaster.description.substring(0, 100)}...</p>
                    <p><strong>Status:</strong> ${disaster.status.toUpperCase()}</p>
                    <p><strong>Reported:</strong> ${new Date(disaster.created_at).toLocaleString()}</p>
                </div>
                <div class="card-footer">
                    <button class="btn btn-small" onclick="viewDisasterDetail(${disaster.id})">View Details</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading disasters:', error);
        showToast('Error loading disasters', 'error');
    }
}

/**
 * Load alerts
 */
async function loadAlerts() {
    try {
        const response = await fetch(`${API_BASE}/public/alerts`);
        const data = await response.json();
        
        const list = document.getElementById('alertsList');
        
        if (data.alerts.length === 0) {
            list.innerHTML = '<p class="empty-state">No alerts at the moment</p>';
            return;
        }
        
        list.innerHTML = data.alerts.map(alert => `
            <div class="alert-card alert-${alert.alert_level.toLowerCase()}">
                <div class="alert-icon">
                    <i class="fas fa-${alert.alert_level === 'critical' ? 'exclamation-circle' : 'info-circle'}"></i>
                </div>
                <div class="alert-content">
                    <h4>${alert.title}</h4>
                    <p>${alert.message}</p>
                    <small>${new Date(alert.created_at).toLocaleString()}</small>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading alerts:', error);
    }
}

/**
 * Handle login
 */
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            currentUser = data.user;
            closeModal('authModal');
            updateUIForLoggedInUser();
            showToast('Login successful', 'success');
            navigateTo('dashboard');
        } else {
            const error = await response.json();
            showToast(error.error || 'Login failed', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showToast('Login error', 'error');
    }
}

/**
 * Handle signup
 */
async function handleSignup(e) {
    e.preventDefault();
    
    const name = document.getElementById('signupName').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const phone = document.getElementById('signupPhone').value;
    const role = document.getElementById('signupRole').value;
    
    try {
        const response = await fetch(`${API_BASE}/auth/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ name, email, password, phone, role })
        });
        
        if (response.ok) {
            showToast('Signup successful! Please login', 'success');
            switchTab('login');
            document.getElementById('signupForm').reset();
        } else {
            const error = await response.json();
            showToast(error.error || 'Signup failed', 'error');
        }
    } catch (error) {
        console.error('Signup error:', error);
        showToast('Signup error: ' + error.message, 'error');
    }
}

/**
 * Handle logout
 */
async function handleLogout(e) {
    e.preventDefault();
    
    try {
        await fetch(`${API_BASE}/auth/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        
        currentUser = null;
        updateUIForLoggedOutUser();
        navigateTo('home');
        showToast('Logged out', 'info');
    } catch (error) {
        console.error('Logout error:', error);
    }
}

/**
 * Handle report submission
 */
async function handleReportSubmit(e) {
    e.preventDefault();
    
    if (!currentUser) {
        showToast('Please login to submit a report', 'error');
        showModal('authModal');
        return;
    }
    
    const title = document.getElementById('reportTitle').value;
    const description = document.getElementById('reportDescription').value;
    const location = document.getElementById('reportLocation').value;
    const latitude = document.getElementById('reportLat').value;
    const longitude = document.getElementById('reportLng').value;
    const severity = document.getElementById('reportSeverity').value;
    
    try {
        const response = await fetch(`${API_BASE}/citizen/reports`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                title,
                description,
                location,
                latitude: latitude ? parseFloat(latitude) : null,
                longitude: longitude ? parseFloat(longitude) : null,
                severity
            })
        });
        
        if (response.ok) {
            showToast('Report submitted successfully', 'success');
            closeModal('reportModal');
            document.getElementById('reportForm').reset();
            loadDisasters();
        } else {
            const error = await response.json();
            showToast(error.error || 'Failed to submit report', 'error');
        }
    } catch (error) {
        console.error('Report submission error:', error);
        showToast('Error submitting report', 'error');
    }
}

/**
 * Navigate to section
 */
function navigateTo(section) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    
    // Show selected section
    const elem = document.getElementById(section);
    if (elem) {
        elem.classList.add('active');
        currentSection = section;
        
        // Load data for section
        if (section === 'disasters') {
            loadDisasters();
        } else if (section === 'alerts') {
            loadAlerts();
        } else if (section === 'dashboard') {
            loadDashboard();
        }
    }
}

/**
 * Load user dashboard
 */
async function loadDashboard() {
    if (!currentUser) {
        navigateTo('home');
        return;
    }
    
    const dashboardContent = document.getElementById('dashboardContent');
    
    try {
        if (currentUser.role === 'admin') {
            await loadAdminDashboard();
        } else {
            let endpoint;
            if (currentUser.role === 'volunteer') {
                endpoint = `${API_BASE}/volunteer/dashboard`;
            } else {
                endpoint = `${API_BASE}/citizen/dashboard`;
            }
            
            const response = await fetch(endpoint, {
                credentials: 'include'
            });
            
            if (response.ok) {
                const data = await response.json();
                dashboardContent.innerHTML = `
                    <div class="dashboard-welcome">
                        <h2>Welcome, ${currentUser.name}</h2>
                        <p>Role: ${currentUser.role.toUpperCase()}</p>
                    </div>
                    <div class="dashboard-stats">
                        ${Object.entries(data).map(([key, value]) => `
                            <div class="stat">
                                <strong>${key}</strong>: ${value}
                            </div>
                        `).join('')}
                    </div>
                `;
            }
        }
    } catch (error) {
        console.error('Dashboard error:', error);
        dashboardContent.innerHTML = '<p>Error loading dashboard</p>';
    }
}

/**
 * Load admin dashboard with reports and actions
 */
async function loadAdminDashboard() {
    const dashboardContent = document.getElementById('dashboardContent');
    
    try {
        const dashResponse = await fetch(`${API_BASE}/admin/dashboard`, {
            credentials: 'include'
        });
        
        const allReportsResponse = await fetch(`${API_BASE}/admin/reports?per_page=100`, {
            credentials: 'include'
        });
        
        const volunteersResponse = await fetch(`${API_BASE}/admin/volunteers`, {
            credentials: 'include'
        });
        
        if (dashResponse.ok && allReportsResponse.ok && volunteersResponse.ok) {
            const dashData = await dashResponse.json();
            const allReportsData = await allReportsResponse.json();
            const volunteersData = await volunteersResponse.json();
            
            const statuses = ['pending', 'acknowledged', 'in_progress', 'resolved', 'cancelled'];
            const statusLabels = {
                'pending': 'PENDING',
                'acknowledged': 'ACKNOWLEDGED',
                'in_progress': 'IN_PROGRESS',
                'resolved': 'RESOLVED',
                'cancelled': 'CANCELLED'
            };
            const reportsByStatus = {};
            
            statuses.forEach(status => {
                reportsByStatus[status] = allReportsData.reports.filter(r => r.status === status);
            });
            
            const reportsHTML = statuses.map(status => `
                <div class="admin-section">
                    <h3>${statusLabels[status]} Reports (${reportsByStatus[status].length})</h3>
                    <div class="reports-container">
                        ${reportsByStatus[status].length === 0 ? 
                            '<p class="empty-state">No reports with this status</p>' :
                            reportsByStatus[status].map(report => `
                                <div class="report-card">
                                    <div class="card-header">
                                        <h4>${report.title}</h4>
                                        <span class="severity-badge severity-${report.severity.toLowerCase()}">${report.severity}</span>
                                    </div>
                                    <div class="card-body">
                                        <p><strong>Location:</strong> ${report.location}</p>
                                        <p><strong>Description:</strong> ${report.description.substring(0, 100)}...</p>
                                        <p><strong>Status:</strong> <span class="status-badge">${report.status}</span></p>
                                        <p><strong>Reported by:</strong> ${report.reporter.name} (${report.reporter.phone})</p>
                                        <p><strong>Created:</strong> ${new Date(report.created_at).toLocaleString()}</p>
                                        ${report.volunteer_tasks && report.volunteer_tasks.length > 0 ? 
                                            `<p><strong>Assigned Tasks:</strong> ${report.volunteer_tasks.length}</p>` : 
                                            '<p><strong>No volunteers assigned</strong></p>'
                                        }
                                    </div>
                                    <div class="card-actions">
                                        <select class="form-control" onchange="changeReportStatus(${report.id}, this.value)">
                                            <option value="">Change Status...</option>
                                            <option value="acknowledged">Acknowledge</option>
                                            <option value="in_progress">In Progress</option>
                                            <option value="resolved">Resolved</option>
                                            <option value="cancelled">Cancel</option>
                                        </select>
                                        <button class="btn btn-small" onclick="openAssignVolunteerModal(${report.id}, '${report.title}')">
                                            Assign Volunteer
                                        </button>
                                        <button class="btn btn-small btn-secondary" onclick="viewReportDetails(${report.id})">
                                            View Details
                                        </button>
                                    </div>
                                </div>
                            `).join('')
                        }
                    </div>
                </div>
            `).join('');
            
            dashboardContent.innerHTML = `
                <div class="admin-dashboard">
                    <div class="dashboard-welcome">
                        <h2>Admin Dashboard</h2>
                        <p>Welcome, ${currentUser.name}</p>
                        <button class="btn btn-small" onclick="exportDisasterLog()">
                            <i class="fas fa-download"></i> Export All Disasters
                        </button>
                    </div>
                    
                    <div class="dashboard-stats">
                        <div class="stat-card">
                            <h3>${dashData.total_reports}</h3>
                            <p>Total Reports</p>
                        </div>
                        <div class="stat-card">
                            <h3>${dashData.pending_reports}</h3>
                            <p>Pending Reports</p>
                        </div>
                        <div class="stat-card">
                            <h3>${dashData.active_volunteers}</h3>
                            <p>Active Volunteers</p>
                        </div>
                        <div class="stat-card">
                            <h3>${dashData.total_resources}</h3>
                            <p>Resources Available</p>
                        </div>
                    </div>
                    
                    <div class="reports-list">
                        ${reportsHTML}
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Admin dashboard error:', error);
        dashboardContent.innerHTML = '<p>Error loading admin dashboard</p>';
    }
}

/**
 * Change report status
 */
async function changeReportStatus(reportId, newStatus) {
    if (!newStatus) return;
    
    try {
        const response = await fetch(`${API_BASE}/admin/reports/${reportId}/status`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ status: newStatus })
        });
        
        if (response.ok) {
            showToast(`Report status updated to ${newStatus}`, 'success');
            loadAdminDashboard();
        } else {
            const error = await response.json();
            showToast(error.error || 'Failed to update status', 'error');
        }
    } catch (error) {
        console.error('Error updating report status:', error);
        showToast('Error updating status', 'error');
    }
}

/**
 * Open modal to assign volunteer
 */
async function openAssignVolunteerModal(reportId, reportTitle) {
    try {
        const response = await fetch(`${API_BASE}/admin/volunteers`, {
            credentials: 'include'
        });
        
        if (response.ok) {
            const data = await response.json();
            const modal = document.getElementById('assignVolunteerModal');
            
            if (!modal) {
                const newModal = document.createElement('div');
                newModal.id = 'assignVolunteerModal';
                newModal.className = 'modal';
                newModal.innerHTML = `
                    <div class="modal-content">
                        <div class="modal-header">
                            <h2>Assign Volunteer to Report</h2>
                            <button class="modal-close" onclick="closeModal('assignVolunteerModal')">&times;</button>
                        </div>
                        <div class="modal-body">
                            <p><strong>Report:</strong> ${reportTitle}</p>
                            <form onsubmit="submitAssignVolunteer(event, ${reportId})">
                                <div class="form-group">
                                    <label>Select Volunteer:</label>
                                    <select id="volunteerSelect" class="form-control" required>
                                        <option value="">-- Select a Volunteer --</option>
                                        ${data.volunteers.map(v => `<option value="${v.id}">${v.name} (${v.email})</option>`).join('')}
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label>Task Description:</label>
                                    <textarea id="taskDescription" class="form-control" rows="4" placeholder="Describe the task for the volunteer" required></textarea>
                                </div>
                                <div class="form-group">
                                    <button type="submit" class="btn btn-primary">Assign</button>
                                    <button type="button" class="btn btn-secondary" onclick="closeModal('assignVolunteerModal')">Cancel</button>
                                </div>
                            </form>
                        </div>
                    </div>
                `;
                document.body.appendChild(newModal);
            }
            
            showModal('assignVolunteerModal');
        }
    } catch (error) {
        console.error('Error loading volunteers:', error);
        showToast('Error loading volunteers', 'error');
    }
}

/**
 * Submit assign volunteer form
 */
async function submitAssignVolunteer(e, reportId) {
    e.preventDefault();
    
    const volunteerId = document.getElementById('volunteerSelect').value;
    const taskDescription = document.getElementById('taskDescription').value;
    
    try {
        const response = await fetch(`${API_BASE}/admin/reports/${reportId}/assign`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                volunteer_id: parseInt(volunteerId),
                task_description: taskDescription
            })
        });
        
        if (response.ok) {
            showToast('Volunteer assigned successfully', 'success');
            closeModal('assignVolunteerModal');
            loadAdminDashboard();
        } else {
            const error = await response.json();
            showToast(error.error || 'Failed to assign volunteer', 'error');
        }
    } catch (error) {
        console.error('Error assigning volunteer:', error);
        showToast('Error assigning volunteer', 'error');
    }
}

/**
 * View disaster detail
 */
function viewDisasterDetail(id) {
    console.log('View disaster:', id);
}

/**
 * View report details for admin
 */
async function viewReportDetails(reportId) {
    try {
        const response = await fetch(`${API_BASE}/admin/reports/${reportId}`, {
            credentials: 'include'
        });
        
        if (response.ok) {
            const report = await response.json();
            showToast(`Report: ${report.title}`, 'info');
        }
    } catch (error) {
        console.error('Error loading report details:', error);
        showToast('Error loading report details', 'error');
    }
}

/**
 * Export all disaster reports as CSV
 */
async function exportDisasterLog() {
    try {
        const response = await fetch(`${API_BASE}/admin/reports/export`, {
            credentials: 'include'
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `disaster_reports_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            showToast('Disasters log exported successfully', 'success');
        } else {
            showToast('Failed to export disaster log', 'error');
        }
    } catch (error) {
        console.error('Error exporting disaster log:', error);
        showToast('Error exporting disaster log', 'error');
    }
}

/**
 * Modal functions
 */
function showModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

/**
 * Tab switching
 */
function switchTab(tab, e) {
    document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    
    document.getElementById(tab + 'Form').classList.add('active');
    if (e && e.target) {
        e.target.classList.add('active');
    }
}

/**
 * Toast notifications
 */
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast active ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('active');
    }, 3000);
}

/**
 * Close modals on outside click
 */
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
});
