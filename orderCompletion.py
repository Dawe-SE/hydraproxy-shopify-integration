import requests, json, os, logging, time, datetime, ssl, random, smtplib
from os import listdir
from smtplib import SMTP
from email.mime.text import MIMEText


headers = {'Accept': 'application/json', 'Authorization': 'Put your token here'}
logging.basicConfig(filename='completor.log', level=logging.INFO)
now = datetime.datetime.now()

sender_email = 'Put your email here'
email_pass = 'Put your password for email here'
context = ssl.create_default_context()

if not os.path.isdir('completed'):
    os.mkdir('completed')

while True:
    cwd = os.getcwd()
    fileList = os.listdir(cwd)
    if len(fileList) > 3:
        orders = []
        for file in fileList:
            if file[5] == "_":
                orders.append(file)
        with open(orders[0], 'r') as f:

            orderData = json.load(f)

        orderNumber = orderData['number']
        orderEmail = orderData['email']


        amountData = 0
        itemList = orderData["line_items"]
        for item in itemList:
            amountData += int(orderData["line_items"][itemList.index(item)]["sku"]) * orderData["line_items"][itemList.index(item)]["quantity"]


        try:
            # Send post request, get response, usr:pass
            postData = {'request_id': random.randint(1000, 100000000000), 'network': 'RESIDENTIAL',
                        'bandwidth': amountData}
            p = requests.post('https://api.hydraproxy.com/buy_proxy/', data=postData, headers=headers)

            if p.status_code == 200 and p.json()["status"] == 'OK':
                jsonObj = p.json()
                print(p.json())
                orderID = str(jsonObj['order_id'])
                username = str(jsonObj['proxy_info']['username'])
                password = str(jsonObj['proxy_info']['password'])
                print(now.strftime("%Y-%m-%d %H:%M:%S"), ' Created user', username, password)
                #logging.info(now.strftime("%Y-%m-%d %H:%M:%S") + ' Added ', amountData, 'GB to ', orderEmail,
                #             ' with order number: ', orderNumber, 'username:pass', username, password)

                try:

                    HOST = 'outlook.office365.com'
                    PORT = '587'
                    server = SMTP(host=HOST, port=PORT)
                    # create an SMTP server object
                    server.connect(host=HOST, port=PORT)
                    # connect
                    server.ehlo()
                    # extended hello; like saying hello
                    server.starttls()
                    server.ehlo()
                    server.login(user='contact@pentaproxies.com', password='Gerbilen801#')
                    # login with your credentials

                    message = """Subject: Your Penta Proxies Login Details \n\n
                    Thank you for your order!
                    Username: {}
                    Password: {}
                    Order ID: {}
                    Join our Discord to use your data!
                    """.format(username, password, orderID)
                    server.sendmail(sender_email, orderEmail, "".join(message))
                    print((now.strftime("%Y-%m-%d %H:%M:%S") + ' Successfully sent email for order:', orderID))
                    os.rename(orders[0], 'completed/'+orders[0])

                except Exception as e:
                    print(e)

            else:
                HOST = 'outlook.office365.com'
                PORT = '587'
                print(message)
                server = SMTP(host=HOST, port=PORT)
                # create an SMTP server object

                server.connect(host=HOST, port=PORT)
                # connect

                server.ehlo()
                # extended hello; like saying hello

                server.starttls()
                server.ehlo()
                server.login(user='contact@pentaproxies.com', password='Gerbilen801#')
                # login with your credentials
                message = """Subject: Your Purchase Failed \n\n
                                   Please contact support.
                                   """
                server.sendmail(sender_email, orderEmail, "".join(message))


                print('Failed adding HydraProxy, sent mail to', orderEmail)
                print(p.json())

        except Exception as e:
            print(e)




    time.sleep(10)
