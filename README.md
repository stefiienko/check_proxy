# Check proxy - python
Simple checker proxy, with notification in slack, python
### Requirements:
Wrote on python 2.7
- urllib2
- requests
- click
### Options
```sh
$ python check_proxy.py --help
Usage: check_proxy.py [OPTIONS]

Options:
  -t, --token TEXT        Token of your slack api. Not necessary.
  -lp, --login_pass TEXT  Login and pass to your proxy. Example:
                          yourlogin@yourpass. Not necessary.
  -pi, --proxy_ip TEXT    If you need check one ip - use this parameter
  -cu, --check_url TEXT   Url for check you proxy, default: https://google.com
                          [required]
  -pf, --proxy_file TEXT  If you need check array of ip - use this argument.
                          Example: name_of_file.txt
  -ll, --log_level TEXT   QUITE - nothing(default), INFO - IP and http code, DEBUG -
                          FULL   [required]
  --help                  Show this message and exit.
```

### How-to
Check one ip with login/pass
```sh
$ python check_proxy.py --proxy_ip=10.10.10.1:8183 --login_pass=user:pass --check_url='https://google.com' --log_level=INFO
 ```
Output:
```
 IP: 10.10.10.1:8183, HTTP code: 200 - all okay
```

Check IPs from file with login/pass
```sh
$ python check_proxy.py --proxy_file=proxy_ip.txt --login_pass=user:pass --check_url='https://google.com' --log_level=INFO
 ```
Output:
```
IP: 10.10.10.1:8183, HTTP code: 200 - all okay
IP: 10.10.10.2:8183, HTTP code: 200 - all okay
IP: 10.10.10.3:8183, HTTP code: 200 - all okay
```

If you need send error to slack, use flag --token

```sh
$ python check_proxy.py --proxy_file=proxy_ip.txt --login_pass=user:pass --check_url='https://google.com' --token=YOUR/SLACK/TOKEN --log_level=INFO
 ```

Output
```
IP: 10.10.10.1:8183, HTTP code: 200 - all okay

YOUR/SLACK/TOKEN
Don't work, was sent to slack: <urlopen error timed out>, 
 proxy ip: 10.10.10.2:8183
<Response [200]>

IP: 10.10.10.3:8183, HTTP code: 200 - all okay
```

Author
----
Anton Stefiienko @ 2017 
Proxy checker (check proxy)


**Free Software, Hell Yeah!**
