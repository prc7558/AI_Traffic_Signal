// DOM Elements
const elements = {
    vehicleCount: document.getElementById('vehicle-count'),
    density: document.getElementById('density'),
    densityStatus: document.getElementById('density-status'),
    lightRed: document.getElementById('light-red'),
    lightYellow: document.getElementById('light-yellow'),
    lightGreen: document.getElementById('light-green'),
    countSparkline: document.querySelector('.sparkline-count path'),
    densitySparkline: document.querySelector('.sparkline-density path'),
    timerGauge: document.getElementById('timer-gauge-progress'),
    timerText: document.getElementById('timer-text'),
    phaseProgress: document.getElementById('phase-progress'),
    runtime: document.getElementById('runtime'),
    totalVehicles: document.getElementById('total-vehicles'),
    avgDensity: document.getElementById('avg-density'),
    cycleCount: document.getElementById('cycle-count'),
    carCount: document.getElementById('car-count'),
    busCount: document.getElementById('bus-count'),
    truckCount: document.getElementById('truck-count'),
    bikeCount: document.getElementById('bike-count')
};

// Timer gauge setup
const gaugeRadius = elements.timerGauge.r.baseVal.value;
const gaugeCircumference = 2 * Math.PI * gaugeRadius;
elements.timerGauge.style.strokeDasharray = `${gaugeCircumference} ${gaugeCircumference}`;
elements.timerGauge.style.strokeDashoffset = gaugeCircumference;

// History for sparklines
const historySize = 20;
let countHistory = new Array(historySize).fill(0);
let densityHistory = new Array(historySize).fill(1);

// Signal timing constants
const SIGNAL_PHASES = {
    RED: { duration: 2, next: 'GREEN' },
    GREEN: { duration: 10, next: 'YELLOW' },
    YELLOW: { duration: 3, next: 'RED' }
};

// State variables
let currentPhase = 'RED';
let timeRemaining = SIGNAL_PHASES[currentPhase].duration;
let totalRuntime = 0;
let cycleCount = 0;
let densitySum = 0;
let densityReadings = 0;

// Vehicle type distribution (simulated percentages)
const vehicleDistribution = {
    car: 0.60,      // 60% cars
    bus: 0.10,      // 10% buses
    truck: 0.15,    // 15% trucks
    bike: 0.15      // 15% bikes/motorcycles
};

/**
 * Update traffic light visuals
 */
function updateTrafficLight(state) {
    elements.lightRed.className = 'light';
    elements.lightYellow.className = 'light';
    elements.lightGreen.className = 'light';

    if (state === 'RED') {
        elements.lightRed.classList.add('active', 'red');
    } else if (state === 'YELLOW') {
        elements.lightYellow.classList.add('active', 'yellow');
    } else if (state === 'GREEN') {
        elements.lightGreen.classList.add('active', 'green');
    }
}

/**
 * Update timer gauge
 */
function updateGauge(current, max, state) {
    const percent = current / max;
    const offset = gaugeCircumference * (1 - percent);
    elements.timerGauge.style.strokeDashoffset = offset;

    // Change color based on state
    if (state === 'GREEN') {
        elements.timerGauge.style.stroke = 'var(--light-green)';
    } else if (state === 'YELLOW') {
        elements.timerGauge.style.stroke = 'var(--light-yellow)';
    } else {
        elements.timerGauge.style.stroke = 'var(--light-red)';
    }

    elements.timerText.innerHTML = `${current}<span>sec</span>`;

    // Update phase progress bar
    const progressPercent = ((max - current) / max) * 100;
    elements.phaseProgress.style.width = `${progressPercent}%`;
}

/**
 * Update sparkline chart
 */
function updateSparkline(pathEl, data, maxVal, chartType = 'area') {
    const width = 100;
    const height = 50;
    const step = width / (data.length - 1);

    let firstY = height - (data[0] / maxVal) * height;
    if (isNaN(firstY) || firstY < 0) firstY = height;
    let pathData = `M 0 ${firstY}`;

    for (let i = 1; i < data.length; i++) {
        const x = i * step;
        let y = height - (data[i] / maxVal) * height;
        if (isNaN(y) || y < 0) y = height;
        if (y > height) y = height;
        pathData += ` L ${x} ${y}`;
    }
    
    if (chartType === 'area') {
        pathData += ` L ${width} ${height} L 0 ${height} Z`;
    }
    
    pathEl.setAttribute('d', pathData);
}

