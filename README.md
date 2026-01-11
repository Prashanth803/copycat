
Below is a clean, realistic JUnit 5 + Mockito test case that forces the catch block of your parseFile(...) method to execute and verifies that a RemittanceParserException is thrown.

I’ll show two approaches.
👉 Approach 1 (Recommended): Force an IOException by giving an invalid file path
👉 Approach 2: Mock an internal dependency to throw BatchProcessingException


---

✅ Assumptions (based on your code)

You are using JUnit 5

You are using Mockito

parseFile(...) is in a service class like RemittanceFileParser

remittanceFileService is fetched from Spring ApplicationContext

You cannot modify the production code



---

✅ Imports (common)

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.io.IOException;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.context.ApplicationContext;


---

✅ APPROACH 1 – Force IOException (Simplest & Most Reliable)

This covers the catch (IOException | BatchProcessingException) block.

✔ Why this works

Files.lines(path, …) throws an IOException if the file does not exist.


---

🔹 Test Case

@ExtendWith(MockitoExtension.class)
class RemittanceFileParserTest {

    @InjectMocks
    private RemittanceFileParser parser; // class containing parseFile()

    @Mock
    private ApplicationContext applicationContext;

    @Mock
    private IRemittanceFileService remittanceFileService;

    @Test
    void parseFile_shouldThrowRemittanceParserException_whenIOExceptionOccurs() {

        // Arrange
        when(applicationContext.getBean("remittanceFileService"))
                .thenReturn(remittanceFileService);

        String invalidFilePath = "non/existing/path/file.txt";

        // Act & Assert
        RemittanceParserException exception =
                assertThrows(RemittanceParserException.class, () ->
                        parser.parseFile(applicationContext, invalidFilePath)
                );

        // Optional validation
        assertNotNull(exception.getErrors());
        assertFalse(exception.getErrors().isEmpty());
    }
}

✔ This guarantees the catch block is executed
✔ No mocking of static Files.lines() needed
✔ Sonar + coverage tools accept this approach


---

✅ APPROACH 2 – Force BatchProcessingException (Mock Dependency)

If you specifically want to trigger the second exception type:


---

🔹 Test Case

@Test
void parseFile_shouldThrowRemittanceParserException_whenBatchProcessingExceptionOccurs() {

    // Arrange
    when(applicationContext.getBean("remittanceFileService"))
            .thenReturn(remittanceFileService);

    when(remittanceFileService.getDetailId())
            .thenThrow(new BatchProcessingException("Test exception"));

    // Create a temporary valid file to avoid IOException
    Path tempFile = Files.createTempFile("test", ".txt");

    // Act & Assert
    RemittanceParserException exception =
            assertThrows(RemittanceParserException.class, () ->
                    parser.parseFile(applicationContext, tempFile.toString())
            );

    assertNotNull(exception.getErrors());
}

✔ Covers BatchProcessingException path
✔ Ensures the catch block logic is executed


---

✅ What This Test Covers

✔ catch (IOException | BatchProcessingException)
✔ Logger.error(...)
✔ errors.add(new ParseError(...))
✔ throw new RemittanceParserException(errors);


---

✅ Best Practice (Sonar-friendly)

Use Approach 1 for basic coverage

Use Approach 2 if Sonar demands explicit coverage of BatchProcessingException



---

If you want, I can also:

Add assertions on ParseError values

Mock Logger verification

Write a 100% coverage test suite for this class

Help suppress Sonar false positives


Just tell me 👍

