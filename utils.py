from tqdm import tqdm
import pandas as pd
import pandas as pd
from openpyxl import load_workbook
from tqdm import tqdm
import os

def get_current_date_and_time():
    
    
    import datetime
    import pytz

    # Get the current date and time in Nigeria
    nigeria_tz = pytz.timezone('Africa/Lagos')
    now_nigeria = datetime.datetime.now(nigeria_tz)

    # Function to get the ordinal suffix for the day
    def get_ordinal_suffix(day):
        if 10 <= day <= 20:
            return 'th'
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        return suffixes.get(day % 10, 'th')

    # Format the current date and time
    current_day_name = now_nigeria.strftime("%A").lower()
    current_day = now_nigeria.day
    current_day_with_suffix = f"{current_day}{get_ordinal_suffix(current_day)}"
    current_month_name = now_nigeria.strftime("%B").lower()
    current_year = now_nigeria.year
    current_hour_12 = now_nigeria.strftime("%I")
    current_minute = now_nigeria.strftime("%M")
    current_am_pm = now_nigeria.strftime("%p").lower()

    formatted_now = f"{current_day_name}.{current_day_with_suffix}.{current_month_name}.{current_year}.{current_hour_12}..{current_minute}{current_am_pm}"

    
    return formatted_now
    

def save_sheet(unFlatteneddata):
    da=[]
    for index,flattenData in tqdm(enumerate(unFlatteneddata),desc="Flattening Extracted data ",total=len(unFlatteneddata),unit="Field"):
        da.append([index+1,flattenData['predicted_reason']['action'],flattenData['location'],flattenData['predicted_reason']['reason'],flattenData['predicted_reason'].get('maintenance') if flattenData['predicted_reason'].get('maintenance',None)!=None else flattenData['predicted_reason'].get('maintenenance',None) ,flattenData['predicted_reason']['equipment'],flattenData['predicted_reason']['category'],flattenData['request_date']])



    print("✅ Done Flattening Extracted Data Properly")
    data = da

    columns = ["S/N", "ACTION/TASK", "Store", "Reason for Breakdown", "Maintenance Category", "Specific Equipment", "Category", "Request Date"]

    df = pd.DataFrame(data, columns=columns)

    
    sheetName=get_current_date_and_time()
    output_file = f"Maintenance_Report{sheetName}.xlsx"
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name=sheetName, index=False)
        
        workbook  = writer.book
        
        worksheet = writer.sheets[sheetName]

        # Freeze top row
        worksheet.freeze_panes(1, 0)

        # Set height of header row (~300px ≈ 225 points)
        worksheet.set_row(0, 40)

        # Create a format for the header row with vertical center alignment
        header_format = workbook.add_format({
            'valign': 'vcenter',
            'align': 'center',  # optional: horizontal centering too
            'bold': True,
            'text_wrap': True
        })

        # Apply header format to all columns
        for col_num, column_title in tqdm( enumerate(df.columns), desc="Saving Flattened Extracted data " ,total=len(df.columns) , unit="Row" ):
            worksheet.write(0, col_num, column_title, header_format)

            # Autofit columns
            col_width = max(df[column_title].astype(str).map(len).max(), len(column_title)) + 2
            worksheet.set_column(col_num, col_num, col_width)

        # Add autofilter
        worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
    print(f"Saved in {output_file}")
