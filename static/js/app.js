/**
 * ResumeOS UI - Application JavaScript
 * =====================================
 * Following best practices:
 * - ES6 modules (or organized functions)
 * - State management
 * - Error handling
 * - Accessibility
 * - Performance optimization
 */

// Application State
const AppState = {
    isLoading: false,
    hasError: false,
    errorMessage: '',
    result: null,
    aiStatus: null,
    authToken: null,
    currentUser: null
};

// API Configuration
const API = {
    base: window.location.origin,

    authHeaders() {
        return AppState.authToken
            ? { Authorization: `Bearer ${AppState.authToken}` }
            : {};
    },
    
    async status() {
        const response = await fetch(`${this.base}/api/status`);
        if (!response.ok) throw new Error('Failed to fetch status');
        return response.json();
    },

    async register(email, password) {
        const response = await fetch(`${this.base}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || 'Failed to register');
        }
        return response.json();
    },

    async login(email, password) {
        const body = new URLSearchParams({ username: email, password });
        const response = await fetch(`${this.base}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || 'Failed to login');
        }
        return response.json();
    },

    async me() {
        const response = await fetch(`${this.base}/auth/me`, {
            headers: { ...this.authHeaders() }
        });
        if (!response.ok) throw new Error('Failed to fetch user');
        return response.json();
    },
    
    async tailor(data) {
        const response = await fetch(`${this.base}/resume/tailor`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', ...this.authHeaders() },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || 'Failed to compile resume');
        }
        
        return response.json();
    },
    
    async download(filename) {
        const response = await fetch(`${this.base}/resume/download/${filename}`);
        if (!response.ok) throw new Error('Failed to download file');
        return response.text();
    },

    async saveMasterResumeFromLatex(latexResume) {
        const response = await fetch(`${this.base}/master-resume/from-latex`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', ...this.authHeaders() },
            body: JSON.stringify({ latex_resume: latexResume })
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || 'Failed to save master resume');
        }
        return response.json();
    },

    async getLatestMasterResume() {
        const response = await fetch(`${this.base}/master-resume/latest`, {
            headers: { ...this.authHeaders() }
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || 'Failed to load latest master resume');
        }
        return response.json();
    }
};

// UI Components
const UI = {
    // Show loading state
    showLoading() {
        document.getElementById('loading').classList.add('loading--show');
        document.getElementById('compileBtn').disabled = true;
        AppState.isLoading = true;
    },
    
    // Hide loading state
    hideLoading() {
        document.getElementById('loading').classList.remove('loading--show');
        document.getElementById('compileBtn').disabled = false;
        AppState.isLoading = false;
    },
    
    // Show error
    showError(message) {
        const errorEl = document.getElementById('error');
        errorEl.textContent = `Error: ${message}`;
        errorEl.classList.add('error--show');
        AppState.hasError = true;
        AppState.errorMessage = message;
        
        // Auto-hide after 5 seconds
        setTimeout(() => this.hideError(), 5000);
    },
    
    // Hide error
    hideError() {
        document.getElementById('error').classList.remove('error--show');
        AppState.hasError = false;
        AppState.errorMessage = '';
    },
    
    // Show results
    showResults() {
        document.getElementById('results').classList.add('results--show');
        this.hideError();
    },
    
    // Hide results
    hideResults() {
        document.getElementById('results').classList.remove('results--show');
    },
    
    // Update AI status indicator
    updateAIStatus(status) {
        const indicator = document.getElementById('aiIndicator');
        if (!indicator) return;
        
        AppState.aiStatus = status;
        
        if (status.ai_enabled) {
            indicator.textContent = '🤖 AI: Enabled';
            indicator.style.color = 'var(--color-success)';
        } else {
            indicator.textContent = '🤖 AI: Disabled (Rule-based)';
            indicator.style.color = 'var(--color-warning)';
        }
    }
};

