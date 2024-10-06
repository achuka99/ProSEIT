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