✅ **Example (`application.yml`):**
```yaml
app:
  name: MyApp
  version: 1.0
  database:
    url: jdbc:mysql://localhost:3306/mydb
    username: root
    password: secret
```
✅ **Java Class:**
```java
@Data
@ConfigurationProperties(prefix = "app")
@Component
public class AppConfig {
    private String name;
    Below is a clean, realistic JUnit 5 + Mockito test case that forces the catch block of your parseFile(...) method to execute and verifies that a RemittanceParserException is thrown.

I’ll show two approaches.
👉 Approach 1 (Recommended): Force an IOException by giving an invalid file path
👉 Approach 2: Mock an internal dependency to throw BatchProcessingException


---

✅ Assumptions (based on your code)

You are using JUnit 5

You are using Mockito

parseFile(...) is in a service class like RemittanceFileParser

remittanceFileService is fetched from Spring ApplicationContext

You cannot modify the production code



---

✅ Imports (common)

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.io.IOException;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.context.ApplicationContext;


---

✅ APPROACH 1 – Force IOException (Simplest & Most Reliable)

This covers the catch (IOException | BatchProcessingException) block.

✔ Why this works

Files.lines(path, …) throws an IOException if the file does not exist.


---

🔹 Test Case

@ExtendWith(MockitoExtension.class)
class RemittanceFileParserTest {

    @InjectMocks
    private RemittanceFileParser parser; // class containing parseFile()

    @Mock
    private ApplicationContext applicationContext;

    @Mock
    private IRemittanceFileService remittanceFileService;

    @Test
    void parseFile_shouldThrowRemittanceParserException_whenIOExceptionOccurs() {

        // Arrange
        when(applicationContext.getBean("remittanceFileService"))
                .thenReturn(remittanceFileService);

        String invalidFilePath = "non/existing/path/file.txt";

        // Act & Assert
        RemittanceParserException exception =
                assertThrows(RemittanceParserException.class, () ->
                        parser.parseFile(applicationContext, invalidFilePath)
                );

        // Optional validation
        assertNotNull(exception.getErrors());
        assertFalse(exception.getErrors().isEmpty());
    }
}

✔ This guarantees the catch block is executed
✔ No mocking of static Files.lines() needed
✔ Sonar + coverage tools accept this approach


---

✅ APPROACH 2 – Force BatchProcessingException (Mock Dependency)

If you specifically want to trigger the second exception type:


---

🔹 Test Case

@Test
void parseFile_shouldThrowRemittanceParserException_whenBatchProcessingExceptionOccurs() {

    // Arrange
    when(applicationContext.getBean("remittanceFileService"))
            .thenReturn(remittanceFileService);

    when(remittanceFileService.getDetailId())
            .thenThrow(new BatchProcessingException("Test exception"));

    // Create a temporary valid file to avoid IOException
    Path tempFile = Files.createTempFile("test", ".txt");

    // Act & Assert
    RemittanceParserException exception =
            assertThrows(RemittanceParserException.class, () ->
                    parser.parseFile(applicationContext, tempFile.toString())
            );

    assertNotNull(exception.getErrors());
}

✔ Covers BatchProcessingException path
✔ Ensures the catch block logic is executed


---

✅ What This Test Covers

✔ catch (IOException | BatchProcessingException)
✔ Logger.error(...)
✔ errors.add(new ParseError(...))
✔ throw new RemittanceParserException(errors);


---

✅ Best Practice (Sonar-friendly)

Use Approach 1 for basic coverage

Use Approach 2 if Sonar demands explicit coverage of BatchProcessingException



---

If you want, I can also:

Add assertions on ParseError values

Mock Logger verification

Write a 100% coverage test suite for this class

Help suppress Sonar false positives


Just tell me  String version;

    @NestedConfigurationProperty
    private DatabaseConfig database;
}

@Data
public class DatabaseConfig {
    private String url;
    private String username;
    private String password;
}
```
📌 **Now, `DatabaseConfig` will be automatically injected into `AppConfig.database` without needing a separate prefix.**

---

### **🌟 Summary: When to Use Which?**
| Annotation                  | Purpose |
|-----------------------------|---------|
| `@Data`                     | Lombok annotation to auto-generate getters, setters, `toString()`, etc. |
| `@ConfigurationProperties`  | Maps external properties (`.yml` or `.properties`) to a POJO. |
| `@NestedConfigurationProperty` | Used inside `@ConfigurationProperties` classes to manage nested properties. |

🚀 **Use `@ConfigurationProperties` for mapping properties, `@NestedConfigurationProperty` for nested objects, and `@Data` for reducing boilerplate code!**


### **📌 When to Use `@Configuration`, `@Service`, `@Component`, and `@Qualifier` in Spring Boot?**  

These annotations are part of Spring's **Dependency Injection (DI)** mechanism and help manage beans in the Spring container.

---

## **1️⃣ `@Configuration`**  
Used when defining a **class that provides bean definitions**.  

🔹 **When to Use?**  
- When you need to create and configure beans manually.
- When using `@Bean` methods inside a class.

🔹 **Example:**
```java
@Configuration
public class AppConfig {

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```
🛠 **This is an alternative to XML-based configuration.**

---

## **2️⃣ `@Service`**  
Used to mark a **service class** that contains business logic.  

🔹 **When to Use?**  
- When writing **business logic** or **service layer** components.

🔹 **Example:**
```java
@Service
public class UserService {
    public String getUser() {
        return "Lisa";
    }
}
```
🛠 **This tells Spring that `UserService` is a service component.**

---

## **3️⃣ `@Component`**  
A generic annotation that marks a class as a **Spring-managed component**.

🔹 **When to Use?**  
- When no specific stereotype (`@Service`, `@Repository`, `@Controller`) fits.
- For general utility classes.

🔹 **Example:**
```java
@Component
public class UtilityClass {
    public String formatText(String text) {
        return text.toUpperCase();
    }
}
```
🛠 **Spring automatically scans and registers this as a bean.**

---

## **4️⃣ `@Qualifier`**  
Used to **resolve conflicts when multiple beans** of the same type exist.  

🔹 **When to Use?**  
- When **two or more beans of the same type** exist and you need to **specify which one to inject**.

