# DatadogDemo
This demo has been tested in Python3 only (v3.7.4)

You will need to install the following third party python modules:
```
pip install tornado==4.5.2
```

The following Environment variables are required for this demo, set with the appropriate values:
```
MY_BOT_ID=1234567890
MY_BOT_TOKEN=ABCDEFG-1234-567A_ZYX
MY_SECRET_PHRASE=datadogtestexample
MY_BOT_PORT=8080
DD_API_KEY=abcdefghijklmnop
DD_APPLICATION_KEY=31415826753492031
DD_CREATOR_ID=abcdefgh-12ab-34cd-56ef-ijklmnopqrstu
```

To run this, you can simply run:
```
python datadog_reply.py
```

Using the bot's token, you can get the bot's personId here:
https://developer.webex.com/docs/api/v1/people/get-my-own-details


You will need to create at least one [webhook](https://developer.webex.com/docs/api/guides/webhooks) to your bot's hosted location + /cards, example:
https://yoursite.com/cards


The DD_API_KEY and DD_APPLICATION_KEY Values need to be setup through Datadog:
https://docs.datadoghq.com/api/latest/authentication/


You can use the Datadog API (https://docs.datadoghq.com/api/latest/users/) to find an appropriate DD_CREATOR_ID value (this will be the user who creates the incident in Datadog).
