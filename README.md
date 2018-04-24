# amazon-selenium-test

This is a python selenium test project which repeats basic user behaviour on Amazon website. 

# Execution

To execute the tests, browse folder which amazon-selenium-test is located in your terminal 
and type:

```
pytest -q  test_amazon.py 
```

# Prerequisites

* Python 2.7.10
* Selenium
* Webdriver
* Pytest


# Implemented Browsers

Tests will run on ChromeDriver.


# Annotations

User config is included in file under a map named as CONFIG . 

*WARNING: Amazon needs authentication via email code after some sign in attempts.*


