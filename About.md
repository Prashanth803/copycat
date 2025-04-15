Got it, Lisa! Let’s break this down step-by-step using the [Playwright-BDD-Automation repo](https://github.com/TestRoverAutomation/Playwright-BDD-Automation), so you can clearly see:

1. **Where the tests are triggered**
2. **Where the test inputs come from**
3. **How the data flows from `.feature` files to actual test logic**

---

### **1. Where are the tests triggered from?**

Tests are triggered by Playwright’s test runner, but with **CucumberJS** integration.

You can see the test script in **`package.json`**:

```json
"scripts": {
  "test": "npx playwright test"
}
```

This **actually runs the tests defined in the `.feature` files**, which are connected via step definitions.

---

### **2. Where are the tests written?**

Tests (test cases) are written in **`features/*.feature`** files in **Gherkin syntax**, like this:

```gherkin
Scenario: Login with valid credentials
  Given I launch the application
  When I login with username "admin" and password "password123"
  Then I should see the dashboard
```

These steps don’t do anything **yet** — they need to be connected to real code.

---

### **3. Where does the step logic live?**

Each step is implemented in a corresponding **`.steps.js` file**, usually inside:

```
tests/step_definitions/
```

For example, a step like this in Gherkin:

```gherkin
When I login with username "admin" and password "password123"
```

Will be matched by code like:

```js
When('I login with username {string} and password {string}', async (username, password) => {
  await loginPage.login(username, password);
});
```

This is where your **data inputs** (`username`, `password`) are extracted and passed to real logic.

---

### **4. What happens inside the page object (`loginPage.login()`)?**

That method is in `auth/loginPage.js` (or similar). It contains the actual Playwright commands:

```js
async login(username, password) {
  await this.page.fill('#username', username);
  await this.page.fill('#password', password);
  await this.page.click('#loginButton');
}
```

So the **data from the `.feature` file** ("admin", "password123") flows like this:

```
.feature file (test inputs)
   ↓
.step.js (step definitions extract strings from Gherkin)
   ↓
pageObject.js (functions that interact with the browser using Playwright)
```

---

### **5. Summary of Test Flow**

```
Gherkin Test Case (.feature)
  ↓
Step Definitions (.steps.js)
  ↓
Page Object Methods (loginPage.js, etc.)
  ↓
Playwright Commands (fill, click, etc.)
```

### **Data Flow Example**

From `.feature`:

```gherkin
When I login with username "admin" and password "password123"
```

To `.steps.js`:

```js
When('I login with username {string} and password {string}', async (username, password) => {
  await loginPage.login(username, password);
});
```

To `loginPage.js`:

```js
async login(username, password) {
  await this.page.fill('#username', username);
  await this.page.fill('#password', password);
}
```

---

Let me know if you want me to trace a **specific test scenario**, or you want help running the project locally!
Great question, Lisa — this one trips up a lot of people new to BDD with Playwright!

Let’s clear this up:

---

### **What are `.spec.js` files doing in this setup?**

In a **BDD-style Playwright setup with Cucumber**, the test logic **usually lives in `.steps.js` files**, not `.spec.js`.

However, **if you’re seeing `.spec.js` files**, there are two possibilities:

#### 1. **Standard Playwright Tests (non-BDD)**:
In vanilla Playwright, tests are written in `.spec.js` (or `.spec.ts`) like:

```js
test('Login works', async ({ page }) => {
  await page.goto('https://site.com');
  await page.fill('#user', 'admin');
  await page.fill('#pass', 'password');
  await page.click('#login');
  await expect(page).toHaveURL('/dashboard');
});
```

These are **not connected to `.feature` files**. They are standalone functional tests.

#### 2. **Spec files calling feature files indirectly**:
Sometimes `.spec.js` files might:
- Import Cucumber setup
- Register steps
- Load feature files
But this is rare — in your repo, it looks like the main structure uses **`.feature` + `.steps.js`** — so `.spec.js` may just be **vanilla Playwright leftovers** or **used for custom flows outside of Gherkin**.

---

### **So how are `.spec.js` and `.feature` files connected?**

**They usually aren’t.** You typically choose one of two testing styles:

| Style | Uses `.feature`? | Uses `.spec.js`? | Step Logic Location |
|-------|------------------|------------------|----------------------|
| **BDD** (Cucumber) | ✅ Yes | ❌ Not needed | In `.steps.js` |
| **Standard Playwright** | ❌ No | ✅ Yes | Directly inside `.spec.js` |

---

### **How to tell what your project is using?**

In your [repo](https://github.com/TestRoverAutomation/Playwright-BDD-Automation):

- Tests are defined in `features/` (like `login.feature`)
- Steps are implemented in `tests/step_definitions/*.steps.js`
- That means this is a **pure BDD Playwright project** — and `.spec.js` files (if present) are probably:
  - Legacy
  - For non-BDD experiments
  - Or just misnamed

---

### Want to clean it up?

If you're going full BDD:
- Stick to `.feature` + `.steps.js`
- Delete unused `.spec.js` files

If you want to mix both BDD and vanilla, that’s possible too — just need to configure the test runner accordingly.

---

Let me know if you want to trace a `.spec.js` file you’re unsure about and I can walk through it with you!


For a **BDD-based web automation framework using Playwright**, the recommended file structure and configuration setup ensures scalability, maintainability, and easy integration with tools like **Cucumber** (or similar like `@cucumber/cucumber` for Node.js). Below is a comprehensive breakdown.

---

### **File Structure**
```
playwright-bdd-framework/
│
├── .env                          # Environment-specific variables
├── package.json                  # NPM dependencies and scripts
├── playwright.config.ts          # Playwright test configuration
│
├── configs/
│   └── test.config.ts            # Custom test-level config (URLs, timeouts)
│
├── features/                     # BDD feature files
│   ├── login.feature
│   └── search.feature
│
├── step-definitions/            # Step definitions corresponding to feature files
│   ├── login.steps.ts
│   └── search.steps.ts
│
├── support/
│   ├── hooks.ts                  # Before/After hooks
│   ├── world.ts                  # Custom World for scenario context
│   └── utils.ts                  # Common utility functions
│
├── pages/                        # Page Object Model files
│   ├── BasePage.ts
│   ├── LoginPage.ts
│   └── SearchPage.ts
│
├── reports/                      # Test execution reports
│
└── tsconfig.json                 # TypeScript configuration
```

---

### **Playwright Config (`playwright.config.ts`)**
```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30000,
  retries: 1,
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    baseURL: process.env.BASE_URL || 'https://yourapp.com',
  },
});
```

---

### **Custom Test Config (`configs/test.config.ts`)**
```ts
export const testConfig = {
  baseURL: process.env.BASE_URL || 'https://yourapp.com',
  timeout: 30000,
  user: {
    username: process.env.TEST_USER || 'test_user',
    password: process.env.TEST_PASS || 'password123',
  },
};
```

---

### **.env File**
```env
BASE_URL=https://yourapp.com
TEST_USER=test_user
TEST_PASS=password123
```

Load this via `dotenv`:
```ts
// e.g., in your hooks.ts
import dotenv from 'dotenv';
dotenv.config();
```

---

### **Cucumber Integration (using @cucumber/cucumber)**

Install dependencies:
```bash
npm install @cucumber/cucumber ts-node typescript dotenv --save-dev
```

Add to `package.json`:
```json
"scripts": {
  "test:bdd": "cucumber-js --require-module ts-node/register --require step-definitions/**/*.ts features/**/*.feature"
}
```

---

### **Hooks Example (`support/hooks.ts`)**
```ts
import { Before, After } from '@cucumber/cucumber';
import { Browser, chromium } from 'playwright';

let browser: Browser;

Before(async function () {
  browser = await chromium.launch();
  this.context = await browser.newContext();
  this.page = await this.context.newPage();
});

After(async function () {
  await this.page.close();
  await this.context.close();
  await browser.close();
});
```

---

### **World File (`support/world.ts`)**
```ts
import { setWorldConstructor, World } from '@cucumber/cucumber';
import { BrowserContext, Page } from 'playwright';

class CustomWorld extends World {
  page!: Page;
  context!: BrowserContext;
}

setWorldConstructor(CustomWorld);
```

---

### Let me know if you’d like a working repo scaffold or examples for login or search test cases.


The **Page Object Model (POM)** is a design pattern used in test automation to create an abstraction of the web pages or screens of your application. In **TypeScript-based automation frameworks** (like with **Playwright**, **Protractor**, or **WebdriverIO**), POM helps organize code and makes it **reusable, maintainable, and readable**.

---

### 🧠 **What is a Page Object Model (POM)?**

- A **Page Object** represents a **single screen/page** in your application.
- It contains:
  - **Locators** (selectors) for elements on the page.
  - **Methods** that perform actions on those elements (e.g., click a button, enter text).
- Test files call these page methods instead of interacting directly with the UI.

---

### 📱 Example: Payment Application with Multiple Screens

Let’s assume your payment app has these screens:
1. **LoginPage**
2. **DashboardPage**
3. **PaymentPage**
4. **TransactionSummaryPage**

You’ll create a separate `Page Object` class for each screen.

---

### ✅ Benefits for Testing Multiple Sites

If you’re testing **multiple sites** or **environments (e.g., staging, dev, prod)** with similar UI structure:
- You **reuse page objects** across sites by **parameterizing** base URLs or elements if selectors vary slightly.
- Maintain **one source of truth** for page logic.

---

### 📦 Example Project Structure

```
/tests
  login.test.ts
  payment.test.ts

/pages
  LoginPage.ts
  DashboardPage.ts
  PaymentPage.ts
  TransactionSummaryPage.ts

/utils
  config.ts
```

---

### 🔧 Sample Page Object (`PaymentPage.ts`)

```ts
// pages/PaymentPage.ts
import { Page } from '@playwright/test';

export class PaymentPage {
  constructor(private page: Page) {}

  amountInput = this.page.locator('#amount');
  payButton = this.page.locator('button#pay');

  async enterAmount(amount: string) {
    await this.amountInput.fill(amount);
  }

  async clickPay() {
    await this.payButton.click();
  }
}
```

---

### 🧪 Sample Test Using the Page Object

```ts
// tests/payment.test.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { PaymentPage } from '../pages/PaymentPage';

test('Make a payment', async ({ page }) => {
  const loginPage = new LoginPage(page);
  const paymentPage = new PaymentPage(page);

  await page.goto('https://staging.paymentapp.com');

  await loginPage.login('user@example.com', 'password123');
  await paymentPage.enterAmount('100');
  await paymentPage.clickPay();

  // Add assertion
  await expect(page.locator('text=Payment Successful')).toBeVisible();
});
```

---

### 🌐 Supporting Multiple Sites

Use a config file to switch URLs or element behavior per site.

```ts
// utils/config.ts
export const config = {
  baseUrl: process.env.SITE === 'prod'
    ? 'https://prod.paymentapp.com'
    : 'https://staging.paymentapp.com'
};
```

```ts
// test file
await page.goto(config.baseUrl);
```

---

### 🔁 Summary: How POM Helps You Reuse Across Sites

| Feature                        | Benefit                                             |
|-------------------------------|-----------------------------------------------------|
| Page Object Classes           | Reuse across all tests                              |
| Centralized Element Locators  | Update in one place if UI changes                   |
| Parameterized URLs & flows    | Easy testing across environments or site versions   |
| Cleaner Tests                 | Focus on logic, not UI details                      |

---

Would you like me to generate a full working Playwright POM example for this use case with a mock payment flow?gjk


Awesome! Here's a full working **Playwright + TypeScript** POM setup for a **Payment Application** with multiple screens.

---

### 📦 Folder Structure

```
/payment-app-playwright
├── /pages
│   ├── LoginPage.ts
│   ├── DashboardPage.ts
│   ├── PaymentPage.ts
│   └── SummaryPage.ts
├── /tests
│   └── paymentFlow.test.ts
├── /utils
│   └── config.ts
├── playwright.config.ts
└── package.json
```

---

### 🔧 `playwright.config.ts`

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  use: {
    baseURL: process.env.BASE_URL || 'https://staging.paymentapp.com',
    headless: true,
    viewport: { width: 1280, height: 720 },
  },
});
```

---

### 📄 `/utils/config.ts`

```ts
export const users = {
  validUser: {
    email: 'user@example.com',
    password: 'password123',
  }
};
```

---

### 📄 `/pages/LoginPage.ts`

```ts
import { Page } from '@playwright/test';

