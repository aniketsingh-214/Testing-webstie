// ==================== SERVER TIME ====================
async function getTime() {
    try {
        const response = await fetch('/time');
        const data = await response.json();
        document.getElementById('server-time').textContent = 'Server Time: ' + data.server_time;
    } catch (error) {
        document.getElementById('server-time').textContent = 'Error fetching time';
        console.error('Error:', error);
    }
}

// ==================== DEFACEMENT DASHBOARD ====================
async function loadBaselineStatus() {
    try {
        const response = await fetch('/api/defacement/baseline/status');
        const data = await response.json();

        const statusDiv = document.getElementById('baseline-status');
        const checkBtn = document.getElementById('check-defacement-btn');
        const resetBtn = document.getElementById('reset-baseline-btn');

        if (data.exists) {
            statusDiv.innerHTML = '<p><strong>✅ Baseline exists</strong></p>' +
                '<p>Created: ' + new Date(data.baseline.created_at).toLocaleString() + '</p>' +
                '<p>Zones: ' + data.baseline.zones_count + ' | Images: ' + data.baseline.images_count + '</p>';
            checkBtn.disabled = false;
            resetBtn.disabled = false;
        } else {
            statusDiv.innerHTML = '<p><strong>⚠️ No baseline found</strong></p>' +
                '<p>Create a baseline to start monitoring for defacement.</p>';
            checkBtn.disabled = true;
            resetBtn.disabled = true;
        }
    } catch (error) {
        console.error('Error loading baseline status:', error);
        document.getElementById('baseline-status').innerHTML = '<p class="alert-danger">Error loading status</p>';
    }
}

async function createBaseline() {
    const btn = document.getElementById('create-baseline-btn');
    btn.disabled = true;
    btn.textContent = '⏳ Creating...';

    try {
        const response = await fetch('/api/defacement/baseline/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: window.location.origin })
        });

        const data = await response.json();

        if (data.success) {
            alert('✅ Baseline created successfully!');
            loadBaselineStatus();
        } else {
            alert('❌ Failed to create baseline');
        }
    } catch (error) {
        console.error('Error creating baseline:', error);
        alert('❌ Error creating baseline: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = '📸 Create Baseline';
    }
}

async function checkDefacement() {
    const btn = document.getElementById('check-defacement-btn');
    btn.disabled = true;
    btn.textContent = '⏳ Checking...';

    try {
        const response = await fetch('/api/defacement/check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: window.location.origin })
        });

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error checking defacement:', error);
        alert('❌ Error checking defacement: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = '🔍 Check Now';
    }
}

function displayResults(data) {
    const resultsDiv = document.getElementById('detection-results');
    const contentDiv = document.getElementById('results-content');

    resultsDiv.style.display = 'block';

    if (data.defacement_detected) {
        let html = '<div class="alert-danger"><strong>🚨 DEFACEMENT DETECTED!</strong></div>';
        html += '<p><strong>Summary:</strong> ' + data.summary + '</p>';
        html += '<p><strong>Time:</strong> ' + new Date(data.timestamp).toLocaleString() + '</p>';

        if (data.changes && data.changes.length > 0) {
            html += '<h5>Changes Detected:</h5>';
            data.changes.forEach(function (change) {
                html += '<div class="change-item">';
                html += '<strong>' + change.type.toUpperCase() + ':</strong> ' + change.description;
                if (change.zone) html += '<br>Zone: ' + change.zone;
                if (change.image) html += '<br>Image: ' + change.image;
                html += '</div>';
            });
        }

        contentDiv.innerHTML = html;
    } else {
        contentDiv.innerHTML = '<div class="alert-success">' +
            '<strong>✅ No defacement detected</strong><br>' +
            'All protected zones and images match the baseline.<br>' +
            'Checked at: ' + new Date(data.timestamp).toLocaleString() +
            '</div>';
    }
}

