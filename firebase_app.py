import RPi.GPIO as GPIO 
import random
import pyrebase
import time

firebaseConfig = {
  "apiKey": "AIzaSyB9zuVPZb85TVl5-LtsMtjjPleP6pF6rug",
  "authDomain": "fir-app-b46e3.firebaseapp.com",
  "databaseURL": "https://fir-app-b46e3-default-rtdb.firebaseio.com",
  "projectId": "fir-app-b46e3",
  "databaseURL":"https://fir-app-b46e3-default-rtdb.firebaseio.com/",
  "storageBucket": "fir-app-b46e3.appspot.com",
  "messagingSenderId": "197150355317",
  "appId": "1:197150355317:web:406fb657d1aa685f382d3c",
  "measurementId": "G-W04RCT671S"
};
firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
auth = firebase.auth()
storage =firebase.storage()
data = {
    "0h":0,
    "2h":0,
    "4h":0,
    "6h":0,
    "8h":0,
    "10h":0,
    "12h":0,
    "14h":0,
    "16h":0,
    "18h":0,
    "20h":0,
    "22h":0,
    "Distance" : 0 
}

gapRec = {
    "hour":0
}

TRIG = 21 
ECHO = 20
GPIO.setmode(GPIO.BCM)
days = ("MON" , "TUE" , "WED" , "THU" , "FRI" , "SAT" , "SUN")
distance = 0
prevdistance = 0
i = 0 
j = 1
#Authentication 
#Login :
try:
    # email = input("Enter email : ")
    # password = input("Enter password : ")
    email = "vireshkamlapure7@gmail.com"
    password = "MitProject"
    auth.sign_in_with_email_and_password(email,password)
    print("Successful login")
except:
    print("Wrong Details ")
while i < 8:
    day = days[i]  
    j = 1
    print(day)
    while j<13:
        print("distance measurement in progress ")
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(12,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        GPIO.output(TRIG,False)
        print("Waiting for sensor to settle")
        time.sleep(2)
        GPIO.output(TRIG,True)
        time.sleep(0.00001) #wait for 10 seconds 
        GPIO.output(TRIG,False)
        while GPIO.input(ECHO)==0: #wait here till echo is HIGH
            pulse_start = time.time()
        while GPIO.input(ECHO)==1: #wait here till echo is HIGH
            pulse_end = time.time()
        pulse_duration = pulse_end-pulse_start
        distance =pulse_duration*17150
        
        prevdistance = distance 
        distance = round(distance,2)
        # distance = random.randint(1,20)

        # data["Distance"] = distance
        gapRec["hour"] = distance

        data["Distance"] = distance
        data["Day"] = day
        # print("Distance ",data["Distance"])
    
        for x in data:
            if(data[x]==0):
                hour = x
                data[x] = data["Distance"]
                break
    
        db.child("users").child(day).child(hour).push(gapRec)

        db.child("users").child(day).child(hour).set(gapRec)
        
        if((prevdistance - distance) > 5):
            GPIO.output(12,GPIO.HIGH)
        else:
            GPIO.output(12,GPIO.LOW)
        print("distance:",distance,"cm")
        
        j+=1
        
    for x in data :
        data[x] = 0 
    i+=1