export class LoginPage {
  constructor(private page: Page) {}

  emailInput = this.page.locator('#email');
  passwordInput = this.page.locator('#password');
  loginButton = this.page.locator('#login');

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }
}
```

---

### 📄 `/pages/DashboardPage.ts`

```ts
import { Page } from '@playwright/test';

export class DashboardPage {
  constructor(private page: Page) {}

  paymentLink = this.page.locator('a[href="/payment"]');

  async navigateToPayment() {
    await this.paymentLink.click();
  }
}
```

---

### 📄 `/pages/PaymentPage.ts`

```ts
import { Page } from '@playwright/test';

export class PaymentPage {
  constructor(private page: Page) {}

  amountInput = this.page.locator('#amount');
  recipientSelect = this.page.locator('#recipient');
  payButton = this.page.locator('#pay');

  async makePayment(amount: string, recipient: string) {
    await this.amountInput.fill(amount);
    await this.recipientSelect.selectOption({ label: recipient });
    await this.payButton.click();
  }
}
```

---

### 📄 `/pages/SummaryPage.ts`

```ts
import { Page, expect } from '@playwright/test';

export class SummaryPage {
  constructor(private page: Page) {}

  confirmationMessage = this.page.locator('#confirmation');

  async verifySuccess() {
    await expect(this.confirmationMessage).toHaveText('Payment Successful');
  }
}
```

---

### 🧪 `/tests/paymentFlow.test.ts`

```ts
import { test } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';
import { PaymentPage } from '../pages/PaymentPage';
import { SummaryPage } from '../pages/SummaryPage';
import { users } from '../utils/config';

