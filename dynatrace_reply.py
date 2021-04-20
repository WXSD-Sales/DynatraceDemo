# -*- coding: utf-8 -*-
#!/usr/bin/env python
import json
import os
import traceback

import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.web

from common.spark import Spark

from dynatrace.settings import Settings

from tornado.options import define, options, parse_command_line
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError

define("debug", default=False, help="run in debug mode")

class TestHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        self.write("OK")

class CardsHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        try:
            webhook = json.loads(self.request.body)
            print("CardsHandler Webhook Attachment Action Received:")
            print(webhook)
            attachment = yield self.application.settings['spark'].get_with_retries_v2('https://api.ciscospark.com/v1/attachment/actions/{0}'.format(webhook['data']['id']))
            print("attachment.BODY:{0}".format(attachment.body))
            message_id = attachment.body['messageId']
            room_id = attachment.body['roomId']
            person_id = attachment.body['personId']
            inputs = attachment.body.get('inputs', {})
            print("messageId:{0}".format(message_id))
            print("roomId:{0}".format(room_id))
            print("inputs:{0}".format(inputs))
            room = yield self.application.settings['spark'].get_with_retries_v2('https://api.ciscospark.com/v1/rooms/{0}'.format(room_id))
            room_type = room.body.get('type')
            person = "you"
            if room_type == "group":
                person = "<@personId:{0}|>".format(person_id)
            reply_msg = ''
            if inputs.get('submit') == "ack" and inputs.get('id') not in [None, ""]:
                yield self.application.settings['spark'].delete('https://api.ciscospark.com/v1/messages/{0}'.format(message_id))
                reply_msg = "Problem ID: **{0}** has been acknowledged by {1}.".format(inputs.get('id'), person)
            elif inputs.get('submit') == "inc":
                if inputs.get('comment') in [None, ""]:
                    reply_msg = "You must enter a message to add a comment."
                else:
                    resp = yield self.post_comment(inputs.get('comment'), inputs.get('pid'))
                    print("comment create resp:{0}".format(resp.body))
                    reply_msg = "Comment posted by {0}, view it [here]({1}).".format(person, inputs.get('url'))
                    #yield self.application.settings['spark'].delete('https://api.ciscospark.com/v1/messages/{0}'.format(message_id))
            if reply_msg != '':
                yield self.application.settings['spark'].post_with_retries('https://api.ciscospark.com/v1/messages', {'markdown':reply_msg, 'roomId':room_id})
        except Exception as e:
            print("CardsHandler General Error:{0}".format(e))
            traceback.print_exc()

    @tornado.gen.coroutine
    def post_comment(self, comment, pid):
        headers={"Content-Type":"application/json",
                 "Authorization" : "Api-token " + Settings.dyna_token}
        data = {"message":comment, "context":"APM Webex Bot"}
        url = 'https://uec79139.live.dynatrace.com/api/v2/problems/{0}/comments'.format(pid)
        request = HTTPRequest(url, method="POST", headers=headers, body=json.dumps(data), request_timeout=20)
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch(request)
        raise tornado.gen.Return(response)


@tornado.gen.coroutine
def main():
    try:
        parse_command_line()
        app = tornado.web.Application(
            [   (r"/cards", CardsHandler),
                #(r"/test", TestHandler),
            ],
            cookie_secret="CHANGE_THIS_TO_SOME_RANDOM_VALUE",
            xsrf_cookies=False,
            debug=options.debug,
            )
        app.settings['debug'] = options.debug
        app.settings['settings'] = Settings
        app.settings['spark'] = Spark(Settings.token)
        server = tornado.httpserver.HTTPServer(app)
        print("Serving... on port {0}".format(Settings.port))
        server.bind(Settings.port)  # port
        print("Debug: {0}".format(app.settings["debug"]))
        server.start()
        tornado.ioloop.IOLoop.instance().start()
        print('Done')
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    main()
