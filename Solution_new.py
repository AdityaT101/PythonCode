import datetime
import json
import requests
import pandas as pd
from pandas.io.json import json_normalize


class Solution() :
   def totalTransactions( self ,  location_id , transactionType  ):

        df1 = pd.DataFrame()

        # Using the api end point by by iterating through all the pages from 1 to 16
        # so that we get a cumulative data for dataframe,
        for x in range(1,17):

                # retriving the data using API end point.
                text = ("https://jsonmock.hackerrank.com/api/transactions/search?txnType={}&page={}".format(transactionType , x) )
                response = requests.get(text)
                data = json.loads( response.content.decode(response.encoding) )

                # Flattening the nested json object
                df2 = json_normalize(data, record_path =['data'])

                #retrieve only 3 columns - 'userId', 'amount','location.id'
                df3 = df2[['userId', 'amount','location.id']]

                #appending to the existing dataframe in a loop
                df1 = df1.append( df3 ,ignore_index=True )



        # remove extra characters - ($ and ,) from amount column
        df1['amount'] = df1['amount'].str.replace(r'$', '')
        df1['amount'] = df1['amount'].str.replace(r',', '')

        # conver the data types of the columns into appropriate types
        df1['userId'] = df1['userId'].astype(int)
        df1['location.id'] = df1['location.id'].astype(int)
        df1['amount'] = df1['amount'].astype(float)


        # filtering based on the location_id
        d_table = df1[ df1['location.id'] == location_id ]

        # return [[-1, -1]] if the no match found for the location id
        if d_table.empty:
            return [[-1, -1]]

        #drop the location Id column because its not required further after filtering
        d_table = d_table.drop('location.id', 1)


        # Grouping dataframe on the user_id and summing up the amount column
        # This further gets converted into list object used for returning
        temp_frame = d_table.groupby('userId').sum().reset_index().values.tolist()

        #declaring a return list
        ret_list = []

        # converting the float values into int values in the return object.
        for i, ele in enumerate(temp_frame):
            ret_list.append( [int(temp_frame[i][0]), int(temp_frame[i][1])] )

        return( ret_list )



obj = Solution()

#calling the totalTransactions function
print( obj.totalTransactions( 1, 'debit' ) )




