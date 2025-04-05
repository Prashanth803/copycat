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
