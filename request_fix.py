import sys
sys.path.append("/search/odin/liujinming/djangoproj/relations")
from urllib.error import URLError, HTTPError
import urllib.request
import urllib.parse
import http.client
import urlhandle # 自定义库


# _method in ('POST','GET')
# _tunnel only in 'POST'
# _headers is a dict
# _data support type in ('str','dict')
# _conn_obj is a http.client.HTTPConnection(host,port)
def request(_method, _tunnel, _headers, _data, _conn_obj, _encoding, _error, _debug=0):
    if isinstance(_data, str):
        if _debug == 1:
            print("[Request][Type]Data_Type is str")
        _data_send = _data
    elif isinstance(_data, dict):
        if _debug == 1:
            print("[Request][Type]Data_Type is dict,transfer to str")
        _data_send = urlhandle.urlencode(_data, _encoding, _error)
    else:
        return {'data': '',
                'error': '_data type error',
                }
    if _debug == 1:
        print(_method,_tunnel,_headers,_data_send)
    try:
        if _method == "GET":
            _tunnel += _data_send
            _data_send = ''
        _conn_obj.request(_method, _tunnel, _data_send, _headers)
        #if not _conn_obj.getresponse().read():
        #    print(_data_send)
        return {'data': _conn_obj.getresponse().read(),
                'error': '',
                'data_send': _data_send,
                }
    except UnicodeError as e:
        return {'data': ''.encode(encoding=_encoding,errors='ignore'),
                'error': e,
                }
    except urllib.error.URLError as e:
        return {'data': ''.encode(encoding=_encoding,errors='ignore'),
                'error': e.reason,
                }
    except ConnectionResetError as e:
        if _debug == 1:
            print(e2)
        try:
            _conn_obj.request(_method, _tunnel, _data_send, _headers)
            return {'data': _conn_obj.getresponse().read(),
                    'error': '',
                    'data_send': _data_send,
                    }
        except Exception as e2:
            return {'data': ''.encode(encoding=_encoding,errors='ignore'),
                    'error': e2,
                   }
    except ConnectionRefusedError as e:
        return {'data': ''.encode(encoding=_encoding,errors='ignore'),
                'error': e,
                }
    except Exception as e:
        if _debug == 1:
            print('Other ERROR from request', e)
        return {'data': ''.encode(encoding=_encoding,errors='ignore'),
                'error': e,
                }
