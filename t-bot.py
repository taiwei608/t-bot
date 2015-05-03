from line import LineClient, LineGroup, LineContact
import re
import regexp
import WebCrawler

KeyFile = open("token", "r")
AuthToken = KeyFile.read().strip()

try:
    client = LineClient(authToken=AuthToken)

except:
    print "Hey Login Failed"

while True:
    op_list = []

    for op in client.longPoll():
        op_list.append(op)

    for op in op_list:
        sender   = op[0]
        receiver = op[1]
        message  = op[2]
        
        msg = message.text
        print str(receiver) + "\t" + str(sender) + "\t" + str(message)
        m = regexp.REMatcher(msg)

        if str(msg).strip() == "None":
            print("It's a Sticker")
            break
        elif m.match(r't-bot'):
            msg = "Dominus."
        elif re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg, re.I):
            m = re.finditer(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg, re.I)
            print "Link detect"
            if m:
                for link in m:
                    URL = link.group(0)
                    print URL
                    msg = str(WebCrawler.get(URL))
                    if msg == 'NO':
                        print "Yahoo internal URL"
                        break
                    else:
                        receiver.sendMessage("%s" % msg)
            break
        else:
            break
        receiver.sendMessage(" %s" % (msg))
        #receiver.sendMessage("[%s] %s" % (sender.name, msg))