test('User can make a successful payment', async ({ page }) => {
  const loginPage = new LoginPage(page);
  const dashboardPage = new DashboardPage(page);
  const paymentPage = new PaymentPage(page);
  const summaryPage = new SummaryPage(page);

  await page.goto('/');
  await loginPage.login(users.validUser.email, users.validUser.password);
  await dashboardPage.navigateToPayment();
  await paymentPage.makePayment('150', 'John Doe');
  await summaryPage.verifySuccess();
});
```

---

### ✅ Running the Test

1. Install dependencies:

```bash
npm install -D @playwright/test
npx playwright install
```

2. Set a custom base URL (optional):

```bash
BASE_URL=https://production.paymentapp.com npx playwright test
```

3. Run tests:

```bash
npx playwright test
```

---

Want me to include Docker, CI config, or mock this as a dummy app with Playwright Test Generator too?




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


Great question, Lisa!

If you're using **Playwright with TypeScript**, it comes **built-in** with test reporting capabilities — and it's super simple to generate rich, interactive reports.

---

## 📊 How to Generate a Test Report in Playwright (TypeScript)

### ✅ Step 1: Use the Built-in HTML Reporter

The HTML reporter is already included with Playwright. You just need to configure it and run the tests.

#### 🔧 `playwright.config.ts`

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  reporter: [['html', { open: 'never' }]], // or 'on', 'always'
});
```

