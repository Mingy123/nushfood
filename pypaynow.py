# Adapted from https://github.com/poonchuanan/Python-PayNow-QR-Code-Generator

import datetime
import uuid

point_of_initiation = '12' # New QR every transaction
proxy_type = '0' # 0 for mobile number
proxy_value = '+6588343074' # Pay me yes
editable = '1' # Can edit amt afterwards
expiry = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y%m%d') # one day later, YYYMMDD

'''
Function to translate QR information dictionary payload to string of characters 
Works for any layers of nested objects (for this case we only have one nested layer ID 26)
'''
def get_info_string(info):
    final_string = '' # Empty string to store the generated output
    for key, value in info.items(): # Loop through the outer dictionary
        if type(value) == dict: # If there is a nested dictionary
            temp_string_length, temp_string = get_info_string(value) #call this function recusively to get the nested info
            # Adds the ID, length and value of the nested object
            final_string += key 
            final_string += temp_string_length
            final_string += temp_string
        else: # Normal value, adds the 3 fields: ID, length, value
            final_string += key
            final_string += str(len(value)).zfill(2)
            final_string += value
    return str(len(final_string)).zfill(2), final_string # Returns the length of the current string and its value

def generatePayNowQR(point_of_initiation,
                    proxy_type,
                    proxy_value,
                    editable,
                    amount,
                    expiry,
                    bill_number
                    ):
       '''
       Nested dictionary that follows the structure of the data object
       dictionary key = data object id, 
       dictionary value = data object value
       Application can also insert new key-value pairs corrosponding to its ID-value in whichever nested layer
       as long as the first and last root ID are 00 and 63 respectively. Order doesnt matter for the rest.
       '''
       info = {"00":"01",
              "01":str(point_of_initiation),
              "26":{"00":"SG.PAYNOW",
                     "01":str(proxy_type),
                     "02":str(proxy_value),
                     "03":str(editable),
                     "04":str(expiry)
                     } ,
              "52":"0000",
              "53":"702",
              "54":str(amount),
              "58":"SG",
              "59":"NA",
              "60":"Singapore",
              "62":{"01":str(bill_number)}
              }
       payload = get_info_string(info)[1] # gets the final string, length is not needed
       payload += '6304' # append ID 63 and length 4 (generated result will always be of length 4)
       crc_value = crc16_ccitt(payload) # calculate CRC checksum
       crc_value = ('{:04X}'.format(crc_value)) #convert into 4 digit uppercase hex
       payload += crc_value # add the CRC checksum result

       return payload
       
def crc16_ccitt(data): 
    crc = 0xFFFF # initial value
    msb = crc >> 8
    lsb = crc & 255
    for c in data:
        x = ord(c) ^ msb
        x ^= (x >> 4)
        msb = (lsb ^ (x >> 3) ^ (x << 4)) & 255
        lsb = (x ^ (x << 5)) & 255
    return (msb << 8) + lsb

def generate_food_paynow(amount):
    bill_ref = str(uuid.uuid4())[:8]
    paynow_str = generatePayNowQR(point_of_initiation,
                proxy_type,
                proxy_value,
                editable,
                amount,
                expiry,
                bill_ref
                )
    return paynow_str, bill_ref