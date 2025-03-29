import json

from communication_protocol.device_message import set_settings_response

message = set_settings_response("asdsadas", "dsadsadsa", {})
abc = json.dumps(message.to_json())
abc = json.loads(abc)
abc = json.loads(abc)
print(abc)
print(abc["payload"])
