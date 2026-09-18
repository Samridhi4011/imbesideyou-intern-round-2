const prepareButton = document.getElementById("prepare-note");
const completeButton = document.getElementById("btn-ob-ok");
const noteField = document.getElementById("ob-note");
const referenceSelect = document.getElementById("reference-select");
const status = document.getElementById("status");
const toast = document.getElementById("toast");
const automationStatus = document.getElementById("automation-status");


const referenceNotes = {
  checklist:
    "Onboarding checklist reference reviewed. The required verification information has been prepared for human review.",

  procedure:
    "Outsourcing acceptance procedure reference reviewed. The relevant onboarding verification information has been prepared for human review.",

  rules:
    "Outsourcing and payroll policy reference reviewed. The relevant verification information has been prepared for human review."
};


// Transfer Reference to HR Note
prepareButton.addEventListener("click", () => {

  const selectedReference = referenceSelect.value;
  const generatedNote = referenceNotes[selectedReference];

  if (!generatedNote) {
    showToast("Please select a reference document.");
    return;
  }

  // Prepare the reference-based note
  noteField.value = generatedNote;

  // Update HR record status
  status.textContent = "レビュー待ち";
  status.style.background = "#fff1c7";
  status.style.color = "#946200";

  // Update automation status
  automationStatus.textContent = "Awaiting Human Review";
  automationStatus.style.background = "#fff1c7";
  automationStatus.style.color = "#946200";

  // Allow completion after human review
  completeButton.disabled = false;

  // Let the user review or edit the prepared note
  noteField.focus();

  showToast("Reference transferred to HR note. Please review it.");
});


// Complete Verification
completeButton.addEventListener("click", () => {

  const note = noteField.value.trim();

  if (!note) {
    showToast("Please prepare or enter a verification note first.");
    noteField.focus();
    return;
  }

  // Mark verification as completed
  status.textContent = "完了";
  status.style.background = "#dff4e8";
  status.style.color = "#16804b";

  // Update automation status
  automationStatus.textContent = "Completed";
  automationStatus.style.background = "#dff4e8";
  automationStatus.style.color = "#16804b";

  completeButton.disabled = true;

  showToast("Verification completed successfully.");
});


// Toast notification
function showToast(message) {

  toast.textContent = message;

  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 3000);
}