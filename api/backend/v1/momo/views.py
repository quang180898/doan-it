import json
import urllib.request
import uuid
import hmac
import hashlib

from api.base.apiViews import APIView
from library.constant.api import SERVICE_CODE_NOT_EXISTS_BODY, SERVICE_CODE_BODY_PARSE_ERROR


class Momo(APIView):
    def pay_with_momo(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.POST
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        if content == {}:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR)
        amount = content['amount'] if content.get('amount') else None

        endpoint = "https://test-payment.momo.vn/gw_payment/transactionProcessor"
        partnerCode = "MOMOMKTA20210508"
        accessKey = "kn68wRx7LGZFIJsZ"
        serectkey = "hOAzKQbJ9cX73kHqJcUyXHPyTxfMdCR8"
        serectkey = str.encode(serectkey)
        orderInfo = "pay with MoMo"
        returnUrl = "https://momo.vn/return"
        notifyurl = "https://dummy.url/notify"
        orderId = str(uuid.uuid4())
        requestId = str(uuid.uuid4())
        requestType = "captureMoMoWallet"
        extraData = "merchantName=;merchantId="

        # before sign HMAC SHA256 with format
        # partnerCode=$partnerCode&accessKey=$accessKey&requestId=$requestId&amount=$amount&orderId=$oderId&orderInfo=$orderInfo&returnUrl=$returnUrl&notifyUrl=$notifyUrl&extraData=$extraData
        rawSignature = "partnerCode=" + partnerCode + "&accessKey=" + accessKey + "&requestId=" + requestId + "&amount=" + amount + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&returnUrl=" + returnUrl + "&notifyUrl=" + notifyurl + "&extraData=" + extraData

        # puts raw signature
        print("--------------------RAW SIGNATURE----------------")
        print(rawSignature)
        # signature
        h = hmac.new(serectkey, rawSignature.encode('utf-8'), hashlib.sha256)
        signature = h.hexdigest()
        print("--------------------SIGNATURE----------------")
        print(signature)

        # json object send to MoMo endpoint

        data = {
            'partnerCode': partnerCode,
            'accessKey': accessKey,
            'requestId': requestId,
            'amount': amount,
            'orderId': orderId,
            'orderInfo': orderInfo,
            'returnUrl': returnUrl,
            'notifyUrl': notifyurl,
            'extraData': extraData,
            'requestType': requestType,
            'signature': signature
        }
        print("--------------------JSON REQUEST----------------\n")
        data = json.dumps(data)
        print(data)
        clen = len(data)
        data = str.encode(data)
        req = urllib.request.Request(endpoint, data, {'Content-Type': 'application/json', 'Content-Length': clen})
        f = urllib.request.urlopen(req)

        response = f.read()
        f.close()
        print(json.loads(response)['payUrl'])
        return self.response(self.response(response))
        # print("--------------------JSON response----------------\n")
        # print(response)
        # print(response + "\n")
        #
        # print("payUrl\n")
        # print(json.loads(response)['payUrl'] + "\n")