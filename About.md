Thanks for the clarification! You're running a **single test suite**, want to:

* ✅ Run everything with **only one worker** (to avoid session invalidation).
* ✅ Automatically **close any unexpected session error popup**.
* ✅ Keep the **watcher running in the background** across the test suite.

---

## ✅ Your Goal

You don’t want to **create a separate test just to watch popups**, but rather want every test in your suite to have this **background protection** without adding extra test files.

---

## ✅ Here's Exactly What You Should Do

### ✅ Step 1: Configure Playwright to Use **1 Worker**

Edit your `playwright.config.ts`:

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests', // your test folder
  workers: 1,         // 🚨 run all tests serially
  use: {
    headless: true,
  },
});
```

---

### ✅ Step 2: Create a **Global Setup Hook** to Watch for Popups

This runs the popup watcher inside each test without creating a separate test.

---

### 🔧 Option A (Simplest): Add `test.beforeEach()` in a Common `setup.ts` File

Create a file: `tests/setup.ts`

```ts
// tests/setup.ts
import { test as base } from '@playwright/test';

base.beforeEach(async ({ page }) => {
  // 👀 Watch and close unexpected error popups in the background
  const watchForPopup = async () => {
    while (true) {
      try {
        const popup = page.locator('.session-error'); // update selector!
        if (await popup.isVisible({ timeout: 1000 })) {
          console.warn('⚠️ Closing unexpected session popup...');
          await page.locator('.session-error button.close').click();
        }
      } catch (e) {
        // silent fail
      }
      await new Promise(res => setTimeout(res, 500)); // poll every 0.5s
    }
  };

  watchForPopup(); // run in background
});
```

---

### ✅ Step 3: Import This `setup.ts` at the Top of Each Test File

```ts
// tests/my-flow.spec.ts
import './setup'; // 👈 this pulls in the popup handler
import { test, expect } from '@playwright/test';

test('long flow', async ({ page }) => {
  await page.goto('https://your-app.com');
  await page.fill('#username', 'user');
  await page.fill('#password', 'pass');
  await page.click('#login');

  // 🧪 continue flow
  await page.click('#next');
  await expect(page.locator('#dashboard')).toBeVisible();
});
```

✅ Now, **every test that imports `./setup`** will have a background process silently checking for the error popup and closing it, without stopping the test.

---

### 🧪 You Can Reuse `setup.ts` in Multiple Test Files

* It doesn't add extra tests.
* It doesn't block the worker.
* It works with **one worker** and supports **long flows**.

---

### ✅ Summary

| Step | What to Do                                          |
| ---- | --------------------------------------------------- |
| 1    | Set `workers: 1` in `playwright.config.ts`          |
| 2    | Create `setup.ts` with the background popup handler |
| 3    | `import './setup'` at the top of each test file     |

---

Let me know if you want to auto-load the setup file into **all tests** without needing to import it manually (e.g., by using custom test fixtures).






Great question! In Playwright, instead of repeating the UI login steps in every test, you can **log in once**, **save the authentication state**, and **reuse it in all tests** by configuring your `playwright.config.ts` and tests accordingly.

Here’s a step-by-step explanation on **how to do that using global setup and `storageState`**:

---

## ✅ 1. **Create a global login script**

This script logs in **once** and saves the storage (cookies + localStorage) into a file.

📄 **`global-setup.ts`**

```ts
import { chromium, FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig) {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Replace with your actual login steps
  await page.goto('https://your-app.com/login');
  await page.fill('#username', 'your-username');
  await page.fill('#password', 'your-password');
  await page.click('button[type="submit"]');

  // Wait until you're logged in and dashboard is visible
  await page.waitForURL('**/dashboard');

  // Save authentication state to file
  await page.context().storageState({ path: 'auth.json' });

  await browser.close();
}

export default globalSetup;
```

---

## ✅ 2. **Update `playwright.config.ts` to use global setup**

📄 **`playwright.config.ts`**

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  globalSetup: './global-setup',
  use: {
    baseURL: 'https://your-app.com',
    storageState: 'auth.json', // load this in every test
    headless: true,
  },
});
```

---

## ✅ 3. **In your tests, start from the authenticated state**

Now, your test automatically starts with the user already logged in.

📄 **`dashboard.spec.ts`**

```ts
import { test, expect } from '@playwright/test';

test('should display user dashboard', async ({ page }) => {
  await page.goto('/dashboard'); // user is already logged in

  await expect(page.locator('h1')).toHaveText('Welcome back');
});
```

---

## ✅ Optional: Test Login Flow Separately

You can keep one dedicated test for validating the login flow using the actual UI interaction.

---

## ✅ Summary

| ✅ Advantage | 💬 Description                                                          |
| ----------- | ----------------------------------------------------------------------- |
| Speed       | Skips repeated login steps, especially for suites with dozens of tests. |
| Isolation   | All tests start from a known, clean, logged-in state.                   |
| Stability   | Reduces flakiness caused by login page UI issues.                       |

---

Would you like me to provide a boilerplate folder structure with this setup?