🔹 **Example:**
```java
@Component("beanOne")
public class BeanOne {
    public String message() {
        return "Bean One";
    }
}

@Component("beanTwo")
public class BeanTwo {
    public String message() {
        return "Bean Two";
    }
}

@Service
public class ExampleService {
    private final BeanOne bean;

    @Autowired
    public ExampleService(@Qualifier("beanOne") BeanOne bean) {
        this.bean = bean;
    }
}
```
🛠 **This ensures `beanOne` is injected instead of `beanTwo`.**

---

### **🌟 Summary: When to Use Which?**
| Annotation       | Purpose |
|-----------------|---------|
| `@Configuration` | Define beans manually inside a configuration class. |
| `@Service` | Mark a service class containing business logic. |
| `@Component` | Generic annotation for any Spring-managed component. |
| `@Qualifier` | Specify which bean to inject when multiple exist. |

🚀 **Use `@Configuration` for defining beans, `@Service` for business logic, `@Component` for general beans, and `@Qualifier` to resolve conflicts in DI.**




### **🛠 Understanding `HttpEntity` in Spring Boot**  

`HttpEntity<T>` in Spring Boot represents an HTTP request or response, including **headers and body**. It's useful when you need to send **custom headers** along with the request.  

---

## **📌 Key Components of `HttpEntity`**
- **Headers**: Meta-information like Content-Type, Authorization, etc.
- **Body**: The actual data being sent.

`HttpEntity<T>` is typically used with `RestTemplate` but can also be used in `WebClient`.

---

## **🔹 Creating an `HttpEntity`**
### **1️⃣ Sending a Request with Headers & Body**
```java
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class ApiService {
    private final RestTemplate restTemplate = new RestTemplate();

    public ResponseEntity<String> sendRequest() {
        String url = "https://jsonplaceholder.typicode.com/posts";

        // Create Headers
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer my_token");
        headers.set("Content-Type", "application/json");

        // Create Request Body
        String body = "{ \"title\": \"New Post\", \"body\": \"This is a post\", \"userId\": 1 }";

        // Create HttpEntity with Headers and Body
        HttpEntity<String> requestEntity = new HttpEntity<>(body, headers);

        // Send POST request
        return restTemplate.exchange(url, HttpMethod.POST, requestEntity, String.class);
    }
}
```

✅ **Explanation**:
- `HttpHeaders headers = new HttpHeaders();` → Creates custom headers.
- `HttpEntity<String> requestEntity = new HttpEntity<>(body, headers);` → Combines headers and body.
- `restTemplate.exchange(url, HttpMethod.POST, requestEntity, String.class);` → Sends the request.

---

## **🔹 Receiving a Response with `HttpEntity`**
```java
public void getRequest() {
    String url = "https://jsonplaceholder.typicode.com/posts/1";

    // Make GET request and receive response
    ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.GET, HttpEntity.EMPTY, String.class);

    System.out.println("Response: " + response.getBody());
}
```
- `HttpEntity.EMPTY` means no body is sent.
- The response is wrapped in `ResponseEntity<T>`.

---

## **🔹 Handling Custom Headers in Response**
```java
public void getWithHeaders() {
    String url = "https://jsonplaceholder.typicode.com/posts/1";

    ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.GET, HttpEntity.EMPTY, String.class);
    
    System.out.println("Headers: " + response.getHeaders());
    System.out.println("Body: " + response.getBody());
}
```

---

## **🌟 Summary**
| Feature       | `HttpEntity<T>` |
|--------------|----------------|
| **Purpose**  | Send/Receive HTTP request & response with headers |
| **Use With** | `RestTemplate` (mostly) |
| **Includes** | HTTP Headers + Body |
| **Alternatives** | `RequestEntity<T>`, `ResponseEntity<T>` |

Would you like an example using **`WebClient`** instead of `RestTemplate`? 🚀



### **Difference Between `@RestControllerAdvice` and `@RestController` in Spring Boot**

Both annotations are used in **Spring Boot's REST API development**, but they serve different purposes.

| Annotation            | Purpose |
|----------------------|---------|
| `@RestController`    | Defines a RESTful controller that handles **HTTP requests** and returns responses. |
| `@RestControllerAdvice` | A **global exception handler** for REST controllers. It provides centralized exception handling across multiple controllers. |

---

### **1️⃣ `@RestController` - Handles HTTP Requests**
- Used for **creating REST APIs**.
- Combines `@Controller` and `@ResponseBody`.
- Maps requests using `@RequestMapping`, `@GetMapping`, etc.

#### **Example**
```java
@RestController
@RequestMapping("/users")
public class UserController {

    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        if (id == 0) {
            throw new UserNotFoundException("User not found");
        }
        return new User(id, "John Doe");
    }
}
```
🔹 **Handles HTTP requests and returns JSON responses**.

---

### **2️⃣ `@RestControllerAdvice` - Global Exception Handling**
- Used for **handling exceptions globally** across multiple controllers.
- Works like `@ExceptionHandler`, but for **all controllers**.
- Improves **code reusability** and keeps controllers clean.

