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
