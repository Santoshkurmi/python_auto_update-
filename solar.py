import requests
import json
import urllib.parse
import os
import random
import time 
import pathlib


def read():
    global sign
    if not os.path.isfile("solar.json"):
        with open("solar.json","w")as f:
            f.write("{}")
    with open("solar.json") as fp:
        sign = json.loads(fp.read())
        
def write(ph,si,user):
    global sign
    # read()
    sign[ph] = {"sign":si,"userid":user}
    with open("solar.json","w") as f:
        f.write(json.dumps(sign,indent=5))

def delete(ph):
    global sign
    read()
    del sign[ph]
    with open("solar.json","w") as f:
        f.write(json.dumps(sign,indent=5))

def set_fav(ph):
    global active_phone
    active_phone = ph 
    sign["fav"] = ph;
    with open("solar.json","w") as f:
        f.write(json.dumps(sign,indent=5))

read()

headers = {"User-Agent":"Android","language":'en-US','Content-Type':'application/json;charset=utf-8',
            "Host":'sharedsunpowercorp.com','Accept-Encoding':'gzip'
}
host = "http://sharedsunpowercorp.com/api/v1"
active_phone = ""
active_phone = "2071159236"
device_id = '1233453343453435343534534534353435345abcda343343'
isLogin = False
try:
    active_phone = sign['fav']
except: active_phone = ""
# print(active_phone)
bank_id = ""
amount = ""
numbers = []
product_id = None
password = None
mobile = ""
indexing = 0
rand_num=[30,31,32,33,34,35,36,37]
refer_code = ""

def c():
        global rand_num
    
        #tmp= random.randint(30,37)
        global indexing
        indexing +=1
        indexing = indexing %8
            
        return f"\u001b[{rand_num[indexing]};1m";

def gen():
    global device_id
    device_id = ""
    for i in range(40):
        num = random.randint(0,15)
        if num==10:num = 'A'
        elif num ==11:num= 'B'
        elif num ==12:num= 'C'
        elif num ==13:num= 'D'
        elif num ==14:num= 'E'
        elif num ==15:num= 'F'
        device_id = device_id + str(num)


def gen_mobile():
    num = ""
    for i in range(10):
        n = random.randint(0,9)
        num = num + str(n) 
    return num
        

bank_number = ""
bank_name = ""
username = ""
email = ""
def getBody(key):
    global refer_code
    if isLogin==False:
        uuu = sign[active_phone]["userid"]
    else:
        uuu = ""
    body = {
        "default":{"language":"en-US","appId":"com.d.c.mill.philippines"},
        # "default2":{"language":"en-US","appId":"com.d.c.mill.philippines"},
        "account_info":{"path":"/home/accountInfo"},
        "get_product_list":{"path":"/product/getProductList"},
        "buy_product":{"path":"/financial/purchaseFinancial","amount":amount,"productId":product_id},
        "team_info":{"path":"/team/teamInfoList"},
        "order_list":{"path":"/financial/financialOrderList"},
        "withdraw_list":{"path":"/pay/withdrawlist","pageSize":"10","page":"1"},
        "deposit_list":{"path":"/pay/depositrecord","pageSize":"10","page":"1"},
        "bank_list":{"path":"/bank/list"},
        "withdraw_money":{"path":"/user/withdraw","bankId":bank_id,"withdrawAmount":amount},
        "deposit_money":{"path":"/pay/deposit","payAmount":amount,"method":"onepay","mpesa":"","payClassName":"onepay","type":"1","userId":uuu},
        "login":{"path":"/sso/login","market":"debug","password":password,"mobile":"977"+mobile,"deviceNumber":device_id},
        "bank_save":{"path":'/bank/save','bankNum':bank_number,'bankName':bank_name,'userName':username,'ifsc':"",'email':email},
        "register":{"path":'/sso/register','countryName':'Nepal','mobile':'977'+mobile,'password':'abcdefg','market':'sp2','verificationCode':'','referralCode':refer_code,'href':f"http://sharedsunpowercorp.com/r/?{refer_code}%2Fsp2"}
    }

    temp = body[key]
    default =body['default']
    for a,value in default.items():
        temp[a] = value
    if isLogin==False:
        temp["sign"] =sign[active_phone]["sign"]
    
    return temp

def send(key):
    data = getBody(key);
    path = data["path"]
    del data["path"]
    # headers["Authorization"] = sign[active_phone]["sign"];
    
    response = requests.post(url=host+path,data=json.dumps(data),headers=headers).json();
    return response

