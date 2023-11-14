import json
import boto3

def lambda_handler(event, context):
    master_id="i-0ed35a18893e4e8c5"
    slave_id="i-05cdb109f20b48997"
    ec2_re=boto3.resource("ec2",'eu-west-2')
    ec2_cli=boto3.client("ec2",'eu-west-2')
    #sns_client=boto3.client("sns",'eu-west-2')
    primary_instance=ec2_re.Instance(master_id)
    secondary_instance=ec2_re.Instance(slave_id)
    response_IP = ec2_cli.describe_addresses()
    
    if primary_instance.state['Name'] != "running":
       print("Primary ASA gone down, Deleted 3.10.245.197 from Primary ASA and Attached 3.10.245.197 in Secondary ASA")
       
       #-------------Replace the Route of 172.16.1.0/24--------------
       Replace_route_172_16_1_0_24 = ec2_cli.replace_route (
       DestinationCidrBlock='172.16.1.0/24',
       NetworkInterfaceId='eni-04099ea4d478df814',              # inside interfce on ASAvTwo
       RouteTableId='rtb-0d6253afbd5268fb1')                    # main RT 
       
       #-------------Replace the Route of x.x.x.x/x--------------
       #Replace_route_x_x_x_x_x = ec2_cli.replace_route (
       #DestinationCidrBlock='x.x.x.x/x',
       #NetworkInterfaceId='eni-08ab1d0bea0c6e57e',
       #RouteTableId='rtb-0f7ebd55e74800462')
                                       
       #---------------DisassociateIP----------------
       disassociateIP_response_Primary = ec2_cli.disassociate_address(
       PublicIp=  '3.10.245.197') 
       #------------------AssociateIP---------------------------------------
       AssociateIP_response_Secondary=ec2_cli.associate_address(
       AllocationId= 'eipalloc-0d684af2afccff218',              # ASAvOne ASAvExternalIp
       NetworkInterfaceId= 'eni-045d87815d166d152')             # outside interface on ASAvTwo
    
    else:
        print("Primary ASA is running")
     
    return None    
        