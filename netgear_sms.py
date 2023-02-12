import requests


class APIError(Exception):
  def __init__(self, err_no, err_detail):
    msg = f'Error {err_no}, field {err_detail}'
    super().__init__(msg)
    self.err_no = err_no
    self.err_detail = err_detail


class API:
  def __init__(self, base_addr, password):
    self.base_addr = base_addr
    self.password = password
    self.session = requests.Session()
    self.csrf_token = None
    self.is_logged_in = False

  def get_model(self):
    self._get_model()
    if self.is_logged_in: return

    self.make_post_request('/Forms/config', {'session.password': self.password})
    self.is_logged_in = True
    return self._get_model()

  def _get_model(self):
    resp = self.session.get(self.base_addr + '/api/model.json').json()
    self.csrf_token = resp['session']['secToken']
    self.is_logged_in = resp['session']['userRole'] != 'Guest'
    return resp

  def make_post_request(self, path, params):
    if not self.csrf_token: self.get_model()

    defaults = {
      'ok_redirect': '/success.json',
      'err_redirect': '/error.json',
      'token': self.csrf_token,
    }
    defaults.update(params)
    resp = self.session.post(self.base_addr + path, data=defaults).json()
    if 'errno' in resp:
      raise APIError(resp['errno'], resp['errdetail'])
    return resp

  def send_sms_message(self, recipient, body, client_id=None):
    if client_id is None:
      client_id = 'netgear-sms'
    self.get_model()
    self.make_post_request('/Forms/smsSendMsg', {
      'sms.sendMsg.receiver': recipient,
      'sms.sendMsg.text': body,
      'sms.sendMsg.clientId': client_id,
      'action': 'send',
    })

  def mark_message_as_read(self, message_id):
    self.get_model()
    self.make_post_request('/Forms/config', {
      'sms.readId': message_id
    })

  def delete_message(self, message_id):
    self.get_model()
    self.make_post_request('/Forms/config', {
      'sms.deleteId': message_id
    })