// Form Handler
const FormHandler = {
    // Get form data
    getFormData() {
        return {
            latexResume: document.getElementById('latexResume').value.trim(),
            jobDescription: document.getElementById('jobDescription').value.trim(),
            roleOverride: document.getElementById('roleOverride').value || null,
            enableAI: document.getElementById('enableAI').checked,
            useStored: document.getElementById('useStored').checked
        };
    },
    
    // Validate form
    validate(data) {
        if (data.useStored && !AppState.authToken) {
            throw new Error('Please log in to use a stored master resume');
        }
        if (!data.useStored && !data.latexResume) {
            throw new Error('Please provide a LaTeX resume or use a stored master resume');
        }
        if (!data.jobDescription) {
            throw new Error('Please provide a job description');
        }
        return true;
    },
    
    // Clear form
    clear() {
        document.getElementById('latexResume').value = '';
        document.getElementById('jobDescription').value = '';
        document.getElementById('roleOverride').value = '';
        document.getElementById('enableAI').checked = true;
        UI.hideResults();
        UI.hideError();
    }
};

// Results Display
const ResultsDisplay = {
    // Display compilation results
    display(result) {
        this.updateMatchScore(result.match_score);
        this.updateTargetRole(result.target_role);
        this.updateKeywords(result.tailored_resume);
        this.updateSkills(result.gap_analysis);
        this.updateRecommendations(result.gap_analysis);
        this.updateLatexOutput(result);
        UI.showResults();
    },
    
    // Update match score
    updateMatchScore(score) {
        const scorePercent = Math.round(score * 100);
        const circle = document.getElementById('scoreCircle');
        circle.textContent = `${scorePercent}%`;
        
        // Update color based on score
        circle.className = 'score-circle';
        if (scorePercent >= 70) {
            circle.classList.add('score-circle--high');
        } else if (scorePercent >= 50) {
            circle.classList.add('score-circle--medium');
        } else {
            circle.classList.add('score-circle--low');
        }
    },
    
    // Update target role
    updateTargetRole(role) {
        document.getElementById('targetRole').textContent = 
            role.replace('_', ' ').toUpperCase();
    },
    
    // Update keywords matched
    updateKeywords(tailoredResume) {
        const count = tailoredResume.metadata?.total_keywords_matched || 0;
        document.getElementById('keywordsMatched').textContent = count;
    },
    
    // Update skills lists
    updateSkills(gapAnalysis) {
        // Matched skills
        const matchedList = document.getElementById('matchedSkills');
        matchedList.innerHTML = '';
        const matched = gapAnalysis.matched_skills || [];
        
        if (matched.length === 0) {
            matchedList.innerHTML = '<li class="info-card__item--empty">None</li>';
        } else {
            matched.slice(0, 10).forEach(skill => {
                const li = document.createElement('li');
                li.className = 'info-card__item';
                li.textContent = skill;
                matchedList.appendChild(li);
            });
        }
        
        // Missing skills
        const missingList = document.getElementById('missingSkills');
        missingList.innerHTML = '';
        const missing = gapAnalysis.missing_required_skills || [];
        
        if (missing.length === 0) {
            missingList.innerHTML = '<li class="info-card__item" style="color: var(--color-success);">None - All required skills present!</li>';
        } else {
            missing.forEach(skill => {
                const li = document.createElement('li');
                li.className = 'info-card__item info-card__item--missing';
                li.textContent = skill;
                missingList.appendChild(li);
            });
        }
    },
    
    // Update recommendations
    updateRecommendations(gapAnalysis) {
        const list = document.getElementById('recommendations');
        list.innerHTML = '';
        const recommendations = gapAnalysis.recommendations || [];
        
        if (recommendations.length === 0) {
            list.innerHTML = '<li class="info-card__item--empty">No recommendations</li>';
        } else {
            recommendations.forEach(rec => {
                const li = document.createElement('li');
                li.className = 'info-card__item';
                li.textContent = rec;
                list.appendChild(li);
            });
        }
    },
    
    // Update LaTeX output
    async updateLatexOutput(result) {
        const output = document.getElementById('latexOutput');
        const downloadLink = document.getElementById('downloadLink');
        
        if (result.latex_content) {
            output.value = result.latex_content;
            this.updateLatexStats(result.latex_content);
        } else if (result.latex_file) {
            // Fallback: fetch from download endpoint
            try {
                const content = await API.download(result.latex_file);
                output.value = content;
                this.updateLatexStats(content);
            } catch (error) {
                output.value = 'Error loading LaTeX content. Use download link.';
                console.error('Failed to fetch LaTeX:', error);
            }
        }
        
        if (result.latex_file) {
            downloadLink.href = `${API.base}/resume/download/${result.latex_file}`;
            downloadLink.style.display = 'inline-block';
        }
    },
    
    // Update LaTeX statistics
    updateLatexStats(content) {
        const lines = content.split('\n').length;
        const words = content.split(/\s+/).filter(w => w.length > 0).length;
        const experiences = (content.match(/\\textbf\{[^}]+\}.*?\\hfill/g) || []).length;
        const projects = (content.match(/\\section\*\{Projects\}.*?\\textbf\{/gs) || []).length;
        
        document.getElementById('latexStats').textContent = 
            `${lines} lines • ${words} words • ${experiences} experiences • ${projects} projects`;
    }
};

