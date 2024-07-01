To test the `DateTimeRangePicker` component using Jest and React Testing Library, you'll need to set up your testing environment properly. Here's how you can write a test program for it:

1. **Install the necessary dependencies**:
   Ensure you have `jest` and `@testing-library/react` installed. You can install them using npm or yarn:

   ```sh
   npm install --save-dev jest @testing-library/react @testing-library/jest-dom
   ```

2. **Write the test**:
   Create a test file, for example, `DateTimeRangePicker.test.js`, and write the test cases:

```javascript
import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import DateTimeRangePicker from './DateTimeRangePicker';

describe('DateTimeRangePicker', () => {
  let setShowRealTime, setStartDateTime, setEndDateTime;

  beforeEach(() => {
    setShowRealTime = jest.fn();
    setStartDateTime = jest.fn();
    setEndDateTime = jest.fn();
  });

  test('renders correctly', () => {
    const { getByLabelText, getByText } = render(
      <DateTimeRangePicker
        setShowRealTime={setShowRealTime}
        startDateTime=""
        setStartDateTime={setStartDateTime}
        endDateTime=""
        setEndDateTime={setEndDateTime}
      />
    );

    expect(getByLabelText(/start/i)).toBeInTheDocument();
    expect(getByLabelText(/end/i)).toBeInTheDocument();
    expect(getByText(/submit/i)).toBeInTheDocument();
    expect(getByText(/reset/i)).toBeInTheDocument();
  });

  test('handles date time input changes', () => {
    const { getByLabelText } = render(
      <DateTimeRangePicker
        setShowRealTime={setShowRealTime}
        startDateTime=""
        setStartDateTime={setStartDateTime}
        endDateTime=""
        setEndDateTime={setEndDateTime}
      />
    );

    const startInput = getByLabelText(/start/i);
    const endInput = getByLabelText(/end/i);

    fireEvent.change(startInput, { target: { value: '2023-07-01T12:00' } });
    fireEvent.change(endInput, { target: { value: '2023-07-01T14:00' } });

    expect(setStartDateTime).toHaveBeenCalledWith('2023-07-01T12:00');
    expect(setEndDateTime).toHaveBeenCalledWith('2023-07-01T14:00');
  });

  test('submits the form and updates showRealTime', () => {
    const { getByText } = render(
      <DateTimeRangePicker
        setShowRealTime={setShowRealTime}
        startDateTime=""
        setStartDateTime={setStartDateTime}
        endDateTime=""
        setEndDateTime={setEndDateTime}
      />
    );

    fireEvent.click(getByText(/submit/i));

    expect(setShowRealTime).toHaveBeenCalledWith(false);
  });

  test('resets the showRealTime state', () => {
    const { getByText } = render(
      <DateTimeRangePicker
        setShowRealTime={setShowRealTime}
        startDateTime=""
        setStartDateTime={setStartDateTime}
        endDateTime=""
        setEndDateTime={setEndDateTime}
      />
    );

    fireEvent.click(getByText(/reset/i));

    expect(setShowRealTime).toHaveBeenCalledTimes(2);
    expect(setShowRealTime).toHaveBeenCalledWith(false);
    expect(setShowRealTime).toHaveBeenCalledWith(true);
  });
});
```

This code includes the following test cases:
- **renders correctly**: Ensures that the component renders the start and end date-time inputs, the submit button, and the reset button.
- **handles date time input changes**: Simulates changing the start and end date-time inputs and verifies that the corresponding state update functions (`setStartDateTime` and `setEndDateTime`) are called with the correct values.
- **submits the form and updates showRealTime**: Simulates submitting the form and verifies that `setShowRealTime` is called with `false`.
- **resets the showRealTime state**: Simulates clicking the reset button and verifies that `setShowRealTime` is called twice, first with `false` and then with `true`.

Make sure you run these tests using Jest. You can add a script in your `package.json` file to run Jest:

```json
"scripts": {
  "test": "jest"
}
```

Then, you can run your tests using:

```sh
npm test
```

This setup ensures that your `DateTimeRangePicker` component behaves as expected.







To write a Jest test case for the provided `Header3` component, we need to ensure the component is correctly formatted and then create the test case using React Testing Library.

### Cleaned Up `Header3` Component

First, let's clean up and properly format the `Header3` component.

#### `Header3.js`

```javascript
import React from 'react';
import { Link } from "react-router-dom";
import { Masthead, ThemeProvider } from "@wf-wfria/pioneer-core";

function Header3() {
  const [open, setOpen] = React.useState(false);

  const openPanel = () => setOpen(true);
  const closePanel = () => setOpen(false);

  const onSubmit = (e, data) => {
    window.alert("Form submitted");
    console.log("Form submitted with: ", data);
  };

  return (
    <ThemeProvider baseTheme='common'>
      <Masthead
        homeUrl="http://wellsfargo.com"
        elementToFocusOnSkip="#main-content"
      >
        <Link to="/About" style={{ marginLeft: "5%", color: "white", fontSize: "20px", fontFamily: "Arial Sans" }}>
          About
        </Link>
        <Link to="/Overview" style={{ marginLeft: "90%", color: "white", fontSize: "20px", fontFamily: "Arial Sans" }}>
          Overview
        </Link>
        <Link to="/Component_page" style={{ marginLeft: "5%", color: "white", fontSize: "20px", fontFamily: "Arial Sans" }}>
          Main
        </Link>
      </Masthead>
    </ThemeProvider>
  );
}

export default Header3;
```

### Jest Test Case

Now, let's write a Jest test case for the `Header3` component using React Testing Library.

#### `Header3.test.js`

```javascript
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import Header3 from './Header3';
import { BrowserRouter as Router } from 'react-router-dom';

test('renders Header3 and checks links functionality', () => {
  render(
    <Router>
      <Header3 />
    </Router>
  );

  // Check if links are rendered and have correct href attributes
  const aboutLink = screen.getByText('About').closest('a');
  const overviewLink = screen.getByText('Overview').closest('a');
  const mainLink = screen.getByText('Main').closest('a');

  expect(aboutLink).toHaveAttribute('href', '/About');
  expect(overviewLink).toHaveAttribute('href', '/Overview');
  expect(mainLink).toHaveAttribute('href', '/Component_page');
});
```

### Explanation

1. **Render Component**: The `Header3` component is rendered using the `render` function from React Testing Library, wrapped in a `Router` since it uses `Link` from `react-router-dom`.
2. **Check Links**: The test verifies that each link has the correct `href` attribute.

