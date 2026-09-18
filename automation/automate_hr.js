const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch({
    channel: "chrome",
    headless: false
  });

  const page = await browser.newPage();

  try {
    // Open the HR onboarding prototype
    await page.goto("http://127.0.0.1:8000");

    // Select the reference document
    await page.selectOption(
      "#reference-select",
      "checklist"
    );

    // Trigger the reference-to-HR transfer
    await page.click("#prepare-note");

    // Verify that the HR note was populated
    const note = await page.inputValue("#ob-note");

    if (!note.trim()) {
      throw new Error("HR note was not populated.");
    }

    console.log("Reference transferred to HR note successfully.");
    console.log("Human review is now required.");

  } catch (error) {
    console.error("Automation failed:", error.message);
    await browser.close();
    process.exit(1);
  }
})();