def register(n):
    global refer_code,mobile,password,device_id
    password = "abcdefg"
    for i in range(0,n):
        # gen()
        refer_code = "2SKT7P5U"
        mobile = gen_mobile()
        print(f"{i+1}. {mobile}")
        res = send("register")
        if not res['state']=='200':print(res['msg']);return;
        data = res['resultData']['user']

        user_id = data['id']
        register_ip = data['registerIp']
        user_sign = res['resultData']['sign']
        write(mobile,user_sign,user_id)
        print(f"UserId: {user_id}\nIp: {register_ip}\nSign:{user_sign}\n\n")
        gen()
        res = send("login")
        print(res['msg'])
        time.sleep(5)


# register(2)
# mobile = "2071159236"
# password = "abcdefg"
# res =send("login")
# print(res['msg'])

def divider():
    print(f"\n{c()}*****{c()}********{c()}******{c()}*****{c()}\n")


def save_bank():
    global bank_number,bank_name,username,email
    username = take(f"{c()}Enter your full name:{c()} ");
    if username=="b":return
    bank_name = take(f"{c()}Enter your bank name:{c()} ");
    if bank_name=="b":return
    bank_number = take(f"{c()}Enter your account num:{c()} ");
    if bank_number=="b":return
    email = take(f"{c()}Enter your email:{c()} ");
    if email=="b":return;

    res = send("bank_save");
    divider()
    if not res['state']=="200":print(res['msg']);divider();input();return;
    data = res['resultData']
    print(f"{c()}1. BankName: {data['bankName']}\n{c()}2. BankNum: {data['bankNum']}\n{c()}3. UserName: {data['userName']}")
    divider()
    input()

def print_accounts():
    global numbers,active_phone
    ca = 1
    numbers = []
    divider()
    status = ""
    for phone in sign:
        if phone=="fav":continue
        if phone == active_phone:status="*" 
        else:status = "" 
        print(f"{ca}. {phone} {status}")
        numbers.append(phone)
        ca = ca +1
    divider()
    choice = take(f"{c()}Choose {c()}from{c()} above:{c()} ")
    if(choice == "b"): return;
    if choice[-1]=="-": choice = choice.replace("-","");delete(numbers[int(choice)-1]);print_accounts()
    else:
        active_phone = numbers[int(choice)-1]
        set_fav(active_phone)
        divider()
        print(f"{c()}Active {c()}number{c()} is set{c()} to{c()} {active_phone}{c()}")
        divider()
        input()

def take(msg):
    on = ""
    while on=="":
        on = input(msg)
        if(on =="e") :exit()
    return on;

def check_balance():
    res = send("account_info")
    data = res['resultData']['userDO']
    id = data['id']
    mobile = data['mobile']
    balance = data['balance']
    invest = data['totalInvest']
    registerIp = data['registerIp']
    device = data['deviceNumber']
    divider()
    print(f"{c()}1. Mobile: {mobile}\n{c()}2. Balance: {balance}\n{c()}3. Invest: {invest}\n{c()}4. Id: {id}\n{c()}5. IP: {registerIp}\n{c()}6. DeviceId: {device}{c()}")
    input()

def team_info():
    res = send("team_info")['resultData']
    today_com = res['todayCommission']
    total_com = res['allCommission']
    team_size = res['teamSize']
    total_cont = res['totalContribution']
    first_bonus = res['firstBonus']
    second_bonus = res['secondBonus']
    third_bonus = res['thirdBonus']
    first_size = res['firstSize']
    second_size = res['secondSize']
    third_size = res['thirdSize']
    refCode = res['refCode']
    divider()
    print(f"{c()}1. Today Commiss: {today_com}\n{c()}2. Total Commiss: {total_com}\n{c()}3. TeamSize: {team_size}\n\
{c()}4. Total Contribution: {total_cont}\n{c()}5. FirstLevelBonus: {first_bonus} ({first_size})\n{c()}6. SecondLevelBonus: {second_bonus} ({second_size})\n{c()}7. ThirdLevelBonus: {third_bonus} ({third_size})\
        {c()}")
    divider()
    input()


def buy_product():
    global product_id,amount
    res = send("get_product_list")
    data = res['resultData']['financialProductResponseList']
    ids = []
    ca = 1
    for each in data:
        if(each['open']==0):continue
        ids.append([each['id'],each['startAmount']])
        divider()
        print(f"{c()}{ca}. Name: {each['name']}\n{c()}i. HourReturn: {each['hourReturn']}\n{c()}ii. DayReturn: {each['dayReturn']}\n{c()}iii. AllReturn: {each['allReturn']}\n{c()}iv. TotalDays: {each['lockDays']}\n{c()}v. StartAmount: {each['startAmount']}")
        ca = ca+1
    divider()
    choice = take(f"{c()}Choose{c()} from{c()} following:{c()} ")
    if choice=="b": return;
    product_id = ids[int(choice)-1][0]
    amount = ids[int(choice)-1][1]
    res = send("buy_product")
    divider()
    print(res['msg'])
    divider()
    input()



