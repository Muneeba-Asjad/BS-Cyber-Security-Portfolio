function validateForm() {

    let text = document.getElementById("text").value.trim();

    if (text === "") {
        alert("Please enter some text!");
        return false;
    }

    // Change button while processing
    const btn = document.getElementById("submitBtn");
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    btn.disabled = true;

    return true;
}