docker build -t maskimage .

docker run -d --name maskapp-container -p 8000:8000 maskimage


request_body:

{"input":"i was born on 13/03/2000 and my number is 0990989899 crdit card number is 0987654321234567 and my name is kiran and i am from Mumbai"}    