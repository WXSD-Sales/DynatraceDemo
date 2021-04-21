# DatadogDemo
This demo has been tested in Python3 only (v3.7.4)

A video walkthrough of this application can be found here:
https://drive.google.com/file/d/1MZzoXa_ZOkpHL1qDP_ZcIHwU4C-YhSVl/view?usp=sharing

# 1
You will need to install the following third party python modules:
```
pip install tornado==4.5.2
```

The following Environment variables are required for this demo, set with the appropriate values:
```
export MY_BOT_ID=Y2lzY123456A
export MY_BOT_TOKEN=ZGNABCDEFG_1234-56AB-CD34-ZYXW
export MY_BOT_PORT=8000

export DYNA_TOKEN="dt1c00.VN6ABCD.EFGH1234"
```

To run this, you can simply run:
```
python datadog_reply.py
```

Using the bot's token, you can get the bot's personId here:
https://developer.webex.com/docs/api/v1/people/get-my-own-details


The DYNA_TOKEN value needs to be setup through Dynatrace:
https://www.dynatrace.com/support/help/dynatrace-api/basics/dynatrace-api-authentication/



# 2
You will need to create at least one Webex [webhook](https://developer.webex.com/docs/api/guides/webhooks) to your bot's hosted location + /cards, example:
https://yoursite.com/cards - required fields:
```
      "name": "Attachment Actions Webhook",
      "targetUrl": "https://yoursite.com/cards",
      "resource": "attachmentActions",
      "event": "created",
```

# 3
In addition, you will need an Integration on the Dynatrace side (https://uec79139.live.dynatrace.com/#settings/integration/notification;gf=all).  The webhook payload you setup should look like this:
```
URL: https://webexapis.com/v1/messages
```
You will need to replace the roomId with a valid Webex [Room (space)](https://developer.webex.com/docs/api/v1/rooms)
```
{
  "roomId": "YOUR_ROOM_ID_HERE",
  "markdown": "Dynatrace Example Alert",
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": 
{
    "type": "AdaptiveCard",
    "body": [
        {
            "type": "TextBlock",
            "size": "Medium",
            "weight": "Bolder",
            "text": "Alert! {ProblemTitle}"
        },
        {
            "type": "FactSet",
            "facts": [
                {
                    "title": "ID",
                    "value": "{PID}"
                }
            ]
        },
        {
            "type": "FactSet",
            "facts": [
                {
                    "title": "ImpactedEntity",
                    "value": "{ImpactedEntity}"
                }
            ]
        },
        {
            "type": "TextBlock",
            "text": "{ProblemDetailsMarkdown}",
            "wrap": true
        },
        {
            "type": "ActionSet",
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Acknowledge",
                    "data":{"id":"{PID}", "submit":"ack"}
                },
                {
                    "type": "Action.OpenUrl",
                    "title": "View",
                    "url":"{ProblemURL}"
                },
                {
                    "type": "Action.ShowCard",
                    "title": "Add Comment",
                    "card":{"type": "AdaptiveCard",
                            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                            "version": "1.2",
                            "body": [
                                    {
                                        "id":"comment",
                                        "type": "Input.Text",
                                        "placeholder": "Write your comment here...",
                                        "spacing": "default"
                                    },
                                    {
                                        "type": "ActionSet",
                                        "actions": [
                                            {
                                                "type": "Action.Submit",
                                                "title": "Add Comment",
                                                "data": {
                                                    "pid": "{PID}",
                                                    "url": "{ProblemURL}",
                                                    "submit": "inc"
                                                }
                                            }
                                        ]
                                    }
                                ]
                        }
                }
            ]
        }
    ],
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.2"
}
}
]
}
```
You will also need to specify 2 Custom Headers, where the Bearer Token value is replaced by the one you get from [creating a bot of your own.](https://developer.webex.com/my-apps)
```
{"Content-Type":"application/json", "Authorization":"Bearer XXXX_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"}
```
