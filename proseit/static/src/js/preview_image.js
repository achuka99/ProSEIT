function nextStep(step) {
    // Show the correct step
    document.querySelectorAll('.form-step').forEach(function(el) {
        el.style.display = 'none';
    });
    document.getElementById('step-' + step).style.display = 'block';

    // Update progress bar
    var progressPercentage = step * 33;
    document.getElementById('registration-progress').style.width = progressPercentage + '%';
    document.getElementById('registration-progress').innerHTML = 'Step ' + step + ' of 3';
}

function prevStep(step) {
    nextStep(step);
}

function previewImage(input) {
    var file = input.files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('image-preview-tag').src = e.target.result;
            document.getElementById('image-preview').style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

function submitForm() {
    document.getElementById("professional-registration-form").submit();
}

// Global variables
let educationCounter = 1;
let educationEntries = {};

// Function to add education entry
function addEducationEntry() {
    const institution = document.getElementById('modal_institution').value;
    const educationLevel = document.getElementById('modal_education_level').value;
    const yearCompleted = document.getElementById('modal_year_completed').value;
    const startYear = document.getElementById("modal_start_year").value;

    // Validate inputs
    if (!institution || !educationLevel || !yearCompleted) {
        alert('Please fill out all fields.');
        return;
    }

    // Add the education entry to the table
    const tableBody = document.getElementById('education-entries-body');
    const newRow = document.createElement('tr');
    newRow.id = `education_row_${educationCounter}`;

    newRow.innerHTML = `
        <td>${institution}</td>
        <td>${educationLevel}</td>
        <td>${startYear}</td>
        <td>${yearCompleted}</td>
        <td>
            <button type="button" class="btn btn-danger" onclick="removeEducationEntry(${educationCounter})">Remove</button>
        </td>
    `;

    tableBody.appendChild(newRow);

    // Store education entry in the object
    educationEntries[`institution_${educationCounter}`] = institution;
    educationEntries[`level_${educationCounter}`] = educationLevel;
    educationEntries[`start_year_${educationCounter}`] = startYear;
    educationEntries[`year_${educationCounter}`] = yearCompleted;

    // Increment counter for next entry
    educationCounter++;

    // Clear modal inputs
    document.getElementById('modal_institution').value = '';
    document.getElementById('modal_education_level').value = '';
    document.getElementById('modal_start_year').value = '';
    document.getElementById('modal_year_completed').value = '';

    // Close the modal
    $('#educationModal').modal('hide');
}

// Function to remove education entry
function removeEducationEntry(index) {
    // Remove the table row
    var row = document.getElementById(`education_row_${index}`);
    if (row) {
        row.remove();
    }

    // Remove the entry from the educationEntries object
    delete educationEntries[`institution_${index}`];
    delete educationEntries[`level_${index}`];
    delete educationEntries[`start_year_${index}`];
    delete educationEntries[`year_${index}`];
}

// Global variables
let certificationCounter = 1;
let certificationEntries = {};

// Function to add certification entry
function addCertificationEntry() {
    const certificationName = document.getElementById('modal_certification_name').value;
    const issuingOrganization = document.getElementById('modal_issuing_organization').value;
    const certificationType = document.getElementById('modal_certification_type').value; 
    const dateAwarded = document.getElementById('modal_date_awarded').value;
    const expirationDate = document.getElementById('modal_expiration_date').value;
    const certificationNumber = document.getElementById('modal_certification_number').value;
    const CertificationCompetencyLevel = document.getElementById('modal_certification_competency').value;

    // Validate inputs
    if (!certificationName || !issuingOrganization) {
        alert('Please fill out all required fields.');
        return;
    }

    // Add the certification entry to the table
    const tableBody = document.getElementById('certification-entries-body');
    const newRow = document.createElement('tr');
    newRow.id = `certification_row_${certificationCounter}`;

    newRow.innerHTML = `
        <td>${certificationName}</td>
        <td>${issuingOrganization}</td>
        <td>${certificationType}</td> <!-- Display selected type -->
        <td>${dateAwarded || 'N/A'}</td>
        <td>${expirationDate || 'N/A'}</td>
        <td>${certificationNumber}</td>
        <td>${CertificationCompetencyLevel}</td>
        <td>
            <button type="button" class="btn btn-danger" onclick="removeCertificationEntry(${certificationCounter})">Remove</button>
        </td>
    `;

    tableBody.appendChild(newRow);

    // Store certification entry in the object
    certificationEntries[`certification_${certificationCounter}`] = {
        name: certificationName,
        organization: issuingOrganization,
        type: certificationType,
        awarded: dateAwarded,
        expiration: expirationDate,
        certification_number: certificationNumber,
        competency_level: CertificationCompetencyLevel
    };

    // Increment counter for next entry
    certificationCounter++;

    // Clear modal inputs
    document.getElementById('modal_certification_name').value = '';
    document.getElementById('modal_issuing_organization').value = '';
    document.getElementById('modal_certification_type').value = '';
    document.getElementById('modal_date_awarded').value = '';
    document.getElementById('modal_expiration_date').value = '';
    document.getElementById('modal_certification_number').value = '';
    document.getElementById('modal_certification_competency').value = '';

    // Close the modal
    $('#certificationModal').modal('hide');
}

// Function to remove certification entry
function removeCertificationEntry(index) {
    // Remove the table row
    var row = document.getElementById(`certification_row_${index}`);
    if (row) {
        row.remove();
    }

    // Remove the entry from the certificationEntries object
    delete certificationEntries[`certification_${index}`];
}

// Global variables
let skillCounter = 1;
let technicalSkillsEntries = {};
let softSkillsEntries = {};

// Function to add skill entry
function addSkillEntry() {
    const skillType = document.getElementById('skill_type').value;
    const skillName = document.getElementById('skill_name').value;
    const competencyLevel = document.getElementById('competency_level').value;

    // Validate inputs
    if (!skillName || !competencyLevel) {
        alert('Please fill out all fields.');
        return;
    }

    // Determine which table to add the skill to based on skill type
    let tableBody;
    let entriesObject;

    if (skillType === 'technical') {
        tableBody = document.getElementById('technical-skills-body');
        entriesObject = technicalSkillsEntries;
    } else {
        tableBody = document.getElementById('soft-skills-body');
        entriesObject = softSkillsEntries;
    }

    // Add the skill entry to the respective table
    const newRow = document.createElement('tr');
    newRow.id = `skill_row_${skillCounter}`;

    newRow.innerHTML = `
        <td>${skillName}</td>
        <td>${competencyLevel}</td>
        <td>
            <button type="button" class="btn btn-danger" onclick="removeSkillEntry(${skillCounter}, '${skillType}')">Remove</button>
        </td>
    `;

    tableBody.appendChild(newRow);

    // Store the skill entry in the respective object
    entriesObject[`skill_${skillCounter}`] = {
        name: skillName,
        competency: competencyLevel
    };

    // Increment counter for next entry
    skillCounter++;

    // Clear modal inputs
    document.getElementById('skill_name').value = '';
    document.getElementById('competency_level').value = '';

    // Close the modal
    $('#skillsModal').modal('hide');
}

// Function to remove skill entry
function removeSkillEntry(index, skillType) {
    // Remove the table row
    var row = document.getElementById(`skill_row_${index}`);
    if (row) {
        row.remove();
    }

    // Remove the entry from the respective object
    if (skillType === 'technical') {
        delete technicalSkillsEntries[`skill_${index}`];
    } else {
        delete softSkillsEntries[`skill_${index}`];
    }
}


// Function to submit the form, including certifications
function submitForm() {
    // You can include the educationEntries and certificationEntries as part of the form submission
    const form = document.getElementById('professional-registration-form');

    // Convert educationEntries and certificationEntries to JSON strings
    const educationData = JSON.stringify(educationEntries);
    const certificationData = JSON.stringify(certificationEntries);

    // Convert technicalSkillsEntries and softSkillsEntries to JSON strings
    const technicalSkillsData = JSON.stringify(technicalSkillsEntries);
    const softSkillsData = JSON.stringify(softSkillsEntries);

    // Create hidden inputs for the JSON data
    const educationInput = document.createElement('input');
    educationInput.type = 'hidden';
    educationInput.name = 'education_entries';
    educationInput.value = educationData;

    const certificationInput = document.createElement('input');
    certificationInput.type = 'hidden';
    certificationInput.name = 'certification_entries';
    certificationInput.value = certificationData;

    // Create hidden inputs for the JSON data
    const technicalSkillsInput = document.createElement('input');
    technicalSkillsInput.type = 'hidden';
    technicalSkillsInput.name = 'technical_skills_entries';
    technicalSkillsInput.value = technicalSkillsData;

    const softSkillsInput = document.createElement('input');
    softSkillsInput.type = 'hidden';
    softSkillsInput.name = 'soft_skills_entries';
    softSkillsInput.value = softSkillsData;


    form.appendChild(educationInput);
    form.appendChild(certificationInput);
    form.appendChild(technicalSkillsInput);
    form.appendChild(softSkillsInput);

    // Submit the form
    form.submit();
}
