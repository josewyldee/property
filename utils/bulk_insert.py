def append_record(length, title, data, i):
    j = 0
    sub_record = {}
    while j < length:
        # print("----------------------")
        
     
      
        try:
            # print("----------------------99999999999999")
            # print("cuuustom",title[3] ,":",data[3][i])
            
            sub_record.update({title[j] : data[j][i]})  
        except:
            print("cuuustom",title[3] ,":",data[3][0])
            # print("changedd",title[j] ,":",data[j][0])
            sub_record.update({title[j] : data[j][0]})
        # print("----------------------")
        # if data[j]:
        #     print("eeeeeeeeeee",title[j] ,"dddddd",data[j][i])
        
        #     sub_record.update({title[j] : data[j][i]})         
        j += 1
    return sub_record
def bulk_data_fomart_receipt(raw_data,look_at):
    look_at_next=look_at+1
    data=dict(raw_data)
    records_title = list(data)
    records = list(data.values())
    record_data = []
    i = 0
    print("reeeeeeeeeeeeeecord",records)
    print("sssssssssssssssstart",data[records_title[look_at]])
    while i < len(data[records_title[look_at_next]]):
        if(records[look_at][i]):
            
            record_data.append(append_record(len(records_title),records_title, records,i))
        i += 1
    return record_data
def bulk_data_fomart(raw_data):
    data=dict(raw_data)
    records_title = list(data)
    records = list(data.values())
    record_data = []
    i = 0
    print("reeeeeeeeeeeeeecord",records)
    print("sssssssssssssssstart",data[records_title[1]])
    while i < len(data[records_title[1]]):
        if(records[0][i]):
            record_data.append(append_record(len(records_title),records_title, records,i))
        i += 1
    return record_data
def bulk_data_fomart_decision(raw_data):
    data=dict(raw_data)
    records_title = list(data)
    records = list(data.values())
    record_data = []
    i = 0
    # print("yyyyyyyyyyyyyyyyyyyyyyyyyya")
    # print(data)
    while i < len(data[records_title[0]]):
        if data['upload_decision'][i]=="upload":
            if(records[0][i]):
                # print("working",records[4][i])
                record_data.append(append_record(len(records_title),records_title, records,i))
        i += 1
    return record_data
def bulk_data_fomart_property(raw_data,bulk_id):
    # print(raw_data)
    data=dict(raw_data)
    records_title = list(data)
    record_data = []
    i = 0
    while i < len(data[records_title[0]]):
        property_type=data['property_type_raw_bulk'][i].split(',')[0]
        property_category=data['property_type_raw_bulk'][i].split(',')[1]
        record_data.append(
            {
                'property_name': data['property_name_bulk'][i],
                'property_type': property_type,
                'property_category': property_category,
                'auto_fee': data['auto_fee'][0],
                'bulk_name': data['bulk_name'][0],
                'bulk_id': bulk_id,
                'year_created': data['year_created'][0],
                'country': data['country'][0],
                'city': data['city'][0],
                'street': data['street'][0],
                'landmark_description': data['landmark_description'][0],
                'managed_by': data['managed_by'][0],
                'owned_by': data['owned_by'][0],
                'auto_tax': data['auto_tax'][0],
                'tax_rate': data['tax_rate'][0],
                'auto_fee': data['auto_fee'][0],
                'fee_rate': data['fee_rate'][0],
                'fee_on': data['fee_on'][0],
                'bulk':True

            })
        i += 1
    # print("jooooooooooooooooooooooooooooooooooooooooooooooe")
    # print(record_data)
    return record_data





# sssssssssssssssstart [['python', 'java'], ['1200', '700'], ['no', 'no'], ['null', 'null'], ['0', '0'], ['0', '0'], ['0', '0'], ['generic', 'generic'], ['email'], [''], ['unit'], ['1'], ['once'], ['A29C2A4F']]
# sssssssssssssssstart ['1200', '700']

    