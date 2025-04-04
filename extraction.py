# import pandas as pd
# import json

# def extract_shit(NAME):
#     # Read the Excel file
#     df = pd.read_excel('My Copy of MaintenanceTracker Monthly update 1.xlsx',header=4,sheet_name=NAME)  # Replace with the path to your spreadsheet
#     print(df)
#     # Display the first few rows
#     # print(df.columns)
#     df_cleaned = df

#     # Display the cleaned DataFrame
#     reasons_for_breakdown=df_cleaned['Reason for Breakdown'].to_list()
#     actions=df_cleaned['ACTION/TASK'].to_list()
#     maintenance_category=df_cleaned['Maintenance Category'].to_list()
#     specific_equipment=df_cleaned['Specific Equipment'].to_list()
#     category=df_cleaned['Category'].to_list()
#     store=[]


#     for action,reason,maintenance,cat,equipement in zip(actions,reasons_for_breakdown,maintenance_category,category,specific_equipment):
#         data={}
#         if type(action)==str:

#             data['action']=action.strip().upper()
        
#         if type(reason)==str:
#             data['reason']=reason.strip().upper()
            
#         if type(maintenance)==str:
#             data['maintenenance']=maintenance.strip().upper()
            
#         if type(cat)==str:
#             data['category']=cat.strip().upper()
            
#         if type(equipement)==str:
#             data['equipment']=equipement.strip().upper()
            
            
#         if type(reason)==str and type(action)==str and type(maintenance)==str:
#             store.append(data)
        
        

#     with open(f'c:\\Users\Mr Dashi\Downloads\email_scanner\data\\action{NAME}.json','w') as file:
#         json.dump(store,file,indent=4)
        
        
        


# df = pd.read_excel('My Copy of MaintenanceTracker Monthly update 1.xlsx',header=4,sheet_name=None) 
# for keys in df.keys() :
#     try:
#         extract_shit(keys)
#     except:
#         pass