### Running the Tests

To run the tests, ensure you have Jest and React Testing Library set up in your project. You can run the tests using the following command:

```bash
npm test
```

This command will execute all test files and output the results, showing which tests passed and which failed.






Let's start by cleaning up and properly formatting the `Header` component. Then, we'll write a Jest test case for it using React Testing Library.

### Cleaned Up `Header` Component

#### `Header.js`
```javascript
import React from 'react';
import { Masthead, ThemeProvider } from "@wf-wfria/pioneer-core";
import SearchBar from '../SearchBar/SearchBar';
import { Link } from "react-router-dom";

const Header = ({ setCurrentCompanyId }) => {
  const [open, setOpen] = React.useState(false);

  const openPanel = () => setOpen(true);
  const closePanel = () => setOpen(false);

  const onSubmit = (e, data) => {
    e.preventDefault();
    console.log("Form submitted with: ", data);
    window.alert("Form submitted");
  };

  return (
    <ThemeProvider baseTheme='common'>
      <Masthead
        homeUrl="/"
        elementToFocusOnSkip="#main-content"
      >
        <div style={{ paddingLeft: "72%", display: "flex", flexDirection: "row" }}>
          <SearchBar setCurrentCompanyId={setCurrentCompanyId} />
          <Link to="/Overview" style={{ position: "absolute", fontSize: "28px", fontFamily: "Arial Sans", paddingTop: "0.65%", right: 10, color: "white" }}>
            Overview
          </Link>
          <Link to="/About" style={{ position: "absolute", fontSize: "20px", fontFamily: "Arial Sans", paddingTop: "0.6%", right: 120, color: "white" }}>
            About
          </Link>
        </div>
        {/* <div style={{ marginLeft: "auto", display: "flex", paddingTop: "22px"}}>
          <h1 style={{ color: "#ffcd41", fontFamily: "Times New Roman, Times, serif", fontWeight: "bolder", fontSize: "30px" }}>
            TRADE VISION
          </h1>
        </div> */}
      </Masthead>
    </ThemeProvider>
  );
};

export default Header;
```

### Jest Test Case

Now, let's write a Jest test case for the `Header` component using React Testing Library.

#### `Header.test.js`
```javascript
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import Header from './Header';
import SearchBar from '../SearchBar/SearchBar';
import { BrowserRouter as Router } from 'react-router-dom';

// Mock the SearchBar component
jest.mock('../SearchBar/SearchBar', () => ({
  __esModule: true,
  default: ({ setCurrentCompanyId }) => (
    <input
      type="text"
      placeholder="Search"
      onChange={(e) => setCurrentCompanyId(e.target.value)}
    />
  )
}));

test('renders Header and checks SearchBar and links functionality', () => {
  const setCurrentCompanyId = jest.fn();

  render(
    <Router>
      <Header setCurrentCompanyId={setCurrentCompanyId} />
    </Router>
  );

  // Check if Masthead and ThemeProvider are rendered
  expect(screen.getByPlaceholderText('Search')).toBeInTheDocument();

  // Simulate SearchBar input change
  fireEvent.change(screen.getByPlaceholderText('Search'), { target: { value: '12345' } });
  expect(setCurrentCompanyId).toHaveBeenCalledWith('12345');

  // Check if links are rendered and have correct href attributes
  const overviewLink = screen.getByText('Overview').closest('a');
  const aboutLink = screen.getByText('About').closest('a');

  expect(overviewLink).toHaveAttribute('href', '/Overview');
  expect(aboutLink).toHaveAttribute('href', '/About');
});
```

### Explanation

1. **Mocking `SearchBar` Component**: The `SearchBar` component is mocked to simplify testing and focus on the `Header` component.
2. **Render Component**: The `Header` component is rendered using the `render` function from React Testing Library, wrapped in a `Router` since it uses `Link` from `react-router-dom`.
3. **Check Text Content**: The test checks if the `SearchBar` input placeholder is present in the document.
4. **Simulate Input Change**: The test simulates changing the input value of the `SearchBar` and verifies that the `setCurrentCompanyId` function is called with the correct argument.
5. **Check Links**: The test verifies that each link has the correct `href` attribute.

### Running the Tests

To run the tests, ensure you have Jest and React Testing Library set up in your project. You can run the tests using the following command:

```bash
npm test
```

This command will execute all test files and output the results, showing which tests passed and which failed.






To write a test case for the `Header` component in Jest, you need to properly format the component first. Then, you can write a test case using Jest and React Testing Library.

### Header Component

First, let's clean up and properly format the `Header` component code.

#### `Header.js`
```javascript
import React from 'react';
import { Masthead, ThemeProvider } from "@wf-wfria/pioneer-core";
import SearchBar from '../SearchBar/SearchBar';
import { Link } from "react-router-dom";

const Header = ({ setCurrentCompanyId }) => {
  const [open, setOpen] = React.useState(false);

  const openPanel = () => setOpen(true);
  const closePanel = () => setOpen(false);

  const onSubmit = (e, data) => {
    e.preventDefault();
    console.log("Form submitted with: ", data);
    window.alert("Form submitted");
  };

  return (
    <ThemeProvider baseTheme='common'>
      <Masthead
        homeUrl="/"
        elementToFocusOnSkip="#main-content"
      >
        <div style={{ paddingLeft: "72%" }}>
          <SearchBar setCurrentCompanyId={setCurrentCompanyId} />
        </div>
        {/* <div style={{ marginLeft: "auto", display: "flex", paddingTop: "22px" }}>
          <h1 style={{ color: "#ffcd41", fontFamily: "Times New Roman, Times, serif", fontWeight: "bolder", fontSize: "30px" }}>
            TRADE VISION
          </h1>
        </div> */}
      </Masthead>
    </ThemeProvider>
  );
};

export default Header;
```

### Jest Test Case

Now, let's write a test case for this component using Jest and React Testing Library.

