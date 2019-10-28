from lxml import etree


def getCustomerData(xmlNode):
    tmpCustData = ["", "", "", "", "", ""]    
    for myNode in xmlNode:        
        if myNode.tag == "CompanyName":
            tmpCustData[1] = myNode.text
        elif myNode.tag == "ContactName":
            tmpCustData[2] = myNode.text
        elif myNode.tag == "ContactTitle":
            tmpCustData[3] = myNode.text
        elif myNode.tag == "Phone":
            tmpCustData[4] = myNode.text
        elif myNode.tag == "Fax":
            tmpCustData[5] = myNode.text
        elif myNode.tag == "FullAddress":
            tmpAddressList = getCustomerAddress(myNode)
            tmpCustData = tmpCustData + tmpAddressList
    return tmpCustData
                    
                                      
def getCustomerAddress(xmlNode):
    tmpCustData = ["", "", "", "", ""]
    for cAddress in xmlNode:
        if cAddress.tag == "Address":
            tmpCustData[0] = cAddress.text
        elif cAddress.tag == "City":
            tmpCustData[1] = cAddress.text
        elif cAddress.tag == "Region":
             tmpCustData[2] = cAddress.text
        elif cAddress.tag == "PostalCode":
            tmpCustData[3] = cAddress.text
        elif cAddress.tag == "Country":
            tmpCustData[4] = cAddress.text
    return tmpCustData
    
                
                      
def parseXML(inputXMLFile, outputFile):
    
    myTextFile= open(outputFile, "w")
    myTextFile.write("CustomerID,CompanyName,ContactName,ContactTitle,Phone,Fax,Address,City,Region,PostalCode,Country")
    myTextFile.close()    
    
    xml = open(inputXMLFile).read()    
    
    xml = bytes(bytearray(xml, encoding = 'utf-8'))
    root = etree.fromstring(xml)
    
    myTextFile= open(outputFile, "a")
    
    for rootNode in root.getchildren():
        for custNode in rootNode:
            if custNode.tag == "Customer":
                custData = getCustomerData(custNode)
                
                #Save Data in text file
                myTextFile.write(",".join(custData) + "\n")
    
    myTextFile.close()
    

if __name__ == "__main__":
    parseXML("customer.xml", "customer.txt")