#### **Example**
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<String> handleUserNotFound(UserNotFoundException ex) {
        return new ResponseEntity<>(ex.getMessage(), HttpStatus.NOT_FOUND);
    }
}
```
🔹 **Intercepts exceptions from any `@RestController` and returns meaningful error responses**.

---

### **📌 Key Differences**
| Feature                | `@RestController` | `@RestControllerAdvice` |
|------------------------|------------------|-------------------------|
| **Purpose**            | Handles HTTP requests | Handles exceptions globally |
| **Usage**              | Used for REST API endpoints | Used for centralized error handling |
| **Annotations Inside** | `@GetMapping`, `@PostMapping`, etc. | `@ExceptionHandler`, `@ModelAttribute`, etc. |
| **Scope**              | Specific to a single class | Applies to multiple controllers |

---

### **🚀 When to Use What?**
- Use `@RestController` to **create API endpoints**.
- Use `@RestControllerAdvice` to **handle exceptions globally**.

This ensures **cleaner controllers** and **better error handling** in your Spring Boot application! 🚀


Yes, an **enum** in Java can store both a **status code** and an **error message**, and you can implement a `findByStatusCode` method to retrieve an enum instance based on the status code.

---

### **✅ Storing Status Code and Error Message in Enum**
Enums in Java can have fields, constructors, and methods. Below is an example:

```java
public enum HttpStatusEnum {
    OK(200, "Success"),
    BAD_REQUEST(400, "Invalid request"),
    UNAUTHORIZED(401, "Unauthorized access"),
    FORBIDDEN(403, "Access denied"),
    NOT_FOUND(404, "Resource not found"),
    INTERNAL_SERVER_ERROR(500, "Internal server error");

    private final int statusCode;
    private final String message;

    // Constructor
    HttpStatusEnum(int statusCode, String message) {
        this.statusCode = statusCode;
        this.message = message;
    }

    // Getter methods
    public int getStatusCode() {
        return statusCode;
    }

    public String getMessage() {
        return message;
    }

    // Method to find enum by status code
    public static HttpStatusEnum findByStatusCode(int code) {
        for (HttpStatusEnum status : HttpStatusEnum.values()) {
            if (status.getStatusCode() == code) {
                return status;
            }
        }
        return null; // Return null or throw an exception if not found
    }
}
```

---

### **✅ Using `findByStatusCode` Method**
You can now find an enum instance based on the status code:

```java
public class Main {
    public static void main(String[] args) {
        HttpStatusEnum status = HttpStatusEnum.findByStatusCode(404);

        if (status != null) {
            System.out.println("Status Code: " + status.getStatusCode());
            System.out.println("Message: " + status.getMessage());
        } else {
            System.out.println("Status code not found.");
        }
    }
}
```

**🛠 Output:**
```
Status Code: 404
Message: Resource not found
```

---

### **📌 Key Takeaways**
1. **Enums can store multiple fields**, including status codes and messages.
2. **Custom methods** like `findByStatusCode` allow you to search through enum values.
3. This approach makes it **cleaner** and **easier to manage HTTP status codes**.

Would you like to modify this approach for a specific use case? 🚀

Your method `findByStatusCode(String statusCode)` is used to retrieve an `ErrorStatus` enum instance based on the provided status code.  

---

### **🔹 How It Works**
1. **`Arrays.stream(values())`** → Converts the list of all enum values into a stream.
2. **`filter(e -> e.getStatusCode().equalsIgnoreCase(statusCode))`** → Filters the enum instances to find the one where `getStatusCode()` matches the provided `statusCode`.
3. **`findFirst()`** → Returns the first matching instance wrapped in an `Optional<ErrorStatus>`.

---

### **✅ Example Usage with Enum**
#### **1️⃣ Define the Enum**
```java
import java.util.Arrays;
import java.util.Optional;

public enum ErrorStatus {
    SUCCESS("200", "Operation Successful"),
    BAD_REQUEST("400", "Invalid Request"),
    NOT_FOUND("404", "Resource Not Found"),
    SERVER_ERROR("500", "Internal Server Error");

    private final String statusCode;
    private final String message;

    ErrorStatus(String statusCode, String message) {
        this.statusCode = statusCode;
        this.message = message;
    }

    public String getStatusCode() {
        return statusCode;
    }

    public String getMessage() {
        return message;
    }