#### `Header.test.js`
```javascript
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import Header from './Header';
import SearchBar from '../SearchBar/SearchBar';

// Mock the SearchBar component
jest.mock('../SearchBar/SearchBar', () => ({
  __esModule: true,
  default: ({ setCurrentCompanyId }) => (
    <input
      type="text"
      placeholder="Search"
      onChange={(e) => setCurrentCompanyId(e.target.value)}
    />
  )
}));

test('renders Header and checks SearchBar functionality', () => {
  const setCurrentCompanyId = jest.fn();

  render(<Header setCurrentCompanyId={setCurrentCompanyId} />);

  // Check if Masthead and ThemeProvider are rendered
  expect(screen.getByText(/Search/)).toBeInTheDocument();

  // Simulate SearchBar input change
  fireEvent.change(screen.getByPlaceholderText('Search'), { target: { value: '12345' } });
  expect(setCurrentCompanyId).toHaveBeenCalledWith('12345');
});
```

### Explanation

1. **Mocking `SearchBar` Component**: The `SearchBar` component is mocked to simplify testing and focus on the `Header` component.
2. **Render Component**: The `Header` component is rendered using the `render` function from React Testing Library.
3. **Check Text Content**: The test checks if the `SearchBar` input placeholder is present in the document.
4. **Simulate Input Change**: The test simulates changing the input value of the `SearchBar` and verifies that the `setCurrentCompanyId` function is called with the correct argument.

### Running the Tests

To run the tests, ensure you have Jest and React Testing Library set up in your project. You can run the tests using the following command:

```bash
npm test
```

This command will execute all test files and output the results, showing which tests passed and which failed.

Let's first clean up and properly format the `Footer_page` component code. Then, I'll provide a Jest test case for it.

### Cleaned Up `Footer_page` Component

```javascript
import React from 'react';
import { ThemeProvider } from '@material-ui/core/styles';

function Footer_page() {
  const [open, setOpen] = React.useState(false);

  const openPanel = () => setOpen(true);
  const closePanel = () => setOpen(false);

  const onSubmit = (e, data) => {
    e.preventDefault();
    console.log("Form submitted with:", data);
    window.alert("Form submitted");
  };

  return (
    <ThemeProvider theme={{ baseTheme: 'vantage' }}>
      <div>
        Footer
        <ul>
          <li>
            <a href="https://wellsoffice.wellsfargo.com/ceoportal/appmanager/ceoPortal/ceoDesktop?_nfpb=true&_pageLabel=SiteMap">
              Site Map
            </a>
          </li>
          <li>
            <a href="https://www.wellsfargo.com/com/">
              Commercial Services
            </a>
          </li>
          <li>
            <a href="https://www.wellsfargo.com/com/services_all">
              Service Descriptions
            </a>
          </li>
          <li>
            <a href="https://wellsoffice.wellsfargo.com/ceoportal/appmanager/ceoPortal/ceoDesktop?_nfpb=true&_pageLabel=PortalSupport&portalSupportNodeName=gotoTermsOfUse&terms=true">
              Terms of Use
            </a>
          </li>
        </ul>
      </div>
    </ThemeProvider>
  );
}

export default Footer_page;
```

### Jest Test Case

Now, let's write a test case for this component using Jest and React Testing Library.

#### `Footer_page.test.js`

```javascript
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import Footer_page from './Footer_page';

test('renders Footer_page and checks links', () => {
  render(<Footer_page />);

  // Check if footer text is rendered
  expect(screen.getByText('Footer')).toBeInTheDocument();

  // Check if all links are rendered
  expect(screen.getByText('Site Map')).toBeInTheDocument();
  expect(screen.getByText('Commercial Services')).toBeInTheDocument();
  expect(screen.getByText('Service Descriptions')).toBeInTheDocument();
  expect(screen.getByText('Terms of Use')).toBeInTheDocument();

  // Check if links have correct href attributes
  expect(screen.getByText('Site Map').closest('a')).toHaveAttribute('href', 'https://wellsoffice.wellsfargo.com/ceoportal/appmanager/ceoPortal/ceoDesktop?_nfpb=true&_pageLabel=SiteMap');
  expect(screen.getByText('Commercial Services').closest('a')).toHaveAttribute('href', 'https://www.wellsfargo.com/com/');
  expect(screen.getByText('Service Descriptions').closest('a')).toHaveAttribute('href', 'https://www.wellsfargo.com/com/services_all');
  expect(screen.getByText('Terms of Use').closest('a')).toHaveAttribute('href', 'https://wellsoffice.wellsfargo.com/ceoportal/appmanager/ceoPortal/ceoDesktop?_nfpb=true&_pageLabel=PortalSupport&portalSupportNodeName=gotoTermsOfUse&terms=true');
});
```

### Explanation

1. **Render Component**: The `Footer_page` component is rendered using the `render` function from React Testing Library.
2. **Check Text Content**: The test checks if the `Footer` text and all link labels are present in the document.
3. **Check Links**: The test verifies that each link has the correct `href` attribute.

### Running the Tests

To run the tests, ensure you have Jest and React Testing Library set up in your project. You can run the tests using the following command:

```bash
npm test
```

This command will execute all test files and output the results, showing which tests passed and which failed.









To test the `DateTimeRangePicker` component in Jest with React Testing Library, you need to verify that the component renders correctly, handles state changes, and submits the form. Here's how you can write a test case for it.

### DateTimeRangePicker Component

First, let's format and complete the component code properly:

#### `DateTimeRangePicker.js`
```javascript
import React from 'react';

const DateTimeRangePicker = ({ setShowRealTime, startDateTime, setStartDateTime, endDateTime, setEndDateTime }) => {
  const handleSubmit = (event) => {
    event.preventDefault();
    setShowRealTime(false);
  };

  const containerStyle = {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    color: '#333',
    fontFamily: "WF Sans Regular, arial, helvetica",
    gap: "12px",
  };

  const inputStyle = {
    margin: '10px 0',
    padding: '10px',
    borderRadius: '5px',
    border: '1px solid #ccc',
  };

  const buttonStyle = {
    padding: '10px 20px',
    borderRadius: '5px',
    border: 'none',
    backgroundColor: '#d71e28',
    color: '#fff',
    cursor: 'pointer',
  };

  return (
    <div className="main-body" style={{ marginTop: "0px" }}>
      <form onSubmit={handleSubmit} style={containerStyle}>
        <label>
          Start:
          <input
            type="datetime-local"
            value={startDateTime}
            onChange={(e) => setStartDateTime(e.target.value)}
            style={inputStyle}
          />
        </label>
        <label>
          End:
          <input
            type="datetime-local"
            value={endDateTime}
            onChange={(e) => setEndDateTime(e.target.value)}
            style={inputStyle}
          />
        </label>
        <button type="submit" style={buttonStyle}>Submit</button>
        <button
          type="button"
          style={buttonStyle}
          onClick={() => { setShowRealTime(false); setShowRealTime(true); }}
        >
          Reset
        </button>
      </form>
    </div>
  );
};

export default DateTimeRangePicker;
```

