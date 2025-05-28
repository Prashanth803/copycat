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