    // Method to find enum by status code
    public static Optional<ErrorStatus> findByStatusCode(String statusCode) {
        return Arrays.stream(values())
                .filter(e -> e.getStatusCode().equalsIgnoreCase(statusCode))
                .findFirst();
    }
}
```

---

#### **2️⃣ Using `findByStatusCode` Method**
```java
public class Main {
    public static void main(String[] args) {
        String inputStatus = "404";

        Optional<ErrorStatus> errorStatus = ErrorStatus.findByStatusCode(inputStatus);

        if (errorStatus.isPresent()) {
            System.out.println("Found: " + errorStatus.get().getStatusCode() + " - " + errorStatus.get().getMessage());
        } else {
            System.out.println("Status code not found.");
        }
    }
}
```

---

### **🛠 Output for `findByStatusCode("404")`:**
```
Found: 404 - Resource Not Found
```

---

### **📌 Key Benefits**
✅ **Encapsulates status codes & messages** in an organized way.  
✅ **Returns `Optional<ErrorStatus>`** → Avoids `null` and helps handle cases where status codes are not found.  
✅ **Efficient Lookup** using Java Streams instead of manual iteration.  

Would you like modifications for specific use cases? 🚀

### **🔹 What is `@Aspect` in Spring AOP?**  
`@Aspect` is an annotation used in **Spring AOP (Aspect-Oriented Programming)** to define **cross-cutting concerns** like logging, security, transaction management, and performance monitoring.  

It allows developers to **separate** these concerns from the core business logic by writing reusable code.

---

### **✅ Key Concepts of AOP (`@Aspect`)**
| **Concept** | **Description** |
|------------|---------------|
| **Aspect (`@Aspect`)** | A class that contains cross-cutting concerns. |
| **Advice (`@Before`, `@After`, `@Around`, etc.)** | The action performed at a specific point in execution. |
| **Join Point** | A point in program execution where advice can be applied (e.g., method execution). |
| **Pointcut (`@Pointcut`)** | Defines where advice should be applied. |
| **Weaving** | The process of applying aspects to target objects at runtime. |

---

### **📌 Example: Logging with `@Aspect`**
#### **1️⃣ Create an Aspect Class**
```java
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.After;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.ProceedingJoinPoint;
import org.springframework.stereotype.Component;

@Aspect  // Declares this class as an Aspect
@Component  // Registers it as a Spring Bean
public class LoggingAspect {

    // Define a Pointcut for all methods in a package
    @Pointcut("execution(* com.example.service.*.*(..))")
    public void serviceMethods() {}

    // Before Advice: Runs before the method execution
    @Before("serviceMethods()")
    public void logBefore() {
        System.out.println("🔹 Before method execution - Logging started...");
    }

    // After Advice: Runs after method execution
    @After("serviceMethods()")
    public void logAfter() {
        System.out.println("🔹 After method execution - Logging completed...");
    }

    // Around Advice: Runs before & after method execution
    @Around("serviceMethods()")
    public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        
        Object result = joinPoint.proceed();  // Proceed with method execution
        
        long end = System.currentTimeMillis();
        System.out.println("⏳ Execution Time: " + (end - start) + "ms");
        
        return result;
    }
}
```

---

#### **2️⃣ Apply Aspect to a Service Class**
```java
import org.springframework.stereotype.Service;

@Service
public class UserService {

    public void getUser() {
        System.out.println("👤 Fetching user details...");
    }
}
```

---

#### **3️⃣ Enable AOP in Spring Boot (`@EnableAspectJAutoProxy`)**
Add this in the **main configuration class**:
```java
import org.springframework.context.annotation.EnableAspectJAutoProxy;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@EnableAspectJAutoProxy  // Enables AOP in Spring Boot
public class AopDemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(AopDemoApplication.class, args);
    }
}
```

---

### **🛠 Output When Calling `getUser()`**
```
🔹 Before method execution - Logging started...
👤 Fetching user details...
🔹 After method execution - Logging completed...
⏳ Execution Time: 5ms
```

---

### **🚀 Advantages of Using `@Aspect`**
✔ **Separation of Concerns** → Keeps business logic clean.  
✔ **Reusability** → A single aspect can be applied across multiple classes.  
✔ **Maintainability** → Easier to update cross-cutting concerns in one place.  
✔ **Performance Monitoring** → Measure method execution time.  

Would you like an example for a **custom exception handling aspect** or **security (authentication)**? 😊

### **Explanation of Annotations in Java**  
The given annotation definition contains two meta-annotations:  

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface EnableAuditEvent {
}
```

These annotations control how `@EnableAuditEvent` behaves.

---

## **1️⃣ @Retention(RetentionPolicy.RUNTIME)**
🔹 **Definition:** Specifies how long the annotation should be retained.  

### **Retention Policies in Java:**
| **RetentionPolicy** | **Description** |
|---------------------|----------------|
| `SOURCE`  | Annotations are **discarded during compilation** and not included in the `.class` file. Used for documentation tools like `@Override`. |
| `CLASS`   | Annotations are **present in the `.class` file** but not available at runtime (default behavior). Used by the compiler. |
| `RUNTIME` | Annotations are **retained in the `.class` file** and are available at runtime via reflection. |

🔹 **Usage in this case (`RetentionPolicy.RUNTIME`)**  
- The annotation **remains available at runtime** for use with **reflection**.  
- This is useful for logging, auditing, or security mechanisms where we process annotations dynamically.  

