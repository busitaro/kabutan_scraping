import sys
import datetime
import pandas as pd

from input import input_data, input_business_day_file


def check_data(file_path, begin_date, end_date):
    check_data = input_data(file_path)
    business_day = input_business_day_file().reset_index()
    business_day = business_day[(begin_date <= business_day.date) & (business_day.date <= end_date)]

    for file_name, data in check_data.items():
        bs_day = business_day.copy()
        bs_day = pd.merge(bs_day, data, left_on='date', right_index=True, how='left')

        check = bs_day[(bs_day.business==True)&(bs_day.begin.isna())]
        check['delta'] = check[['date']] - check[['date']].shift()
        check['from'] = check.delta != datetime.timedelta(days=1)
        check['to'] = (check.delta == datetime.timedelta(days=1)) & (check.shift(-1).delta != datetime.timedelta(days=1))
        check['group'] = check['from'].cumsum()
        output = pd.concat(
            [check.groupby('group').min()[['date']].rename(columns={'date': 'from'}), 
            check.groupby('group').max()[['date']].rename(columns={'date': 'to'})], axis=1)
        output = output.astype({'from': str, 'to': str})
        output['str'] = output['from'].where(output['from'] == output['to'], output['from'] + ' - ' + output['to'])
        yield file_name, output.str.to_csv(header=False, index=False).replace('\r\n', '\n').replace('\n',',')


def main(file_path, begin_date, end_date):
    for file, check_result in check_data(file_path, begin_date, end_date):
        print(file, check_result, sep=' => ')


###################
# parameters
#    1: data_file_path
#    2: check_begin_date (yyyy-mm-dd)
#    3: check_end_date (yyyy-mm-dd)
###################
if __name__ == '__main__':
    args = sys.argv
    if len(args) != 4:
        print('prameters are invalid')
    
    file_path = args[1]
    begin_date = args[2]
    end_date = args[3]
    main(file_path, begin_date, end_date)
