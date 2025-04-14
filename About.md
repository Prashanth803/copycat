Great question! To fit these into BDD **feature files**, you organize them into separate or grouped `.feature` files based on related functionality. Here's how you can structure and write them in clean, modular BDD files using Gherkin syntax.

---

### ✅ **Folder Structure Suggestion**
```
features/
│
├── login/
│   └── sign_on.feature
│
├── payment/
│   ├── create_payment.feature
│   └── review_and_submit.feature
│
└── utils/
    └── email_dropdown_behavior.feature
```

---

### 🔐 **File: `sign_on.feature`**
```gherkin
Feature: User Sign On

  Scenario: Successful Sign On and navigation
    Given the user is on the Sign On page
    And the Sign On page contains fields for Company, Username, and Password
    When the user enters valid Company, Username, and Password
    And the user clicks the Sign On button
    Then the user should be navigated to the Create Options page
    And a Create button should be visible
```

---

### 💳 **File: `create_payment.feature`**
```gherkin
Feature: Payment Option Selection and Navigation

  Scenario: Viewing Create Options
    Given the user is on the Create Options page
    When the user clicks the Create button
    Then the user should see options: "Payment", "Payment with Template", and "File Upload"

  Scenario: Navigating to Payment Page
    Given the user selects the "Payment" option
    When the page loads
    Then the user should be prompted to enter a Passcode

  Scenario: Validating Passcode and Navigating to Payment Creation
    Given the user enters a valid Passcode
    When the passcode is submitted
    Then the user should be navigated to the Payment Creation page
```

---

### 📧 **File: `email_dropdown_behavior.feature`**
```gherkin
Feature: Email Dropdown Behavior in Payment Form

  Scenario: Email option is selected
    Given the user is on the Payment Creation page
    When the user selects "Email" from the Email dropdown
    Then the adjacent Email input field should become active
    And the user should enter a valid email address

  Scenario: No Email option is selected
    Given the user is on the Payment Creation page
    When the user selects "No Email" from the Email dropdown
    Then the Email input field should disappear
```

---

### 🧾 **File: `review_and_submit.feature`**
```gherkin
Feature: Review and Submit Payment

  Scenario: Reviewing Payment Details
    Given all required fields are filled on the Payment Creation page
    When the user clicks the Review button
    Then a summary of all entered details should be displayed
    And "Edit", "Cancel", and "Create" buttons should be visible

  Scenario: Editing Payment Details
    Given the user is on the Review page
    When the user clicks the Edit button
    Then the user should be redirected to the Payment Creation page
    And all previously entered values should be retained

  Scenario: Cancelling the Payment Creation
    Given the user is on the Review page
    When the user clicks the Cancel button
    Then the user should be redirected to the Create Options page

  Scenario: Creating Virtual Card
    Given the user is on the Review page
    When the user clicks the Create button
    Then a virtual card should be created
    And the user should be shown card details
    And dropdown options should be viewable by clicking the dropdown icon
```

---

Would you like me to help you scaffold these into a Cucumber or Behave (Python) project with matching step definitions?

Absolutely! To integrate BDD `.feature` files with TypeScript, you'd typically use **Cucumber.js** along with **TypeScript** and a test runner like **Playwright**, **WebDriverIO**, or **Puppeteer** (optional). Here's a clean and modern setup using `@cucumber/cucumber` + TypeScript:

---

## ✅ Prerequisites

### Install packages:
```bash
npm install --save-dev @cucumber/cucumber ts-node typescript @types/node
```

### Optional (for browser automation):
```bash
npm install --save-dev playwright
```

---

## 📁 Project Structure
```
.
├── features/
│   ├── login/
│   │   └── sign_on.feature
│   ├── step_definitions/
│   │   ├── login.steps.ts
│   │   ├── payment.steps.ts
│   │   └── utils.steps.ts
│   └── support/
│       ├── hooks.ts
│       └── world.ts
├── tsconfig.json
├── cucumber.tsconfig.json
└── cucumber.js
```

---

## 🧠 `cucumber.js` – Cucumber Config
```js
module.exports = {
  default: `--require-module ts-node/register --require features/**/*.steps.ts --publish-quiet`
}
```

---

## 🛠️ `tsconfig.json`
```json
{
  "compilerOptions": {
    "target": "es6",
    "module": "commonjs",
    "lib": ["es6", "dom"],
    "strict": true,
    "esModuleInterop": true,
    "outDir": "./dist",
    "rootDir": "./"
  },
  "include": ["features/**/*.ts"]
}
```

---

## ✍️ Example: `features/login/sign_on.feature`
```gherkin
Feature: User Sign On

  Scenario: Successful Sign On and navigation
    Given the user is on the Sign On page
    And the Sign On page contains fields for Company, Username, and Password
    When the user enters valid Company, Username, and Password
    And the user clicks the Sign On button
    Then the user should be navigated to the Create Options page
    And a Create button should be visible
```

---

## ✅ `features/step_definitions/login.steps.ts`
```ts
import { Given, When, Then } from '@cucumber/cucumber';
import assert from 'assert';

Given('the user is on the Sign On page', function () {
  console.log('Navigating to Sign On page...');
  // browser.goto('/signon') if using Playwright/WebDriver
});

Given('the Sign On page contains fields for Company, Username, and Password', function () {
  console.log('Checking for form fields...');
});

When('the user enters valid Company, Username, and Password', function () {
  console.log('Filling out form...');
});

When('the user clicks the Sign On button', function () {
  console.log('Clicking Sign On button...');
});

Then('the user should be navigated to the Create Options page', function () {
  console.log('Validating navigation...');
});

Then('a Create button should be visible', function () {
  const isVisible = true;
  assert.strictEqual(isVisible, true);
});
```

---

## 🧩 Optional: Playwright Integration (Example)
If you use Playwright, you can import and use it:

```ts
import { chromium, Browser, Page } from 'playwright';

let browser: Browser;
let page: Page;

Given('the user is on the Sign On page', async function () {
  browser = await chromium.launch();
  page = await browser.newPage();
  await page.goto('https://your-app.com/signon');
});

When('the user enters valid Company, Username, and Password', async function () {
  await page.fill('#company', 'MyCompany');
  await page.fill('#username', 'myuser');
  await page.fill('#password', 'mypassword');
});
```

---

## 🚀 Running the Tests
```bash
npx cucumber-js
```

---

Would you like me to generate a ready-to-run GitHub template project for this with Playwright or Puppeteer baked in?


