Yes. **Start with the Documentation MCP Server.** Do not build the entire migration platform yet.

Your first milestone should be:

> **Ask the MCP server: `search_company_docs("How do I create a table?")` → get the correct internal documentation back.**

Once this works, you have proven the core pattern.

---

# Module 1: Documentation MCP Server

The architecture:

```text
Internal Documentation
        │
        ▼
   Scraper
        │
        ▼
 Markdown Files
        │
        ▼
 Chunking + Embeddings
        │
        ▼
    Chroma DB
        │
        ▼
 Documentation MCP Server
        │
        ▼
 search_company_docs()
        │
        ▼
 GitHub Copilot / MCP Client
```

The MCP server is simply the bridge between the AI and your vector database.

---

# Step 1: Create the project

Since you already use Python and `uv`, I would create:

```text
jsp-react-migration/
│
└── docs-mcp-server/
    │
    ├── pyproject.toml
    ├── server.py
    │
    ├── data/
    │   ├── raw/
    │   └── markdown/
    │
    ├── vectorstore/
    │
    └── src/
        ├── scraper.py
        ├── indexer.py
        └── retriever.py
```

Create it:

```bash
mkdir jsp-react-migration
cd jsp-react-migration

mkdir docs-mcp-server
cd docs-mcp-server

uv init
uv add mcp chromadb langchain langchain-community
```

The official Python MCP SDK supports building servers with tools, resources, prompts, and standard transports. The current SDK's simple server abstraction is `FastMCP`. ([MCP Python SDK][1])

---

# Step 2: First build the MCP server WITHOUT Chroma

Do not immediately add scraping, embeddings, and vector search.

First prove MCP itself works.

Create:

```text
server.py
```

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Company React Documentation")


@mcp.tool()
def search_company_docs(query: str) -> str:
    """
    Search the company's React framework documentation.

    Use this tool when you need information about:
    - company React components
    - component usage
    - folder structure
    - styling standards
    - forms
    - validation
    - routing
    """

    return f"""
Mock documentation result for query: {query}

Company React Framework Documentation:

Use the approved company Button component.
Do not use native HTML buttons unless explicitly permitted.

Example:

<CompanyButton
    variant="primary"
    onClick={handleClick}
>
    Submit
</CompanyButton>
"""


if __name__ == "__main__":
    mcp.run()
```

Run:

```bash
uv run mcp dev server.py
```

The MCP Python SDK documents `mcp dev` with the MCP Inspector as a development workflow for testing servers. ([MCP Python SDK][1])

Your first success criteria:

```text
MCP Inspector
      │
      ▼
search_company_docs
      │
      ▼
"Button"
      │
      ▼
Documentation result
```

Do not move on until this works.

---

# Step 3: Replace the mock with actual Markdown files

Now create:

```text
data/markdown/button.md
```

````markdown
# Company Button

## Usage

Use the CompanyButton component for all user actions.

## Example

```tsx
<CompanyButton
    variant="primary"
    onClick={handleSubmit}
>
    Submit
</CompanyButton>
````

## Restrictions

Do not use native HTML buttons.

Do not create custom button styles.

## Import

Use the approved company import path.

````

Now change your server:

```python
from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Company React Documentation")

DOCS_DIR = Path("data/markdown")


@mcp.tool()
def search_company_docs(query: str) -> str:
    """
    Search company React documentation.

    Use this when converting JSP pages to the company React framework.
    """

    results = []

    for file_path in DOCS_DIR.glob("*.md"):

        content = file_path.read_text(
            encoding="utf-8"
        )

        if query.lower() in content.lower():

            results.append(
                f"""
DOCUMENT: {file_path.name}

{content}
"""
            )

    if not results:
        return "No matching company documentation found."

    return "\n\n".join(results)


if __name__ == "__main__":
    mcp.run()
````

Now:

```text
search_company_docs("Button")
```

returns:

```text
button.md
```

This is already a valid MCP tool.

---

# Step 4: Add the real documentation scraper

Only after the previous steps work should you add scraping.

Your scraper should be separate from the MCP server.

```text
scraper.py
```

```python
from pathlib import Path

from playwright.async_api import async_playwright


async def scrape_page(
    url: str,
    output_file: str
):

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        page = await browser.new_page()

        await page.goto(
            url,
            wait_until="networkidle"
        )

        content = await page.locator(
            "main"
        ).inner_text()

        Path(output_file).write_text(
            content,
            encoding="utf-8"
        )

        await browser.close()
```

But your actual enterprise documentation may require:

* login
* SSO
* JavaScript rendering
* clicking accordions
* pagination
* internal authentication

So you should make the scraper specific to your documentation system.

The result should be:

```text
Internal Web Page
        │
        ▼
Playwright
        │
        ▼
Clean Markdown
        │
        ▼
data/markdown/
```

---

# Step 5: Add the vector database

Now you have:

```text
data/markdown/

button.md
table.md
form.md
routing.md
folder-structure.md
```

Create:

```text
indexer.py
```

Conceptually:

```python
from pathlib import Path

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter


def index_documents():

    documents = []

    for file_path in Path(
        "data/markdown"
    ).glob("*.md"):

        content = file_path.read_text(
            encoding="utf-8"
        )

        documents.append({
            "content": content,
            "source": str(file_path)
        })

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.create_documents(
        [
            document["content"]
            for document in documents
        ]
    )

    # Add embeddings here
    # Add documents to Chroma here
```

The important thing is:

```text
Markdown
    ↓
Documents
    ↓
Chunks
    ↓
Embeddings
    ↓
Chroma
```

---

# Important: Do not hardcode the embedding model yet

You need to determine what your enterprise allows.

Possible choices:

```text
Enterprise embedding API
        │
        OR
Local embedding model
        │
        OR
Tachyon embedding endpoint
```

This is a key architectural decision.

Your MCP server should not care which embedding model you use.

Create an abstraction:

```python
class DocumentationRetriever:

    def search(
        self,
        query: str,
        k: int = 5
    ):
        ...
```

Then your MCP tool simply calls:

```python
retriever.search(query)
```

This lets you change from:

```text
Chroma + Local Embeddings
```

to:

```text
Chroma + Enterprise Embeddings
```

without changing your MCP interface.

---

# Step 6: Connect the MCP tool to Chroma

Your final first tool should look conceptually like this:

```python
from mcp.server.fastmcp import FastMCP

from retriever import DocumentationRetriever


mcp = FastMCP(
    "Company React Documentation"
)


retriever = DocumentationRetriever()


@mcp.tool()
def search_company_docs(
    query: str,
    max_results: int = 5
) -> str:
    """
    Search internal React framework documentation.

    Use this before generating or modifying React code.
    """

    results = retriever.search(
        query=query,
        k=max_results
    )

    if not results:
        return "No relevant documentation found."

    output = []

    for result in results:

        output.append(
            f"""
SOURCE: {result.source}

{result.content}
"""
        )

    return "\n\n".join(output)


if __name__ == "__main__":
    mcp.run()
```

Now the complete flow is:

```text
Copilot Agent
      │
      │
      ▼
search_company_docs(
    "How should I implement a table?"
)
      │
      ▼
MCP Server
      │
      ▼
Retriever
      │
      ▼
Chroma
      │
      ▼
Relevant Internal Documentation
      │
      ▼
Copilot Agent
```

---

# Step 7: Give the agent instructions

Create your agent file:

```text
.github/
└── agents/
    └── jsp-react-migrator.md
```

Example:

```markdown
---
name: JSP React Migrator
description: Migrates JSP pages to the company's React framework.
---

# Role

You are a senior enterprise software migration engineer.

Your job is to migrate legacy JSP applications to the company's approved React framework.

# Mandatory Rules

Before generating React code:

1. Analyze the legacy JSP.
2. Identify all UI components.
3. Identify forms and validations.
4. Identify API calls.
5. Identify routing.
6. Search the company documentation using the
   `search_company_docs` MCP tool.
7. Follow the retrieved company documentation.

# Documentation Rule

Never invent company framework APIs.

If you need information about:

- Button
- Table
- Modal
- Form
- Validation
- Routing
- Styling
- Folder structure

you MUST search the company documentation first.

# Code Generation Rules

Use only approved company components.

Do not use native HTML components when a company equivalent exists.

Do not invent import paths.

Do not create a new component if an approved company component already exists.

Preserve existing JSP business behavior.

Do not start with code generation.

First produce:

1. JSP analysis
2. Dependencies
3. Required company documentation
4. Migration plan
5. Proposed file structure
```

The important concept is:

```text
Agent Instructions
        +
MCP Tools
        =
AI Software Engineer
```

The `.md` file tells the agent **when it should use the tool**.

The MCP server tells it **how the tool actually works**.

---

# Your first complete milestone

I would define your first milestone as:

### Input

```text
"How should I create a customer search table using our company's React framework?"
```

### Agent behavior

```text
1. Understand question
2. Call search_company_docs()
3. Receive internal documentation
4. Generate answer using that documentation
```

### You should see

```text
Agent
  │
  ▼
search_company_docs(
    "customer search table React"
)
  │
  ▼
MCP Server
  │
  ▼
Vector Database
  │
  ▼
Internal Documentation
  │
  ▼
Agent
  │
  ▼
Company-compliant React code
```

**Do not start with JSP conversion.** First prove that your agent can reliably retrieve and use your company's React documentation. Then add the JSP analyzer as your second MCP server/tool.

The official MCP Python SDK supports this exact pattern: a `FastMCP` server exposes typed tools, while the client/agent discovers and invokes those tools; for local development, the SDK provides an MCP Inspector workflow for testing. ([MCP Python SDK][1])

### My recommendation for your immediate next step

Build only this:

```text
docs-mcp/
│
├── server.py
├── data/
│   └── markdown/
│       └── one-real-company-doc.md
└── retriever.py
```

Then get this working:

```text
Copilot
    ↓
search_company_docs("Button")
    ↓
Your internal documentation
```

Once you have that working, send me your **actual MCP server code, project structure, and the way your internal documentation is hosted**, and I can help you build the next module—the **JSP Architecture Analyzer**—on top of this foundation.

[1]: https://py.sdk.modelcontextprotocol.io/server/?utm_source=chatgpt.com "Building Servers - MCP Python SDK"
