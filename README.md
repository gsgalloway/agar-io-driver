# Agar.io Driver
A tool for automating interaction with Agar.io.

## Dependencies
`chromedriver` must be on your path. Download it [here](https://sites.google.com/a/chromium.org/chromedriver/)

[Burp Suite](https://portswigger.net/burp/) requires Java. This project has been tested with Java version 1.8.0_40. Java must also be on your path.

Then `pip install -r requirements.txt`

## Use
The driver uses Burp Suite to inject a few hooks into the agar client code to make automated interaction feasible. A copy of `burp` and its dependencies is included with this project.

First run:

```bash
cd burp

# Windows
.\suite.bat

# Mac/linux
./suite.sh
```

Then run `agar_io_driver.py` as a standalone python executable or import it into your project.