Options for `open`:
- `'on'`: open report if there are failures
- `'never'`: never open automatically
- `'always'`: always open after tests

---

### ✅ Step 2: Run Tests and Generate Report

```bash
npx playwright test
```

This runs the tests and saves the report in:

```
./playwright-report/
```

---

### ✅ Step 3: View the Report

```bash
npx playwright show-report
```

This opens an interactive HTML report in your default browser with:
- Pass/fail status
- Duration of each test
- Trace view (if enabled)
- Screenshots (if configured)

---

## 💡 Optional: Add Screenshots & Traces to Your Report

Update your config to enable them:

```ts
use: {
  screenshot: 'only-on-failure',
  trace: 'on-first-retry',
}
```

---

## 🧪 Sample Report View

The report looks like a dashboard:
- ✅ Passed tests in green
- ❌ Failed tests in red
- 📍 Click to expand and see logs, screenshots, traces

---

## 🛠️ Other Reporters (if needed)

You can use multiple reporters:

```ts
reporter: [
  ['list'],
  ['html', { outputFolder: 'playwright-report', open: 'never' }],
  ['json', { outputFile: 'report.json' }],
  ['junit', { outputFile: 'results.xml' }]
]
```

---

## 📁 Java: Test Reports (Just FYI)

In Java (e.g., using TestNG, JUnit, Selenium):
- Use **Allure**, **ExtentReports**, or **Surefire** for reporting.
- But for TypeScript, **Playwright HTML Reporter** is the most native and simplest.