### **Example: How Reflection Uses `RUNTIME` Annotations**
```java
import java.lang.annotation.*;
import java.lang.reflect.*;

@Retention(RetentionPolicy.RUNTIME) // Available at runtime
@Target(ElementType.METHOD)         // Applicable only to methods
@interface EnableAuditEvent {}

class UserService {
    @EnableAuditEvent
    public void createUser() {
        System.out.println("User created.");
    }
}

public class AnnotationProcessor {
    public static void main(String[] args) throws Exception {
        Method method = UserService.class.getMethod("createUser");

        if (method.isAnnotationPresent(EnableAuditEvent.class)) {
            System.out.println("Audit Event Enabled for createUser()");
        }
    }
}
```
### **🛠 Output:**
```
Audit Event Enabled for createUser()
```
👉 **Why?** Since `@EnableAuditEvent` is retained at runtime, the reflection API can detect and process it.

---

## **2️⃣ @Target(ElementType.METHOD)**
🔹 **Definition:** Specifies where the annotation can be applied.  

### **Possible `ElementType` Values:**
| **ElementType**      | **Applies To** |
|----------------------|---------------|
| `TYPE`              | Classes, interfaces, or enums. |
| `FIELD`             | Instance and static variables. |
| `METHOD`            | Methods only. |
| `PARAMETER`         | Method parameters. |
| `CONSTRUCTOR`       | Constructors. |
| `LOCAL_VARIABLE`    | Local variables (inside methods). |
| `ANNOTATION_TYPE`   | Another annotation (meta-annotation). |
| `PACKAGE`           | A package declaration. |

🔹 **Usage in this case (`ElementType.METHOD`)**  
- The annotation can **only be applied to methods**.
- It **prevents incorrect usage** (e.g., it cannot be used on classes, fields, or variables).

### **Example of Invalid Use**
```java
@EnableAuditEvent  // ❌ ERROR: Cannot be used on a class
class UserService {
}
```
✅ **Correct Use:**
```java
class UserService {
    @EnableAuditEvent  // ✅ Correct! Applied to a method
    public void createUser() {
        System.out.println("User created.");
    }
}
```

---

## **🚀 Key Takeaways**
| **Annotation** | **Purpose** |
|---------------|------------|
| `@Retention(RetentionPolicy.RUNTIME)` | Makes the annotation available at runtime for reflection. |
| `@Target(ElementType.METHOD)` | Ensures the annotation can **only** be used on methods. |

Would you like me to show how to **process this annotation in Spring Boot** (e.g., logging audit events using AOP)? 😊

### **@Value Annotation in Spring Boot**
The `@Value` annotation in Spring is used for injecting values into variables, typically from **application properties**, **environment variables**, or **default values**.

---

## **🔹 Basic Usage: Injecting Property Values**
You can use `@Value` to inject values from the `application.properties` or `application.yml` file.

### **1️⃣ Inject a Property Value**
🔹 **In `application.properties`:**
```properties
app.name=My Spring App
```
🔹 **In Java Class:**
```java
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class AppConfig {
    
    @Value("${app.name}")  // Injects value from properties file
    private String appName;

    public void printAppName() {
        System.out.println("Application Name: " + appName);
    }
}
```
✅ **Output:**
```
Application Name: My Spring App
```

---

## **🔹 Injecting Default Values**
If the property is missing in `application.properties`, you can provide a **default value**:
```java
@Value("${app.version:1.0.0}")  // Default value = "1.0.0" if property is missing
private String appVersion;
```

---

## **🔹 Injecting Environment Variables**
You can also inject **system environment variables**.
```java
@Value("${JAVA_HOME}")
private String javaHome;
```
✅ This will inject the system's `JAVA_HOME` path.

---

## **🔹 SpEL (Spring Expression Language) Support**
`@Value` supports **mathematical expressions**, **method calls**, and **conditional logic**.

### **1️⃣ Math Operations**
```java
@Value("#{10 * 2}")  // Injects 20
private int calculatedValue;
```

### **2️⃣ Calling Methods**
```java
@Value("#{T(java.lang.Math).random() * 100}")  // Injects a random number
private double randomValue;
```

### **3️⃣ Using Other Beans**
```java
@Value("#{appConfig.appName}")  // Injects value from another bean
private String appName;
```

---

## **🔹 Injecting List or Array**
You can inject **comma-separated values** into a List or Array.
```properties
app.languages=Java,Python,JavaScript
```
```java
@Value("${app.languages}")
private String[] languages;
```
✅ `languages` will contain `["Java", "Python", "JavaScript"]`.

---

## **🔹 Injecting Maps**
Spring does not directly support `Map<String, String>`, but you can use SpEL:
```properties
app.settings={'theme':'dark', 'mode':'production'}
```
```java
@Value("#{${app.settings}}")
private Map<String, String> settings;
```
✅ `settings.get("theme")` → `"dark"`

---