// Utility Functions
const Utils = {
    // Copy text to clipboard
    async copyToClipboard(text) {
        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                await navigator.clipboard.writeText(text);
                return true;
            } else {
                // Fallback for older browsers
                const textarea = document.createElement('textarea');
                textarea.value = text;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                return true;
            }
        } catch (error) {
            console.error('Failed to copy:', error);
            return false;
        }
    },
    
    // Show toast notification
    showToast(message, type = 'success') {
        // Simple toast implementation
        const toast = document.createElement('div');
        toast.className = `toast toast--${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 12px 24px;
            background: ${type === 'success' ? 'var(--color-success)' : 'var(--color-error)'};
            color: white;
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-lg);
            z-index: var(--z-toast);
            animation: slideIn 0.3s ease;
        `;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
};

// Example Data Loader
const ExampleLoader = {
    async loadLatex() {
        try {
            const response = await fetch('/static/example_resume.tex');
            const latex = await response.text();
            document.getElementById('latexResume').value = latex;
        } catch (error) {
            // Fallback sample
            const sample = `\\documentclass[11pt,a4paper]{article}
\\usepackage[margin=0.75in]{geometry}
\\usepackage{enumitem}

\\begin{document}
\\begin{center}
    {\\LARGE\\textbf{Your Name}}\\\\[4pt]
    Software Engineer\\[4pt]
    email@example.com $|$ +1-234-567-8900 $|$ City, Country
\\end{center}

\\section*{Technical Skills}
Python, JavaScript, React, FastAPI, PostgreSQL, Docker, AWS

\\section*{Professional Experience}
\\noindent\\textbf{Company Name} \\hfill Jan 2023 - Present\\\\
\\textit{Software Engineer}
\\begin{itemize}
    \\item Built scalable microservices using FastAPI
    \\item Implemented REST APIs handling 1M+ requests per day
\\end{itemize}

\\section*{Projects}
\\noindent\\textbf{Project Name} $|$ \\textit{Python, FastAPI}
\\begin{itemize}
    \\item Developed feature X achieving Y result
\\end{itemize}

\\end{document}`;
            document.getElementById('latexResume').value = sample;
        }
    },
    
    loadJD(type) {
        const jds = {
            ai: `AI/ML Engineer - Computer Vision Team

We're looking for an AI Engineer to join our computer vision team building next-generation video analytics systems.

Required Qualifications:
- Strong experience with Python and machine learning frameworks (TensorFlow, PyTorch)
- Proven track record in computer vision and deep learning
- Experience with object detection models (YOLO, R-CNN family)
- Proficiency in OpenCV for image/video processing
- Understanding of model deployment and serving at scale
- Experience with REST APIs and microservices

Preferred Qualifications:
- Experience with real-time video processing
- Knowledge of MLOps and model monitoring
- Familiarity with cloud platforms (AWS, GCP)
- Experience with FastAPI or similar frameworks
- Background in distributed systems`,
            
            backend: `Senior Backend Engineer - Platform Team

Join our platform team to build highly scalable distributed systems powering millions of users.

Required Skills:
- 3+ years experience building backend services
- Strong proficiency in Python, Java, or Go
- Deep understanding of distributed systems and microservices architecture
- Experience with relational databases (PostgreSQL) and caching (Redis)
- Proficiency in REST API design and implementation
- Experience with containerization (Docker) and orchestration (Kubernetes)

Preferred Skills:
- Experience with message queues and event-driven architecture
- Knowledge of FastAPI, Django, or similar frameworks
- Understanding of system design and scalability patterns
- Familiarity with AWS cloud services
- Experience with CI/CD pipelines`,
            
            devops: `DevOps Engineer - Infrastructure Team

We're seeking a DevOps Engineer to build and maintain our cloud infrastructure and deployment pipelines.

Required Qualifications:
- Strong experience with AWS (EC2, EKS, S3, RDS)
- Proficiency with Infrastructure as Code (Terraform preferred)
- Deep knowledge of Kubernetes and container orchestration
- Experience building CI/CD pipelines (Jenkins, GitHub Actions)
- Strong scripting skills (Python, Bash)
- Understanding of monitoring and observability (Prometheus, Grafana)

Preferred Qualifications:
- Experience with configuration management (Ansible, Chef)
- Knowledge of service mesh technologies
- Familiarity with security best practices
- Experience with disaster recovery and backup strategies
- Background in system administration`
        };
        
        document.getElementById('jobDescription').value = jds[type] || '';
    }
};

