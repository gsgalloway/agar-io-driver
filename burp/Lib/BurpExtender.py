from burp import IBurpExtender, IProxyListener

class BurpExtender(IBurpExtender):

    def registerExtenderCallbacks(self, callbacks):
        print "AgarIO Extension loaded. Waiting for HTTP traffic..."
        helpers = callbacks.getHelpers()
        callbacks.setExtensionName("AgarIO Extension")

        # Disable interception from the Proxy. This stops Burp from freezing
        # all HTTP traffic that passes through it and waiting for the user
        # to click "forward." This plugin will still receive all HTTP messages
        # before they're automatically forwarded.
        callbacks.setProxyInterceptionEnabled(False)

        callbacks.registerProxyListener(ProxyListener(helpers))


class ProxyListener(IProxyListener):
    def __init__(self, helpers):
        self._helpers = helpers

    def processProxyMessage(self, messageIsRequest, message):
        messageIsResponse = not messageIsRequest
        if messageIsResponse:
            print("Intercepting HTTP response")
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
