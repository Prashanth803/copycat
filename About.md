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