### Test Case with Jest and React Testing Library

Now, let's write a test case for this component.

#### `DateTimeRangePicker.test.js`
```javascript
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import DateTimeRangePicker from './DateTimeRangePicker';

test('renders DateTimeRangePicker and handles input and submission', () => {
  const setShowRealTime = jest.fn();
  const setStartDateTime = jest.fn();
  const setEndDateTime = jest.fn();
  const startDateTime = '2023-01-01T00:00';
  const endDateTime = '2023-01-01T23:59';

  render(
    <DateTimeRangePicker
      setShowRealTime={setShowRealTime}
      startDateTime={startDateTime}
      setStartDateTime={setStartDateTime}
      endDateTime={endDateTime}
      setEndDateTime={setEndDateTime}
    />
  );

  // Check if inputs are rendered with initial values
  expect(screen.getByLabelText(/Start:/i)).toHaveValue(startDateTime);
  expect(screen.getByLabelText(/End:/i)).toHaveValue(endDateTime);

  // Simulate changing the start date time
  fireEvent.change(screen.getByLabelText(/Start:/i), { target: { value: '2023-01-02T00:00' } });
  expect(setStartDateTime).toHaveBeenCalledWith('2023-01-02T00:00');

  // Simulate changing the end date time
  fireEvent.change(screen.getByLabelText(/End:/i), { target: { value: '2023-01-02T23:59' } });
  expect(setEndDateTime).toHaveBeenCalledWith('2023-01-02T23:59');

  // Simulate form submission
  fireEvent.submit(screen.getByRole('form'));
  expect(setShowRealTime).toHaveBeenCalledWith(false);

  // Simulate reset button click
  fireEvent.click(screen.getByText(/Reset/i));
  expect(setShowRealTime).toHaveBeenCalledTimes(2);
});
```

### Explanation

1. **Mock Functions**: Use `jest.fn()` to create mock functions for `setShowRealTime`, `setStartDateTime`, and `setEndDateTime`.
2. **Render Component**: Use `render` to render the `DateTimeRangePicker` component with mock props.
3. **Initial Value Checks**: Verify that the input elements are rendered with the correct initial values using `screen.getByLabelText` and `expect`.
4. **Simulate Input Change**: Use `fireEvent.change` to simulate changing the input values and verify that the appropriate mock functions are called with the correct arguments.
5. **Simulate Form Submission**: Use `fireEvent.submit` to simulate form submission and verify that `setShowRealTime` is called correctly.
6. **Simulate Reset Button Click**: Use `fireEvent.click` to simulate clicking the reset button and verify that `setShowRealTime` is called correctly again.

This test case ensures that the `DateTimeRangePicker` component renders correctly, handles state changes, and submits the form as expected.





To test the `DateTimeRangePicker` component in Jest with React Testing Library, you need to verify that the component renders correctly, handles state changes, and submits the form. Here's how you can write a test case for it.

### DateTimeRangePicker Component

First, let's format and complete the component code properly:

#### `DateTimeRangePicker.js`
```javascript
import React from 'react';

const DateTimeRangePicker = ({ setShowRealTime, startDateTime, setStartDateTime, endDateTime, setEndDateTime }) => {
  const handleSubmit = (event) => {
    event.preventDefault();
    setShowRealTime(false);
  };

  const containerStyle = {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    color: '#333',
    fontFamily: "WF Sans Regular, arial, helvetica",
    gap: "12px",
  };

  const inputStyle = {
    margin: '10px 0',
    padding: '10px',
    borderRadius: '5px',
    border: '1px solid #ccc',
  };

  const buttonStyle = {
    padding: '10px 20px',
    borderRadius: '5px',
    border: 'none',
    backgroundColor: '#d71e28',
    color: '#fff',
    cursor: 'pointer',
  };

  return (
    <div className="main-body" style={{ marginTop: "0px" }}>
      <form onSubmit={handleSubmit} style={containerStyle}>
        <label>
          Start:
          <input
            type="datetime-local"
            value={startDateTime}
            onChange={(e) => setStartDateTime(e.target.value)}
            style={inputStyle}
          />
        </label>
        <label>
          End:
          <input
            type="datetime-local"
            value={endDateTime}
            onChange={(e) => setEndDateTime(e.target.value)}
            style={inputStyle}
          />
        </label>
        <button type="submit" style={buttonStyle}>Submit</button>
        <button
          type="button"
          style={buttonStyle}
          onClick={() => { setShowRealTime(false); setShowRealTime(true); }}
        >
          Reset
        </button>
      </form>
    </div>
  );
};

export default DateTimeRangePicker;
```

### Test Case with Jest and React Testing Library

Now, let's write a test case for this component.

#### `DateTimeRangePicker.test.js`
```javascript
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import DateTimeRangePicker from './DateTimeRangePicker';

test('renders DateTimeRangePicker and handles input and submission', () => {
  const setShowRealTime = jest.fn();
  const setStartDateTime = jest.fn();
  const setEndDateTime = jest.fn();
  const startDateTime = '2023-01-01T00:00';
  const endDateTime = '2023-01-01T23:59';

  render(
    <DateTimeRangePicker
      setShowRealTime={setShowRealTime}
      startDateTime={startDateTime}
      setStartDateTime={setStartDateTime}
      endDateTime={endDateTime}
      setEndDateTime={setEndDateTime}
    />
  );

  // Check if inputs are rendered with initial values
  expect(screen.getByLabelText(/Start:/i)).toHaveValue(startDateTime);
  expect(screen.getByLabelText(/End:/i)).toHaveValue(endDateTime);

  // Simulate changing the start date time
  fireEvent.change(screen.getByLabelText(/Start:/i), { target: { value: '2023-01-02T00:00' } });
  expect(setStartDateTime).toHaveBeenCalledWith('2023-01-02T00:00');

  // Simulate changing the end date time
  fireEvent.change(screen.getByLabelText(/End:/i), { target: { value: '2023-01-02T23:59' } });
  expect(setEndDateTime).toHaveBeenCalledWith('2023-01-02T23:59');

  // Simulate form submission
  fireEvent.submit(screen.getByRole('form'));
  expect(setShowRealTime).toHaveBeenCalledWith(false);

  // Simulate reset button click
  fireEvent.click(screen.getByText(/Reset/i));
  expect(setShowRealTime).toHaveBeenCalledTimes(2);
});
```

