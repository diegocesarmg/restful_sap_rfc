import os
from io import StringIO
from http.server import BaseHTTPRequestHandler, HTTPServer
from src.helpers import RFCHelper
import xmltodict
from dict2xml import dict2xml
import zlib

erp_helper = RFCHelper(user=os.environ['ERP_USER'], passwd=os.environ['ERP_PWD'], ashost=os.environ['ERP_HOST'],
                                sysnr=os.environ['ERP_SYSNR'], client=os.environ['ERP_CLIENT'], saprouter=os.environ['ERP_ROUTER'])
class handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes("Hello World", "utf8"))

    def do_POST(self):
        # Basic auth
        if self.headers['Authorization'] != 'Basic ' + os.environ['AUTH_KEY']:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="SAP ERP"')
            self.end_headers()
            self.wfile.write(bytes("Authentication failed", "utf8"))
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length) 
        post_data = post_data.decode('utf-8')

        # xml to dict
        post_data_dict = xmltodict.parse(post_data, process_namespaces=True, force_list={'ITEM': True})

        # Get rfc name
        rfc_data = self.prepare_rfc_data(post_data_dict)

        try:
            response = dict2xml(erp_helper.rfc_execute(rfc_data["rfc_name"], rfc_data["rfc_params"]))
            self.send_response(200)
            self.send_header('Content-type','application/xml')
            self.end_headers()
            self.wfile.write(bytes(response, "utf8"))

            # self.send_header("Content-type", 'application/xml') # or whatever you expect
            # # self.send_header("Content-Encoding", 'gzip')
            # # don't forget to import zlib
            # gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
            # # response is the string where your response is
            # content = gzip_compress.compress(bytes(str(response), "utf8")) + gzip_compress.flush()
            # compressed_content_length = len(content)
            # self.send_header("Content-Length", compressed_content_length)
            # self.wfile.write(content)
            

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type','application/xml')
            self.end_headers()
            self.wfile.write(bytes(str(e), "utf8"))

    def prepare_rfc_data(self, rfc_post_data):
        # Read first key of post_data_dict
        key = list(rfc_post_data.keys())[0]
        # Read last item from splitted by :
        rfc_name = key.split(":")
        rfc_name = rfc_name[len(rfc_name) - 1]
        return {
            "rfc_name": rfc_name,
            "rfc_params": self.prepare_rfc_params(rfc_post_data[key])
        }

    def prepare_rfc_params(self, d):
        if isinstance(d, dict):
            for k, v in d.items():
                if "ITEM" in v:
                    d[k] = v["ITEM"]

        return d


with HTTPServer(('', 8000), handler) as server:
    print('Starting server at http://localhost:8000')
    server.serve_forever()