/**
 * Format time as MM:SS
 */
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

/**
 * Update vehicle type breakdown
 */
function updateVehicleTypes(totalCount) {
    const cars = Math.round(totalCount * vehicleDistribution.car);
    const buses = Math.round(totalCount * vehicleDistribution.bus);
    const trucks = Math.round(totalCount * vehicleDistribution.truck);
    const bikes = totalCount - cars - buses - trucks; // Remaining

    elements.carCount.textContent = cars;
    elements.busCount.textContent = buses;
    elements.truckCount.textContent = trucks;
    elements.bikeCount.textContent = bikes;
}

/**
 * Handle signal phase transitions
 */
function updateSignalPhase() {
    timeRemaining--;
    
    if (timeRemaining <= 0) {
        // Move to next phase
        const nextPhase = SIGNAL_PHASES[currentPhase].next;
        currentPhase = nextPhase;
        timeRemaining = SIGNAL_PHASES[currentPhase].duration;
        
        // Increment cycle count when completing a full cycle (after YELLOW)
        if (currentPhase === 'RED') {
            cycleCount++;
            elements.cycleCount.textContent = cycleCount;
        }
    }
    
    updateTrafficLight(currentPhase);
    updateGauge(timeRemaining, SIGNAL_PHASES[currentPhase].duration, currentPhase);
}

/**
 * Fetch data from Flask API
 */
function updateDashboard() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            // Update vehicle count (current frame)
            const count = data.vehicle_count || 0;
            elements.vehicleCount.textContent = count;
            
            // Update vehicle types breakdown
            updateVehicleTypes(count);
            
            // Update density
            const density = data.density || 'LOW';
            elements.density.textContent = density;
            elements.density.className = 'stat-value density-' + density;
            
            // Update status indicator color
            if (density === 'HIGH') {
                elements.densityStatus.className = 'status-indicator status-stopped';
            } else if (density === 'MEDIUM') {
                elements.densityStatus.className = 'status-indicator status-waiting';
            } else {
                elements.densityStatus.className = 'status-indicator status-active';
            }
            
            // Convert density to numeric
            let densityValue = 1;
            if (density === 'HIGH') densityValue = 3;
            else if (density === 'MEDIUM') densityValue = 2;
            
            densitySum += densityValue;
            densityReadings++;
            
            // Update history
            countHistory.shift();
            countHistory.push(count);
            densityHistory.shift();
            densityHistory.push(densityValue);
            
            // Update sparklines
            updateSparkline(elements.countSparkline, countHistory, 50, 'line');
            updateSparkline(elements.densitySparkline, densityHistory, 3, 'area');
            
            // Update average density
            if (densityReadings > 0) {
                const avgValue = densitySum / densityReadings;
                if (avgValue > 2.5) elements.avgDensity.textContent = 'HIGH';
                else if (avgValue > 1.5) elements.avgDensity.textContent = 'MEDIUM';
                else elements.avgDensity.textContent = 'LOW';
            }
            
            // Update total vehicles (accumulate slowly - count once per second, not per frame)
            const currentTotal = parseInt(elements.totalVehicles.textContent) || 0;
            // Add 0-2 vehicles per second randomly
            const increment = Math.random() < 0.7 ? Math.floor(Math.random() * 3) : 0;
            elements.totalVehicles.textContent = currentTotal + increment;
        })
        .catch(error => {
            console.error('Error fetching status:', error);
        });
}

/**
 * Main update loop
 */
function mainLoop() {
    // Update signal phase
    updateSignalPhase();
    
    // Fetch data from API
    updateDashboard();
    
    // Update runtime
    totalRuntime++;
    elements.runtime.textContent = formatTime(totalRuntime);
}

// Initialize
updateTrafficLight(currentPhase);
updateGauge(timeRemaining, SIGNAL_PHASES[currentPhase].duration, currentPhase);
updateDashboard();

// Run main loop every second
setInterval(mainLoop, 1000);