async function resetBaseline() {
    if (!confirm('Are you sure you want to delete the baseline?')) {
        return;
    }

    try {
        const response = await fetch('/api/defacement/baseline/reset', {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            alert('✅ Baseline deleted');
            loadBaselineStatus();
            document.getElementById('detection-results').style.display = 'none';
        }
    } catch (error) {
        console.error('Error resetting baseline:', error);
        alert('❌ Error resetting baseline: ' + error.message);
    }
}

// Load baseline status on page load
if (document.getElementById('baseline-status')) {
    loadBaselineStatus();
}

// ==================== DEFACEMENT MONITORING ====================
function initDefacementMonitoring() {
    const protectedZones = ['header', 'sidebar', 'footer'];
    const protectedImages = [
        { id: 'logo', selector: '#header .logo', expectedSrc: '/static/images/logo1.png' },
        { id: 'sidebar-image', selector: '.sidebar-image', expectedSrc: '/static/images/image2.png' },
        { id: 'main-image', selector: '#main-image', expectedSrc: '/static/images/image1.png' },
        { id: 'footer-image', selector: '.footer-image', expectedSrc: '/static/images/image3.png' }
    ];

    // Store initial hashes for protected zones
    protectedZones.forEach(function (zoneId) {
        const zone = document.getElementById(zoneId);
        if (zone) {
            const content = zone.innerHTML;
            const hash = simpleHash(content);
            localStorage.setItem('zone_' + zoneId + '_hash', hash);
            console.log('[DEFACEMENT MONITOR] Protected zone "' + zoneId + '" hash stored: ' + hash);
        }
    });

    // Store initial image sources
    protectedImages.forEach(function (img) {
        const element = document.querySelector(img.selector);
        if (element) {
            localStorage.setItem('image_' + img.id + '_src', element.src);
            console.log('[DEFACEMENT MONITOR] Protected image "' + img.id + '" source stored: ' + element.src);
        }
    });

    // Periodic monitoring (every 5 seconds)
    setInterval(function () {
        checkDefacement(protectedZones, protectedImages);
    }, 5000);
}

function checkDefacement(zones, images) {
    let defacementDetected = false;

    // Check protected zones
    zones.forEach(function (zoneId) {
        const zone = document.getElementById(zoneId);
        if (zone) {
            const currentHash = simpleHash(zone.innerHTML);
            const storedHash = localStorage.getItem('zone_' + zoneId + '_hash');

            if (currentHash !== storedHash) {
                console.warn('[DEFACEMENT ALERT] Zone "' + zoneId + '" has been modified!');
                console.warn('Expected hash: ' + storedHash + ', Current hash: ' + currentHash);
                defacementDetected = true;
            }
        }
    });

    // Check protected images
    images.forEach(function (img) {
        const element = document.querySelector(img.selector);
        if (element) {
            const currentSrc = element.src;
            const storedSrc = localStorage.getItem('image_' + img.id + '_src');

            if (currentSrc !== storedSrc) {
                console.warn('[DEFACEMENT ALERT] Image "' + img.id + '" has been modified!');
                console.warn('Expected: ' + storedSrc + ', Current: ' + currentSrc);
                defacementDetected = true;
            }

            // Check if image exists and loads properly
            if (element.complete && element.naturalHeight === 0) {
                console.warn('[DEFACEMENT ALERT] Image "' + img.id + '" failed to load or is missing!');
                defacementDetected = true;
            }
        } else {
            console.warn('[DEFACEMENT ALERT] Protected image "' + img.id + '" is missing from DOM!');
            defacementDetected = true;
        }
    });

    if (defacementDetected) {
        console.error('[DEFACEMENT MONITOR] DEFACEMENT DETECTED - IMMEDIATE ACTION REQUIRED');
    }
}

function simpleHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return hash.toString(36);
}

// Initialize monitoring on page load
document.addEventListener('DOMContentLoaded', function () {
    initDefacementMonitoring();
    console.log('%c🏛️ Government Portal - Defacement Testing', 'font-size: 16px; font-weight: bold; color: #2c3e50;');
    console.log('%cDefacement monitoring active', 'font-size: 12px; color: #27ae60;');
});
