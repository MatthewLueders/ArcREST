"""
   This sample shows how to create a list in json
   of all items in a group
"""
import arcrest
import os,io
import json
from arcresthelper import orgtools
import csv
def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback, inspect,sys
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    filename = inspect.getfile(inspect.currentframe())
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, filename, synerror

if __name__ == "__main__":
    proxy_port = None
    proxy_url = None    

    securityinfo = {}
    securityinfo['security_type'] = 'Portal'#LDAP, NTLM, OAuth, Portal, PKI
    securityinfo['username'] = ""#<UserName>
    securityinfo['password'] = ""#<Password>
    securityinfo['org_url'] = "http://www.arcgis.com"
    securityinfo['proxy_url'] = proxy_url
    securityinfo['proxy_port'] = proxy_port
    securityinfo['referer_url'] = None
    securityinfo['token_url'] = None
    securityinfo['certificatefile'] = None
    securityinfo['keyfile'] = None
    securityinfo['client_id'] = None
    securityinfo['secret_id'] = None   
      
    groups = ["Network Services"] #Name of groups
    outputlocation = r"C:\TEMP"
    outputfilename = "group.json"
    outputitemID = "id.csv"
    try:

        orgt = orgtools.orgtools(securityinfo)

        groupRes = []
        if orgt.valid:
            fileName = os.path.join(outputlocation,outputfilename)
            csvFile = os.path.join(outputlocation,outputitemID)
            iconPath = os.path.join(outputlocation,"icons")  
            if not os.path.exists(iconPath):
                os.makedirs(iconPath)                                                    
            file = io.open(fileName, "w", encoding='utf-8')  
            with open(csvFile, 'wb') as csvfile:
                idwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)                
                for groupName in groups:
                    results = orgt.getGroupContent(groupName=groupName)  
                   
                    if not results is None and 'results' in results:

                      
                        for result in results['results']:
                            idwriter.writerow([result['title'],result['id']])
                            thumbLocal = orgt.getThumbnailForItem(itemId=result['id'],fileName=result['title'],filePath=iconPath)
                            result['thumbnail']=thumbLocal
                            groupRes.append(result)
                           
                if len(groupRes) > 0:
                    print "%s items found" % str(len(groupRes))
                    file.write(unicode(json.dumps(groupRes, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))))                                              
            file.close()
            
    except:
        line, filename, synerror = trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror