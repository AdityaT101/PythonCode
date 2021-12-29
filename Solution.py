import json
import requests
import pandas as pd


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
                df2 = pd.json_normalize(data, record_path =['data'])

                df1 = df1.append( df2 ,ignore_index=True )


        # inner and outer list for creating dataframe for the return object.
        outer = []
        inner = []

        for index, row in df1.iterrows():
            # regex for the amount column
            dg1 = float( row['amount'].replace("$", "").replace(",", "") )

            # retrieving user_id column
            dg2 = row['userId']

            dg3 = row['location.id']

            # filtering based on the location_id
            if( dg3 == location_id ):
                inner.append(  int(dg2)  )
                inner.append(  float(dg1)  )

            if inner != []:
                outer.append(inner)

            inner = []

        # return the following result if no match found for the location_id
        if outer == []:
            return [[-1, -1]]

        #creating dataframe for the return object and adding column to the frame
        d_table = pd.DataFrame(outer)
        d_table.columns = ['user_Id', 'amount']


        d_table.sort_values(by=['user_Id'], inplace=True)

        # Grouping dataframe on the user_id and summing up the amount column
        # This further gets converted into list object used for returning
        temp_frame = d_table.groupby('user_Id').sum().reset_index().values.tolist()

        ret_list = []

        #converting the float values into int values in the return object.
        for i, ele in enumerate(temp_frame):
            ret_list.append( [ int(temp_frame[i][0]) , int(temp_frame[i][1]) ] )

        return ( ret_list )


obj = Solution()

#calling the totalTransactions function
print( obj.totalTransactions( 1, 'debit' ) )
