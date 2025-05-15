Perfect — here’s a full Java + Playwright setup, including test suite creation and test report integration using JUnit and Allure.


---

1. Maven Setup

Add these dependencies to your pom.xml:

<dependencies>
  <!-- Playwright for Java -->
  <dependency>
    <groupId>com.microsoft.playwright</groupId>
    <artifactId>playwright</artifactId>
    <version>1.43.0</version>
  </dependency>

  <!-- JUnit Jupiter -->
  <dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.10.0</version>
    <scope>test</scope>
  </dependency>

  <!-- Allure for reporting -->
  <dependency>
    <groupId>io.qameta.allure</groupId>
    <artifactId>allure-junit5</artifactId>
    <version>2.24.0</version>
    <scope>test</scope>
  </dependency>
</dependencies>

<build>
  <plugins>
    <!-- Surefire plugin to run tests -->
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-surefire-plugin</artifactId>
      <version>3.1.2</version>
    </plugin>

    <!-- Allure report plugin -->
    <plugin>
      <groupId>io.qameta.allure</groupId>
      <artifactId>allure-maven</artifactId>
      <version>2.11.2</version>
    </plugin>
  </plugins>
</build>


---

2. Playwright Test Example (JUnit5)

Create src/test/java/tests/LoginTest.java:

package tests;

import com.microsoft.playwright.*;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class LoginTest {
  static Playwright playwright;
  static Browser browser;
  static Page page;

  @BeforeAll
  static void setup() {
    playwright = Playwright.create();
    browser = playwright.chromium().launch(new BrowserType.LaunchOptions().setHeadless(true));
    page = browser.newPage();
  }

  @Test
  @Order(1)
  public void testLoginPage() {
    page.navigate("http://localhost:8080/login");
    assertTrue(page.title().contains("Login"));
  }

  @Test
  @Order(2)
  public void testLoginSuccess() {
    page.navigate("http://localhost:8080/login");
    page.fill("#username", "admin");
    page.fill("#password", "admin");
    page.click("button[type='submit']");
    assertTrue(page.url().contains("dashboard"));
  }

  @AfterAll
  static void teardown() {
    browser.close();
    playwright.close();
  }
}


---

3. Test Suite

Create a test suite AllTestsSuite.java:

package tests;

import org.junit.platform.suite.api.SelectPackages;
import org.junit.platform.suite.api.Suite;

@Suite
@SelectPackages("tests") // runs all test classes in this package
public class AllTestsSuite {}

Run it via Maven:

mvn test


---

4. Allure Reporting Integration

Step-by-step:

1. Run tests to generate results:



mvn clean test

2. Serve Allure report:



allure serve target/allure-results

If you don’t have Allure installed:

npm install -g allure-commandline --save-dev

Or use the Allure CLI installer.


---

Summary

Would you like a GitHub project template or help setting up headless testing in CI?





Great catch! The issue arises due to **floating point rounding** and potentially the way the last few payments get very small amounts. To ensure every generated payment amount is **non-zero** and accurately sums to the total, here are improvements:

1. **Calculate raw values first**, then round only at the end.
2. Ensure the smallest chunk doesn't go below 0.01.

Here’s the updated class:

```js
class PaymentGenerator {
  constructor(amount) {
    this.amount = amount;
  }

  generatePayments(invoice) {
    const paymentList = [];
    const numberOfPayments = invoice === 0 ? 1 + Math.floor(Math.random() * 5) : 150;

    let weights = [];
    let weightSum = 0;

    for (let i = 0; i < numberOfPayments; i++) {
      const weight = 1 + Math.random(); // ensures at least some weight
      weights.push(weight);
      weightSum += weight;
    }

    let remaining = this.amount;

    for (let i = 0; i < numberOfPayments; i++) {
      const payment = {};

      payment.facilityName = `fcl${Math.floor(100 + Math.random() * 900)}`;
      payment.invoiceNumber = `${Math.floor(Math.random() * 20)}`;
      payment.purchaseOrderNumber = `po${Math.floor(Math.random() * 1000)}`;
      payment.description = `desc${Math.floor(Math.random() * 100)}`;

      let rawAmount;

      if (i === numberOfPayments - 1) {
        // Last payment gets whatever is left
        rawAmount = remaining;
      } else {
        rawAmount = (weights[i] / weightSum) * this.amount;
        rawAmount = Math.max(rawAmount, 0.01); // prevent zero
        rawAmount = Math.min(rawAmount, remaining); // don't overdraw
      }

      const invoiceAmount = Math.round(rawAmount * 100) / 100;
      remaining = Math.round((remaining - invoiceAmount) * 100) / 100;

      payment.amount = invoiceAmount;
      paymentList.push(payment);
    }

    return paymentList;
  }
}
```

### Notes:
- Every payment will now be at least **0.01**.
- The final payment ensures **total = this.amount** (subject to small rounding loss).
- If you want to **guarantee total match** to cents, we can adjust the last amount to cover the rounding gap precisely.

Let me know if you'd like that version too!


Here’s the **Java-to-JavaScript** conversion of your `paymentInfo(int invoice)` method. It simulates payment splits using weighted random distribution, mimicking `SecureRandom`, `List<Map<String, Object>>`, and rounding to two decimal places:

---

### ✅ JavaScript Version

```js
class PaymentGenerator {
  constructor(amount) {
    this.amount = amount;
  }

  getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  getRandomDouble(min, max) {
    return Math.random() * (max - min) + min;
  }

  roundToTwo(value) {
    return Math.round(value * 100) / 100;
  }

  paymentInfo(invoice) {
    const paymentList = [];
    let remainingAmount = this.amount;
    const numberOfPayments = invoice === 0 ? this.getRandomInt(1, 5) : 150;

    // Generate weights
    const weights = Array.from({ length: numberOfPayments }, () => 1 + Math.random());
    const weightSum = weights.reduce((acc, val) => acc + val, 0);

    for (let i = 0; i < numberOfPayments; i++) {
      const payment = {};

      const facilityName = "fcl" + this.getRandomInt(100, 999);
      const invoiceNumber = this.getRandomInt(0, 19).toString();
      const purchaseOrderNumber = "po" + this.getRandomInt(0, 999);
      const description = "desc" + this.getRandomInt(0, 99);

      let invoiceAmount;

      if (i === numberOfPayments - 1) {
        invoiceAmount = this.roundToTwo(remainingAmount);
      } else {
        invoiceAmount = this.roundToTwo((weights[i] / weightSum) * this.amount);
        remainingAmount -= invoiceAmount;
      }

      payment.facilityName = facilityName;
      payment.invoiceNumber = invoiceNumber;
      payment.purchaseOrderNumber = purchaseOrderNumber;
      payment.description = description;
      payment.invoiceAmount = invoiceAmount;

      paymentList.push(payment);
    }

    return paymentList;
  }
}
```

---

### ✅ Usage Example:

```js
const generator = new PaymentGenerator(1000.0); // amount
const payments = generator.paymentInfo(0); // Pass 0 or any number

console.log(payments);
```

Let me know if you want to include dates like `addedDate`, or return the result as JSON!
