import protected.passwords as pwords
from selenium import webdriver
from time import sleep

app = pwords.apps["instagram"]
username = app["username"]
password = app["password"]


XPATHS = {
    "loginButton": '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a',
    "loginUser": '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input',
    "loginPass": '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input',
    "loginSubmit": '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button',
    "dismiss": '/html/body/div[4]/div/div/div[3]/button[2]',
    "profileLink": '//*[@id="react-root"]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a',
    "followersLink": '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a',
    "followersBox": '/html/body/div[4]/div/div[2]',
    "closeButton": '/html/body/div[4]/div/div[1]/div/div[2]/button',
    "followingLink": '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'
}

class InstaBot:
    def __init__(kevin, username, password):
        kevin.username = username
        kevin.password = password
        kevin.driver = webdriver.Chrome()
        kevin.followersList = []
        kevin.followingList = []

    def getUnfollowers(kevin):
        kevin.fillCredentials()
        kevin.handleList()
        kevin.compareFollowers()
        kevin.checkNotFollowedBack()
        kevin.driver.close()
        kevin.driver.quit()

    def fillCredentials(kevin):
        kevin.driver.get("https://www.instagram.com/")
        sleep(1)
        kevin.driver.find_element_by_xpath(XPATHS["loginButton"]).click()
        sleep(1)
        kevin.driver.find_element_by_xpath(XPATHS["loginUser"]).send_keys(kevin.username)
        kevin.driver.find_element_by_xpath(XPATHS["loginPass"]).send_keys(kevin.password)
        sleep(1)
        kevin.driver.find_element_by_xpath(XPATHS["loginSubmit"]).click()
        sleep(5)
        kevin.driver.find_element_by_xpath(XPATHS["dismiss"]).click()

    def handleList(kevin):
        sleep(2)
        kevin.driver.find_element_by_xpath(XPATHS["profileLink"]).click()
        sleep(2)
        kevin.driver.find_element_by_xpath(XPATHS["followersLink"]).click()
        sleep(3)

        kevin.scrollList(0)

    def scrollList(kevin, listSwitch):
        followersHTMLClass = "FPmhX"
        fl = kevin.driver.find_element_by_xpath(XPATHS["followersBox"])

        appendList = []

        lastHeight = 0
        currentHeight = 1
        while lastHeight != currentHeight:
            lastHeight = currentHeight
            appendList = [element.text for element in kevin.driver.find_elements_by_class_name(followersHTMLClass)]
            currentHeight = kevin.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, fl)
            sleep(1)

        if listSwitch:
            kevin.followingList = appendList
        else:
            kevin.followersList = appendList

    def compareFollowers(kevin):
        newFollowers = []
        missingFollowers = []

        f = open('oldFollowers', 'r')
        oldFollows = f.read().splitlines()

        for curr in kevin.followersList:
            if curr not in oldFollows:
                newFollowers.append(curr)

        for old in oldFollows:
            if old not in kevin.followersList:
                missingFollowers.append(old)
        f.close()

        f2 = f = open('oldFollowers', 'w')
        for follower in kevin.followersList:
            f.write(follower + "\n")
        f.close()

        kevin.prettyPrint(newFollowers, missingFollowers)

    def prettyPrint(kevin, newFollows, missFollows):
        print("Checking for new followers and unfollowers ------->")
        print('\n')
        # when u get new follower u be like
        if len(newFollows) != 0:
            print("YAYYY BAEEE #LOVEEEE NEWWW FOLLOWEERSSSSSSSSSS\n")
            for follower in newFollows:
                print("🤟", follower)
            print("\n")
        else:
            print("No new followers :(")

        # when someone unfollows u u be like
        if len(missFollows) != 0:
            print("u scum of the earth i ought to give u no more warnings but here it is... that is... one more\n")
            for idiot in missFollows:
                print("🙊", idiot)
        else:
            print("NOBODY UNFOLLOWED YOU!")
        print("\n")
        print("<-------")

    def checkNotFollowedBack(kevin):
        sleep(1)
        kevin.driver.find_element_by_xpath(XPATHS["closeButton"]).click()
        sleep(2)
        kevin.driver.find_element_by_xpath(XPATHS["followingLink"]).click()
        sleep(1)
        kevin.scrollList(1)
        kevin.compareLists()

    def compareLists(kevin):
        print("\n\nChecking for people who do not follow you back ------->")
        print("\n")
        for following in kevin.followingList:
            if following not in kevin.followersList:
                print("fuck", following, "I am unfollowing you")
        print("\n")
        print("<-------")


bot = InstaBot(username, password)
bot.getUnfollowers()
