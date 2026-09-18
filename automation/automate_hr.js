const fs = require("fs");
const { chromium } = require("playwright");

(async () => {
  const referencePath = "automation/references/onboarding_reference.txt";

  // Read the reference file
  const referenceText = fs.readFileSync(referencePath, "utf8").trim();

  if (!referenceText) {
    throw new Error("Reference file is empty.");
  }

  const browser = await chromium.launch({
    channel: "chrome",
    headless: false
  });

  const page = await browser.newPage();

  try {
    // Open the HR onboarding prototype
    await page.goto("http://127.0.0.1:8000");

    // Transfer the reference information into the HR note field
    await page.fill("#ob-note", referenceText);
    await page.locator("#ob-note").dispatchEvent("input");
    await page.locator("#ob-note").dispatchEvent("change");

    // Verify that the HR note was populated
    const note = await page.inputValue("#ob-note");

    if (!note.trim()) {
      throw new Error("HR note was not populated.");
    }

    console.log("Reference file read successfully.");
    console.log("Reference information transferred to HR note successfully.");
    console.log("Human review is now required.");

    await page.waitForTimeout(3000);

  } catch (error) {
    console.error("Automation failed:", error.message);
    await browser.close();
    process.exit(1);
  }
})();
