const prepareButton = document.getElementById("prepare-note");
const completeButton = document.getElementById("btn-ob-ok");
const noteField = document.getElementById("ob-note");
const referenceSelect = document.getElementById("reference-select");
const status = document.getElementById("status");
const toast = document.getElementById("toast");

const referenceNotes = {
  checklist:
    "Onboarding checklist reference reviewed. The required verification information has been prepared for human review.",

  procedure:
    "Outsourcing acceptance procedure reference reviewed. The relevant onboarding verification information has been prepared for human review.",

  rules:
    "Outsourcing and payroll policy reference reviewed. The relevant verification information has been prepared for human review."
};


// Prepare Note
prepareButton.addEventListener("click", () => {
  const selectedReference = referenceSelect.value;
  const generatedNote = referenceNotes[selectedReference];

  if (!generatedNote) {
    showToast("Please select a reference document.");
    return;
  }

  // Automatically fill the HR note field
  noteField.value = generatedNote;

  // Move record to review state
  status.textContent = "レビュー待ち";
  status.style.background = "#fff1c7";
  status.style.color = "#946200";

  // Allow completion after note preparation
  completeButton.disabled = false;

  // Let user review/edit the note
  noteField.focus();

  showToast("Verification note prepared. Please review it.");
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