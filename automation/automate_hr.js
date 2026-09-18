const { chromium } = require("playwright");
const { extractReferenceNotes } = require("./extract_reference");

(async () => {
  // Extract only the relevant Notes for HR section from the DOCX
  const referenceText = await extractReferenceNotes();

  const browser = await chromium.launch({
    channel: "chrome",
    headless: false
  });

  const page = await browser.newPage();

  try {
    // Open the HR onboarding prototype
    await page.goto("http://127.0.0.1:8000");

    // Fill the HR note field with extracted reference information
    await page.fill("#ob-note", referenceText);
    await page.locator("#ob-note").dispatchEvent("input");
    await page.locator("#ob-note").dispatchEvent("change");

    // Verify that the HR note was populated
    const note = await page.inputValue("#ob-note");

    if (!note.trim()) {
      throw new Error("HR note was not populated.");
    }

    console.log("DOCX reference processed successfully.");
    console.log("Relevant reference information transferred to HR note successfully.");
    console.log("Human review is now required.");

    await page.waitForTimeout(3000);

  } catch (error) {
    console.error("Automation failed:", error.message);
    await browser.close();
    process.exit(1);
  }
})();