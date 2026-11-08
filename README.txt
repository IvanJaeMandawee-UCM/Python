SEMI-FINAL: SOFTWARE TESTING  -  Mandawe, Ivan Jae D.

Test_Report.pdf / Test_Report.docx   the test report
userlogin/                           the web app (register, login, logout)
tests/                               automated test script + screenshots/results of every run

RUN THE APP
  cd userlogin
  python -m venv venv
  venv\Scripts\activate            (Windows)   |   source venv/bin/activate  (Mac/Linux)
  python -m pip install flask
  python app.py
  open http://127.0.0.1:5000       sample login: alpha@uc.com / hello123  (or click "Register here")

RE-RUN THE TESTS (optional)
  python -m pip install playwright && python -m playwright install chromium
  cd tests
  python run_tests.py my-run
