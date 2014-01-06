from _pytest.mark import MarkInfo
import json
import requests
import time
import os.path


class SauceLabs(object):
    def __init__(self, username, key):
        self.username = username
        self.key = key

    def update_job_from_item(self, item):
        # session couldn't be established for some reason
        if not hasattr(item.parent._obj.driver, "session_id"):
            return

        self.log_dir = item.parent._obj.config["saunter"]["log_dir"]

        j = {}

        # name
        j["name"] = item.name

        # result
        if item.outcome.lower() == 'passed':
            # print("pass")
            j["passed"] = True
        else:
            # print("fail")
            j["passed"] = False

        # tags
        j["tags"] = []
        j["custom-data"] = {}
        for keyword in item.keywords:
            if isinstance(item.keywords[keyword], MarkInfo):
                # per item custom data
                if keyword == "saucelabs_customdata":
                    for key, value in item.keywords[keyword].kwargs.iteritems():
                        j["custom-data"][key] = value
                # tags
                else:
                    j["tags"].append(keyword)

        # browser custom data
        if "custom data" in item.parent._obj.config["browsers"][item.parent._obj.config["saunter"]["default_browser"]]["sauce labs"]:
                for option in item.parent._obj.config["browsers"][item.parent._obj.config["saunter"]["default_browser"]]["sauce labs"]["custom data"]:
                    j["custom-data"][option] = item.parent._obj.config["browsers"][item.parent._obj.config["saunter"]["default_browser"]]["sauce labs"]["custom data"][option]

        # global custom data
        if "custom data" in item.parent._obj.config["sauce labs"]:
            for option in item.parent._obj.config["sauce labs"]["custom data"]:
                j["custom-data"][option] = item.parent._obj.config["sauce labs"]["custom data"][option]

        # build
        if item.parent._obj.config['sauce labs']['build']:
            j["build"] = item.parent._obj.config['sauce labs']['build']
        # print(json.dumps(j))

        # update
        which_url = "https://saucelabs.com/rest/v1/%s/jobs/%s" % (self.username, item.parent._obj.driver.session_id)
        r = requests.put(which_url,
                         data=json.dumps(j),
                         headers={"Content-Type": "application/json"},
                         auth=(self.username, self.key))
        r.raise_for_status()

        # if item.parent._obj.config.getboolean("SauceLabs", "get_video"):
        #     self._fetch_sauce_artifact("video.flv")

        # if item.parent._obj.config.getboolean("SauceLabs", "get_log"):
        #     self._fetch_sauce_artifact("selenium-server.log")

    def _fetch_sauce_artifact(self, which):
        sauce_session = self.sauce_session
        which_url = "https://saucelabs.com/rest/%s/jobs/%s/results/%s" % (self.username, self.sauce_session, which)
        code = 404
        timeout = 0
        while code in [401, 404]:
            r = requests.get(which_url, auth=(self.username, self.key))
            try:
                code = r.status_code
                r.raise_for_status()
            except requests.exceptions.HTTPError, e:
                time.sleep(4)

        artifact = open(os.path.join(self.log_dir, which), "wb")
        artifact.write(r.content)
        artifact.close()

    def update_name(self, session_id, name):
        j = {"name": name}

        which_url = "https://saucelabs.com/rest/v1/%s/jobs/%s" % (self.username, session_id)
        r = requests.put(which_url,
                         data=json.dumps(j),
                         headers={"Content-Type": "application/json"},
                         auth=(self.username, self.key))
        r.raise_for_status()