### Explanation

1. **Mock Functions**: Use `jest.fn()` to create mock functions for `setShowRealTime`, `setStartDateTime`, and `setEndDateTime`.
2. **Render Component**: Use `render` to render the `DateTimeRangePicker` component with mock props.
3. **Initial Value Checks**: Verify that the input elements are rendered with the correct initial values using `screen.getByLabelText` and `expect`.
4. **Simulate Input Change**: Use `fireEvent.change` to simulate changing the input values and verify that the appropriate mock functions are called with the correct arguments.
5. **Simulate Form Submission**: Use `fireEvent.submit` to simulate form submission and verify that `setShowRealTime` is called correctly.
6. **Simulate Reset Button Click**: Use `fireEvent.click` to simulate clicking the reset button and verify that `setShowRealTime` is called correctly again.

This test case ensures that the `DateTimeRangePicker` component renders correctly, handles state changes, and submits the form as expected.









To test the `DateTimeRangePicker` component in Jest with React Testing Library, you need to verify that the component renders correctly, handles state changes, and submits the form. Here's how you can write a test case for it.

### DateTimeRangePicker Component

First, let's format and complete the component code properly:

#### `DateTimeRangePicker.js`
```javascript
import React from 'react';

const DateTimeRangePicker = ({ setShowRealTime, startDateTime, setStartDateTime, endDateTime, setEndDateTime }) => {
  const handleSubmit = (event) => {
    event.preventDefault();
    setShowRealTime(false);
  };

  const containerStyle = {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    color: '#333',
    fontFamily: "WF Sans Regular, arial, helvetica",
    gap: "12px",
  };

  const inputStyle = {
    margin: '10px 0',
    padding: '10px',
    borderRadius: '5px',
    border: '1px solid #ccc',
  };

  const buttonStyle = {
    padding: '10px 20px',
    borderRadius: '5px',
    border: 'none',
    backgroundColor: '#d71e28',
    color: '#fff',
    cursor: 'pointer',
  };

  return (
    <div className="main-body" style={{ marginTop: "0px" }}>
      <form onSubmit={handleSubmit} style={containerStyle}>
        <label>
          Start:
          <input
            type="datetime-local"
            value={startDateTime}
            onChange={(e) => setStartDateTime(e.target.value)}
            style={inputStyle}
          />
        </label>
        <label>
          End:
          <input
            type="datetime-local"
            value={endDateTime}
            onChange={(e) => setEndDateTime(e.target.value)}
            style={inputStyle}
          />
        </label>
        <button type="submit" style={buttonStyle}>Submit</button>
        <button
          type="button"
          style={buttonStyle}
          onClick={() => { setShowRealTime(false); setShowRealTime(true); }}
        >
          Reset
        </button>
      </form>
    </div>
  );
};

export default DateTimeRangePicker;
```

### Test Case with Jest and React Testing Library

Now, let's write a test case for this component.

#### `DateTimeRangePicker.test.js`
```javascript
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import DateTimeRangePicker from './DateTimeRangePicker';

test('renders DateTimeRangePicker and handles input and submission', () => {
  const setShowRealTime = jest.fn();
  const setStartDateTime = jest.fn();
  const setEndDateTime = jest.fn();
  const startDateTime = '2023-01-01T00:00';
  const endDateTime = '2023-01-01T23:59';

  render(
    <DateTimeRangePicker
      setShowRealTime={setShowRealTime}
      startDateTime={startDateTime}
      setStartDateTime={setStartDateTime}
      endDateTime={endDateTime}
      setEndDateTime={setEndDateTime}
    />
  );

  // Check if inputs are rendered with initial values
  expect(screen.getByLabelText(/Start:/i)).toHaveValue(startDateTime);
  expect(screen.getByLabelText(/End:/i)).toHaveValue(endDateTime);

  // Simulate changing the start date time
  fireEvent.change(screen.getByLabelText(/Start:/i), { target: { value: '2023-01-02T00:00' } });
  expect(setStartDateTime).toHaveBeenCalledWith('2023-01-02T00:00');

  // Simulate changing the end date time
  fireEvent.change(screen.getByLabelText(/End:/i), { target: { value: '2023-01-02T23:59' } });
  expect(setEndDateTime).toHaveBeenCalledWith('2023-01-02T23:59');

  // Simulate form submission
  fireEvent.submit(screen.getByRole('form'));
  expect(setShowRealTime).toHaveBeenCalledWith(false);

  // Simulate reset button click
  fireEvent.click(screen.getByText(/Reset/i));
  expect(setShowRealTime).toHaveBeenCalledTimes(2);
});
```

### Explanation

1. **Mock Functions**: Use `jest.fn()` to create mock functions for `setShowRealTime`, `setStartDateTime`, and `setEndDateTime`.
2. **Render Component**: Use `render` to render the `DateTimeRangePicker` component with mock props.
3. **Initial Value Checks**: Verify that the input elements are rendered with the correct initial values using `screen.getByLabelText` and `expect`.
4. **Simulate Input Change**: Use `fireEvent.change` to simulate changing the input values and verify that the appropriate mock functions are called with the correct arguments.
5. **Simulate Form Submission**: Use `fireEvent.submit` to simulate form submission and verify that `setShowRealTime` is called correctly.
6. **Simulate Reset Button Click**: Use `fireEvent.click` to simulate clicking the reset button and verify that `setShowRealTime` is called correctly again.

This test case ensures that the `DateTimeRangePicker` component renders correctly, handles state changes, and submits the form as expected.






import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import DateTimeRangePicker from './DateTimeRangePicker';

