def fix_errors_bulk(raw_error_list):
    error_list = []
    for dic in raw_error_list:
        for val,cal in dic.items():
            error_list.append(f'(error at {val}) {cal[0]}')
        final_errors=error_list
    return final_errors
def fix_errors(raw_error_list):
    error_list = []
    print("JOOOOOOOOSEPH")
    print(raw_error_list)
    for dic in raw_error_list:
     
        error_list.append(f'(Error at {dic}) {raw_error_list[dic][0]}')
        # for val,cal in dic.values():
        #     error_list.append(f'(error at {val}) {cal[0]}')
        final_errors=error_list
    return final_errors
# def fix_errors(raw_error_list):
#     print("JOOOOOOOOSEPH")
#     print(raw_error_list)
#     error_list = []
#     for variable, data in reversed(raw_error_list):
#         error_list.append(f'(error at {variable}) {data[0]}')
#     return error_list