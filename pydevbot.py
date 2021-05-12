from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import time
import time as t
import smtplib

def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login("impowaste39@gmail.com","<password>")
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail("impowaste39@gmail.com", "impowaste39@gmail.com", message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email not sent!")

with Display():
    browser = webdriver.Firefox()
    try:
        browser.implicitly_wait(20)
        browser.get('https://notpydev.pythonanywhere.com')
        start = time()
        username = browser.find_element_by_id('username').send_keys('karthikeyan59')
        password = browser.find_element_by_id('password').send_keys('karthi123')
        signin = browser.find_element_by_id('signin').click()
        print('logged in successfull')
        t.sleep(1)
        newpost = browser.find_element_by_id('newpost').click()
        title = browser.find_element_by_id('title').send_keys('PyDev Bot')
        content = browser.find_element_by_id('content').send_keys('python is awesome AF')
        t.sleep(1)
        addpost = browser.find_element_by_id('addpost').click()
        print('post successful')
        like = browser.find_element_by_id('like').click()
        print('like successful')
        t.sleep(1)
        searchbar = browser.find_element_by_id('searchbar')
        searchbar.send_keys('pydev bot')
        t.sleep(2)
        searchbar.send_keys(Keys.ENTER)
        t.sleep(2)
        content = browser.find_element_by_id('content').send_keys("that's true")
        addcomment = browser.find_element_by_id('addcomment').click()
        t.sleep(1)
        print('comment successful')
        t.sleep(1)
        deletecomment = browser.find_element_by_id('deletecomment').click()
        print('delete comment successful')
        home = browser.find_element_by_link_text('Home').click()
        t.sleep(1)
        unlike = browser.find_element_by_id('unlike').click()
        print('like unlike successful')
        deletepost = browser.find_element_by_id('deletepost').click()
        print('postdeleted')
        t.sleep(1)
        logout = browser.find_element_by_link_text('Logout').click()
        print('success')
        total = time() - start
        actual = time() - start - 11
        browser.quit()
        subject = "Hello From NotPyDev"
        msg = "Hello Master KARTHIKEYAN\n\nTask 1:We are from DB department(code:001),we are good and running!.\n\nTask 2:We are from TEMPLATES department(code:002),we are good and running!.\n\nTask 3:We are from STATIC department(code:003),we are good and running!.\n\nTask 4:We are from VIEWS department(code:004),we are good and running!.\n\nTotal runtime {:.2f} seconds.\n\nActual runtime {:.2f} seconds.\n\nThis is your PyDev Bot ,ALL SYSTEMS RUNNING SUCCESSFULLY!!.\n\nvisit:https://notpydev.pythonanywhere.com/".format(total,actual)
        send_email(subject, msg)
    finally:
        browser.quit()
