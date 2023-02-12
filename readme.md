# Netgear SMS
API for the SMS function of Netgear LTE modems.

## Supported models
Only tested and developed for the Netgear LM1200. Other models may work.
This will work even if there's no SMS/Messages page in the web UI.
Most of this is from the browser devtools - check the XHR tab to see what data is returned from the `/api/model.json`
URL.

## Example

    from netgear_sms import API

    client = API('http://192.168.5.1', 'mysupersecurepassword')

    # Read messages
    message = client.get_model()['sms']['msgs'][0]
    print(f'Message from {message['sender']}: {message['text']}')

    # Send a message
    client.send_sms_message(1234, 'Hello you')

    # Check the outbox
    print(client.get_model()['sms']['sendMsg'][0]['text'])

    # Mark a message as read
    client.mark_message_as_read(message['msgId'])

    # Delete a received message
    client.delete_message(message['msgId'])

## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
