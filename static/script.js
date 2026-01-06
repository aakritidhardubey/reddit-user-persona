// DOM Elements
const usernameInput = document.getElementById('usernameInput');
const generateBtn = document.getElementById('generateBtn');
const loadingIndicator = document.getElementById('loadingIndicator');
const resultsSection = document.getElementById('resultsSection');
const usernameDisplay = document.getElementById('usernameDisplay');

// Download buttons
const downloadText = document.getElementById('downloadText');
const downloadJson = document.getElementById('downloadJson');
const downloadPdf = document.getElementById('downloadPdf');

// Current persona data
let currentPersona = null;

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
});

function setupEventListeners() {
    // Generate button click
    generateBtn.addEventListener('click', generatePersona);
    
    // Enter key in input
    usernameInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            generatePersona();
        }
    });
    
    // Download buttons
    downloadText.addEventListener('click', () => downloadFile('text'));
    downloadJson.addEventListener('click', () => downloadFile('json'));
    downloadPdf.addEventListener('click', () => downloadFile('pdf'));
}

async function generatePersona() {
    const username = usernameInput.value.trim();
    
    if (!username) {
        showError('Please enter a Reddit username');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    
    try {
        const response = await fetch('/api/generate-persona', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: username })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate persona');
        }
        
        // Store current persona
        currentPersona = data;
        
        // Display results
        displayPersona(data);
        
    } catch (error) {
        showError(error.message);
    } finally {
        setLoadingState(false);
    }
}