// Main Application
const App = {
    // Initialize application
    async init() {
        this.setupEventListeners();
        await this.checkAIStatus();
        await this.restoreSession();
    },
    
    // Setup event listeners
    setupEventListeners() {
        // Form submission
        document.getElementById('resumeForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });
        
        // Clear button
        const clearBtn = document.querySelector('button[onclick="clearForm()"]');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => FormHandler.clear());
        }
        
        // Copy LaTeX button
        const copyBtn = document.querySelector('button[onclick="copyLatex()"]');
        if (copyBtn) {
            copyBtn.addEventListener('click', () => this.copyLatex());
        }

        const loginBtn = document.getElementById('loginBtn');
        const registerBtn = document.getElementById('registerBtn');
        const logoutBtn = document.getElementById('logoutBtn');
        const saveMasterBtn = document.getElementById('saveMasterBtn');
        const useStored = document.getElementById('useStored');

        if (loginBtn) loginBtn.addEventListener('click', () => this.login());
        if (registerBtn) registerBtn.addEventListener('click', () => this.register());
        if (logoutBtn) logoutBtn.addEventListener('click', () => this.logout());
        if (saveMasterBtn) saveMasterBtn.addEventListener('click', () => this.saveMasterResume());
        if (useStored) {
            useStored.addEventListener('change', () => this.toggleStoredMode(useStored.checked));
        }
    },
    
    // Check AI status
    async checkAIStatus() {
        try {
            const status = await API.status();
            UI.updateAIStatus(status);
        } catch (error) {
            console.error('Failed to check AI status:', error);
            UI.updateAIStatus({ ai_enabled: false });
        }
    },
    
    // Handle form submission
    async handleSubmit() {
        try {
            // Get and validate form data
            const data = FormHandler.getFormData();
            FormHandler.validate(data);
            
            // Show loading
            UI.showLoading();
            UI.hideError();
            UI.hideResults();
            
            // Submit to API
            let payload = {
                job_description: data.jobDescription,
                role_override: data.roleOverride,
                enable_ai: data.enableAI
            };

            if (data.useStored) {
                const latest = await API.getLatestMasterResume();
                payload.master_resume_id = latest.id;
            } else {
                payload.latex_resume = data.latexResume;
            }

            const result = await API.tailor(payload);
            
            // Display results
            ResultsDisplay.display(result);
            AppState.result = result;
            
        } catch (error) {
            UI.showError(error.message);
            console.error('Compilation error:', error);
        } finally {
            UI.hideLoading();
        }
    },
    
    // Copy LaTeX to clipboard
    async copyLatex() {
        const output = document.getElementById('latexOutput');
        const success = await Utils.copyToClipboard(output.value);
        
        if (success) {
            Utils.showToast('LaTeX copied to clipboard!', 'success');
            const btn = event.target;
            const original = btn.textContent;
            btn.textContent = '✓ Copied!';
            btn.classList.add('btn--success');
            setTimeout(() => {
                btn.textContent = original;
                btn.classList.remove('btn--success');
            }, 2000);
        } else {
            Utils.showToast('Failed to copy. Please select and copy manually.', 'error');
        }
    }
};