def withdraw():
    global bank_id,amount
    res = send("bank_list")['resultData']['userBankList'];
    ids = []
    ca=1
    divider()
    for each in res:
        ids.append(each['id'])
        print(f"{c()}{ca}. BankName: {each['bankName']}\n{c()}-> BankNum: {each['bankNum']}\n{c()}-> UserName: {each['userName']}\n")
        ca = ca+1
    divider()
    choice = take(f"{c()}Choose {c()}the {c()}bank:{c()} ")
    if choice == "b": return;
    bank_id = ids[int(choice)-1]
    choice = take(f"{c()}Enter {c()}the {c()}amount:{c()} ")
    if(choice == "b"): return;
    amount = choice
    
    res = send("withdraw_money")
    divider()
    print(res['msg'])
    divider()
    input()

def withdraw_record():
    res = send("withdraw_list")
    data = res['resultData']['record']
    count = 1
    divider()
    for each in data:
        userid = each['userId']
        rec_amount = each['amount']
        total_amount = each['payOutAmount']
        username = each["payOutUserName"]
        bank = each['bankName']
        account = each['accountNumber']
        fee = total_amount - rec_amount
        date = each['createTime']
        adate  = each['updateTime']
        status = each['status']
        pending = "pending"
        if status==2:pending = "success"
        print(f"{c()}{count}. BankName: {bank}\n{c()}-> BankNum: {account}\n{c()}-> Username: {username}\n{c()}->TotalAmount: {total_amount}\n{c()}->ReceiveAmount: {rec_amount}\n{c()}->Fee: {fee}\n{c()}->Date: {date}\n{c()}->UpdateTime: {adate}\n{c()}->Status: {pending}\n")
        count = count + 1
    divider()
    input()

def balance_record():
    res = send("order_list")['resultData']
    ca = 1
    divider()
    for each in res:
        print(f"{c()}{ca}. {each['productName']}\n{c()}-> TotalDays: {each['lockDays']}\n{c()}-> Amount: {each['amount']}\n{c()}-> TotalInterest: {each['totalInterest']}\n{c()}-> LastDate: {each['lastDate']}\n")
        ca = ca +1
    divider()
    input()

def recharge_record():
    res = send("deposit_list")['resultData']['record']
    ca = 1
    divider()
    status = ""
    for each in res:
        if(each['status']==1): status = "pending"
        else: status = "success"
        print(f"{c()}{ca}.Amount: {each['amount']}\n{c()}-> CreatedDate: {each['createTime']}\n{c()}-> Status: {status}\n")
        ca = ca+1

    divider()
    input()

def invite():
    res = send("account_info")['resultData']['userDO']
    refer = res['referralCode']
    link = f"http://sharedsunpowercorp.com/r/?{refer}/sp2"
    # href =urllib.parse.unquote(res['href'])
    divider()
    print(f"{c()}1. Mobile: {res['mobile']}\n{c()}2. ReferLink: {link}")
    divider()
    os.system(f"termux-open {link}")
    input()


def recharge():
    global amount;
    choose = take(f"{c()}Enter {c()}the {c()}amount {c()}to {c()}deposit:{c()}")
    if choose =='b':return
    amount = int(choose)
    res = send("deposit_money")
    divider();
    if not res['state']=="200":print(res['msg']);divider();input();return;
    print(res['resultData']['thirdUrl'])
    divider()
    os.system(f"termux-open {res['resultData']['thirdUrl']}")
    input()


def login():
    global mobile,password,isLogin
    mobile = take(f"{c()}Enter your{c()} number:{c()} ");
    if mobile=="b":return;
    password = take(f"{c()}Enter {c()}your {c()}password:{c()} ");
    if password == "b":return;
    gen()
    isLogin = True
    res = send("login")
    isLogin = False
    divider()
    if not res['state']=="200":print(res['msg']);divider();return;
    data = res['resultData']['user']
    write(mobile,res['resultData']['sign'],data['id'])
    set_fav(mobile)
    print(f"{c()}1. Id: {data['id']}\n{c()}2. DeviceId: {data['deviceNumber']}\n{c()}3. sign: {res['resultData']['sign']}")
    divider()
    input()


def main():
    func = [print_accounts,check_balance,team_info,buy_product,recharge,withdraw,withdraw_record,balance_record,recharge_record,invite,save_bank]
    while True:
        divider()
        print(f"\n{c()}1. Choose Account({active_phone})\n{c()}2. Check Balance\n{c()}3. Team Info\n{c()}4. Buy product\n{c()}5.Recharge\n{c()}6. Withdraw Money\n{c()}7. Withdraw Record\n{c()}8. Order Record\n{c()}9. Rechare Record\n{c()}10. Invite\n{c()}11. Bank Save")
        choice = take(f"{c()}Choose {c()}from {c()}above\n{c()}=>{c()}")
        if(choice == "b") :exit()
        elif choice=="l":login()
        else: func[int(choice)-1]()
        divider()
main()

