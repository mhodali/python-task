import yaml
import json
import re
import os
import logging

logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
def create_files(): 
 flag = 0
 with open("config.yaml", "r") as my_file ,open("VM_PE_GI-7.7r1.7.1-20200319-x86_64.release_note", "w") as note, open("temp.yaml", "w") as temp:
   for line in my_file:
      if line.strip() == "The CVM_PE_GI-7.7r1.7.1-20200319 patch fixes the following CVEs:" or flag == 1:
         note.write("\n")
         note.write(format(line.rstrip()))
    
         flag =1
      else:
         temp.write("\n")
         temp.write(format(line.rstrip()))
   logger.info("split yml file into CVM and VM")

          
       

def convert():
    with open("temp.yaml", 'r') as yaml_in, open("CVM_RPM_LIST_MANIFEST.json", "w") as json_out:
        yaml_object = yaml.safe_load(yaml_in) # yaml_object will be a list or a dict
        json.dump(yaml_object, json_out, indent=2)
        logger.info("convert yaml to json")


create_files()
convert()
with open('CVM_RPM_LIST_MANIFEST.json') as json_file:
 #data = json.dump(json_file)
 data = json_file.read()
 #json_data = json.dumps(json_file)
 p = re.compile('"rpm_pkg": ".* *."')
 data=p.findall(data)
 l=0
 logger.info("take name of packege and save it in list")
 for i in data:
   temp=data[l]
   temp=temp.lstrip('"rpm_pkg": ')
   temp=temp.rstrip('"')
   if "ython" in temp:
     temp ="p"+temp
   data[l]=temp
   l=l+1
for i in data:
 os.system('sudo yum localinstall -y {} '.format(i))
 logger.info("install rpm")

