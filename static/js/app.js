// DOM elements
const form = document.getElementById('tts-form');
const textInput = document.getElementById('text');
const modelSelect = document.getElementById('model');
const languageSelect = document.getElementById('language');
const speakerSelect = document.getElementById('speaker');
const speedInput = document.getElementById('speed');
const speedValue = document.getElementById('speed-value');
const generateBtn = document.getElementById('generate-btn');
const clearBtn = document.getElementById('clear-btn');
const charCount = document.getElementById('char-count');
const voiceCloningSection = document.getElementById('voice-cloning-section');
const speakerAudioInput = document.getElementById('speaker-audio');

// Container elements
const loadingContainer = document.getElementById('loading');
const resultContainer = document.getElementById('result');
const errorContainer = document.getElementById('error');

// Result elements
const audioPlayer = document.getElementById('audio-player');
const downloadLink = document.getElementById('download-link');
const resultText = document.getElementById('result-text');
const resultModel = document.getElementById('result-model');
const resultFilename = document.getElementById('result-filename');

// Action buttons
const generateAnotherBtn = document.getElementById('generate-another');
const retryBtn = document.getElementById('retry-btn');
const errorMessage = document.getElementById('error-message');

// Initialize the app
document.addEventListener('DOMContentLoaded', function () {
    initializeApp();
});

function initializeApp() {
    // Set up event listeners
    form.addEventListener('submit', handleFormSubmit);
    clearBtn.addEventListener('click', clearForm);
    textInput.addEventListener('input', updateCharCount);
    speedInput.addEventListener('input', updateSpeedValue);
    modelSelect.addEventListener('change', loadModelData);
    generateAnotherBtn.addEventListener('click', resetToForm);
    retryBtn.addEventListener('click', resetToForm);

    // Initial setup
    updateCharCount();
    updateSpeedValue();
    loadAvailableModels();
}

async function handleFormSubmit(e) {
    e.preventDefault();

    const text = textInput.value.trim();
    if (!text) {
        showError('Please enter some text to convert.');
        return;
    }

    const selectedModel = modelSelect.value;
    const isVoiceCloningModel = selectedModel.includes('xtts') ||
        selectedModel.includes('your_tts') ||
        selectedModel.includes('openvoice');

    try {
        showLoading();
        let response;

        if (isVoiceCloningModel && speakerAudioInput.files.length > 0) {
            // Use FormData for file upload
            const formData = new FormData();
            formData.append('text', text);
            formData.append('model', selectedModel);
            formData.append('language', languageSelect.value);
            formData.append('speaker', speakerSelect.value || '');
            formData.append('speed', speedInput.value);
            formData.append('speaker_audio', speakerAudioInput.files[0]);

            response = await fetch('/generate', {
                method: 'POST',
                body: formData
            });
        } else {
            // Use JSON for regular requests
            const jsonData = {
                text: text,
                model: selectedModel,
                language: languageSelect.value,
                speaker: speakerSelect.value || null,
                speed: parseFloat(speedInput.value)
            };

            response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(jsonData)
            });
        }

        const data = await response.json();

        if (response.ok && data.success) {
            showResult(data);
        } else {
            throw new Error(data.error || 'Failed to generate audio');
        }
    } catch (error) {
        console.error('Error generating audio:', error);
        showError(error.message || 'An unexpected error occurred');
    }
}

function showLoading() {
    hideAllContainers();
    loadingContainer.style.display = 'block';
    loadingContainer.classList.add('fade-in');
    generateBtn.disabled = true;
}

function showResult(data) {
    hideAllContainers();

    // Set audio source and result info
    audioPlayer.src = data.audio_url;
    downloadLink.href = data.audio_url;
    downloadLink.download = data.filename;

    resultText.textContent = data.text;
    resultModel.textContent = data.model;
    resultFilename.textContent = data.filename;

    // Show result container
    resultContainer.style.display = 'block';
    resultContainer.classList.add('fade-in');

    // Re-enable generate button
    generateBtn.disabled = false;
}

function showError(message) {
    hideAllContainers();
    errorMessage.textContent = message;
    errorContainer.style.display = 'block';
    errorContainer.classList.add('fade-in');
    generateBtn.disabled = false;
}

function hideAllContainers() {
    loadingContainer.style.display = 'none';
    resultContainer.style.display = 'none';
    errorContainer.style.display = 'none';
}

function resetToForm() {
    hideAllContainers();
    textInput.focus();
}

function clearForm() {
    textInput.value = '';
    modelSelect.selectedIndex = 0;
    languageSelect.selectedIndex = 0;
    speakerSelect.selectedIndex = 0;
    speedInput.value = 1.0;
    updateCharCount();
    updateSpeedValue();
    resetToForm();
    loadModelData(); // Reload speakers for default model
}

