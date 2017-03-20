#   File:
#       check_proxy.py
#   Requirements:
#       urllib2
#       requests
#       click
#   Version:
#       0.1.1
#   HowTo:
#             python check_proxy.py --login_pass=login:pass  \
#                                 --proxy_ip=127.0.0.1:8183 \
#                                 --check_url='https://google.com' \
#                                 --token=your/slack/token
#   token - is not necessary
#   HardCode style: Don't forget change slack channel.

import urllib2
import requests
import click


#Function for check proxy
def check_proxy(login_pass,proxy_ip,check_url,token,log_level):
    if login_pass and proxy_ip:
        proxy_full = login_pass+'@'+proxy_ip.strip('\n')
    else:
        proxy_full = proxy_ip.strip('\n')
    proxy_url = "http://%s" % proxy_full
    proxy = urllib2.ProxyHandler({'http': proxy_url,
                                  'https': proxy_url})
    auth = urllib2.HTTPBasicAuthHandler()
    opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    try:
        conn = urllib2.urlopen(check_url, timeout=10)
        h = conn.getcode()
        if log_level == 'DEBUG':
            print "Proxy url: "+proxy_url
            print "Proxy login and pass: "+proxy_full.strip('\n')
            print "Proxy check ulr: "+check_url
            print "Slack Token: "+token
            print "HTTP code: %s " % h
            print conn.read()
            print "\n"
        elif log_level == 'INFO':
            print "IP: %s, HTTP code: %s - all okay" %(proxy_ip.strip('\n'),h)
        return True
    except Exception as e:
        if not token:
            print "Don't work: %s, %s" % (e,proxy_ip)
        else:
            print token
            slack_message = "Don't work, was sent to slack: %s, \n proxy ip: %s" % (e,proxy_ip)
            print slack_message
            slack_notification(token,slack_message)
        return False


# Function for notification to slack
def slack_notification(token,slack_message):
    try:
        url = "https://hooks.slack.com/services/%s" % token
        payload = {"channel": "hugochat",
                   "title": "Priority",
                   "value": "High",
                   "attachments": [{"fallback": "This attachement isn't supported.",
                        "title": "Something going wrong with proxy servers",
                        "text": "%s" % slack_message,
                        "short": "true",
                        "color": "#9C1A22"}],
                   }
        message = requests.post(url, json=payload)
        print(message)
    except requests.HTTPError as err:
        print "__slack_notification__: %s" % err
    except BaseException as unk_err:
        print "__slack_notification__. Unkown errors: %s" % unk_err
    except:
        print '__slack_notification__. UNKNOWN UNHANDLED EXCEPTION.'

@click.command()
@click.option('--token', '-t', help='Token of your slack api', type=str, required=False, default='')
@click.option('--login_pass','-lp', help='Login and pass to your proxy. Example: yourlogin@yourpass', type=str, required=True, default='')
@click.option('--proxy_ip', '-pi', help='If you need check one ip - use this parameter', type=str, required=False)
@click.option('--check_url', '-cu', help='Url for check you proxy. Example: https://google.com', type=str, required=True, default='https://google.com')
@click.option('--proxy_file', '-pf', help='If you need check array of ip - use this argument. Example: name_of_file.txt ', type=str, required=False)
@click.option('--log_level', '-ll', help='QUITE - nothing, INFO - IP and http code, DEBUG - FULL ', type=str, required=True, default='QUITE')


def main(login_pass,proxy_ip,check_url,proxy_file,token,log_level):
    exit_code = 0

    if proxy_ip:
        check_proxy(login_pass,proxy_ip,check_url,token,log_level)
    elif proxy_file:
        array_ip = []
        with open(proxy_file) as my_file:
            for line in my_file:
                array_ip.append(line)
        for ip in array_ip:
            proxy_status = check_proxy(login_pass,ip, check_url,token,log_level)
            if not proxy_status:
                exit_code = 1

    else:
        print 'Something going wrong =)\nMaybe you forget arguments'
        print 'python proxy_test.py --help'

    exit(exit_code)


main()