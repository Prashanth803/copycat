Good catch! The infinite loop issue is likely due to the remaining amount being **too small** to generate a valid `invoiceAmount > 0.01`, especially in the later iterations.

### Here’s a **more robust alternative approach**:
Instead of using a `do-while` loop to generate valid invoice amounts, we'll **pre-calculate a safe minimum amount for each invoice** and distribute the total accordingly.

### Updated Approach:

```java
public List<Map<String, Object>> paymentInfo(int invoice, double amount) {
    List<Map<String, Object>> paymentList = new ArrayList<>();
    SecureRandom random = new SecureRandom();

    double remainingAmount = amount;
    int numberOfPayments = (invoice == 0) ? 1 + random.nextInt(5) : invoice;

    // Ensure minimum value of 0.01 for each invoice
    double minPerInvoice = 0.01;
    if (amount < minPerInvoice * numberOfPayments) {
        throw new IllegalArgumentException("Amount too low to divide among payments.");
    }

    // Generate random weight factors to proportionally split the amount
    double[] weights = new double[numberOfPayments];
    double weightSum = 0;
    for (int i = 0; i < numberOfPayments; i++) {
        weights[i] = 1 + random.nextDouble(); // at least 1 to prevent zero division
        weightSum += weights[i];
    }

    for (int i = 0; i < numberOfPayments; i++) {
        Map<String, Object> payment = new HashMap<>();

        String facilityName = "fcl" + (random.nextInt(900) + 100);
        String invoiceNumber = String.valueOf(random.nextInt(10000));
        String purchaseOrderNumber = "po" + (random.nextInt(1000));
        String description = "desc" + random.nextInt(100);

        double invoiceAmount;
        if (i == numberOfPayments - 1) {
            // Last one gets the remaining
            invoiceAmount = Math.round(remainingAmount * 100.0) / 100.0;
        } else {
            invoiceAmount = Math.round((weights[i] / weightSum * amount) * 100.0) / 100.0;
            remainingAmount -= invoiceAmount;
        }

        // Ensure amount is at least 0.01
        if (invoiceAmount < minPerInvoice) invoiceAmount = minPerInvoice;

        payment.put("facilityName", facilityName);
        payment.put("invoiceNumber", invoiceNumber);
        payment.put("purchaseOrderNumber", purchaseOrderNumber);
        payment.put("invoiceAmount", invoiceAmount);
        payment.put("discountAmount", 0);
        payment.put("description", description);

        paymentList.add(payment);
    }

    return paymentList;
}
```

### Key Improvements:
- No infinite loop.
- Uses **random weights** to split the amount.
- Ensures **each invoice amount is above 0.01**.
- Last item receives the remainder to ensure total sum consistency.

Let me know if you'd like the output to always total exactly the given amount (e.g., rounded total adjustment logic).





Absolutely! Let’s break down what you want:

### 📝 Requirements Recap:
- A **global `totalAmount`** needs to be split across a **random number of payments (between 1 and 5)**.
- Each **payment map** should include:
  - Random `facilityName`, `invoiceNumber`, `purchaseOrderNumber`, and `description`
  - A portion of the `invoiceAmount` (which together sums up to the `totalAmount`)
  - `discountAmount` can be `0` (or randomized too if you want)
- All maps are added under the `"paymentInformation"` key inside a main map.

---

### ✅ Here's the complete Java implementation:

```java
import java.util.*;
import java.security.SecureRandom;

public class RandomPaymentGenerator {
    private static final SecureRandom random = new SecureRandom();

    public static Map<String, List<Map<String, Object>>> generatePaymentInfo(double totalAmount) {
        int numberOfPayments = 1 + random.nextInt(5); // 1 to 5
        List<Map<String, Object>> paymentList = new ArrayList<>();

        // Distribute totalAmount randomly but fairly
        double remainingAmount = totalAmount;

        for (int i = 0; i < numberOfPayments; i++) {
            Map<String, Object> payment = new HashMap<>();

            // Randomly generate fields
            String facilityName = "fcl" + (random.nextInt(900) + 100); // fcl100 - fcl999
            String invoiceNumber = String.valueOf(random.nextInt(10000)); // 0 - 9999
            String purchaseOrderNumber = "po" + (random.nextInt(1000)); // po0 - po999
            String description = "desc" + random.nextInt(100);

            // Last payment takes the remaining to avoid rounding issues
            double invoiceAmount;
            if (i == numberOfPayments - 1) {
                invoiceAmount = Math.round(remainingAmount * 100.0) / 100.0;
            } else {
                invoiceAmount = Math.round((random.nextDouble() * (remainingAmount / 2)) * 100.0) / 100.0;
                remainingAmount -= invoiceAmount;
            }

            payment.put("facilityName", facilityName);
            payment.put("invoiceNumber", invoiceNumber);
            payment.put("purchaseOrderNumber", purchaseOrderNumber);
            payment.put("invoiceAmount", invoiceAmount);
            payment.put("discountAmount", 0);
            payment.put("description", description);

            paymentList.add(payment);
        }

        Map<String, List<Map<String, Object>>> paymentInfoWrapper = new HashMap<>();
        paymentInfoWrapper.put("paymentInformation", paymentList);

        return paymentInfoWrapper;
    }

    public static void main(String[] args) {
        double globalAmount = 100.00;
        Map<String, List<Map<String, Object>>> result = generatePaymentInfo(globalAmount);

        // Pretty-print result
        for (Map<String, Object> entry : result.get("paymentInformation")) {
            System.out.println(entry);
        }

        // Optional: check total distributed
        double total = result.get("paymentInformation").stream()
                .mapToDouble(p -> (double) p.get("invoiceAmount"))
                .sum();
        System.out.println("Total distributed: " + total);
    }
}
```

---

### 🧪 Example Output:
```java
{facilityName=fcl934, invoiceNumber=3821, purchaseOrderNumber=po567, invoiceAmount=34.12, discountAmount=0, description=desc55}
{facilityName=fcl108, invoiceNumber=8120, purchaseOrderNumber=po75, invoiceAmount=21.77, discountAmount=0, description=desc10}
{facilityName=fcl721, invoiceNumber=4261, purchaseOrderNumber=po200, invoiceAmount=44.11, discountAmount=0, description=desc77}
Total distributed: 100.0
```

---

Would you like to:
- Include random `discountAmount`s too?
- Serialize this to JSON for API use?
- Save it to a file or database?

Happy to build on it!
