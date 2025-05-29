You're absolutely right — and this is a key point in large refactorings like migrating from **Axis2 to Apache CXF**.

### 🔁 The Dilemma:

* **You want to delete the Axis2 stub files** to fully migrate.
* **But many parts of your code still import or use those stubs**, so removing them breaks compilation, and Rewrite recipes can't run.

---

### ✅ Here's a Step-by-Step Strategy That Works

Instead of immediately deleting the Axis2-generated stubs, **transition gradually**:

---

### ✅ Phase 1: Let Rewrite Help You Identify Axis2 Usage

1. **Restore Axis2 stub files temporarily** so the build can compile.

2. In your `build.gradle`, **enable OpenRewrite with this recipe**:

   ```groovy
   rewrite {
       activeRecipe("org.openrewrite.java.search.FindTypes")
       // This recipe will help us identify Axis2 usage.
   }
   ```

3. In your `rewrite.yml` file (create if needed):

   ```yaml
   type: specs.openrewrite.org/v1beta/recipe
   name: find.axis2.usages
   recipeList:
     - org.openrewrite.java.search.FindTypes:
         fullyQualifiedTypeName: org.apache.axis2.AxisFault
   ```

   You can add more like:

   ```yaml
     - org.openrewrite.java.search.FindTypes:
         fullyQualifiedTypeName: org.apache.axis2.client.ServiceClient
     - org.openrewrite.java.search.FindTypes:
         fullyQualifiedTypeName: org.apache.axis2.databinding.ADBBean
   ```

4. Run the Rewrite plugin:

   ```bash
   ./gradlew rewriteRun
   ```

   This will annotate or highlight all usages of Axis2 types.

---

### ✅ Phase 2: Manually Replace Axis2-Specific Code

After identifying all usage points:

1. **Refactor the code manually or with additional Rewrite recipes** to:

   * Replace `AxisFault` with `javax.xml.ws.WebServiceException` or a CXF-specific exception.
   * Replace `ServiceClient` logic with JAX-WS `Service` and proxy usage.
   * Replace data-binding objects with JAXB-based CXF stubs.

2. **Then safely delete Axis2 stubs and dependencies**.

---

### ✅ Phase 3: Regenerate Stubs with CXF

After Axis2 usage is eliminated:

* Remove the Axis2 dependencies and stub files.
* Use your `generateStubs` Gradle task to regenerate stubs from WSDL via CXF.
* Update service calls to use new CXF-generated service classes.

---

### If You Prefer a One-Shot Migration…

You could use **OpenRewrite’s custom recipes** to:

* Replace `AxisFault` with a more generic `WebServiceException`
* Replace all Axis2 classes with mocks
* Then **delete the stubs**
* Then regenerate CXF stubs and finally adjust imports

But in practice, **gradual migration** as described is more stable and manageable.

Would you like help writing custom Rewrite recipes to replace specific Axis2 usages like `AxisFault` or `ServiceClient`?




Great, Lisa. Here's exactly where and how to integrate that `generateStubs` task into your Gradle project.

---

## ✅ Where to Place the Code

You should place this code **inside your main `build.gradle` file** — typically found at:

```
<your-project-root>/build.gradle
```

---

## 🧩 Final Integration Steps

### 1. **Paste the code at the bottom of your `build.gradle`** file:

Place the following block **after** your `dependencies {}` block:

```groovy
configurations {
    cxfTools
}

dependencies {
    // Your existing dependencies...

    // Add these just below
    cxfTools 'org.apache.cxf:cxf-tools-wsdlto-core:3.5.3'
    cxfTools 'org.apache.cxf:cxf-tools-common:3.5.3'
    cxfTools 'org.apache.cxf:cxf-tools-wsdlto-frontend-jaxws:3.5.3'
    cxfTools 'org.apache.cxf:cxf-tools-wsdlto-databinding-jaxb:3.5.3'
}

task generateStubs(type: Exec) {
    def outputDir = "$buildDir/generated-sources/wsdl"
    def wsdlFile = "$projectDir/src/main/resources/service.wsdl"

    doFirst {
        file(outputDir).mkdirs()
    }

    commandLine 'java',
        '-cp', configurations.cxfTools.asPath,
        'org.apache.cxf.tools.wsdlto.WSDLToJava',
        '-d', outputDir,
        wsdlFile
}

sourceSets.main.java.srcDirs += "$buildDir/generated-sources/wsdl"
```

---

### 2. **Make sure your `.wsdl` file exists**

Put your WSDL file here:

```
src/main/resources/service.wsdl
```

If it's named differently, update:

```groovy
def wsdlFile = "$projectDir/src/main/resources/YOUR_FILENAME.wsdl"
```

---

### 3. **Generate the CXF Stubs**

Run this command:

```bash
./gradlew generateStubs
```

This will generate the Java client code in:

```
build/generated-sources/wsdl/
```

And your project will automatically include them in the main source set.

---

### ✅ Optional: Use the Generated Classes

You can now create the client like this (based on the generated classes):

```java
MyService_Service service = new MyService_Service();
MyService port = service.getMyServicePort();

port.callSomeSoapMethod();
```

---

Let me know if you want to automate stub generation as part of the build, or need help refactoring old Axis2 code to use these new CXF stubs!