// Auth helpers
App.updateAuthUI = function () {
    const statusEl = document.getElementById('authStatus');
    const logoutBtn = document.getElementById('logoutBtn');
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');

    if (AppState.currentUser) {
        statusEl.textContent = `Logged in as ${AppState.currentUser.email}`;
        logoutBtn.style.display = 'inline-block';
        loginBtn.style.display = 'none';
        registerBtn.style.display = 'none';
    } else {
        statusEl.textContent = 'Not logged in';
        logoutBtn.style.display = 'none';
        loginBtn.style.display = 'inline-block';
        registerBtn.style.display = 'inline-block';
    }
};

App.restoreSession = async function () {
    const token = localStorage.getItem('resumeos_token');
    if (!token) {
        this.updateAuthUI();
        return;
    }
    AppState.authToken = token;
    try {
        const user = await API.me();
        AppState.currentUser = user;
    } catch (error) {
        AppState.authToken = null;
        AppState.currentUser = null;
        localStorage.removeItem('resumeos_token');
    }
    this.updateAuthUI();
};

App.login = async function () {
    try {
        const email = document.getElementById('authEmail').value.trim();
        const password = document.getElementById('authPassword').value;
        if (!email || !password) throw new Error('Email and password required');
        const token = await API.login(email, password);
        AppState.authToken = token.access_token;
        localStorage.setItem('resumeos_token', token.access_token);
        AppState.currentUser = await API.me();
        this.updateAuthUI();
        Utils.showToast('Logged in successfully', 'success');
    } catch (error) {
        Utils.showToast(error.message, 'error');
    }
};

App.register = async function () {
    try {
        const email = document.getElementById('authEmail').value.trim();
        const password = document.getElementById('authPassword').value;
        if (!email || !password) throw new Error('Email and password required');
        await API.register(email, password);
        await this.login();
    } catch (error) {
        Utils.showToast(error.message, 'error');
    }
};

App.logout = function () {
    AppState.authToken = null;
    AppState.currentUser = null;
    localStorage.removeItem('resumeos_token');
    this.updateAuthUI();
    Utils.showToast('Logged out', 'success');
};

App.saveMasterResume = async function () {
    try {
        if (!AppState.authToken) throw new Error('Please log in first');
        const latex = document.getElementById('latexResume').value.trim();
        if (!latex) throw new Error('Please provide a LaTeX resume to save');
        await API.saveMasterResumeFromLatex(latex);
        Utils.showToast('Master resume saved', 'success');
    } catch (error) {
        Utils.showToast(error.message, 'error');
    }
};

App.toggleStoredMode = function (enabled) {
    const latexEl = document.getElementById('latexResume');
    latexEl.disabled = enabled;
    if (enabled) {
        latexEl.placeholder = 'Using latest stored master resume';
    } else {
        latexEl.placeholder = '\\documentclass{article}...';
    }
};

// Global functions for onclick handlers (backward compatibility)
window.loadExampleLatex = () => ExampleLoader.loadLatex();
window.loadExampleJD = (type) => ExampleLoader.loadJD(type);
window.clearForm = () => FormHandler.clear();
window.copyLatex = () => App.copyLatex();

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => App.init());
} else {
    App.init();
}