test('renders DateTimeRangePicker and handles input and submission', () => {
  const setShowRealTime = jest.fn();
  const setStartDateTime = jest.fn();
  const setEndDateTime = jest.fn();
  const startDateTime = '2023-01-01T00:00';
  const endDateTime = '2023-01-01T23:59';

  render(
    <DateTimeRangePicker
      setShowRealTime={setShowRealTime}
      startDateTime={startDateTime}
      setStartDateTime={setStartDateTime}
      endDateTime={endDateTime}
      setEndDateTime={setEndDateTime}
    />
  );

  // Check if inputs are rendered with initial values
  expect(screen.getByLabelText(/Start:/i)).toHaveValue(startDateTime);
  expect(screen.getByLabelText(/End:/i)).toHaveValue(endDateTime);

  // Simulate changing the start date time
  fireEvent.change(screen.getByLabelText(/Start:/i), { target: { value: '2023-01-02T00:00' } });
  expect(setStartDateTime).toHaveBeenCalledWith('2023-01-02T00:00');

  // Simulate changing the end date time
  fireEvent.change(screen.getByLabelText(/End:/i), { target: { value: '2023-01-02T23:59' } });
  expect(setEndDateTime).toHaveBeenCalledWith('2023-01-02T23:59');

  // Simulate form submission
  fireEvent.submit(screen.getByRole('form'));
  expect(setShowRealTime).toHaveBeenCalledWith(false);

  // Simulate reset button click
  fireEvent.click(screen.getByText(/Reset/i));
  expect(setShowRealTime).toHaveBeenCalledTimes(2);
});

 
 
 
 
 
 
 
 
 
 
 plugins and polyfills you need based on your targeted environments.
2. **`@babel/preset-react`**: This preset is specifically designed for transforming React JSX syntax into JavaScript.
3. **`@babel/plugin-syntax-jsx`**: This plugin allows Babel to parse JSX syntax but doesn't transform it. This is useful if you are using a different tool for the actual transformation or if you only need to parse JSX for some reason.

### Example Project Structure

Here's an example of what your project structure might look like:

```
my-project/
├── node_modules/
├── src/
│   ├── index.js
│   └── CandlestickChart.js
├── .babelrc
├── package.json
└── yarn.lock (or package-lock.json)
```

### Running Babel

If you don't already have a build script set up, you can add one to your `package.json`:

```json
{
  "scripts": {
    "build": "babel src --out-dir dist"
  }
}
```

Then run the build script with:

```bash
npm run build
```

This will transform your source files in the `src` directory and output the results to the `dist` directory.

By following these steps, you should be able to enable JSX transformation or parsing in your project using Babel.



using `screen.getByRole`.

2. **Integration Test with Puppeteer**:
   - Use Puppeteer to launch a headless browser and navigate to your application's URL.
   - Wait for the `canvas` element to appear in the DOM using `page.waitForSelector`.
   - Verify the presence of the `canvas` element using `page.$eval`.
   - Optionally take a screenshot for visual verification.

### Running the Tests

- **Unit Tests**: Run using `npm test` or `npx jest`.
- **Integration Tests**: Add a separate script in `package.json`:
  ```json
  "scripts": {
    "test": "jest",
    "test:puppeteer": "jest --config=puppeteer.config.js"
  }
  ```

Create `puppeteer.config.js` for configuring Jest to run Puppeteer tests:
```javascript
module.exports = {
  preset: 'jest-puppeteer',
};
```

Run the Puppeteer tests with:
```bash
npm run test:puppeteer
```

This setup ensures comprehensive testing of your graph module, covering both the logic and the actual rendering in the browser.






To create a Socket.IO client in JavaScript, you will need to follow these steps:

### Step 1: Install the `socket.io-client` Library

If you're using a package manager like npm, you can install the `socket.io-client` library:

```sh
npm install socket.io-client
```

### Step 2: Create a JavaScript File for the Socket.IO Client

Here's a basic example of how to set up a Socket.IO client in JavaScript:

```javascript
// Import the Socket.IO client library
import { io } from "socket.io-client";

// Connect to the server
const socket = io('http://localhost:3000'); // Replace with your server URL

// Listen for the 'connect' event
socket.on('connect', () => {
  console.log('Connected to the server');
});

// Listen for the 'disconnect' event
socket.on('disconnect', () => {
  console.log('Disconnected from the server');
});

// Listen for custom events from the server
socket.on('message', (data) => {
  console.log('Message from server:', data);
});

// Emit events to the server
socket.emit('message', { msg: 'Hello, server!' });

```

### Explanation

1. **Import the Socket.IO Client Library**: Use `import { io } from "socket.io-client";` to import the Socket.IO client library.
2. **Connect to the Server**: Use `io('http://localhost:3000')` to connect to the Socket.IO server. Replace `'http://localhost:3000'` with your server's URL.
3. **Listen for Connection Events**:
   - `socket.on('connect', () => { ... })` listens for the 'connect' event, which is emitted when the client successfully connects to the server.
   - `socket.on('disconnect', () => { ... })` listens for the 'disconnect' event, which is emitted when the client is disconnected from the server.
4. **Listen for Custom Events**: Use `socket.on('message', (data) => { ... })` to listen for custom events from the server. In this example, we listen for a 'message' event and log the data received from the server.
5. **Emit Events to the Server**: Use `socket.emit('message', { ... })` to emit events to the server. In this example, we emit a 'message' event with some data.

### Step 3: Running the Client

Save the JavaScript file (e.g., `client.js`) and run it in your environment where you have set up a Socket.IO server running at the specified URL. If you're using a web browser environment, include the script in your HTML file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Socket.IO Client</title>
  <script src="/path/to/your/client.js" defer></script>
</head>
<body>
  <h1>Socket.IO Client</h1>
