from burp import IBurpExtender

from burp import IProxyListener

class BurpExtender(IBurpExtender):

    def registerExtenderCallbacks(self, callbacks):

        print "Hello!"

        self._callbacks = callbacks

        self._helpers = callbacks.getHelpers()

        callbacks.setExtensionName("AgarIO Extension")

        callbacks.registerProxyListener(ProxyListener(self._helpers))


class ProxyListener(IProxyListener):

    def __init__(self, helpers):
        self._helpers = helpers

    def processProxyMessage(self, messageIsRequest, message):
        if not messageIsRequest:
            messageInfo = message.getMessageInfo()
            rawResponse = messageInfo.getResponse()
            response = self._helpers.analyzeResponse(rawResponse)
            headers = response.getHeaders()
            rawMsgBody = rawResponse[response.getBodyOffset():]
            msgBody = self._helpers.bytesToString(rawMsgBody)

            newBody = self._editAgarHtml(msgBody)

            newBodyBytes = self._helpers.stringToBytes(newBody)

            newResponse = self._helpers.buildHttpMessage(headers, newBodyBytes)

            messageInfo.setResponse(newResponse)
        return

    def _editAgarHtml(self, html):
        targetScoreString = 'P=Math.max(P,Db());'
        scoreStringAddition = 'document.getElementById("score").innerHTML=Db();'
        newScoreString = targetScoreString + scoreStringAddition
        html = html.replace(targetScoreString, newScoreString)

        bodyEndTag = '</body>'
        scoreDiv = '<div id="score"></div>'
        newBodyEndTag = scoreDiv + bodyEndTag
        html = html.replace(bodyEndTag, newBodyEndTag)

        return html
