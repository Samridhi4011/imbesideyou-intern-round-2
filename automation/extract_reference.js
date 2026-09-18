const mammoth = require("mammoth");

async function extractReferenceNotes() {
  const filePath = "automation/references/onboarding_reference.docx";

  const result = await mammoth.extractRawText({
    path: filePath
  });

  const text = result.value.trim();

  if (!text) {
    throw new Error("No text could be extracted from the DOCX file.");
  }

  const marker = "Notes for HR";
  const markerIndex = text.indexOf(marker);

  if (markerIndex === -1) {
    throw new Error("Notes for HR section was not found.");
  }

  const notes = text
    .slice(markerIndex + marker.length)
    .trim();

  if (!notes) {
    throw new Error("Notes for HR section is empty.");
  }

  return notes;
}

(async () => {
  const notes = await extractReferenceNotes();

  console.log("Relevant reference information extracted successfully:\n");
  console.log(notes);
})();

module.exports = { extractReferenceNotes };