---

Would you like me to include:
- Screenshots and traces in the report config?
- A script in `package.json` to auto-generate and open reports?

Let me know!


Great! If you want to integrate **BDD (Behavior-Driven Development)** style with your **Playwright + TypeScript** tests, you can use a library called **`@cucumber/cucumber`** with Playwright.

This will let you write `.feature` files using **Gherkin syntax** (`Given`, `When`, `Then`), and implement step definitions using **TypeScript**. You can still use the Page Object Model (POM) structure for logic reusability.

---

## ✅ 1. Install Required Packages

```bash
npm install -D @cucumber/cucumber typescript ts-node playwright
```

---

## 🧱 2. Project Structure (With BDD)

```
/payment-app-bdd
├── /features
│   └── makePayment.feature
├── /step-definitions
│   └── paymentSteps.ts
├── /pages
│   └── PaymentPage.ts
├── cucumber.js
├── tsconfig.json
└── package.json
```

---

## ✍️ 3. Example Feature File (`features/makePayment.feature`)

```gherkin
Feature: Payment Flow

  Scenario: Make a successful payment
    Given the user is on the login page
    When the user logs in with valid credentials
    And navigates to the payment page
    And submits a payment of "100" to "John Doe"
    Then the payment should be successful
```

---

## 🧾 4. Step Definitions (`step-definitions/paymentSteps.ts`)

```ts
import { Given, When, Then, setDefaultTimeout } from '@cucumber/cucumber';
import { chromium, Browser, Page, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';
import { PaymentPage } from '../pages/PaymentPage';
import { SummaryPage } from '../pages/SummaryPage';

let browser: Browser;
let page: Page;
let loginPage: LoginPage;
let dashboardPage: DashboardPage;
let paymentPage: PaymentPage;
let summaryPage: SummaryPage;

setDefaultTimeout(60 * 1000);

Given('the user is on the login page', async () => {
  browser = await chromium.launch();
  page = await browser.newPage();
  await page.goto('https://staging.paymentapp.com');

  loginPage = new LoginPage(page);
  dashboardPage = new DashboardPage(page);
  paymentPage = new PaymentPage(page);
  summaryPage = new SummaryPage(page);
});

When('the user logs in with valid credentials', async () => {
  await loginPage.login('user@example.com', 'password123');
});

When('navigates to the payment page', async () => {
  await dashboardPage.navigateToPayment();
});

When('submits a payment of {string} to {string}', async (amount: string, recipient: string) => {
  await paymentPage.makePayment(amount, recipient);
});

Then('the payment should be successful', async () => {
  await summaryPage.verifySuccess();
  await browser.close();
});
```

---

## ⚙️ 5. Cucumber Config (`cucumber.js`)

```js
module.exports = {
  default: {
    require: ['step-definitions/**/*.ts'],
    requireModule: ['ts-node/register'],
    format: ['html:cucumber-report.html'],
    paths: ['features/**/*.feature'],
    publishQuiet: true
  }
};
```

---

## 🧪 6. Run the Test

```bash
npx cucumber-js
```

This runs the `.feature` file using your Playwright-based step definitions and generates an HTML report (`cucumber-report.html`).

---

## 💡 Tips

- You can still use the **Page Object Model** to keep your step definitions clean.
- Cucumber steps can reuse page classes across scenarios.
- Combine with Playwright Traces/Screenshots for rich reporting.

---

Would you like me to generate a working GitHub repo structure with all boilerplate files so you can clone and run directly?