</body>
</html>
```

If you're using a Node.js environment, you can run the client script using:

```sh
node client.js
```

This will establish a connection to the Socket.IO server and handle events as specified in the script.





// Import the Socket.IO client library
import { io } from "socket.io-client";

// Connect to the server
const socket = io('http://localhost:3000'); // Replace with your server URL

// Listen for the 'connect' event
socket.on('connect', () => {
  console.log('Connected to the server');
});

// Listen for the 'disconnect' event
socket.on('disconnect', () => {
  console.log('Disconnected from the server');
});

// Listen for custom events from the server
socket.on('message', (data) => {
  console.log('Message from server:', data);
});

// Emit events to the server
socket.emit('message', { msg: 'Hello, server!' });






Here’s a sample design document for a Trading Recommendation System:

---

**Title Page**

- **Project Title**: Trading Recommendation System
- **Author(s)**: Jane Doe, John Smith
- **Date**: June 27, 2024
- **Version**: 1.0

---

**Table of Contents**

1. Introduction
2. Project Overview
3. Requirements
4. System Architecture
5. Detailed Design
6. User Interface Design
7. Security Considerations
8. Testing and Validation
9. Deployment Plan
10. Maintenance and Support
11. Appendices
12. Revision History

---

**1. Introduction**

**Purpose**: This document outlines the design for a Trading Recommendation System that provides trading recommendations based on market data analysis.

**Scope**: The system will analyze market trends and data to recommend buy or sell actions for stocks and other financial instruments.

**Audience**: This document is intended for software developers, system architects, and stakeholders involved in the project.

**Overview**: The document covers the system’s architecture, components, user interface, security considerations, and testing plan.

---

**2. Project Overview**

**Background**: With the growing complexity of financial markets, traders need automated systems to assist in making informed decisions.

**Objectives**: 
- Develop a system that provides accurate trading recommendations.
- Ensure real-time data processing and analysis.
- Maintain high levels of security and reliability.

**Stakeholders**:
- Traders
- Financial Analysts
- IT Support Team
- Project Managers

---

**3. Requirements**

**Functional Requirements**:
- Analyze market data in real-time.
- Generate buy/sell recommendations.
- Provide a user interface for viewing recommendations.
- Allow users to configure alert thresholds.

**Non-functional Requirements**:
- High availability and reliability.
- Fast processing of data streams.
- Secure handling of user data.

**Constraints**:
- Limited to publicly available market data.
- Must comply with relevant financial regulations.

---

**4. System Architecture**

**High-Level Architecture**: 

- **Data Ingestion**: Collects market data from various sources.
- **Data Processing**: Analyzes data to identify trends and generate recommendations.
- **Recommendation Engine**: Core logic for making buy/sell decisions.
- **User Interface**: Displays recommendations and alerts to users.

**Components**:
- **Data Ingestion Module**: APIs for fetching market data.
- **Processing Engine**: Algorithms for trend analysis and signal generation.
- **Recommendation Engine**: Decision-making algorithms.
- **User Interface**: Web-based dashboard.

**Data Flow**:
1. Market data is ingested.
2. Data is processed to identify trends.
3. Recommendations are generated.
4. Recommendations are displayed on the user interface.

---

**5. Detailed Design**

**Component Design**:
- **Data Ingestion Module**: Uses REST APIs to fetch data from market sources.
- **Processing Engine**: Utilizes machine learning algorithms for trend analysis.
- **Recommendation Engine**: Implements decision trees for generating recommendations.

**Interfaces**:
- **Data Ingestion Module ↔ Processing Engine**: JSON data exchange.
- **Processing Engine ↔ Recommendation Engine**: Internal data structures.
- **Recommendation Engine ↔ User Interface**: REST API for recommendation data.

**Data Models**:
- **Market Data**: Timestamp, price, volume, etc.
- **Recommendations**: Signal (buy/sell), confidence score, timestamp.

---

**6. User Interface Design**

**Wireframes**:
- **Dashboard**: Overview of market trends and recommendations.
- **Detail View**: Detailed analysis of a specific stock or instrument.
- **Alerts**: Notifications for configured thresholds.

**User Flows**:
1. User logs in.
2. User views dashboard.
3. User clicks on a specific recommendation for details.
4. User sets alert thresholds.

---

**7. Security Considerations**

**Threat Model**:
- Unauthorized access to user data.
- Data tampering and injection attacks.

**Security Measures**:
- **Authentication**: Multi-factor authentication for users.
- **Data Encryption**: Encrypt data in transit and at rest.
- **Input Validation**: Sanitize inputs to prevent injection attacks.

---

**8. Testing and Validation**

**Test Plan**:
- Unit tests for individual components.
- Integration tests for combined modules.
- System tests for end-to-end functionality.

**Test Cases**:
- **Data Ingestion**: Verify data is correctly fetched from sources.
- **Processing Engine**: Validate trend analysis algorithms.
- **Recommendation Engine**: Ensure accurate recommendation generation.
- **User Interface**: Check usability and responsiveness.

**Validation**: Compare system recommendations with actual market performance to validate accuracy.

---

**9. Deployment Plan**

**Environment**:
- **Development**: Local and staging environments.
- **Production**: Cloud-based environment for scalability.

**Deployment Steps**:
1. Code review and testing.
2. Deploy to staging environment.
3. Perform user acceptance testing.
4. Deploy to production environment.

**Rollback Plan**:
- Maintain previous stable version for rollback in case of issues.

---

**10. Maintenance and Support**

**Maintenance Plan**:
- Regular updates for market data sources.
- Periodic review of algorithm performance.
- Scheduled security audits.

**Support**:
- Dedicated support team for user queries and issues.
- Online documentation and FAQs.

---

**11. Appendices**

**Glossary**:
- **API**: Application Programming Interface
- **JSON**: JavaScript Object Notation

**References**:
- Financial market data sources
- Machine learning libraries

---

**12. Revision History**

**Change Log**:
- **v1.0**: Initial document release (June 27, 2024)

---

This sample document provides a structured approach to designing a Trading Recommendation System. Adjust the content and sections as necessary to fit the specific needs and requirements of your project.








A design document, often referred to as a design doc, is a comprehensive guide that outlines the architecture, components, and processes of a project. Here’s a general structure to help you get started:

1. **Title Page**
   - Project Title
   - Author(s)
   - Date
   - Version

2. **Table of Contents**
   - List of sections and subsections with page numbers

3. **Introduction**
   - **Purpose**: Explain the purpose of the document and the project.
   - **Scope**: Define the scope of the project.
   - **Audience**: Identify the intended audience for the document.
   - **Overview**: Provide a brief overview of what the document contains.

4. **Project Overview**
   - **Background**: Context and background information about the project.
   - **Objectives**: Clear and measurable objectives of the project.
   - **Stakeholders**: List of stakeholders involved in the project.

5. **Requirements**
   - **Functional Requirements**: Specific behaviors or functions of the system.
   - **Non-functional Requirements**: Performance, security, usability, etc.
   - **Constraints**: Any limitations or constraints affecting the design.

6. **System Architecture**
   - **High-Level Architecture**: Overview of the system architecture with diagrams.
   - **Components**: Description of major system components.
   - **Data Flow**: Data flow diagrams or descriptions.

7. **Detailed Design**
   - **Component Design**: Detailed design of each component.
   - **Interfaces**: Description of interfaces between components.
   - **Data Models**: Database schemas, data models, and related information.

8. **User Interface Design**
   - **Wireframes**: Sketches or wireframes of key screens.
   - **User Flows**: Descriptions or diagrams of user flows.

9. **Security Considerations**
   - **Threat Model**: Potential security threats and mitigation strategies.
   - **Security Measures**: Specific security measures implemented.

10. **Testing and Validation**
    - **Test Plan**: Plan for testing the system.
    - **Test Cases**: Specific test cases with expected outcomes.
    - **Validation**: How the system will be validated against requirements.

11. **Deployment Plan**
    - **Environment**: Description of the deployment environment.
    - **Deployment Steps**: Steps for deploying the system.
    - **Rollback Plan**: Plan for rolling back if deployment fails.

12. **Maintenance and Support**
    - **Maintenance Plan**: Plan for ongoing maintenance.
    - **Support**: Support processes and contacts.

13. **Appendices**
    - **Glossary**: Definitions of terms used in the document.
    - **References**: References to other documents or resources.

14. **Revision History**
    - **Change Log**: Record of changes made to the document.

When writing a design document, aim for clarity and conciseness. Use diagrams and visual aids to supplement the text and make complex information more accessible.






The error you're encountering, `SQLite objects created in a thread can only be used in that same thread`, occurs because SQLite connections are not thread-safe. When you try to use the same SQLite connection in multiple threads, it leads to this error. 

To prevent this, you need to ensure that each thread or async task gets its own database connection. Here are some ways to handle this:

1. **Connection Pooling**: Use a connection pool to manage SQLite connections. This ensures that each thread gets a fresh connection from the pool.

2. **Pass Connections to Threads**: Create a new connection in each thread or async task.

Here's an example of how you can modify your code to create a new SQLite connection for each async task:

### Modified Code

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import json
import pandas as pd
from process import Indicator
from engine import AnalysisEngine
from minordb.db_controller import DBController

# Database Controller Initialization
# Removed global dbController to prevent shared usage in threads

def get_db_controller():
    return DBController()

def fetch_data(topic, db_controller):
    prev_data = db_controller.findStockDataByCompanyId(topic)
    columns = ['companyId', 'frame', 'open', 'close', 'high', 'low', 'volume', 'timestamp', 'UpperBand', 'LowerBand', 
               'MACD', 'MACD_Signal', 'MACD_Hist', 'vwap', 'rsi', 'obv', 'ema_5', 'ema_13', 'ema_26', 'supertrend']
    new_stock = pd.DataFrame(columns=columns)
    
    if len(prev_data) == 0:
        return new_stock

    for _dict in prev_data:
        data = pd.DataFrame([_dict])
        data = data.reindex(columns=columns)  # Ensure columns are in the correct order and missing columns are added as NaN
        data.dropna(axis=1, how="all", inplace=True)
        new_stock = pd.concat([new_stock, data], ignore_index=True)

    return new_stock

def add_message_to_dataframe(topic, message, db_controller):
    new_stock = fetch_data(topic, db_controller)
    new_stock.dropna(axis=1, how="all", inplace=True)
    new_stock = pd.concat([new_stock, message], ignore_index=True)

    indicator = Indicator(new_stock)
    results = indicator.process_data()

    new_data = new_stock.iloc[-1].copy()
    new_data['UpperBand'] = results[0][0]
    new_data['LowerBand'] = results[0][1]
    new_data['MACD'] = results[1][0]
    new_data['MACD_Signal'] = results[1][1]
    new_data['MACD_Hist'] = results[1][2]
    new_data['vwap'] = results[2]
    new_data['rsi'] = results[3]
    new_data['obv'] = results[4]
    new_data['ema_5'] = results[5][0]
    new_data['ema_13'] = results[5][1]
    new_data['ema_26'] = results[5][2]
    new_data['supertrend'] = results[6]

    return new_data

def process_message(msg, topic):
    topic = str(topic)
    df_po = pd.DataFrame([msg])
    db_controller = get_db_controller()  # Create a new DB controller for this thread
    new_data = add_message_to_dataframe(topic, df_po, db_controller)
    new_data = new_data.to_frame().T

    stock = fetch_data(topic, db_controller)
    stock.dropna(axis=1, how="all", inplace=True)
    stock = pd.concat([stock, new_data], ignore_index=True)

    AnalysisEngine(stock)

    result_dict = (stock.iloc[-1]).to_dict()
    res = db_controller.insertStockData(result_dict)
    print(res)
    return stock.iloc[-1]

async def process_partition_messages(topic, message_queue, lock, executor):
    loop = asyncio.get_running_loop()
    while True:
        message = await message_queue.get()
        if message is None:
            break
        try:
            result = await loop.run_in_executor(executor, process_message, message, topic)
            message_queue.task_done()
            return result
        except asyncio.CancelledError:
            print("Task cancelled")
            break

class EngineServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.partition_locks = defaultdict(asyncio.Lock)
        self.partition_queues = defaultdict(asyncio.Queue)
        self.executor = ThreadPoolExecutor(max_workers=10)

    async def handle_request(self, reader, writer):
        try:
            # Read data from client
            message = await reader.read(1024)
            data = message.decode()

            # Parse JSON data
            msg = json.loads(data)
            jon = pd.DataFrame([msg])

            part = str(jon['frame'].iloc[0])
            topic = str(jon['companyId'].iloc[0])

            lock = self.partition_locks[topic]
            queue = self.partition_queues[topic]

            await queue.put(msg)

            res = asyncio.create_task(process_partition_messages(topic, queue, lock, self.executor))
            result = await res

            result_json = result.to_json()
            result_str = str(result_json)

            print(result_str)
            writer.write(result_str.encode())
            await writer.drain()
        except Exception as e:
            response = f"Error: {str(e)}"
            writer.write(response.encode())
            await writer.drain()

    async def start_server(self):
        server = await asyncio.start_server(self.handle_request, self.host, self.port)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Server is running at {addrs}')
        async with server:
            await server.serve_forever()

async def main():
    server = EngineServer('localhost', 12345)
    await server.start_server()

if __name__ == "__main__":
    dbController = get_db_controller()  # Setup initial DB controller to create tables, etc.
    print(dbController.setup("./databases/stock.db", 35))
    asyncio.run(main())
```

### Key Changes:
1. **Removed Global DB Controller**: The `dbController` is not shared globally to avoid cross-thread issues.
2. **New DB Controller Per Task**: Added a function `get_db_controller()` to create a new `DBController` instance for each thread or async task.
3. **Reindexing DataFrame**: Ensured DataFrame has the correct columns and added as NaN if missing.
4. **Isolated Database Operations**: Database operations are now confined to the thread or task that initiated them, ensuring thread safety.

By making these changes, each thread or async task gets its own connection to the database, preventing the cross-thread SQLite usage issue.