## **🔹 When to Use `@Value` vs. `@ConfigurationProperties`?**
| Feature             | `@Value`                     | `@ConfigurationProperties` |
|--------------------|---------------------------|-----------------------------|
| Simplicity         | Simple for single values  | Better for groups of values |
| Type Safety       | Limited                   | Strong type-checking |
| Maps & Lists      | Requires SpEL             | Native support |
| Binding Prefix    | Not possible              | Uses property prefixes |

If you need **multiple properties**, prefer `@ConfigurationProperties`.

---

## **🔥 Conclusion**
- `@Value` injects values from **application properties**, **environment variables**, and **SpEL expressions**.
- Supports **default values**, **mathematical expressions**, **method calls**, and **list/array injection**.
- Best for **single values**, but use `@ConfigurationProperties` for structured data.

Would you like an example using `@ConfigurationProperties` for better property management? 😊

### **🌐 RestTemplate in Spring Boot**
`RestTemplate` is a class in Spring Boot used for making **synchronous HTTP requests** to external APIs or services. It simplifies the process of sending HTTP requests and handling responses.

---

## **🚀 How to Use RestTemplate**
### **1️⃣ Add Dependencies**
If you’re using Spring Boot **2.x**, add the dependency in `pom.xml` (if not already present):

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```
For **Spring Boot 3.x**, `RestTemplate` is **deprecated** in favor of `WebClient`, but you can still use it.

---

## **2️⃣ Create a Bean for `RestTemplate`**
Since `RestTemplate` is not automatically available, define it as a bean in your `@Configuration` class.

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class AppConfig {
    
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```
---

## **📌 Basic HTTP Methods with `RestTemplate`**
You can perform **GET, POST, PUT, DELETE** requests using `RestTemplate`.

### **1️⃣ Perform a GET Request**
Fetching data from a public API (e.g., JSONPlaceholder API):

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class ApiService {

    @Autowired
    private RestTemplate restTemplate;

    public String getPosts() {
        String url = "https://jsonplaceholder.typicode.com/posts/1";
        return restTemplate.getForObject(url, String.class);
    }
}
```
✅ **Response:**
```json
{
  "userId": 1,
  "id": 1,
  "title": "Sample title",
  "body": "Sample body text..."
}
```
---

### **2️⃣ Perform a POST Request**
Sending data (JSON) to an API:

```java
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class ApiService {
    
    @Autowired
    private RestTemplate restTemplate;

    public String createPost() {
        String url = "https://jsonplaceholder.typicode.com/posts";

        // Create request body
        String requestBody = "{ \"title\": \"New Post\", \"body\": \"This is a post\", \"userId\": 1 }";
        
        // Set headers
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        
        // Create HttpEntity with headers and body
        HttpEntity<String> request = new HttpEntity<>(requestBody, headers);

        // Perform POST request
        return restTemplate.postForObject(url, request, String.class);
    }
}
```
---

### **3️⃣ Perform a PUT Request**
Updating existing data:

```java
public void updatePost() {
    String url = "https://jsonplaceholder.typicode.com/posts/1";

    String updatedBody = "{ \"title\": \"Updated Post\", \"body\": \"Updated content\", \"userId\": 1 }";
    
    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);
    
    HttpEntity<String> request = new HttpEntity<>(updatedBody, headers);

    restTemplate.put(url, request);
}
```

---

### **4️⃣ Perform a DELETE Request**
Deleting a resource:

```java
public void deletePost() {
    String url = "https://jsonplaceholder.typicode.com/posts/1";
    restTemplate.delete(url);
}
```

---

## **🛠 Handling Response with `ResponseEntity`**
`ResponseEntity` allows handling HTTP responses properly.

```java
import org.springframework.http.ResponseEntity;

public void fetchWithResponseEntity() {
    String url = "https://jsonplaceholder.typicode.com/posts/1";
    ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);

    System.out.println("Status Code: " + response.getStatusCode());
    System.out.println("Response Body: " + response.getBody());
}
```

✅ **Output:**
```
Status Code: 200 OK
Response Body: { "userId": 1, "id": 1, "title": "...", "body": "..." }
```

---

## **🔄 Handling Timeouts and Errors**
To configure timeouts and better error handling, use **RestTemplate with `HttpClient`**:

```java
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;

public class CustomRestTemplate {

    public RestTemplate getRestTemplate() {
        CloseableHttpClient httpClient = HttpClients.custom()
                .setConnectionTimeToLive(10, java.util.concurrent.TimeUnit.SECONDS)  // Timeout
                .build();
        
        HttpComponentsClientHttpRequestFactory factory = new HttpComponentsClientHttpRequestFactory(httpClient);
        return new RestTemplate(factory);
    }
}
```

---

## **🚨 Should You Use `RestTemplate` in Spring Boot 3.x?**
🔴 **`RestTemplate` is deprecated in Spring Boot 3.x** in favor of `WebClient` (from Spring WebFlux).  
✅ For new projects, use **`WebClient`**, which is more flexible and supports asynchronous requests.

---

## **🔥 Conclusion**
- `RestTemplate` is a simple way to make **synchronous HTTP requests**.
- Supports **GET, POST, PUT, DELETE**.
- `ResponseEntity` helps handle responses efficiently.
- **Use `WebClient` in Spring Boot 3.x for better async support.**

Would you like an example using `WebClient` instead? 😊

### **🌐 WebClient in Spring Boot (Reactive HTTP Client)**
`WebClient` is the modern alternative to `RestTemplate` in **Spring Boot 3.x**. It supports **asynchronous, non-blocking HTTP requests**, making it more efficient for handling concurrent API calls.

---

## **🚀 Setting Up WebClient**
### **1️⃣ Add Dependencies**
If you are using **Spring Boot 3.x**, add the **Spring WebFlux** dependency:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
```
This will provide `WebClient` instead of `RestTemplate`.