function displayPersona(data) {
    // Show results section
    resultsSection.classList.add('show');
    
    // Update username display
    usernameDisplay.textContent = `u/${data.username}`;
    
    // Populate detailed analysis first
    populateDetailedAnalysis(data.persona_text);
    
    // Populate persona cards
    populatePersonaCards(data.persona_json);
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function displayPersona(data) {
    // Show results section
    resultsSection.classList.add('show');
    
    // Update username display
    usernameDisplay.textContent = `u/${data.username}`;
    
    // Populate persona cards first
    populatePersonaCards(data.persona_json);
    
    // Populate detailed analysis
    populateDetailedAnalysis(data.persona_text, data.persona_json);
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function populateDetailedAnalysis(personaText, personaJson) {
    const detailedContent = document.getElementById('detailedContent');
    const analysisTime = document.getElementById('analysisTime');
    const confidenceScore = document.getElementById('confidenceScore');
    
    if (detailedContent && personaText) {
        detailedContent.textContent = personaText;
    } else {
        detailedContent.textContent = 'No detailed analysis available.';
    }
    
    // Update analysis stats
    if (analysisTime) {
        const now = new Date();
        analysisTime.textContent = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    }
    
    if (confidenceScore && personaJson) {
        // Calculate confidence based on available data
        const dataFields = ['demographics', 'interests', 'personality_traits', 'career', 'technical_skills', 'social_behavior'];
        const filledFields = dataFields.filter(field => {
            const value = personaJson[field];
            return value && (
                (typeof value === 'string' && value !== 'Unknown' && value.length > 0) ||
                (Array.isArray(value) && value.length > 0) ||
                (typeof value === 'object' && Object.keys(value).length > 0)
            );
        });
        
        const confidencePercentage = Math.round((filledFields.length / dataFields.length) * 100);
        let confidenceLevel = 'Low Confidence';
        let confidenceColor = '#e53e3e';
        
        if (confidencePercentage >= 80) {
            confidenceLevel = 'High Confidence';
            confidenceColor = '#38a169';
        } else if (confidencePercentage >= 60) {
            confidenceLevel = 'Medium Confidence';
            confidenceColor = '#d69e2e';
        }
        
        confidenceScore.innerHTML = `<span style="color: ${confidenceColor}">${confidenceLevel} (${confidencePercentage}%)</span>`;
    }
}

function populatePersonaCards(personaJson) {
    // Check if there's an error and try to parse raw_output
    if (personaJson.error && personaJson.raw_output) {
        try {
            // Try to extract JSON from raw_output
            let rawOutput = personaJson.raw_output;
            
            // Remove markdown code blocks
            if (rawOutput.includes('```json')) {
                rawOutput = rawOutput.split('```json')[1].split('```')[0];
            } else if (rawOutput.includes('```')) {
                // Find the part that contains JSON
                const parts = rawOutput.split('```');
                for (const part of parts) {
                    const trimmed = part.trim();
                    if (trimmed.startsWith('{') || trimmed.startsWith('[')) {
                        rawOutput = trimmed;
                        break;
                    }
                }
            }
            
            // Try to parse the cleaned output
            const parsedJson = JSON.parse(rawOutput.trim());
            personaJson = parsedJson;
        } catch (e) {
            console.error('Failed to parse raw_output:', e);
            showErrorInCards('Failed to parse persona data');
            return;
        }
    }
    
    // Demographics
    const demographics = personaJson.demographics || {};
    const demographicsContent = document.getElementById('demographicsContent');
    demographicsContent.innerHTML = `
        <div class="info-item">
            <span class="info-label">Age:</span>
            <span class="info-value">${demographics.age || 'Unknown'}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Location:</span>
            <span class="info-value">${demographics.location || 'Unknown'}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Gender:</span>
            <span class="info-value">${demographics.gender || 'Unknown'}</span>
        </div>
    `;
    
    // Interests
    const interests = personaJson.interests || [];
    const interestsContent = document.getElementById('interestsContent');
    if (interests.length > 0) {
        interestsContent.innerHTML = interests.map(interest => 
            `<span class="tag">${interest}</span>`
        ).join('');
    } else {
        interestsContent.innerHTML = '<p>No specific interests identified</p>';
    }
    
    // Personality Traits
    const personality = personaJson.personality_traits || [];
    const personalityContent = document.getElementById('personalityContent');
    if (personality.length > 0) {
        personalityContent.innerHTML = personality.map(trait => 
            `<span class="tag">${trait}</span>`
        ).join('');
    } else {
        personalityContent.innerHTML = '<p>No specific personality traits identified</p>';
    }
    
    // Career & Skills
    const career = personaJson.career || 'Unknown';
    const skills = personaJson.technical_skills || [];
    const careerContent = document.getElementById('careerContent');
    careerContent.innerHTML = `
        <div class="info-item">
            <span class="info-label">Career:</span>
            <span class="info-value">${career}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Technical Skills:</span>
            <div style="margin-top: 10px;">
                ${skills.length > 0 ? skills.map(skill => `<span class="tag">${skill}</span>`).join('') : '<p>No specific technical skills identified</p>'}
            </div>
        </div>
    `;
    
    // Activity Patterns
    const activity = personaJson.activity_patterns || {};
    const activityContent = document.getElementById('activityContent');
    activityContent.innerHTML = `
        <div class="info-item">
            <span class="info-label">Posting Frequency:</span>
            <span class="info-value">${activity.posting_frequency || 'Unknown'}</span>
        </div>
        <div class="info-item">
            <span class="info-label">Top Subreddits:</span>
            <div style="margin-top: 10px;">
                ${(activity.top_subreddits || []).length > 0 ? 
                    (activity.top_subreddits || []).map(sub => `<span class="tag">r/${sub}</span>`).join('') :
                    '<p>No specific subreddits identified</p>'
                }
            </div>
        </div>
    `;
    
    // Social Behavior
    const social = personaJson.social_behavior || 'No social behavior analysis available';
    const socialContent = document.getElementById('socialContent');
    socialContent.innerHTML = `<p>${social}</p>`;
}

function downloadFile(type) {
    if (!currentPersona) {
        showError('No persona data available to download');
        return;
    }
    
    const username = currentPersona.username;
    
    if (type === 'text') {
        downloadTextFile(currentPersona.persona_text, `${username}_persona.txt`);
    } else if (type === 'json') {
        downloadJsonFile(currentPersona.persona_json, `${username}_persona.json`);
    } else if (type === 'pdf') {
        downloadPdfFile(username);
    }
}

function downloadTextFile(content, filename) {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

function downloadJsonFile(content, filename) {
    const blob = new Blob([JSON.stringify(content, null, 2)], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

function downloadPdfFile(username) {
    const { jsPDF } = window.jspdf;
    
    // Create new PDF document
    const doc = new jsPDF();
    
    // Add title
    doc.setFontSize(20);
    doc.setTextColor(255, 69, 0); // Reddit orange
    doc.text(`Reddit User Persona: u/${username}`, 20, 30);
    
    // Add generation date
    doc.setFontSize(10);
    doc.setTextColor(100, 100, 100);
    doc.text(`Generated on: ${new Date().toLocaleDateString()}`, 20, 40);
    
    let yPosition = 60;
    const lineHeight = 8;
    const pageHeight = doc.internal.pageSize.height;
    
    // Helper function to add section
    function addSection(title, content, color = [255, 69, 0]) {
        // Skip empty sections
        if (!content || (Array.isArray(content) && content.length === 0) || content === 'Unknown') {
            return;
        }
        
        // Check if we need a new page
        if (yPosition > pageHeight - 40) {
            doc.addPage();
            yPosition = 30;
        }
        
        // Section title
        doc.setFontSize(14);
        doc.setTextColor(color[0], color[1], color[2]);
        doc.text(title, 20, yPosition);
        yPosition += lineHeight + 2;
        
        // Section content
        doc.setFontSize(10);
        doc.setTextColor(50, 50, 50);
        
        if (typeof content === 'string') {
            const lines = doc.splitTextToSize(content, 170);
            lines.forEach(line => {
                if (yPosition > pageHeight - 20) {
                    doc.addPage();
                    yPosition = 30;
                }
                doc.text(line, 20, yPosition);
                yPosition += lineHeight;
            });
        } else if (Array.isArray(content)) {
            content.forEach(item => {
                if (yPosition > pageHeight - 20) {
                    doc.addPage();
                    yPosition = 30;
                }
                doc.text(`• ${item}`, 25, yPosition);
                yPosition += lineHeight;
            });
        }
        
        yPosition += 5; // Extra space after section
    }
    
    const persona = currentPersona.persona_json;
    
    // Demographics
    if (persona.demographics) {
        const demo = persona.demographics;
        const demoText = `Age: ${demo.age || 'Unknown'}\nLocation: ${demo.location || 'Unknown'}\nGender: ${demo.gender || 'Unknown'}`;
        addSection('Demographics', demoText);
    }
    
    // Interests
    if (persona.interests && persona.interests.length > 0) {
        addSection('Interests & Hobbies', persona.interests, [255, 99, 20]);
    }
    
    // Personality Traits
    if (persona.personality_traits && persona.personality_traits.length > 0) {
        addSection('Personality Traits', persona.personality_traits, [255, 135, 23]);
    }
    
    // Career
    if (persona.career) {
        let careerText = `Career: ${persona.career}`;
        if (persona.technical_skills && persona.technical_skills.length > 0) {
            careerText += `\n\nTechnical Skills:\n${persona.technical_skills.join(', ')}`;
        }
        addSection('Career & Skills', careerText, [255, 171, 26]);
    }
    
    // Activity Patterns
    if (persona.activity_patterns) {
        const activity = persona.activity_patterns;
        let activityText = `Posting Frequency: ${activity.posting_frequency || 'Unknown'}`;
        if (activity.top_subreddits && activity.top_subreddits.length > 0) {
            activityText += `\n\nTop Subreddits:\n${activity.top_subreddits.map(sub => `r/${sub}`).join(', ')}`;
        }
        addSection('Activity Patterns', activityText, [255, 215, 0]);
    }
    
    // Social Behavior
    if (persona.social_behavior) {
        addSection('Social Behavior', persona.social_behavior, [255, 69, 0]);
    }
    
    // Save the PDF
    doc.save(`${username}_persona.pdf`);
}

function showErrorInCards(message) {
    const cardContents = [
        'detailedContent', 'demographicsContent', 'interestsContent', 'personalityContent',
        'careerContent', 'activityContent', 'socialContent'
    ];
    
    cardContents.forEach(contentId => {
        const element = document.getElementById(contentId);
        if (element) {
            if (contentId === 'detailedContent') {
                element.textContent = `Error: ${message}`;
            } else {
                element.innerHTML = `<p style="color: #e53e3e; font-style: italic;">${message}</p>`;
            }
        }
    });
}

function setLoadingState(loading) {
    if (loading) {
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        loadingIndicator.classList.add('show');
    } else {
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-search"></i> Analyze Profile';
        loadingIndicator.classList.remove('show');
    }
}

function showError(message) {
    // Remove existing error messages
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Create new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
    
    // Insert after input card
    const inputCard = document.querySelector('.input-card');
    inputCard.parentNode.insertBefore(errorDiv, inputCard.nextSibling);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);
}