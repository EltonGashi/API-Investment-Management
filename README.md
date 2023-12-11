Follow these steps:

1. go to the terminal and use this command : docker-compose up --build

2. then in order to access the upload files and all other methods for calculating u need to register first as a user in
   this link : http://127.0.0.1:8000/account/register/

in the body , form - data as key values give these

username test
email test
password Password@123
password2 Password@123

3. after you get the token go to this link : http://127.0.0.1:8000/api/upload/ , go to Header,
   and pass Authorization as key and as values pass Token and the token you got from register and upload files,
   also dont forget to upload the trade file first then the cashflows file

dont forget to pass a POST method

4. for testing the methods to calculate go to these links

pass the loan_id and the reference_date in the link

Realized Amount : http://127.0.0.1:8000/api/trade/realized-amount/<str:loan_id>/<str:reference_date>/

Remaining Invested Amount : http://127.0.0.1:8000/api/trade/remaining-invested-amount/<str:loan_id>/<str:reference_date>/

Gross Expected Amount : http://127.0.0.1:8000/api/trade/gross-expected-amount/<str:loan_id>/<str:reference_date>/

Closing Date : http://127.0.0.1:8000/api/trade/closing-date/<str:loan_id>/

Get Cashflows : http://127.0.0.1:8000/account/logout/ , and pass the token and you will be logged out .

5. If u want to log out go to this link : http://127.0.0.1:8000/api/trade/gross-expected-amount/<str:loan_id>/<str:reference_date>/