---

## **2️⃣ Creating a `WebClient` Bean**
`WebClient` is not automatically available like `RestTemplate`, so define it as a **Spring Bean** in your configuration class.

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class WebClientConfig {

    @Bean
    public WebClient webClient() {
        return WebClient.builder()
                .baseUrl("https://jsonplaceholder.typicode.com") // Set a base URL (optional)
                .build();
    }
}
```

---

## **📌 Basic HTTP Requests with `WebClient`**
### **1️⃣ GET Request (Fetching Data)**
```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Service
public class ApiService {

    @Autowired
    private WebClient webClient;

    public Mono<String> getPost() {
        return webClient.get()
                .uri("/posts/1") // Complete URL: https://jsonplaceholder.typicode.com/posts/1
                .retrieve()
                .bodyToMono(String.class); // Convert response to String
    }
}
```
✅ **Output:**
```json
{
  "userId": 1,
  "id": 1,
  "title": "Sample title",
  "body": "Sample body text..."
}
```

🔹 **`Mono<String>`** means the response will be retrieved **asynchronously**.

---

### **2️⃣ POST Request (Sending Data)**
```java
public Mono<String> createPost() {
    String requestBody = "{ \"title\": \"New Post\", \"body\": \"This is a post\", \"userId\": 1 }";

    return webClient.post()
            .uri("/posts")
            .header("Content-Type", "application/json")
            .bodyValue(requestBody)
            .retrieve()
            .bodyToMono(String.class);
}
```

---

### **3️⃣ PUT Request (Updating Data)**
```java
public Mono<String> updatePost() {
    String updatedBody = "{ \"title\": \"Updated Post\", \"body\": \"Updated content\", \"userId\": 1 }";

    return webClient.put()
            .uri("/posts/1")
            .header("Content-Type", "application/json")
            .bodyValue(updatedBody)
            .retrieve()
            .bodyToMono(String.class);
}
```

---

### **4️⃣ DELETE Request**
```java
public Mono<Void> deletePost() {
    return webClient.delete()
            .uri("/posts/1")
            .retrieve()
            .bodyToMono(Void.class);
}
```

---

## **🛠 Handling Responses with `ResponseEntity`**
You can handle HTTP response status codes using `exchangeToMono()`.

```java
public Mono<String> fetchWithResponseEntity() {
    return webClient.get()
            .uri("/posts/1")
            .exchangeToMono(response -> {
                if (response.statusCode().is2xxSuccessful()) {
                    return response.bodyToMono(String.class);
                } else {
                    return Mono.error(new RuntimeException("Failed to fetch data!"));
                }
            });
}
```

---

## **🔄 Handling Timeouts & Retries**
To **set timeouts**, use `WebClient.builder()`.

```java
@Bean
public WebClient webClient() {
    return WebClient.builder()
            .baseUrl("https://jsonplaceholder.typicode.com")
            .codecs(configurer -> configurer.defaultCodecs().maxInMemorySize(16 * 1024 * 1024)) // Increase buffer size
            .build();
}
```

To **retry failed requests**:
```java
public Mono<String> fetchWithRetry() {
    return webClient.get()
            .uri("/posts/1")
            .retrieve()
            .bodyToMono(String.class)
            .retry(3); // Retries up to 3 times
}
```

---

## **🔹 Comparison: `WebClient` vs `RestTemplate`**
| Feature         | `RestTemplate` (Deprecated) | `WebClient` (Recommended) |
|---------------|-----------------|----------------|
| **Blocking?** | Yes (Synchronous) | No (Asynchronous) |
| **Performance** | Slower (1 request at a time) | Faster (Handles multiple requests) |
| **Streaming Support?** | No | Yes |
| **Spring Boot 3.x?** | ❌ Deprecated | ✅ Recommended |

---

## **🔥 Conclusion**
- `WebClient` is the preferred HTTP client in **Spring Boot 3.x**.
- Supports **async & reactive programming**.
- Use **`Mono`** (for single response) and **`Flux`** (for streaming multiple responses).
- Use `retrieve()` for simple calls and `exchangeToMono()` for advanced handling.

Would you like an example with **error handling and logging**? 🚀

