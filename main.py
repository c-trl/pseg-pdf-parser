import os, re
import pandas as pd
from datetime import datetime
from PyPDF2 import PdfReader

# requires PDF files to be downloaded into local folder called 'bills'

single_line_hitlist = [
    'Totalgasdeliverycharges',
    'Totalgassupplycharges',
    'Totalgascharges',
    'Totalelectricdeliverycharges',
    'Totalelectricsupplycharges',
    'Totalelectriccharges'
]
    
final_column_order = [
    'Start Period', 'End Period', 'Electric Charges', 'Gas Charges', 'Amount Due', 
    'Usage (kWh)', 'Delivery Rate ($/kWh)', 'Delivery Charges (Electric)', 'Supply Rate ($/kWh)', 'Supply Charges (Electric)', 
    'Usage (Therms)', 'Delivery Rate ($/Therm)', 'Delivery Charges (Gas)', 'Supply Rate ($/Therm)', 'Supply Charges (Gas)'
]

def parse_line(target):
    key, value = target.split(' ')
    return value

def pdf_to_csv(pdf_filepath, data_filepath):
    
    saved = {} # parsed data will go here
    
    reader = PdfReader(pdf_filepath)
    
    # turning data into iterable lines. index is needed to refer to preceeding/following lines (eg. content following titles)
    for page in reader.pages:
        text = str(page.extract_text(0))
        lines = text.split('\n')
        lines_dict = dict(enumerate(lines))
        
        for ix in lines_dict:
            line = lines_dict[ix]
            key = line.split(' ')[0]

            # simple string splits
            if key in single_line_hitlist:
                try:
                    saved[key] = parse_line(line)
                except Exception:
                    raise Exception('could not parse single line!')

            # accounting for utility used in variable "n" days; need to use regex to match the text before
            elif key[:17] == 'Totalgasyouusedin':
                saved_key = 'Totalgasused'
                try:
                    saved[saved_key] = parse_line(line)
                except Exception:
                    raise Exception('could not parse total gas used!')
            
            elif key[:22] == 'Totalelectricyouusedin':
                saved_key = 'Totalelectricused'
                try:
                    saved[saved_key] = parse_line(line)
                except Exception:
                    raise Exception('could not parse total electric used!')

            # monthly service fees preceeding delivery charge sections; need to index lines
            # and
            # delivery rates
            elif key == "Chargesfordeliveringgastoyou:":
                try:
                    saved_key = f'Monthly Service Charge (Gas)'
                    target = lines_dict[ix - 1]
                    saved[saved_key] = parse_line(target)
                except Exception:
                    raise Exception('could not parse gas delivery service charge!',line)

                try:
                    saved_key = 'Delivery Rate ($/Therm)'
                    target = lines_dict[ix + 1]
                    saved[saved_key] = target.split('thermsx')[1].split(' ')[0]
                except Exception:
                    raise Exception('could not parse gas delivery service charge!',line)

            elif key == "Chargesfordeliveringelectrictoyou:":
                try:
                    saved_key = f'Monthly Service Charge (Electric)'
                    target = lines_dict[ix - 1]
                    saved[saved_key] = parse_line(target)
                except Exception:
                    raise Exception('could not parse electric delivery service charge!',line)
                # turns out i don't have to pay the monthly service charges... ok!
                
                try:
                    saved_key = 'Delivery Rate ($/kWh)'
                    target = lines_dict[ix + 1]
                    if target == 'kWhcharges':
                        target = lines_dict[ix + 2]
                    saved[saved_key] = target.split('kWhx')[1].split(' ')[0]
                except Exception:
                    raise Exception('could not parse electric delivery rates!',line)

            elif key == 'CostofgassuppliedbyPSE&G:':
                try:
                    saved_key = 'Supply Rate ($/Therm)'
                    target = lines_dict[ix + 1]
                    saved[saved_key] = target.split('thermsx')[1].split(' ')[0]
                except Exception:
                    raise Exception('could not parse gas supply rates!',line)

            elif key == 'CostofelectricsuppliedbyPSE&G:':
                try:
                    saved_key = 'Supply Rate ($/kWh)'
                    target = lines_dict[ix + 1]
                    if 'kWhx' not in target:
                        target = lines_dict[ix + 2]
                    saved[saved_key] = target.split('kWhx')[1].split(' ')[0]                    
                except Exception:
                    raise Exception('could not parse electric supply rates!',line)

            # getting period date range, will hold for dataframe later
            # this doesn't really follow the flow of this code because this was an afterthought... afterrealization*
            # this became grosser and grosser. we need regex to differentiate the "to" in "October" from the deliminating "to"
            elif key[:13] == 'Fortheperiod:':
                try:
                    if 'October' in line:
                        line = line.replace('October','Octber')
                    start_period, end_period = line.split('Fortheperiod:')[1].split(' ')[0].split('to')
                    if 'Octber' in start_period:
                        start_period = start_period.replace('Octber','October')
                    if 'Octber' in end_period:
                        end_period = end_period.replace('Octber','October')
                except Exception:
                    raise Exception('could not parse period dates!', line)

            else:
                pass

    # formatting dictionary values
    for key in saved:
        val = saved[key]
        if 'kWh' in val:
            new_val = val.replace('kWh','')
        else:
            new_val = re.findall("\d{1,10}\.\d*", val)[0]
        saved[key] = [float(new_val)] #turning new_val into an array to make it readable by from_dict below

    # write to file
    df = pd.DataFrame.from_dict(saved)
    df['Start Period'] = str(datetime.strptime(start_period, '%B%d,%Y').date())
    df['End Period'] = str(datetime.strptime(end_period, '%B%d,%Y').date())
    df['Amount Due'] = df['Totalgascharges'] + df['Totalelectriccharges']

    column_formatting = {
    'Totalgasused': 'Usage (Therms)',
    'Totalgasdeliverycharges': 'Delivery Charges (Gas)',
    'Totalgassupplycharges': 'Supply Charges (Gas)',
    'Totalgascharges': 'Gas Charges',
    'Totalelectricused': 'Usage (kWh)',
    'Totalelectricdeliverycharges': 'Delivery Charges (Electric)',
    'Totalelectricsupplycharges': 'Supply Charges (Electric)',
    'Totalelectriccharges': 'Electric Charges'
    }

    for column in column_formatting:
        df[column_formatting[column]] = df[column]
        df = df.drop(column,axis=1)

    df = df[final_column_order]

    df.to_csv(data_filepath, mode='a', index=False, header=False)

folder = os.path.expanduser('./bills/')
data_filepath = os.path.expanduser('./data.csv')
if os.path.exists(data_filepath):
    os.remove(data_filepath)

for filename in os.listdir(folder):
    pdf_filepath = os.path.expanduser(folder + filename)
    pdf_to_csv(pdf_filepath, data_filepath)

data_df = pd.read_csv(data_filepath,names=final_column_order)
data_df = data_df.sort_values(by='Start Period',ascending=True)
data_df.to_csv(data_filepath, index=False, sep='\t')
