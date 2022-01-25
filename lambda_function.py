#Import necessary dependencies
import json
import boto3
import uuid

#Assign rds database details using Secret Manager
rds_client=boto3.client('rds-data')
databasename='bestbrands'
dbclusterarn='arn:aws:rds:us-east-1:118383306190:cluster:marketing'
db_secret_store_arn='arn:aws:secretsmanager:us-east-1:118383306190:secret:rds-db-credentials/cluster-PQUJSVPFEJTFCY3INBPCKJ4J5A/admin-O1wdTq'

#The Handler that will be triggered externally

def lambda_handler(event, context):
    
    #Initialize the response object
    response = {}
    try:
        
        if event['httpMethod']=='GET':
            
            #Read parameters from queary String
            try: #Try and catch input parameter exceptions
                userid=event['queryStringParameters']['userid']
                useremail=event['queryStringParameters']['useremail']
                brandid=event['queryStringParameters']['brandid']
            except:
                response['statusCode'] = '200'
                response['body'] = 'Insuficient Parameters'
                return response
                
            #Check for valid user and brand
            if validate_user(userid) and validate_brand(brandid):
            
                #Call get discount code providing the userid and brandid
                #TODO Parse the records jason to get the exact tag of discount code
                discountcode=get_discount(userid,brandid)
                response['statusCode'] = '200'
                response['body'] = "{'Discount_Code':'"+str(discountcode['records'][0][0]['stringValue']+"'}")
                
                #Send brand and fethed user detail to SQS
                sendstatus = senduser_SQS(brandid,userid,useremail)
                
            else:
               
                response['statusCode'] = '400'
                response['body'] = 'Invalid User or brand'
                    
        
        elif event['httpMethod']=='POST':
            #ToDO Read jason body and get values for brand and N
            brand='SONY'
            N=3
            # check if valid brand ID
            if validate_brand(brand):
            
                dbrespons=create_discount(brand,N)
            
                response['statusCode'] = '200'
                response['body'] = "Discount codes were created successfully"
            else:
                response['statusCode'] = '400'
                response['body'] = 'Invalid BrandID'

        
    except Exception as e:
        response['statusCode'] = '500'
        response['body'] = e
                
        
    return response
        

#The methode that fetch a discount code
 
def get_discount(userid,brandid, dynamodb=None):
    
    
    get_discount_sql="select code as id from Discount_Codes where brand_id='"+brandid+"' and fetcheduser_id IS NULL ORDER BY RAND() LIMIT 1"
    response=execute_sql(get_discount_sql)
    #To DO
    #Update the table with fetched userID so that same code is not picked again
   
    return response

 #The methode to create discount codes  
    
def create_discount(brandid,N,dynamodb=None):
   
    for i in range(N):
        code_id=str(uuid.uuid1())
        code=brandid+code_id
        insert_sql="insert into Discount_Codes (code_id,code,brand_id) values ('"+code_id+"','"+code+"','"+brandid+"')"
        response= execute_sql(insert_sql)
    
  
    return response
    
def execute_sql(sql):
    response=rds_client.execute_statement(
        secretArn=db_secret_store_arn,
        database=databasename,
        resourceArn=dbclusterarn,
        sql=sql
        )
    return response
    
#The method to validate userid        
def validate_user(userid):
    
    #ToDo: Write the code to validate the user against user table. Setting the return value as True for test purpose
    return True

#The method to validate bandid        
def validate_brand(brandid):
    
    #ToDo: Write the code to validate the bandid against brand table. Setting the return value as True for test purpose
    return True

# The mothod to send user data to a SQS

def senduser_SQS(brandid,userid,useremail):
    
    #TODO: Write the code to send the user data to SQS
    Response='Message sent to SQS'
    
    return Response
    