function updateCharCount() {
    const count = textInput.value.length;
    charCount.textContent = count;

    // Add visual feedback for character count
    if (count > 1000) {
        charCount.style.color = '#dc3545';
    } else if (count > 500) {
        charCount.style.color = '#ffc107';
    } else {
        charCount.style.color = '#666';
    }
}

function updateSpeedValue() {
    speedValue.textContent = speedInput.value + 'x';
}

async function loadAvailableModels() {
    try {
        const response = await fetch('/models');
        const data = await response.json();

        if (response.ok && data.models) {
            populateModelSelect(data.models);
            // Load data for the default selected model
            await loadModelData();
        }
    } catch (error) {
        console.error('Error loading models:', error);
    }
}

function populateModelSelect(models) {
    // Clear existing options except the first few default ones
    const defaultOptions = modelSelect.innerHTML;

    models.forEach(model => {
        // Check if option already exists
        const existingOption = Array.from(modelSelect.options).find(opt => opt.value === model);
        if (!existingOption) {
            const option = document.createElement('option');
            option.value = model;
            option.textContent = formatModelName(model);
            modelSelect.appendChild(option);
        }
    });
}

function formatModelName(modelName) {
    // Format model name for display
    return modelName.split('/').pop().replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

async function loadModelData() {
    const selectedModel = modelSelect.value;

    // Show/hide voice cloning section based on model
    const isVoiceCloningModel = selectedModel.includes('xtts') ||
        selectedModel.includes('your_tts') ||
        selectedModel.includes('openvoice');
    if (voiceCloningSection) {
        voiceCloningSection.style.display = isVoiceCloningModel ? 'block' : 'none';
    }

    // Load speakers
    try {
        const speakersResponse = await fetch(`/speakers/${encodeURIComponent(selectedModel)}`);
        const speakersData = await speakersResponse.json();

        if (speakersResponse.ok && speakersData.speakers) {
            populateSpeakerSelect(speakersData.speakers);
        }
    } catch (error) {
        console.error('Error loading speakers:', error);
    }

    // Load languages
    try {
        const languagesResponse = await fetch(`/languages/${encodeURIComponent(selectedModel)}`);
        const languagesData = await languagesResponse.json();

        if (languagesResponse.ok && languagesData.languages) {
            populateLanguageSelect(languagesData.languages);
        }
    } catch (error) {
        console.error('Error loading languages:', error);
    }
}

function populateSpeakerSelect(speakers) {
    // Clear existing options except default
    speakerSelect.innerHTML = '<option value="">Default Speaker</option>';

    if (speakers && speakers.length > 0) {
        speakers.forEach(speaker => {
            const option = document.createElement('option');
            option.value = speaker;
            option.textContent = speaker;
            speakerSelect.appendChild(option);
        });
        speakerSelect.disabled = false;
    } else {
        speakerSelect.disabled = true;
    }
}

function populateLanguageSelect(languages) {
    if (languages && languages.length > 0) {
        // Store current selection
        const currentLang = languageSelect.value;

        // Clear and repopulate
        languageSelect.innerHTML = '';
        languages.forEach(lang => {
            const option = document.createElement('option');
            option.value = lang.code || lang;
            option.textContent = lang.name || lang;
            languageSelect.appendChild(option);
        });

        // Restore selection if it exists in new options
        const optionExists = Array.from(languageSelect.options).some(opt => opt.value === currentLang);
        if (optionExists) {
            languageSelect.value = currentLang;
        }
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function (e) {
    // Ctrl/Cmd + Enter to generate
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (!generateBtn.disabled) {
            form.dispatchEvent(new Event('submit'));
        }
    }

    // Escape to clear form
    if (e.key === 'Escape') {
        clearForm();
    }
});

// Auto-save form data to localStorage
function saveFormData() {
    const formData = {
        text: textInput.value,
        model: modelSelect.value,
        language: languageSelect.value,
        speaker: speakerSelect.value,
        speed: speedInput.value
    };
    localStorage.setItem('tts-form-data', JSON.stringify(formData));
}

function loadFormData() {
    const savedData = localStorage.getItem('tts-form-data');
    if (savedData) {
        try {
            const data = JSON.parse(savedData);
            textInput.value = data.text || '';
            modelSelect.value = data.model || modelSelect.value;
            languageSelect.value = data.language || languageSelect.value;
            speakerSelect.value = data.speaker || '';
            speedInput.value = data.speed || 1.0;
            updateCharCount();
            updateSpeedValue();
            // Trigger model data load to update UI after restoring selection
            loadModelData();
        } catch (error) {
            console.error('Error loading saved form data:', error);
        }
    }
}

// Save form data on input
textInput.addEventListener('input', saveFormData);
modelSelect.addEventListener('change', saveFormData);
languageSelect.addEventListener('change', saveFormData);
speakerSelect.addEventListener('change', saveFormData);
speedInput.addEventListener('input', saveFormData);

// Load saved form data on page load
setTimeout(loadFormData, 100);