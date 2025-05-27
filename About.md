Sure, Lisa! Here's how you can refactor the Java method into a **JUnit test** that uses **`assertTrue()`**, **`assertFalse()`**, and **`assertEquals()`** instead of `System.out.println`.

We'll use **JUnit 5** for the testing framework, but if you're using JUnit 4, I can provide that version too.

---

### ✅ **Maven Dependency for JUnit 5** (if not already added)

```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.10.0</version>
    <scope>test</scope>
</dependency>
```

---

### ✅ **Java Test Class with Assertions**

```java
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class VirtualCardResponseTest {

    private boolean hasValidVirtualCardStructure(JsonNode root) {
        if (!root.has("virtualCard")) return false;

        JsonNode card = root.get("virtualCard");

        String[] requiredKeys = {
            "cardNumber", "expirationDate", "securityCode", "status", "createdDatetime"
        };

        for (String key : requiredKeys) {
            if (!card.has(key)) return false;
        }

        return "Approved".equals(card.get("status").asText());
    }

    @Test
    public void testValidVirtualCardResponse() throws Exception {
        String json = """
        {
            "virtualCard": {
                "cardNumber": "4159285815450059",
                "expirationDate": "2025-06-10",
                "securityCode": "500",
                "status": "Approved",
                "createdDatetime": "2025-05-26T04:52:48"
            }
        }
        """;

        ObjectMapper mapper = new ObjectMapper();
        JsonNode root = mapper.readTree(json);

        assertTrue(root.has("virtualCard"), "Missing 'virtualCard' key");

        JsonNode card = root.get("virtualCard");

        assertAll("Verify required fields exist",
            () -> assertTrue(card.has("cardNumber"), "Missing 'cardNumber'"),
            () -> assertTrue(card.has("expirationDate"), "Missing 'expirationDate'"),
            () -> assertTrue(card.has("securityCode"), "Missing 'securityCode'"),
            () -> assertTrue(card.has("status"), "Missing 'status'"),
            () -> assertTrue(card.has("createdDatetime"), "Missing 'createdDatetime'")
        );

        assertEquals("Approved", card.get("status").asText(), "Status is not 'Approved'");
    }

    @Test
    public void testInvalidStatus() throws Exception {
        String json = """
        {
            "virtualCard": {
                "cardNumber": "4159285815450059",
                "expirationDate": "2025-06-10",
                "securityCode": "500",
                "status": "Declined",
                "createdDatetime": "2025-05-26T04:52:48"
            }
        }
        """;

        ObjectMapper mapper = new ObjectMapper();
        JsonNode root = mapper.readTree(json);
        JsonNode card = root.get("virtualCard");

        assertNotEquals("Approved", card.get("status").asText(), "Status should not be 'Approved'");
    }

    @Test
    public void testMissingVirtualCardKey() throws Exception {
        String json = """
        {
            "cardNumber": "4159285815450059"
        }
        """;

        ObjectMapper mapper = new ObjectMapper();
        JsonNode root = mapper.readTree(json);

        assertFalse(root.has("virtualCard"), "Should not contain 'virtualCard'");
    }
}
```

---

### 🧪 Summary of What This Covers:

| Test Method                    | What it Verifies                                           |
| ------------------------------ | ---------------------------------------------------------- |
| `testValidVirtualCardResponse` | Full valid structure with all keys and `status = Approved` |
| `testInvalidStatus`            | The `status` is **not** Approved                           |
| `testMissingVirtualCardKey`    | Response does **not** contain `virtualCard` key            |

---

Let me know if you want:

* To integrate it with **RestAssured** API test
* JUnit 4 version
* Add regex/date format checks to the test
